"""
    Generates 2 csv files after running each county through Prophet:
        results_cases.csv - Infection cases
        results_deaths.csv - Infection cases

    This had to be done in a seperate script. Jupyter notebook would not finish running even with
    concurrency.
"""
from urllib.request import urlopen
import concurrent.futures
import os, json, time
import pandas as pd
import numpy as np
import plotly.express as px
from fbprophet import Prophet

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

"""
    Load and preprocess the COVID and Census population data
"""
def load_data():
    covid_cols = ['date', 'fips', 'cases', 'deaths']
    df = pd.read_csv("../data/raw/covid-19-data/us-counties.csv", dtype={'fips': str},
            usecols=covid_cols)
    df.dropna(inplace=True)
    fields = ['STATE', 'COUNTY', 'POPESTIMATE2019']
    popdf = pd.read_csv("../data/raw/co-est2019-alldata.csv", encoding='ISO-8859-1', usecols=fields)
    popdf.dropna(inplace=True)
    popdf['STATE'] = popdf['STATE'].apply('{:0>2}'.format)
    popdf['COUNTY'] = popdf['COUNTY'].apply('{:0>3}'.format)
    popdf['FIPS'] = popdf['STATE'] + popdf['COUNTY']
    popdf = popdf.drop(['STATE', 'COUNTY'], axis=1)
    df = df.merge(popdf, how='left', left_on='fips', right_on='FIPS')
    df['rate_deaths'] = df['deaths'] / df['POPESTIMATE2019'] * 100000
    df['rate_cases'] = df['cases'] / df['POPESTIMATE2019'] * 100000
    df = df.loc[df['fips'].str.startswith(("0", "1", "2", "3", "4", "5"))]
    df['ds'] = pd.to_datetime(df['date'])
    df = df.drop(['FIPS', 'POPESTIMATE2019', 'cases', 'deaths'], 1)
    return df

df = load_data()

"""
    Preprocessing for Prophet based on infection cases.
"""
def add_cases(fips):
    data = df[df['fips'] == fips]
    data = data[['ds', 'rate_cases']]
    data = data.rename(columns={'rate_cases': 'y'})
    data['fips'] = fips
    return (fips, data)

fips_cases = {}
with concurrent.futures.ProcessPoolExecutor() as executor:
    results = executor.map(add_cases, df.fips.unique())
    for (fips, result) in results:
        fips_cases[fips] = result

"""
    Preprocessing for Prophet based on deaths.
"""
def add_deaths(fips):
    data = df[df['fips'] == fips]
    data = data[['ds', 'rate_deaths']]
    data = data.rename(columns={'rate_deaths': 'y'})
    data['fips'] = fips
    return (fips, data)

fips_deaths = {}
with concurrent.futures.ProcessPoolExecutor() as executor:
    results = executor.map(add_deaths, df.fips.unique())
    for (fips, result) in results:
        fips_deaths[fips] = result

"""
    Prophet models for each county's infection cases.
"""
def prophet_cases(data):
    m = Prophet()
    m.fit(fips_cases[data]);
    future = m.make_future_dataframe(periods=90)
    result = m.predict(future)
    result['data'] = data
    return (data, result)

forcast = {}
print(f'Started processing forcasts')
with concurrent.futures.ProcessPoolExecutor() as executor:
    results = executor.map(prophet_cases, fips_cases)
    for (fips, result) in results:
        forcast[fips] = result

result = pd.concat(forcast)
result.to_csv('results_cases.csv')

"""
    Prophet models for each county's deaths.
"""
def prophet_deaths(data):
    m = Prophet()
    m.fit(fips_deaths[data]);
    future = m.make_future_dataframe(periods=90)
    result = m.predict(future)
    result['data'] = data
    return (data, result)

forcast = {}
print(f'Started processing forcasts')
with concurrent.futures.ProcessPoolExecutor() as executor:
    results = executor.map(prophet_deaths, fips_deaths)
    for (fips, result) in results:
        forcast[fips] = result

result = pd.concat(forcast)
result.to_csv('results_deaths.csv')
