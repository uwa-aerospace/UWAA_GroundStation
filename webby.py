# -*- coding: utf-8 -*-
import os
import pathlib

import dash
from dash.dependencies import Input, Output, State
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
pf = []

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

#Graphing the second data set the "temperature" one
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

def top_panel():
    return html.Div(
        html.Div(
            id="tabs-top-content",
            children=[
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
                                value=972,
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
            style={
                'padding': '10px',
                'margin-top': '10px',
            },
        ),
        className="ten columns",
        
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
                            'lineHeight': '40px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px',
                            "background": '#110e2c',
                        },
                        # Allow multiple files to be uploaded
                        multiple=False
                    ),
                ],
                    style={
                        "background": '#201a52',
                        'height': '100px',
                        'padding': '5px',
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
                    value='predicted_tab', 
                    children=[
                        dcc.Tab(label='Plot', value='predicted_tab'),
                        dcc.Tab(label='Wind', value='actual_tab'),
                    ],
                    colors={
                        "background": '#110e2c'
                    },
                    style={
                        'align-items': 'center',
                        'justify-content': 'center',
                        'padding': '1px',
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
                graphy_graph(pf)
            )
    )

def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            pf = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            pf = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            pf = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        graphy_graph(pf)
    ])

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
              Input('upload-data', 'filename')])
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children

#Graphing the first data set the "pressure" one
def graphy_graph(pf):
    if pf!=[]:
        pressure_fig = go.Figure(go.Scatter())
        pressure_fig.update_layout(
            title='Travel BLog',
            xaxis_title='Time (s)',
            yaxis_title='Pressure (Pa)',
            plot_bgcolor='rgb(32, 26, 82)',
            showlegend=False,
            template="plotly_dark",)
    else:
        pressure_fig = go.Figure(go.Scatter())
        pressure_fig.update_layout(
            title='Travel Log',
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
            'margin':'10px',
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