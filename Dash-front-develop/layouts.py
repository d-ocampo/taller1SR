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

# Surprise libraries

from surprise import Reader
from surprise import Dataset
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import accuracy

#export libraries

# from sklearn.externals import joblib
import joblib
import pickle

#graph libraries
import plotly.graph_objects as go
import networkx as nx
import plotly
import random


#Resources

#Cargar la ruta

ruta=os.getcwd()+'/Data/'

####Funciones 

#nombre de canción con el id
def nombre_cancion(traid):
    name=song_dict['traname'][traid]
    return name

def nombre_artista(artid):
    name=art_dict['artname'][artid]
    return name

#base de la prediccion de algún modelo


def base_prediccion(user,prediccion,columnid,n):
    #Predicciones usuario user
    user_predictions_a = []
    #borrar
    if columnid=='traid':
        user_predictions_a = list(filter(lambda x: x[0]==user,prediccion))
    else:
        user_predictions_a = list(filter(lambda x: x[1]==user,prediccion))
    user_predictions_a.sort(key=lambda x : x.est, reverse=True)
    
    #Se convierte a dataframe
    labels = [columnid, 'estimation']
    if columnid=='traid':
        df_predictions_a = pd.DataFrame.from_records(list(map(lambda x: (x.iid, x.est) , user_predictions_a)), columns=labels)
    else:
        df_predictions_a = pd.DataFrame.from_records(list(map(lambda x: (x.uid, x.est) , user_predictions_a)), columns=labels)
    #mostrar las primeras n predicciones
    show_pred=df_predictions_a.sort_values('estimation',ascending=False).head(n)
    
    #mostrar el nombre de la canción
    if columnid=='traid':
        show_pred['track-name']=show_pred[columnid].apply(nombre_cancion)
    else:
        show_pred['user-name']=show_pred[columnid]
    return show_pred



#graficar la red de recomendaciones


