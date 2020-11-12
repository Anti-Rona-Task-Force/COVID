from urllib.request import urlopen
import concurrent.futures
import os, json, time
import pandas as pd
import numpy as np
import plotly.express as px
from fbprophet import Prophet

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

df = pd.read_csv("../data/raw/covid-19-data/us-counties.csv", dtype={'fips': str})
df.dropna(inplace=True)
fields = ['STATE', 'COUNTY', 'POPESTIMATE2019']
popdf = pd.read_csv("../data/raw/co-est2019-alldata.csv", encoding='ISO-8859-1', usecols=fields)
popdf.dropna(inplace=True)
popdf['STATE'] = popdf['STATE'].apply('{:0>2}'.format)
popdf['COUNTY'] = popdf['COUNTY'].apply('{:0>3}'.format)
popdf['FIPS'] = popdf['STATE'] + popdf['COUNTY']
popdf = popdf.drop(['STATE', 'COUNTY'], axis=1)
df = df.merge(popdf, how='left', left_on='fips', right_on='FIPS')
df['ratio'] = df['POPESTIMATE2019'] / 100000
df['rate'] = df['cases'] / df['ratio']
df = df.loc[df['fips'].str.startswith(("0", "1", "2", "3", "4", "5"))]

# Too much data. Lets take 1 week at a time.
df['dt'] = pd.to_datetime(df['date'])
#df = df.loc[df['dt'].dt.dayofweek == 1]

#print(f"Processing figure.")
#fig = px.choropleth(df, geojson=counties, locations='fips', color='rate',
#        color_continuous_scale="thermal",
#        animation_frame='date',
#        range_color=(0, 6000),
#        scope="usa",
#        labels={'cases':'cases'}
#        )
#fig.show()


def addfips(fips):
    data = df[df['fips'] == fips]
    data = data[['dt', 'rate']]
    data = data.rename(columns={'dt': 'ds', 'rate': 'y'})
    data['fips'] = fips
    return (fips, data)

fipsall = df.fips.unique()
fips_collection = {}

fipsstart = time.perf_counter()
print(f'Started processing fips')

with concurrent.futures.ProcessPoolExecutor() as executor:
    results = executor.map(addfips, fipsall)

    for (fips, result) in results:
        fips_collection[fips] = result

fipsend = time.perf_counter()
print(f'Finished fips processing in {round(fipsend - fipsstart, 2)} seconds')


def prophet(data):
    m = Prophet()
    m.fit(fips_collection[data]);
    future = m.make_future_dataframe(periods=90)
    result = m.predict(future)
    result['data'] = data
    return (data, result)

forcast = {}
forcaststart = time.perf_counter()
print(f'Started processing forcasts')
with concurrent.futures.ProcessPoolExecutor() as executor:
    results = executor.map(prophet, fips_collection)

    for (fips, result) in results:
        forcast[fips] = result

forcastend = time.perf_counter()
print(f'Finished forcast processing in {round(forcastend - forcaststart, 2)} seconds')

result = pd.concat(forcast)
result.to_csv('results.csv')
