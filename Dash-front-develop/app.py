from layouts import ruta, home, dashboard, aboutus, nombre_cancion, nombre_artista, get_key, prediccion_modelo,crear_modelo ,base_prediccion,graficar_red,crear_nueva, song_dict, art_dict ,ratings, ratings_art, rmse ,test_set_a_user,model_a_user,test_predictions_a_user,users_set_a_user, test_set_a_item,model_a_item,test_predictions_a_item,item_set_a_item, model_cos_user, test_set_cos_user, model_cos_item, test_set_cos_item, model_person_user,test_set_person_user, model_person_item, test_set_person_item 
from lay import  risk
from script_inicial.RMSE import calcular_rmse 


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


###### DashBoard ################

#Cambiar el valor de las tarjetas rmse
@app.callback(
    Output("dashboard rmse", "figure"),
    [Input("dashboard base", "value"),
     Input("dashboard model", "value"),
     Input("dashboard useritem", "value")],
)
def place(base,model,useritem):
    fig=px.line(rmse[(rmse['base']==base) & (rmse['modelo']==model) & (rmse['user']==useritem)],x="k",y="rmse")
    return fig

# ejecutar los modelos nuevamente
@app.callback(
    Output("dashboard respuesta", "children"),
    [Input("dashboard corrermodelo", "n_clicks"),
     ],
    [State("dashboard testmodelo","value"),
     State("dashboard modelmodelo","value"),
     State("dashboard useritemmodelo","value"),
     State("dashboard trimmodelo","value"),
     State("dashboard kmodelo","value")]
)
def time_graph(click,test, modelo,userbased,recorte,k): 
    if (userbased==True) & (modelo=='cosine'):
        base=ratings
        col='traid'
        nombre='cos_user'
    if (userbased==True) & (modelo=='pearson'):
        base=ratings
        col='traid'
        nombre='person_user'
    if (userbased==False) & (modelo=='cosine'):
        base=ratings_art
        col='artid'
        nombre='cos_item'
    if (userbased==False) & (modelo=='pearson'):
        base=ratings_art
        col='artid'
        nombre='person_item'     
    if click:
        crear_modelo(test, modelo, userbased, k, nombre, base,col,recorte)
    return 'Modelo con test: '+ str(test)+' Modelo elegido: ' +str(modelo)+',¡Creado con éxito!'

########### Reconmendation #################

#valor del drodown, la idea listar usuarios
@app.callback(
    Output("recomend drop", "options"),
    [Input("recomend seleccion", "value")],
)
def place(value):
    if value==1:
        return [{"label": i, "value": i} for i in users_set_a_user][0:100]
    else: 

        return [{"label": nombre_artista(i), "value": i} for i in item_set_a_item][0:100]

#graficar la red con los valores del drop
#valor del drodown, la idea listar usuarios
@app.callback(
    [Output("recomend red", "figure"),
     Output("recomend lista","children")],
    [Input("recomend drop", "value"),
     Input("recomend seleccion", "value"),
     Input("recomend slider", "value")],
)
def place(value,seleccion,slider):
    if seleccion == 1:
        show=base_prediccion(value,test_predictions_a_user,'traid',int(slider))
        lista_recomend=list(show['track-name'])
        edges=[(value,itm[1][2],itm[1][1]) for itm in show.iterrows()]
        fig=graficar_red(edges,value)
        return fig, [html.Li(x) for x in lista_recomend]
    else:
        show=base_prediccion(value,test_predictions_a_item,'userid',int(slider))
        lista_recomend=list(show['user-name'])
        edges=[(value,itm[1][2],itm[1][1]) for itm in show.iterrows()]
        fig=graficar_red(edges,value)
        return fig ,[html.Li(x) for x in lista_recomend]   

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
        figart = px.pie(df2, values='rating_count', names='artist-name')   
        return [figart,figsong]

#seleccionar la data de los gráficos
##Modelo user-based
@app.callback(
    [Output('exploration modelo', 'children'),
    Output('exploration real', 'children'),
    Output('exploration prediccion', 'children')],
    [Input('exploration songgraph', 'clickData'),
     Input('exploration artgraph', 'clickData'),
     Input('exploration model', 'value')], 
    [State('exploration user', "value")])
def display_click_data(clickDataSong,clickDataArt,model,user):
    while clickDataSong:
        display=clickDataSong
        song=display["points"][0]["x"]
        real=display["points"][0]["y"]    
        if model=='cosine':
            modelo=model_cos_user
        else:
            modelo=model_person_user    
        est=round(prediccion_modelo(modelo,user,get_key(song,song_dict),int(real)),2)
        clickDataArt=False
        return 'Modelo basado en usuario para: '+ song,str(real),str(est)
    while clickDataArt:
        display=clickDataArt
        artist=display["points"][0]["label"]
        real=display["points"][0]["value"]
        if model=='cosine':
            modelo=model_cos_item
        else:
            modelo=model_person_item
        est=round(prediccion_modelo(modelo,user,get_key(artist,art_dict),int(real)),2)
        clickDataSong=False
        return 'Modelo basado en artista para: '+ artist,str(real),str(est)

##Modelo user-based
@app.callback(
    Output('exploration mensaje', 'children'),
    [Input('exploration newbutton', 'n_clicks')], 
    [State('exploration newuser', "value"),
     State('exploration newsong', "value"),
     State('exploration newartist', "value")])
def display_click_data(click,user,songs,artist):
    if click>1:
        if artist is None:
            return 'Por favor seleccione al menos un artista'
        elif songs is None:
            return 'Por favor seleccione al menos una canción'
        else:
            #canciones
            canciones=songs
            usuario=[user]*len(canciones)
            cals=[1]*len(canciones)
            df = pd.DataFrame([usuario,canciones,cals]).transpose()
            df.columns=['userid','traid','rating_count']

            artistas=artist
            usuario_art=[user]*len(artistas)
            cals_art=[1]*len(artistas)
            df2 = pd.DataFrame([usuario_art,artistas,cals_art]).transpose()
            df2.columns=['userid','artid','rating_count']
            
            crear_nueva(df,df2,ratings,ratings_art)

            return 'Usuario creado con éxito'








if __name__ == "__main__":
    app.run_server(debug=False,
                   host ='0.0.0.0',
                   port=8000,
                   threaded=True,
                   dev_tools_hot_reload=True
                   )
    

# Images etc
