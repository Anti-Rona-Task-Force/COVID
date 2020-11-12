from urllib.request import urlopen
import os
import json
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

print(f"Processing figure.")
#fig = px.choropleth(df, geojson=counties, locations='fips', color='rate',
#        color_continuous_scale="thermal",
#        animation_frame='date',
#        range_color=(0, 6000),
#        scope="usa",
#        labels={'cases':'cases'}
#        )
#fig.show()

fipsall = df.fips.unique()
fips_collection = {}
for fips in fipsall:
    print(f"Adding {fips}")
    fips_collection[fips] = df[df['fips'] == fips]
    fips_collection[fips] = fips_collection[fips][['dt', 'rate']]
    fips_collection[fips] = fips_collection[fips].rename(columns={'dt': 'ds', 'rate': 'y'})
    fips_collection[fips]['fips'] = fips

total = len(fips_collection)
predict = {}
for i, data in enumerate(fips_collection):
    m = Prophet()
    print(f"Processing {data}: {i} of {total}")
    m.fit(fips_collection[data]);
    future = m.make_future_dataframe(periods=90)
    predict[data] = m.predict(future)
    predict[data]['fips'] = data

result = pd.concat(predict)
result.to_csv('results.csv')
