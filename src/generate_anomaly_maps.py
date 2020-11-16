import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
from urllib.request import urlopen
import os
import json
import pandas as pd
import numpy as np
import plotly.express as px
from fbprophet import Prophet
import os.path
import datetime 

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
df = pd.read_csv("results.csv", dtype={"data": str})
df['date'] = pd.to_datetime(df['ds'])
df = df.loc[df['date'].dt.dayofweek == 1]
print(df)

fig = px.choropleth(df, geojson=counties, locations='data', color='yhat',
        color_continuous_scale="thermal",
        animation_frame='ds',
        range_color=(0, 6000),
        scope="usa",
        labels={'cases':'cases'}
        )

fig.write_html("forcast.html")