def graficar_red(edges,user):
    if len(edges)<2:
        words = ['No existe información suficiente']
        colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(30)]
        colors = colors[0]
        weights =[40]
        
        data = go.Scatter(x=[random.random()],
                         y=[random.random()],
                         mode='text',
                         text=words,
                         marker={'opacity': 0.3},
                         textfont={'size': weights,
                                   'color': colors})
        layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                            'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
        fig = go.Figure(data=[data], layout=layout)
        return fig
    H=nx.Graph()
    # Generar lista con los pesos de la red
    H.add_weighted_edges_from(edges)
    
    #Posición de los nodos
    pos = nx.nx_agraph.graphviz_layout(H)
    
    #Lista para generar las líneas de unión con el nodo
    edge_x = []
    edge_y = []
    for edge in H.edges():
        #Asigna la posición que generamos anteriormente
        H.nodes[edge[0]]['pos']=list(pos[edge[0]])
        H.nodes[edge[1]]['pos']=list(pos[edge[1]])
        x0, y0 = H.nodes[edge[0]]['pos']
        x1, y1 = H.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    #Crea el gráfico de caminos
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    #Lista para posición de los nodos
    node_x = []
    node_y = []
    for node in H.nodes():
        x, y = H.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)
    
    #Crear el gráfico de nodos con la barra de calor
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # Escala de colores 
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlOrRd',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Gusto del usuario',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    
    #Crear el color y el texto de cada nodo
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(H.adjacency()):
    # Se usa porque el usuario siempre va a tener más uniones
        if len(adjacencies[1])>1:
            node_adjacencies.append(0)
            node_text.append(adjacencies[0])
        else:
            #### OJO que toca modificarle el user
            node_adjacencies.append(adjacencies[1][user]['weight'])
            node_text.append(adjacencies[0] +' | Afinidad: ' +str(round(adjacencies[1][user]['weight'],2)))
    
    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    
    
    #Generar el gráfico con los nodos, títulos, etc....
    fig = go.Figure(data=[edge_trace, node_trace],
                  layout=go.Layout(
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Sistema de Recomendación interactivo",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig






#diccionario de canciones y artistas
with open(ruta+'song_dict.json') as f:
  song_dict = json.load(f)
with open(ruta+'art_dict.json') as f:
  art_dict = json.load(f)

# CSVS


#Cargar base de rating
ratings=pd.read_csv(ruta+'ratings.csv',sep=';')
ratings_art=pd.read_csv(ruta+'ratings_art.csv',sep=';')


##Modelo a
#usuario
#Abrir lista test
with open(ruta+'test_set_a_user.data', 'rb') as filehandle:
    # read the data as binary data stream
    test_set_a_user = pickle.load(filehandle)
#Abrir modelo
model_a_user= joblib.load(ruta+'model_a_user.pkl' , mmap_mode ='r')
#Predicciones del modelo
test_predictions_a_user=model_a_user.test(test_set_a_user)
#Listar los usuarios del test
users_set_a_user=[]
for i in range(len(test_set_a_user)):
    if test_set_a_user[i][0] not in users_set_a_user:
        users_set_a_user.append(test_set_a_user[i][0])

#item
#Abrir lista test
with open(ruta+'test_set_a_item.data', 'rb') as filehandle:
    # read the data as binary data stream
    test_set_a_item = pickle.load(filehandle)
#Abrir modelo
model_a_item= joblib.load(ruta+'model_a_item.pkl' , mmap_mode ='r')
#Predicciones del modelo
test_predictions_a_item=model_a_user.test(test_set_a_item)
#Listar los usuarios del test
item_set_a_item=[]
for i in range(len(test_set_a_item)):
    #ojo oca cambiar por el 1 que es el id del item
    if test_set_a_item[i][1] not in item_set_a_item:
        item_set_a_item.append(test_set_a_item[i][1])







top_cards = dbc.Row([
        dbc.Col([dbc.Card(
            [
                dbc.CardBody(
                    [
                        # html.Span(html.I("add_alert", className="material-icons"),
                        #           className="float-right rounded w-40 danger text-center "),
                        html.H5(
                            "Year of census", className="card-title text-muted font-weight-normal mt-2 mb-3 mr-5"),
                        html.H4(id="year census"),
                    ],

                    className="pt-2 pb-2 box "
                ),
            ],
            # color="danger",
            outline=True,
            #style={"width": "18rem"},
        ),
        ],
            className="col-xs-12 col-sm-6 col-xl-3 pl-3 pr-3 pb-3 pb-xl-0"
        ),
        dbc.Col([dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H5(
                            "France Population", className="card-title text-muted font-weight-normal mt-2 mb-3 mr-5"),
                        html.H4(id="total population"),

                     ],

                    className="pt-2 pb-2 box"
                ),
            ],
            # color="success",
            outline=True,
            #style={"width": "18rem"},
        ),
        ],

            className="col-xs-12 col-sm-6 col-xl-3 pl-3 pr-3 pb-3 pb-xl-0"
        ),
        dbc.Col([dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H5(
                            "Place", className="card-title text-muted font-weight-normal mt-2 mb-3 mr-5"),
                        html.H4(id="place"),
                    ],

                    className="pt-2 pb-2 box"
                ),
            ],
            # color="info",
            outline=True,
            #style={"width": "18rem"},
        ),
        ],

            className="col-xs-12 col-sm-6 col-xl-3 pl-3 pr-3 pb-3 pb-xl-0"
        ),
        dbc.Col([dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H5(
                            "Name", className="card-title text-muted font-weight-normal mt-2 mb-3 mr-5"),
                        html.H4(id="name of place"),
                    ],

                    className="pt-2 pb-2 box"
                ),
            ],
            # color="warning",
            outline=True,
            #style={"width": "18rem"},
        ),
        ],

            className="col-xs-12 col-sm-6 col-xl-3 pl-3 pr-3 pb-3 pb-xl-0"
        ),


    ],
        className="mt-1 mb-2"

    )


