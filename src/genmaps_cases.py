"""
    Genmaps generates a map using plotly express and the results_*.csv generated from
    forecast_multi.py.

    This also would not run in Jupyter notebook. On my system I ran out of memory.

    The plots are saved as html files.
"""
from urllib.request import urlopen
import os
import json
import pandas as pd
import numpy as np
import plotly.express as px
from fbprophet import Prophet

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
df = pd.read_csv("results_cases.csv", dtype = {"data": str})
df['date'] = pd.to_datetime(df['ds'])
df = df.loc[df['date'].dt.dayofweek == 1]

fig = px.choropleth(df, geojson = counties, locations = 'data', color = 'yhat',
        color_continuous_scale = "thermal",
        animation_frame = 'ds',
        range_color = (0, 8000),
        scope = "usa",
        labels = {'cases':'cases'}
        )

fig.update_layout(
    coloraxis_colorbar = dict(
        title = "Infection Rates per 100,000",
        title_side = 'right',
        title_font = dict(
            size = 18,
            color = "Black"
        ),
        x = 0.9,
        tickfont = dict(
            size = 18,
            color = "Black"
        )
    )
)

for i, frame in enumerate(fig.frames):
    titledate = pd.Timestamp(frame.name)
    current = pd.Timestamp.now()
    tense = "Historical"
    if titledate.date() > current.date():
        tense = "Forecasted"
    frame.layout.title = {
        'text': f'{tense}: <br>{titledate.month_name()} {titledate.year}',
        'y': 0.33,
        'x': 0.73,
        'xanchor': 'left',
        'font': dict(
            size = 28,
            color = "Black"
        )}

fig.write_html("forecast_cases.html")
