from dash import dcc, html, Dash, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np
import wbgapi as wb
from urllib.request import urlopen
import json

#external stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#initialize app
app = Dash(__name__)

#gather data (DONE)

## get world population data from world bank by country
### the world bank database is: SP.POP.TOTL
pop_df = wb.data.DataFrame(['SP.POP.TOTL'],mrv=1)
pop_df.reset_index(inplace=True)
pop_df.rename(columns={'SP.POP.TOTL':'population'}, inplace=True)

## get income data per country
### the world bank database for income per capita is: NY.ADJ.NNTY.PC.CD
income_per_capita = wb.data.DataFrame(['NY.ADJ.NNTY.PC.CD'],mrv=1)
income_per_capita.reset_index(inplace=True)
income_per_capita.rename(columns={'NY.ADJ.NNTY.PC.CD':'income_per_capita'}, inplace=True)

### the world bank database for gdp per capita is: NY.GDP.PCAP.CD
gdp_per_capita = wb.data.DataFrame(['NY.GDP.PCAP.CD'],mrv=1)
gdp_per_capita.reset_index(inplace=True)
gdp_per_capita.rename(columns={'NY.GDP.PCAP.CD':'gdp_per_capita'}, inplace=True)

### get the country names 
economies = wb.economy.list(id='all', q=None, labels=False, skipAggs=False, db=None)
countries = pd.DataFrame(list(economies))

### merge the dataframes and cleanup
df = pop_df.merge(
    income_per_capita,
    how="outer",
    on='economy',
    sort=True,
    copy=True,
    indicator=False,
    validate=None,
    ).merge(
    gdp_per_capita,
    how="outer",
    on='economy',
    sort=True,
    copy=True,
    indicator=False,
    validate=None,
    ).merge(
    countries, 
    how='left',
    left_on='economy',
    right_on='id',
    sort=True,
    copy=True,
    indicator=False,
    validate=None,
    )

df = df[~df['aggregate']]

df.drop(['id','aggregate','region', 'adminregion',
       'lendingType', 'incomeLevel'], axis=1, inplace=True)

'''
only for use in production 
with urlopen('https://datahub.io/core/geo-countries/r/countries.geojson') as response:
    countries_geo = json.load(response)
'''
with open('Training_projects/World_population/countries.geojson') as response:
    countries_geo = json.load(response)
#app layout

##Create a map showing population in a graph on map (OPEN)

app.layout = html.Div(children=[
                                dcc.Graph(
                                            id='population',    
                                         ),
                                dcc.RadioItems(['world'],
                                                id='select',
                                                value='all')
                                ],style={'width': '70%','height':'100%'}
                     )



##Show average income on graph on map (OPEN)

##show population growth as a time series (OPEN)
##show income growth as a time series in same graph (seperate y axis) (OPEN)


#callbacks (OPEN)

@app.callback(
    Output('population', 'figure'),
    Input('select','value') 
    )

def update_map(Select):
    fig = px.choropleth_mapbox(df, geojson=countries_geo, locations='economy', color='population',
                           color_continuous_scale="sunsetdark",
                           featureidkey="properties.ISO_A3",
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 46.8131873, "lon": 8.22421}, 
                           opacity=0.5,
                           labels={'population':'Population'}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig

##be able to select up to three countries for comparison
##the time series data should be shown next to each other -> https://pythonprogramming.net/vehicle-data-visualization-application-dash-python-tutorial/?completed=/live-graphs-data-visualization-application-dash-python-tutorial/
##the map should highlight selected countries
##create a slider to select timeframe


#run

if __name__ == '__main__':
    app.run_server(debug=True)