home = html.Div([
    # dbc.Jumbotron(
    #     [
    #         html.Img(src="/assets/images/francebanner.webp",
    #                  className="img-fluid")
    #     ], className="text-center"),


    dbc.Row(

        dbc.Col([
#banner del home
            html.I(className="fa fa-bars",
                   id="tooltip-target-home",
                   style={"padding": "1rem", "transform" : "rotate(90deg)", "font-size": "2rem", "color": "#999999"}, ),
# Descripción del problema
            html.P('''
                    This dataset contains <user, timestamp, artist, song> tuples collected from Last.fm API, 
                    using the user.getRecentTracks() method.
                    This dataset represents the whole listening habits (till May, 5th 2009) for nearly 1,000 users.
                   ''',
            style = { "font-color": "#666666", "font-size": "16px", "margin": "1rem auto 0", "padding": "0 12rem"}, className="text-muted"
            
            ),


            html.Hr(style = {"width" : "100px", "border": "3px solid #999999", "background-color": "#999999", "margin": "3rem auto"}),

        ],
        style = {"text-align": "center"},
        ),
    ),

    dbc.Container(
        [

            dbc.CardGroup([
                dbc.Card(
                    [
                        dbc.CardImg(
                            src="/assets/images/dashboard.jpeg", top=True),
                        dbc.CardBody(
                            [
                                html.H3("Dashboard", style = {"color": "#66666"}),
                                html.P(
                                    '''Acá se pueden obtener las estadísticas básicas de los ratings
                                    
                                    ''',
                                    className="card-text", style = {"font-size": "15px"},
                                ),
                                dbc.Button(
                                    "Dashboard", color="primary", href="/page-5"),
                            ],
                            className="text-center"
                        ),
                    ],
                    style={"width": "18rem", "margin": "0 1rem 0 0"},
                ),
                dbc.Card(
                    [
                        dbc.CardImg(
                            src="/assets/images/spatial_model.jpeg", top=True),
                        dbc.CardBody(
                            [

                                html.H3("Recomendación", style = {"color": "#66666"}),

                                html.P(
                                    '''Acá puede encontrar el sistema de recomendación basado en perfiles de usuario y canciones con la primera mitad de los datos de ratings.''',
                                    className="card-text", style = {"font-size": "15px"},
                                ),
                                dbc.Button("Sistema de recomendación",
                                           color="primary", href="/page-2"),
                            ],
                            className="text-center"
                        ),
                    ],
                    style={"width": "18rem"},
                ),

                dbc.Card(
                    [
                        dbc.CardImg(
                            src="/assets/images/map.png", top=True),
                        dbc.CardBody(

                            [  html.H3("Exploración por usuarios", style = {"color": "#66666"}),

                                html.P(
                                    '''
                                    Acá puede encontrar las predicciones y sistema para usuarios nuevos y antiguos
                                    ''',
                                    className="card-text", style = {"font-size": "15px"},
                                ),

                                dbc.Button("Exploration", color="primary",
                                           href="/page-3", style={"align": "center"}),
                            ],
                            className="text-center"
                        ),
                    ],
                    style={"width": "18rem", "margin": "0 0 0 1rem"},                
                    )

            ]),

            html.Hr(style = {"width" : "100px", "border": "3px solid #999999", "background-color": "#999999", "margin": "3rem auto"}),

            dbc.Row(


                dbc.Col(
                
               
                html.H1("PARTNERS"),
                style = {"align": "center", "color": "#66666", "margin" : "0 auto 2rem"},
                className="text-center",


                ),

            ),

            dbc.Row ([

                dbc.Col (

                    html.Img(src="/assets/images/uniandes.png", className="img-fluid"),
                    className = "d-flex justify-content-center align-items-center",


                ),          


            ], 
            style = {"padding" : "0 0 5rem"}),
        ]

    )

])

