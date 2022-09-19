
from dash import dcc, html, Dash, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np

#load external data----------------------------------------------------


#load data
df = pd.read_csv('Training_projects/Tutorials/dash/Unfall_nach_Kanton.csv', encoding='unicode_escape', delimiter=';')


#initialize app
app = Dash(__name__)


#Create the app layout-----------------------------------------------

#create app layout
app.layout = html.Div()

#create callbacks-----------------------------------------------




#Run app---------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)

