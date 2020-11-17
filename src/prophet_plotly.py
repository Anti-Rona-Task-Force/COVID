from urllib.request import urlopen
import concurrent.futures
import os, json, time
import pandas as pd
import numpy as np
import plotly.express as px
from fbprophet import Prophet

df = pd.read_csv("../data/raw/covid-19-data/us-counties.csv", dtype={'fips': str})
df = df.dropna()
df = df.loc[df['fips'].str.startswith(("0", "1", "2", "3", "4", "5"))]
df['ds'] = pd.to_datetime(df['date'])
df['y'] = df.cases
print(df.describe())

counties = ['06075', '47169']
for county in counties:
    data = df[df['fips'].str.contains('06075')]
    m = Prophet()
    m.fit(data);
    future = m.make_future_dataframe(periods=90)
    result = m.predict(future)

    fig = m.plot(result)
    fig.write_html(county + ".html")
