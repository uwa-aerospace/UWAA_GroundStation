# -*- coding: utf-8 -*-
import base64
import datetime
import os
import io
import pathlib

import dash
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.config.suppress_callback_exceptions = True

#Reading a csv file for Wind Measurement and Graph
df = px.data.wind()
tf = []



#Plotting the Wind Measurement
fig = px.bar_polar(df, r="frequency", theta="direction", color="strength", template="plotly_dark", title='Wind Measurement', 
                    color_discrete_sequence= px.colors.sequential.Plasma_r)

########___MAP___#########
#mark things on the map (Will convert this to trail of the rocket)
locat = go.Figure(go.Scattermapbox(
        lat=['-31.981179'],
        lon=['115.819910'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        text=['UWA'],
    ))

#Map layout
locat.update_layout(
    hovermode='closest',
    mapbox=dict(
        accesstoken='pk.eyJ1IjoicGV5bGlubmciLCJhIjoiY2s5aXBqcmptMWEzNzNtcDR4MWJvd2FuNSJ9.N7Q2yH7WQFsMv6uP8YOCEQ',
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=-31.981179,
            lon=115.819910
        ),
        pitch=0,
        zoom=15,
        style='outdoors',
    ),
    title='Rocket Trail',
    plot_bgcolor='rgb(32, 26, 82)',
    showlegend=False,
    template="plotly_dark",

)


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
                            html.Div([
                                daq.PowerButton(
                                    id="button-1",
                                    on=False,
                                    color='#00FF00'
                                ),
                                html.Div(id='power-button-1'),
                                ],
                                style={
                                'textAlign': 'center',
                                'padding':'5px',
                                "padding-top": "10px",
                                }),
                        ], 
                        className="two columns"
                        ),
                        
                    ],
                ),
                html.Div(
                    id="Parachute-indicator",
                    children=[
                        html.Div([
                            html.Div([
                                daq.PowerButton(
                                    id="button-2",
                                    on=False,
                                    color='#00FF00'
                                ),
                                html.Div(id="power-button-2")
                            ],
                                style={
                                'textAlign': 'center',
                                'padding':'5px',
                                "padding-top": "10px",
                                }),
                        ], 
                        className="two columns"
                        ),
                        
                    ],
                ),
                html.Div(
                    id="Landing-indicator",
                    children=[
                        html.Div([
                            html.Div([
                                daq.PowerButton(
                                    id="button-3",
                                    on=False,
                                    color='#00FF00'
                                ),
                                html.Div(id="power-button-3")
                            ],
                                style={
                                'textAlign': 'center',
                                'padding':'5px',
                                "padding-top": "10px",
                                }),
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

@app.callback(
    dash.dependencies.Output('power-button-1', 'children'),
    [dash.dependencies.Input('button-1', 'on')])
def update_output(on):
    if on:
        return 'Launched'
    else:
        return 'Not Launched'

@app.callback(
    dash.dependencies.Output('power-button-2', 'children'),
    [dash.dependencies.Input('button-2', 'on')])
def update_output(on):
    if on:
        return 'Delpoyed'
    else:
        return 'Not Deployed'

@app.callback(
    dash.dependencies.Output('power-button-3', 'children'),
    [dash.dependencies.Input('button-3', 'on')])
def update_output(on):
    if on:
        return 'Landed'
    else:
        return 'Not Landed'

def top_panel():
    return html.Div(
        html.Div(
            id="tabs-top-content",
            className="ten columns",
            children=[
                html.Div(
                    html.Br(),
                    style={
                        "background": '#110e2c',
                        'height': '160px',
                        'width': '10px'
                    },
                    className ="one columns"
                ),
                html.Div([
                    html.Div(
                        id="card-4",
                        children=[
                            daq.Gauge(
                                id="progress-gauge",
                                label='Velocity',
                                max=100,
                                min=0,
                                showCurrentValue=True,  # default size 200 pixel
                                value=75,
                                units="m/s",
                                size=80,
                            ),
                        ],
                        style={
                            "background": '#201a52',
                            'padding': '10px',
                            'height': '125px',
                            'width': '120px'
                        },
                    )],
                    className="two columns",
                ),

                html.Div([
                    html.Div(
                        id="card-5",
                        children=[
                            daq.Gauge(
                                id="progress-gauge",
                                label='Acceleration',
                                max=80,
                                min=0,
                                showCurrentValue=True,  # default size 200 pixel
                                value=66,
                                units="m/s^2",
                                size=80,
                            ),
                        ],
                        style={
                            "background": '#201a52',
                            'padding': '10px',
                            'height': '125px',
                            'width': '120px'
                        },
                    )],
                    className="two columns",
                ),

                html.Div([
                    html.Div(
                        id="card-6",
                        children=[
                            daq.Gauge(
                                id="progress-gauge",
                                label='Height',
                                max=20,
                                min=0,
                                showCurrentValue=True,  # default size 200 pixel
                                value=4,
                                units="m",
                                size=80,
                            ),
                        ],
                        style={
                            "background": '#201a52',
                            'padding': '10px',
                            'height': '125px',
                            'width': '120px'
                        },
                    )],
                    className="two columns",
                ),

                html.Div([
                    html.Div(
                        id="card-7",
                        children=[
                            daq.Gauge(
                                id="progress-gauge",
                                label='Temperature',
                                max=50,
                                min=0,
                                showCurrentValue=True,  # default size 200 pixel
                                value=35,
                                units="Degrees C",
                                size=80,
                            ),
                        ],
                        style={
                            "background": '#201a52',
                            'padding': '10px',
                            'height': '125px',
                            'width': '120px'
                        },
                    )],
                    className="two columns",
                ),

                html.Div([
                    html.Div(
                        id="card-8",
                        children=[
                            daq.Gauge(
                                id="progress-gauge",
                                label='Time',
                                max=1000,
                                min=0,
                                showCurrentValue=True,  # default size 200 pixel
                                value=52,
                                units="s",
                                size=80,
                            ),
                        ],
                        style={
                            "background": '#201a52',
                            'padding': '10px',
                            'height': '125px',
                            'width': '120px'
                        },
                        
                    )],
                    className="two columns",
                ),

            ],
        ),
        style={
                'height': '160px',
                'margin-left': '10px',
                "background": '#201a52',
            },
    )

#Creating the side panel.
#Still need to implement the "upload" function to upload data
def side_panel():
    
    return html.Div(
        id="quick-stats",
        className="two columns",
        children=[
            html.Br(),
            html.Div([
                html.Div([
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            html.Button('Upload File'),
                        ],),
                        # Allow multiple files to be uploaded
                        multiple=True
                    ),
                ],
                    style={
                        "background-color": '#201a52',
                        'height': '100px',
                    },)
                ],
                className="rows",
            ),
            html.Br(),
            html.Div([
                html.Div(
                    id="card-2",
                    children=[
                        daq.LEDDisplay(
                            id="operator-led",
                            label='Max. Height',
                            value="1704",
                            color="#92e0d3",
                            backgroundColor="#110e2c",
                            size=30,
                        ),
                    ],
                    style={
                        "background": '#201a52',
                        'height': '120px',
                        'align-items': 'center',
                    },
                )],
                className="rows",
            ),
            html.Br(),
            html.Div([
                html.Div(
                    id="card-3",
                    children=[
                        daq.Gauge(
                            id="progress-gauge",
                            label='Max. Pressure',
                            max=2,
                            min=0,
                            showCurrentValue=True,  # default size 200 pixel
                            size=120,
                            value=1,
                            units="MPa",
                        ),
                    ],
                    style={
                        "background": '#201a52',
                        'height': '200px',
                        'align-items': 'center',
                    },
                )],
                className="rows",
                ),
            html.Br(),
            html.Div([
                dcc.Tabs(
                    id="tabs", 
                    value='second_tab', 
                    children=[
                        dcc.Tab(label='Plot', value='second_tab'),
                        dcc.Tab(label='Wind', value='first_tab'),
                    ],
                    colors={
                        "background": '#110e2c'
                    },
                    style={
                        'align-items': 'center',
                        'justify-content': 'center',
                        'border': '5px solid #201a52'
                        },
                ),
            ],
            className="rows",
            ),
        ],
        style={
            'text-align': 'center',
            'width': '150px',
            'height': '620px',
            "background": '#201a52',
            },
    )

#Callback implementation for the tabs
@app.callback(Output('tabs-graph-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):

    if tab == 'first_tab':
        return html.Div([
            wind_map()
        ])
    
    elif tab == 'second_tab':
        return (
            html.Div(id='output-data-upload'),
        )


def parse_contents(contents, filename, date):

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            pf = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            rf = np.append(tf,pf)

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            pf = pd.read_excel(io.BytesIO(decoded))
            rf = np.append(tf,pf)
        
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            pf = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
            rf = np.append(tf,pf)

    except:
        return html.Div([
            dcc.ConfirmDialog(
                id='confirm',
                message='There was an error processing this file.',
            )
        ])

    return html.Div([
        graphy_graph(rf, pf, filename)
    ])

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_upload_output(list_of_contents, list_of_names, list_of_dates):

    if list_of_contents is not None:

        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        
        return children

    else :
        pressure_fig = go.Figure(go.Scatter())
        pressure_fig.update_layout(title= dict(text ='No File Uploaded', font =dict( color = 'white')),
                            plot_bgcolor='rgb(32, 26, 82)', paper_bgcolor='#111111', showlegend=False)
        return (
            html.Div(  
                id="control-chart-container",
                className="five columns",
                children=[
                    html.Div(dcc.Graph(id="pressure", figure = pressure_fig))
                ],
                style={
                    'backgroundColor': '#110e2c',
                    'margin':'10px',
                    'color': '#110e2c',
                }
            )
        )

#Graphing the uploaded data
def graphy_graph(rf, pf, filename):

    return (

        html.Div(
            children=[  
                html.Div(
                    id="control-chart-container",
                    className="five columns",
                    children=[
                        dcc.Graph(
                            id="pressure", 
                            figure = {
                                'data': [
                                    {'x': pf['distance'], 
                                    'y': pf['pressure'],
                                    'type': 'scatter'}
                                ],
                                'layout':{
                                    'hovermode': True,
                                    'title': filename,
                                    'xaxis_title': "Distance (m)",
                                    'yaxis_title': "Pressure (MPa)",
                                    'plot_bgcolor': '#110e2c',
                                    'paper_bgcolor': '#111111'
                                }
                            }),
                    ],
                    style={
                        'margin':'10px',
                        'backgroundColor': '#110e2c',
                        'color': "#110e2c",
                    },),
            ],)
    )
##

#Graphing the wind map
def wind_map():
    return html.Div(
        id="control-chart-container",
        className="five columns",
        children=[
           dcc.Graph(id="Wind_measurement", figure = fig),
        ],
        style={
            'margin':'10px',
            'background-color': '#201a52',
        },
    )

def map_panel():
    return html.Div(
        html.Div(
            id="tabs-map-content",
            className="five columns",
            children=[
                dcc.Graph(id="Rocket_location", figure = locat),
            ],
            style={
                'margin':'10px',
            },
        ),
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
                html.Div([
                    html.Div(
                        id="tabs-top-content",
                        children=[
                            top_panel(),
                        ]),
                    html.Div(id='tabs-graph-content'),
                    html.Div(
                        id="tabs-map-content",
                        children=[
                            map_panel(),
                        ]),
                ])
                
            ],
            className="twelve columns",
            style={
                    'background-color': '#110e2c',
                    'margin':'10px',
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
                'height':'40%',
                'width' : '40%',
                },
        ),
    ]),
    dcc.Link(html.Button('Launch'), href='/main-page',
        style={
            'font-weight': 'bold',
            'color': 'white',
            'padding': '10px 10px',
            'position': 'relative',
            'text-decoration': 'none',
            'text-transform': 'uppercase',
        }),
    ],
    className="twelve columns",
    style={
        'text-align': 'center',
        'color':'white',
        'top':'50%',
        'transform': 'translate(0, 50%)'
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