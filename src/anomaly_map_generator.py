import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import os
import json
import pandas as pd
import numpy as np
import plotly.express as px

with open('data/raw/geojson-counties-fips.json') as json_file:
    counties = json.load(json_file)

df = pd.read_csv('data/processed/anomalyIsoForestTimeSpread.csv', dtype={"fips": str})
df['date'] = pd.to_datetime(df['date'])
# df = df.loc[df['date'].dt.dayofweek == 1]
print(len(df))

fig = px.choropleth(df, geojson=counties, locations='fips', color='anomalyScore',
       color_continuous_scale="thermal",
       animation_frame='anomalyScore',
       range_color=(-2, 0),
       scope="usa",
       labels={'cases':'cases'}
       )

fig.write_html("iso_forest_anomalies_timespread.html")