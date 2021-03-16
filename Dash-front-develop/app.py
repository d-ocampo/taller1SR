from layouts import home, dashboard, aboutus, nombre_cancion, nombre_artista, get_key, prediccion_modelo, base_prediccion,graficar_red, song_dict, art_dict ,ratings, ratings_art ,test_set_a_user,model_a_user,test_predictions_a_user,users_set_a_user, test_set_a_item,model_a_item,test_predictions_a_item,item_set_a_item 
from lay import  risk

from app_ import app
from spatial import spatial
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import math
import json

##Graph libraries
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import pandas as pd


server = app.server

# Resources

# end resources


# Top bar
top_navbar = dbc.Navbar(
    [
        #Nombre de cada página, 
        dbc.NavbarBrand(["Sistemas de Recomendación"],
                        id="top_title", className="ml-2 wd"),

    ],
    color="white",
    sticky="top",
    id="topBar",
    style={'z-index': 1}
)

# end top bar

sidebar_header = dbc.Row(
    [
        dbc.Col(

            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col([html.Img(src="/assets/images/LastFMR.png",
                                         className="img-fluid w-50 text-center w-75 pt-5")], className="text-center"),
                       
                        ],
                    align="center",
                    no_gutters=True,
                    className="justify-content-center"
                ),
                href="#",

            ),
            
        ),
        dbc.Col(
            html.Button(
                # use the Bootstrap navbar-toggler classes to style the toggle
                html.Span(className="navbar-toggler-icon"),
                className="navbar-toggler",
                # the navbar-toggler classes don't set color, so we do it here
                style={
                    "color": "rgba(255,255,255,.5)",
                    "border-color": "rgba(255,255,255,.1)",
                },
                id="toggle",
            ),
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="rigth",
        ),
    ]
)

sidebar = dbc.Navbar([html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be

        dbc.Collapse(
            dbc.Nav(
                [

             
                    dbc.NavLink( [  html.Span(html.I("home", className="material-icons"),
                                           className="nav-icon"),  html.Span("Home", className="nav-text") 
                                           ], href="/", id="page-1-link", className="nav-header"),

                    dbc.NavLink([html.Span(html.I("dashboard", className="material-icons"),
                                           className="nav-icon"),  html.Span("Dashboard", className="nav-text")
                                           ], href="/page-5", id="page-5-link", className="nav-header"),

                     dbc.NavLink([html.Span(html.I("map", className="material-icons"),
                                           className="nav-icon"),  html.Span("Recomendación", className="nav-text")
                                           ], href="/page-2", id="page-2-link", className="nav-header"),

                     dbc.NavLink([html.Span(html.I("favorite", className="material-icons"),
                                           className="nav-icon"),  html.Span("Exploración", className="nav-text")
                                           ], href="/page-3", id="page-3-link", className="nav-header"),


                    dbc.NavLink([html.Span(html.I("supervisor_account", className="material-icons"),
                                           className="nav-icon"),  html.Span("About us", className="nav-text")
                                           ], href="/page-4", id="page-4-link", className="nav-header"),

                     ],
                vertical=True,
                navbar=True
            ),
            id="collapse",
        ),
    ],

),

],
    color="#5663A9",
    dark=True,
    id="sidebar",
    className="mm-show",
)

content = html.Div(id="page-content")
content2 = html.Div([top_navbar,  content], id="content")
app.layout = html.Div([dcc.Location(id="url"),  sidebar, content2])


# fin Navbar


