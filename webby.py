# -*- coding: utf-8 -*-
import os
import pathlib

import dash
from dash.dependencies import Input, Output
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
import plotly.express as px
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.config.suppress_callback_exceptions = True

#Reading a csv file
df = pd.read_csv('/Users/GoldenFace/Desktop/Avionics/DataV/Data/temperature.csv')
pf = pd.read_csv('/Users/GoldenFace/Desktop/Avionics/DataV/Data/pressure.csv')

#Plotting the data
fig = go.Figure(go.Scatter(x=df['Time'], y=df['Temp'], name='Temperature in Kelvin'))
fig.update_layout(title='Travel Log 1',
                   plot_bgcolor='rgb(32, 26, 82)',
                   showlegend=False)

pressure_fig = go.Figure(go.Scatter(x=pf['distance'], y=pf['pressure'], name='Pressure in Pa'))
pressure_fig.update_layout(title='Travel Log 2',
                   plot_bgcolor='rgb(32, 26, 82)',
                   showlegend=False)

#Building the banner that sits on top.
#Logo on the left hand side and Rocket Progress Indicators on the right hand side.
def build_banner():
    return html.Div([
        html.Div(
            id="banner",
            children=[
                html.Div(
                    id="banner-text",
                    children=[
                        html.Div([
                            html.Img(
                                src=app.get_asset_url("Logo.png"),
                                id="plotly-image1",
                                style={
                                    "height": "100px",
                                    },
                            ),
                        ], 
                        className="six columns"
                        ),
                        
                    ],
                ),
                html.Div(
                    id="Launch-indicator",
                    children=[
                        html.Div([
                            html.Img(
                                src=app.get_asset_url("LaunchYes.png"),
                                id="plotly-image2",
                                style={
                                    "height": "100px",
                                    },
                            ),
                        ], 
                        className="two columns"
                        ),
                        
                    ],
                ),
                html.Div(
                    id="Parachute-indicator",
                    children=[
                        html.Div([
                            html.Img(
                                src=app.get_asset_url("ParachuteYes.png"),
                                id="plotly-image3",
                                style={
                                    "height": "100px",
                                    },
                            ),
                        ], 
                        className="two columns"
                        ),
                        
                    ],
                ),
                html.Div(
                    id="Landing-indicator",
                    children=[
                        html.Div([
                            html.Img(
                                src=app.get_asset_url("LandNo.png"),
                                id="plotly-image4",
                                style={
                                    "height": "100px",
                                    },
                            ),
                        ], 
                        className="two columns"
                        ),
                        
                    ],
                ),
            ],
            style={
                "height": "100px",
                "width": "auto",
                'background-color': '#110e2c',
                'color': '#FFFFFF',
                "margin-bottom": "10px",
            },
        ),
        html.Div(
            html.Br(),
            style={
                "height": "10px",
                'background-color': '#201a52',
            },
        )
    ])

#Graphing the first data set the "pressure" one
def predicted_map():
    return html.Div(
        id="control-chart-container",
        className="ten columns",
        children=[
            dcc.Graph(id="pressure", figure = pressure_fig),
        ],
        style={
            'margin':'20px',
        },
        
    )

#Graphing the second data set the "temperature" one
def actual_map():
    return html.Div(
        id="control-chart-container",
        className="ten columns",
        children=[
            dcc.Graph(id="Temperature_Sensor", figure = fig),
        ],
        style={
            'margin':'20px',
        },
    )

#Creating the side panel.
#Still need to implement the "upload" function to upload data
#Also a space to capture main info like height and pressure.
#At the there is a function to switch between the two graphs.
def side_panel():
    return html.Div(
        id="quick-stats",
        className="two columns",
        children=[
            html.Br(),
            html.Div([
                html.Div(
                    id="card-1",
                    children=[
                        html.P("UPLOAD DATA"),
                    ],
                )],
                className="rows",
            ),
            html.Br(),
            html.Div([
                html.Div(
                    id="card-2",
                    children=[
                        html.P("MAX HEIGHT"),
                        daq.LEDDisplay(
                            id="operator-led",
                            value="1704",
                            color="#92e0d3",
                            backgroundColor="#110e2c",
                            size=30,
                        ),
                    ],
                )],
                className="rows",
            ),
            html.Br(),
            html.Div([
                html.Div(
                    id="card-3",
                    children=[
                        html.P("MAX PRESSURE"),
                        daq.Gauge(
                            id="progress-gauge",
                            max= 2,
                            min=0,
                            showCurrentValue=False,  # default size 200 pixel
                            size=120,
                        ),
                    ],
                )],
                className="rows",
                ),
            html.Br(),
            html.Div([
                dcc.Tabs(
                    id="tabs", 
                    value='predicted_tab', 
                    children=[
                        dcc.Tab(label='DATA1', value='predicted_tab'),
                        dcc.Tab(label='DATA2', value='actual_tab'),
                    ],
                    style={
                        'background-color': '#201a52',
                    },
                ),
            ],
            className="rows",
            ),
        ],
        style={
                'background-color': '#201a52',
                'text-align': 'center',
            },
    )

#Callback implementation for the tabs
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'actual_tab':
        return html.Div([
            actual_map()
        ])
    elif tab == 'predicted_tab':
        return (
            html.Div(    
                predicted_map()
            )
    )

#Main content section
def build_content():
    return html.Div(
         html.Div([    
                html.Div(
                    id="status-container",
                    children=[
                        side_panel(),
                    ],
                ),
                html.Div(id='tabs-content'),
            ],
            className="twelve columns",
            style={
                    'background-color': '#110e2c',
                    'margin':'20px',
                },
        )
    )

#The fun little Welcome page
index_page = html.Div([
    html.Div([
        html.Img(
            src=app.get_asset_url("Logo.png"),
            id="plotly-image",
            style={
                'object-fit': 'none',
                'object-position': '30%',
                },
        ),
    ]),
    dcc.Link('Launch', href='/main-page'),
    ],
    className="twelve columns",
    style={
        'text-align': 'center',
        'color':'white',
        },
)

#Main structure section
main_page_content = html.Div([
    html.Div(
        id="big-app-container",
        className="rows",
        children=[
            build_banner(),
            build_content(),
        ],
    ), 
])

#Layouts
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


#Callback for the link function to go from the Welcome page into the main page
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/main-page':
        return main_page_content
    else:
        return index_page


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)