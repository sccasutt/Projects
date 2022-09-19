
from dash import dcc, html, Dash, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np

#external stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#initialize app
app = Dash(__name__,external_stylesheets=external_stylesheets,)

#load data
unf_df = pd.read_csv('Training_projects/Unfall_statistik/Unfall_nach_Kanton.csv', encoding='unicode_escape', delimiter=';')


#-----------------------------------------------

#create app layout
app.layout = html.Div(children=[
    html.H1(children='Unfall Statistik Schweiz nach Kanton',style={
            'textAlign': 'center'}),

    html.H5(children='''
        Ein Interaktives Dashboard
    ''',style={'textAlign': 'center'}),

    html.Br(),
    #Make Kantone selectable
    html.Div(children=[
        html.Label('Kanton(e) Auswählen'),
        dcc.Checklist([*np.sort(unf_df['Kanton'].unique())], 
                     id='Kanton_Auswahl',
                     value=['Aargau']
                     ),
        #make year selectable
        html.Label('Yahr'),
        dcc.RadioItems(unf_df.columns[4:],
                        id='Yahr',
                        value='2021'
                        ),
        ],style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
    #grafic
    html.Div(children=[
    dcc.Graph(
        id='Unfall_Statistik',    
    ),
    #text unnter Grafik
    html.Div(children=[
    html.H6(children='Total Verunfallte:'),
    html.H5(id='Unfallzahl'),
    html.H6(children='Verunfallte Nach Kanton:'),
    dbc.Table(id='Zahl_nach_Kanton')
    ], style={'display': 'flex', 'justify-content': 'space-between'})
    
    ],style={'width': '70%','height':'50%', 'display': 'inline-block', 'vertical-align': 'top'}
    ),
   
    
])

#-----------------------------------------------

#creating callbacks
@app.callback(
    Output('Unfall_Statistik', 'figure'), 
    Input('Kanton_Auswahl','value'),
    Input('Yahr','value'))

def update_graph(Kanton, Yahr):
    dff = unf_df[unf_df['Kanton'].isin(Kanton)]

    fig = px.bar(dff, x='Kanton',y=Yahr,color="Strassenart", barmode="group")

    fig.update_xaxes(categoryorder='category ascending')

    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output('Unfallzahl','children'),
    Input('Kanton_Auswahl','value'),
    Input('Yahr','value'))

def update_text(Kanton, Yahr):
    anzahl = unf_df[unf_df['Kanton'].isin(Kanton)][Yahr].sum()
    return anzahl

@app.callback(
    Output('Zahl_nach_Kanton','children'),
    Input('Kanton_Auswahl','value'),
    Input('Yahr','value'))

def update_text(Kanton, Yahr):
    anz={}
    for k in Kanton:
        a = unf_df[unf_df['Kanton'] == k][Yahr].sum()
        anz[a] = k
    dfff = pd.DataFrame.from_dict([anz]).melt(var_name='Anzahl', value_name='Kanton')
    table = dbc.Table.from_dataframe(dfff, striped=True, bordered=True, hover=True)
    return table





if __name__ == '__main__':
    app.run_server(debug=True)