# Establecer ruta de las páginas
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/home"]:
        return home
    elif pathname == "/page-5":
        return dashboard
    elif pathname == "/page-2":
        return spatial
    elif pathname == "/page-3":
        return risk
    elif pathname == "/page-4":
        return aboutus
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    Output("collapse", "is_open"),
    [Input("toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output("top_title", "children"), [Input("url", "pathname")])
def update_topTitle(pathname):
    if pathname in ["/", "/home"]:
        return "Sistema de recomendación - LastFM 1k"
    elif pathname == "/page-5":
        return "Dashboard"
    elif pathname == "/page-2":
        return "Recomendación"
    elif pathname == "/page-3":
        return "Exploración"
    elif pathname == "/page-4":
        return "About us"



##############################################
#### Recomendations S ########################
##############################################


###### Dash Board ################

#Cambiar el valor de las tarjetas - lugar 
@app.callback(
    Output("place", "children"),
    [Input("base select", "value")],
)
def place(value):
    if value==0:
        return "Region"
    else: 
        return "Department"


@app.callback(
    Output("dash time", "figure"),
    [Input("dash slider", "value"),
     Input("base select", "value"),
     Input("name list", "value"),
     Input("variable", "value"),
     Input("option select", "value")
     ],
)
def time_graph(year, base,terreno,var,opcion):
    df=seleccion_base(int(base),int(opcion))
    if int(base)==0:
        fig = px.line(df[df['REGION']==cod_reg[terreno]].sort_values(by=['ANS']), x="ANS", y=dict_variables[var])
    else:
        fig = px.line(df[df['REGION']==cod_dep[terreno]].sort_values(by=['ANS']), x="ANS", y=dict_variables[var])      
    return fig

########### Reconmendation #################

#valor del drodown, la idea listar usuarios
@app.callback(
    Output("recomend drop", "options"),
    [Input("recomend seleccion", "value")],
)
def place(value):
    if value==1:
        return [{"label": i, "value": i} for i in users_set_a_user][0:20]
    else: 

        return [{"label": nombre_artista(i), "value": i} for i in item_set_a_item][0:20]

#graficar la red con los valores del drop
#valor del drodown, la idea listar usuarios
@app.callback(
    Output("recomend red", "figure"),
    [Input("recomend drop", "value"),
     Input("recomend seleccion", "value"),
     Input("recomend slider", "value")],
)
def place(value,seleccion,slider):
    if seleccion == 1:
        show=base_prediccion(value,test_predictions_a_user,'traid',int(slider))
        edges=[(value,itm[1][2],itm[1][1]) for itm in show.iterrows()]
        fig=graficar_red(edges,value)
        return fig
    else:
        show=base_prediccion(value,test_predictions_a_item,'userid',int(slider))
        edges=[(value,itm[1][2],itm[1][1]) for itm in show.iterrows()]
        fig=graficar_red(edges,value)
        return fig    

########### Exploration #################
#valor del drodown, la idea listar usuarios
@app.callback(
    [Output("exploration artgraph", "figure"),
     Output("exploration songgraph", "figure")],
    [Input("exploration button","n_clicks")],
    [State("exploration user", "value"),
     State("exploration pass", "value")],
)
def place(n,user,password):
    if (user==password) & n>=1 :
        df=ratings[ratings['userid']==user][['traid','rating_count']].sort_values('rating_count',ascending=False).head(20)
        df['track-name']=df['traid'].apply(nombre_cancion)
        figsong = px.bar(df, x='track-name', y='rating_count')
        df2=ratings_art[ratings_art['userid']==user][['artid','rating_count']].sort_values('rating_count',ascending=False).head(20)
        df2['artist-name']=df2['artid'].apply(nombre_artista)
        labels = list(df2['artist-name'])
        values = list(df2['rating_count'])
        # Use `hole` to create a donut-like pie chart
        figart = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])       
        return [figart,figsong]

#seleccionar la data de los gráficos
##Modelo item-based
@app.callback(
    [Output('exploration modelo', 'children'),
    Output('exploration real', 'children'),
    Output('exploration prediccion', 'children')],
    [Input('exploration songgraph', 'clickData')], 
    [State('exploration user', "value")])
def display_click_data(clickData,user):
    display=clickData
    song=display["points"][0]["x"]
    real=display["points"][0]["y"]
    est=round(prediccion_modelo(model_a_user,user,get_key(song,song_dict),int(real)),2)
    return 'Modelo basado en usuario para: '+ song,str(real),str(est)




if __name__ == "__main__":
    app.run_server(debug=False,
                   host ='0.0.0.0',
                   port=8000
                   )
    

# Images etc
