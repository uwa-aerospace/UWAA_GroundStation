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

#Reading a csv file for Wind Measurement and Graph
df = px.data.wind()
pf = pd.read_csv('/Users/GoldenFace/Desktop/Avionics/DataV/Data/pressure.csv')

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
def graphy_graph():

    pressure_fig = go.Figure(go.Scatter(x=pf['distance'], y=pf['pressure']))
    pressure_fig.update_layout(title='Travel Log',
                    xaxis_title='Time (s)',
                   yaxis_title='Pressure (Pa)',
                   plot_bgcolor='rgb(32, 26, 82)',
                   showlegend=False,
                   template="plotly_dark",)

    return html.Div(
        id="control-chart-container",
        className="five columns",
        children=[
            dcc.Graph(id="pressure", figure = pressure_fig),
        ],
        style={
            'margin':'20px',
        },
        
    )

#Graphing the second data set the "temperature" one
def wind_map():
    return html.Div(
        id="control-chart-container",
        className="five columns",
        children=[
           dcc.Graph(id="Wind_measurement", figure = fig),
        ],
        style={
            'margin':'20px',
            'background-color': '#201a52',
        },
    )

def top_panel():
    return html.Div(
        html.Div(
            id="tabs-top-content",
            children=[
                html.Div([
                    html.Div(
                        id="card-4",
                        children=[
                            html.P("MARK 1"),
                            daq.Gauge(
                                id="progress-gauge",
                                max=100,
                                min=0,
                                showCurrentValue=False,  # default size 200 pixel
                                size=120,
                            ),
                        ],
                    )],
                    className="two columns",
                ),

                html.Div([
                    html.Div(
                        id="card-5",
                        children=[
                            html.P("MARK 2"),
                            daq.Gauge(
                                id="progress-gauge",
                                max=80,
                                min=0,
                                showCurrentValue=False,  # default size 200 pixel
                                size=120,
                            ),
                        ],
                    )],
                    className="two columns",
                ),

                html.Div([
                    html.Div(
                        id="card-6",
                        children=[
                            html.P("MARK 3"),
                            daq.Gauge(
                                id="progress-gauge",
                                max=20,
                                min=0,
                                showCurrentValue=False,  # default size 200 pixel
                                size=120,
                            ),
                        ],
                    )],
                    className="two columns",
                ),

                html.Div([
                    html.Div(
                        id="card-7",
                        children=[
                            html.P("MARK 4"),
                            daq.Gauge(
                                id="progress-gauge",
                                max=50,
                                min=0,
                                showCurrentValue=False,  # default size 200 pixel
                                size=120,
                            ),
                        ],
                    )],
                    className="two columns",
                ),

                html.Div([
                    html.Div(
                        id="card-8",
                        children=[
                            html.P("MARK 5"),
                            daq.Gauge(
                                id="progress-gauge",
                                max=1000,
                                min=0,
                                showCurrentValue=False,  # default size 200 pixel
                                size=120,
                            ),
                        ],
                    )],
                    className="two columns",
                ),

            ],
        ),
        className="ten columns",
        style={
                'margin': '0 0 0 20px',
                'background-color': '#201a52',
                'text-align': 'center',
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
                html.Div([
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '80%',
                            'height': '80px',
                            'lineHeight': '40px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=True
                    ),
                ])
                ],
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
                            max=2,
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
                'width': '150px',
                'heigh': 'auto'
            },
    )

#Callback implementation for the tabs
@app.callback(Output('tabs-graph-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'actual_tab':
        return html.Div([
            wind_map()
        ])
    elif tab == 'predicted_tab':
        return (
            html.Div(    
                graphy_graph()
            )
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
                'margin':'20px',
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