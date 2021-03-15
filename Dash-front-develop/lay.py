import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import base64
from app_ import app
from dash import callback_context as ctx


from dash.dependencies import Input, Output, State
# Data analytics library

import os
import pandas as pd
import numpy as np
import plotly.express as px
import json

# Risk Model --------------------------------------------------------------------------

# Layout definition

risk = html.Div([

    dcc.Tabs(children=[
        dcc.Tab(label='Usuarios Registrados', children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Input(
                                id="exploration user",
                                placeholder="Ingrese su usario",
                                style={'width' : '100%'}, 
                                value="user_000021"
                            ),
                            html.Br(),
                            dcc.Input(
                                id="exploration pass",
                                type="password",
                                placeholder="Ingrese contraseña",
                                style={'width' : '100%'},
                                value="user_000021"
                            ),
                            html.Button('Login', id='exploration button', n_clicks=0),
                            
                        ])
                    ])
                ], className="mt-1 mb-2 pl-3 pr-3")
            ]),
            dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H5("Artistas preferios",
                                                        className="card-title"),
                                                html.P("Muestra los artistas que más ha escuchado"),
                                                dcc.Graph(id="exploration artgraph")

                                            ]
                                        ),
                                    ],
                                )
                            ],
                            className="mt-1 mb-2 pl-3 pr-3", lg="6", sm="12", md="auto"
                        ),

                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H5("Canciones escuchadas",
                                                        className="card-title"),
                                                html.P("Acá puede ver las principales canciones escuchadas"),
                                                dcc.Graph(id="exploration songgraph"),
                                            ]
                                        ),
                                    ],
                                )
                            ],
                            className="mt-1 mb-2 pl-3 pr-3", lg="6", sm="12", md="auto"
                        ),
                    ],
                ),

        ]),
        dcc.Tab(label='Nuevo Usuario'),
    ]),

],
    className='container',
)
