
from dash import dcc, html, Dash, Input, Output
import pandas as pd
import plotly.express as px

#load external data----------------------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


#load and transform data
df = pd.read_csv('Training_projects/Tutorials/dash/Unfall_nach_Kanton.csv', encoding='unicode_escape', delimiter=';')
df = df.melt(id_vars=['Unfallschwere', 'Kanton', 'Strassenart', 'Unfallort'], var_name='Year', value_name='Amount')
line_df = pd.DataFrame(df.groupby(['Year'])['Amount'].sum())
line_df.reset_index(inplace=True)
line_df['Year'] = pd.to_numeric(line_df['Year'])


#initialize app
app = Dash(__name__,external_stylesheets=external_stylesheets)


#Create the app layout-----------------------------------------------

#create app layout

app.layout = html.Div(children=[
                                html.H1(children='Total Traffic Accidents in Switzerland by Year'),
                                html.H5(children='Interactive Visualization Tutorial'),
                                html.Div(children=[dcc.RangeSlider(int(line_df['Year'].min()), int(line_df['Year'].max()), 
                                                                    marks={str(year): str(year) for year in line_df['Year'].unique()},
                                                                    value=[int(line_df['Year'].min())+10,int(line_df['Year'].max())-10], 
                                                                    id='year_selector')]),
                                html.Div(children=[dcc.Graph(id='accidents_graphic')]),
                                
                     ])

#create callbacks-----------------------------------------------

@app.callback(Output('accidents_graphic','figure'),
              Input('year_selector','value'))

def update_figure(year_range):
    updated_df = line_df[line_df['Year'].between(year_range[0],year_range[-1])]
    fig = px.line(updated_df, x='Year', y='Amount')
    fig.update_layout(transition_duration=500)
    return fig

#Run app---------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)