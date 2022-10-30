
from dash import dcc, html, Dash, Input, Output
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

#load external data----------------------------------------------------

#external Stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


#load and transform data
df = pd.read_csv('Training_projects/Tutorials/dash/Unfall_nach_Kanton.csv', encoding='unicode_escape', delimiter=';')
df = df.melt(id_vars=['Unfallschwere', 'Kanton', 'Strassenart', 'Unfallort'], var_name='Year', value_name='Amount')
df['Year'] = pd.to_numeric(df['Year'])
#create DF for use in line chart
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
                                
                                ### Top half of the app
                                html.Div(children=[
                                                    
                                    html.Div(children=[
                                                                        
                                        html.Br(),
                                         #left side of the top half                               
                                        html.Div(children=[
                                            html.H6('Select a range of years to inspect:'),

                                            html.Br(),

                                            #Year range selector
                                            dcc.RangeSlider(int(line_df['Year'].min()), int(line_df['Year'].max()), 
                                                            marks={str(year): str(year)[-2:] for year in line_df['Year'].unique()},
                                                            value=[int(line_df['Year'].min())+10,int(line_df['Year'].max())-10],  
                                                            id='year_selector'
                                                            
                                                            ),
                                                                                            
                                            #graph to be displayed                                               
                                            dcc.Graph(id='accidents_graphic')
                                                                                                                
                                            #don't fill the screen                                                         
                                            ],style={'width': '60%',
                                                     'display': 'inline-block', 
                                                     'vertical-align': 'top'} 
                                            ), 
                                    #Right side of the top half
                                    html.Div(children=[
                                        html.H3('Key insights:'),
                                        html.H5(id='delta_percent'),
                                        html.H6(id='delta_by_accident_type'),
                                        html.H6(id='delta_dy_road_type'),


                                    ],style={'width': '30%',
                                             'display': 'inline-block', 
                                             'vertical-align': 'top',
                                             "margin-left": "3rem", 
                                             'margin-top':'14rem'})  
                                                                                            
                                        ],style={'width': '100%',
                                                 'height':'50%', 
                                                 'display': 'inline-block', 
                                                 'vertical-align': 'top'}  
                                        )
                                ]),

                #Bottom part of the layout
                html.Div(children = [
                #create dropdown for canton selection
                dcc.Dropdown(
                    #create dict of values
                    options=sorted({str(canton): str(canton) for canton in df['Kanton'].unique()}),
                    #select first element as default value
                    value=list(sorted({str(canton): str(canton) for canton in df['Kanton'].unique()}))[0],
                    id='canton_selection'
                            ),
                #create single value range selector 
                dcc.RangeSlider(int(line_df['Year'].min()), int(line_df['Year'].max()), 
                                                marks={str(year): str(year) for year in line_df['Year'].unique()},
                                                value=[int(line_df['Year'].max())],  
                                                id='singe_year_selector', 
                                                ),
                dcc.Graph(id='bottom') 
                ]),
                ])

                                   

#create callbacks-----------------------------------------------

@app.callback(Output('accidents_graphic','figure'),
              Input('year_selector','value'))

## Create an update linechart showing total accidents in CH within a selected range
def update_figure(year_range):
    updated_df = line_df[line_df['Year'].between(year_range[0],year_range[-1])]
    fig = px.line(updated_df, x='Year', y='Amount')
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(Output('delta_percent','children'),
              Input('year_selector','value'))

## Create delta percent vartiable and display as KPI in App
def update_delta(year_range):
    start_total = line_df[line_df['Year'] == int(year_range[0])]['Amount'].values[0]
    end_total = line_df[line_df['Year'] == int(year_range[-1])]['Amount'].values[0]
    delta_percent = 100-(start_total/end_total)*100
    return f'From {year_range[0]:.0f} to {year_range[-1]:.0f} the total number of accidents changed by {delta_percent:.2f}%.'


@app.callback(Output('delta_by_accident_type','children'),
              Input('year_selector','value'))

## Create delta percent by accident type vartiable and display as KPI in App
def update_delta_acc_type(year_range):
    acc_df = pd.DataFrame(df.groupby(['Unfallschwere','Year'])['Amount'].sum())
    acc_df.reset_index(inplace=True)
    acc_df['Year'] = pd.to_numeric(acc_df['Year'])
    start_total = acc_df[acc_df['Year'] == int(year_range[0])]['Amount'].values
    end_total = acc_df[acc_df['Year'] == int(year_range[-1])]['Amount'].values
    delta_percent = 100-(start_total/end_total)*100
    return f'Deadly accidents changed by {delta_percent[0]:.2f}%, Accidents with serious bodly harm changed by {delta_percent[1]:.2f}% and non serious accidents changed by {delta_percent[2]:.2f}%.'

@app.callback(Output('delta_dy_road_type','children'),
              Input('year_selector','value'))

## Create most accidents by road type and display as KPI in App
def update_delta_acc_type(year_range):
    road_df = pd.DataFrame(df.groupby(['Strassenart','Year'])['Amount'].sum())
    road_df.reset_index(inplace=True)
    road_df['Year'] = pd.to_numeric(road_df['Year'])
    road_df_update = road_df[road_df['Year'].between(year_range[0],year_range[-1])]
    max_acc_road = road_df_update['Amount'].values.max()
    road_type = road_df_update[road_df_update['Amount'] == road_df_update['Amount'].max()]['Strassenart'].values[0]
    max_year = road_df_update[road_df_update['Amount'] == road_df_update['Amount'].max()]['Year'].values[0]
    return f'Most accidents happend on {road_type} with {max_acc_road} accidents in {max_year}.'


#bottom half of app in a single figure
@app.callback(Output('bottom','figure'),
            Input('singe_year_selector','value'), 
            Input('canton_selection','value'),
            )


def update_bottom_half(selected_year, canton):

    #select only year and canton from df
    up_df = df[(df['Year'] == selected_year[0]) & (df['Kanton'] == canton)]


    #create subplots to display bottom half of app
    fig = make_subplots(rows=1, cols = 3, 
                        specs=[[{'type':'bar'},{'type':'pie'},{'type':'scatter'}]],
                        subplot_titles=('Amount of Accidents by Road Type', 'Percentage by accident severity', 'Total from start to selection')
                        )
    
    
    #create barchart showing only selected year and canton
    bar1 = px.bar(up_df, x='Strassenart',y='Amount', barmode='stack')

    #add traces to subplots
    for trace in bar1.data:
        fig.add_trace(trace, row=1, col=1)

    fig.update_xaxes(categoryorder='category ascending')

    #create pie chart to display accident severity
    pie1 = px.pie(up_df, values='Amount', names='Unfallschwere')

    #add traces to subplots
    for trace in pie1.data:
        fig.add_trace(trace, row=1, col=2)


    #select data needed to show 
    dff = df[(df['Kanton'] == canton) & (df['Year'].between(df['Year'].min(),selected_year[0]))]
    up_line_df = pd.DataFrame(dff.groupby(['Year','Strassenart'])['Amount'].sum())
    up_line_df.reset_index(inplace=True)
    up_line_df['Year'] = pd.to_numeric(up_line_df['Year'])
        
    #create line plot 
    line1 = px.line(up_line_df, x='Year', y='Amount', color='Strassenart')
    #add traces to subplots
    for trace in line1.data:
        fig.add_trace(trace, row=1, col=3)
    
    #update layout to exclude legend
    fig.update_layout(showlegend=False)

    return fig

#Run app---------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)