dashboard = html.Div([

    top_cards,
       dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [

                                    html.H3("Analysis Selection",
                                            className="card-title",
                                            id="seleccion analisis"),
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "Region", "value": 0},
                                            {"label": "Department", "value": 1}
                                        ],
                                        value=0,
                                        id="base select",
                                        # switch=True,
                                        # className="md",
                                        style={'display': 'inline-block'}
                                    ),
                                    dbc.RadioItems(
                                        options=[
                                            {"label":1, "value": 1} 
                                        ],
                                        value=0,
                                        id="option select",
                                        # switch=True,
                                        # className="md",
                                        style={'display': 'inline-block'}
                                    ),

                                ]
                            ),
                        ],
                    )
                ],
                className="mt-1 mb-2 pl-3 pr-3"
            ),
        ],
    ),



    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [

                                    dcc.Dropdown(
                                        clearable=False,
                                        # className="float-right",
                                        id="name list",
                                        style=dict(
                                            width='50%',
                                            verticalAlign="middle", 
                                            # position = "fixed",
                                            # top      = "0px",
                                            # right    = "0px"
                                        )
                                    ),

                                    # dcc.Slider(
                                    #     # min=min(ans),
                                    #     # max=max(ans),
                                    #     step=None,
                                    #     marks={
                                    #         i: i for i in ans
                                    #     },
                                    #     value=ans[0],
                                    #     id='dash slider',
                                    #     included=False
                                    # ),  

                                    html.H5("Drill down analysis",
                                            className="card-title"),

                                    dcc.Graph(
                                        id='dash drill'),
                                    dbc.RadioItems(
                                        options=[
                                            {"label": 1, "value": 1} 
                                        ],
                                        value="SEXE",
                                        id="variable",
                                        # switch=True,
                                    ),

                                ]
                            ),
                        ],
                    )
                ],
                className="mt-1 mb-2 pl-3 pr-3"
            ),
        ],
    ),

    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H5("Regions Analysis",
                                            className="card-title"),

                                    dcc.Graph(id='dash region'),
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
                                    html.H5("Time Analysis",
                                            className="card-title"),

                                    dcc.Graph(id='dash time'),
                                ]
                            ),
                        ],
                    )
                ],
                className="mt-1 mb-2 pl-3 pr-3", lg="6", sm="12", md="auto"
            ),
        ],
    ),


],
    className='container',
)




aboutus = html.Div([

    dbc.CardDeck([

        dbc.Card([

            html.Div([

                 dbc.CardImg(src="assets/images/profiles/ocampo.jpg",
                             top=True, className="img-circle", style = {"margin-top": "1.125rem"}),
                 dbc.CardBody([
                     html.H4("David Ocampo",
                             className="card-title m-a-0 m-b-xs"),
                     html.Div([
                         html.A([
                                html.I(className="fa fa-linkedin"),
                                html.I(className="fa fa-linkedin cyan-600"),
                                ], className="btn btn-icon btn-social rounded white btn-sm", 
                                href="https://www.linkedin.com/in/david-alejandro-o-710247163/"),

                         html.A([
                             html.I(className="fa fa-envelope"),
                             html.I(className="fa fa-envelope red-600"),
                         ], className="btn btn-icon btn-social rounded white btn-sm", 
                            href="mailto:daocampol@unal.edu.co"),

                     ], className="block clearfix m-b"),
                     html.P(
                         "Statistician at Allianz. Universidad Nacional. Universidad de Los Andes.",
                         className="text-muted",
                     ),

                 ]

                 ),

                 ],
                className="opacity_1"
            ),


        ],
            className="text-center",

        ),

        dbc.Card([

            html.Div([

                dbc.CardImg(src="/assets/images/profiles/quinonez.png",
                            top=True, className="img-circle", style = {"margin-top": "1.125rem"}),
                dbc.CardBody([
                    html.H4("Juan David Quiñonez",
                            className="card-title m-a-0 m-b-xs"),
                    html.Div([
                        html.A([
                            html.I(className="fa fa-linkedin"),
                            html.I(className="fa fa-linkedin cyan-600"),
                        ], className="btn btn-icon btn-social rounded white btn-sm", href="https://www.linkedin.com/in/juandavidq/"),

                        html.A([
                            html.I(className="fa fa-envelope"),
                            html.I(className="fa fa-envelope red-600"),
                        ], className="btn btn-icon btn-social rounded white btn-sm", href="mailto:jdquinoneze@unal.edu.co"),

                    ], className="block clearfix m-b"),
                    html.P(
                        "Statistician at BBVA. Universidad Nacional. Universidad de Los Andes.",
                        className="text-muted",
                    ),

                ]

                ),

            ],
                className="opacity_1"
            ),


        ],
            className="text-center",

        ),

    ]),



])
