from dash import Input, Output, callback, html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from data_preparation import *
from utils import *




@callback(
    Output("geo-map", "figure"),
    Output("geo-map_", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
    # Input("choice_serie_type_countries", "value"),
)
def region_map(range_date, geo, cause, group, attack, target, weapon):
    data = data_date_filter(range_date)
    data = data_geo_filter(data, geo)
    data = data_filter(data, group, attack, target, weapon) 
    
    data_attack = data.groupby(["code", "country"], as_index=False).size()
    data_casualty = data.groupby(["code", "country"], as_index=False)[["nkill", "nwound"]].sum()
    data = pd.merge(data_attack, data_casualty, on=["code", "country"])
    data["casualties"] = data["nkill"] + data["nwound"]
    
    fig = go.Figure(
        go.Choropleth(
            z=data[cause],
            locations=data["code"],
            colorscale=px.colors.sequential.Reds[1:],
            marker=dict(line=dict(width=.3, color="black")),
            zmin=0, zmax=8000,
            customdata=data,
            showscale=False
        )
    )
    
    fig2 = go.Figure(
        go.Choropleth(
            z=data[cause],
            locations=data["code"],
            colorscale=px.colors.sequential.Reds[1:],
            marker=dict(line=dict(width=.3, color="black")),
            customdata=data,
            showscale=False
        )
    )
    
    def layout(height):
        return dict(
            **update_layout_geo,
            height=height,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),

        )
        
    fig.update_layout(**layout(600))
    fig2.update_layout(**layout(150))
    
    return fig, fig2





@callback(
    Output("serie-area", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
    # Input("choice_serie_type_countries", "value"),
)
def eries_area(range_date, geo, cause, group, attack, target, weapon):
    data = data_date_filter(range_date)
    data = data_geo_filter(data, geo)
    data = data_filter(data, group, attack, target, weapon) 
    
    data_attack = data.groupby(["year"], as_index=False).size()
    data_casualty = data.groupby(["year"], as_index=False)[["nkill", "nwound", "casualties"]].sum()
    data = pd.merge(data_attack, data_casualty, on=["year"])
    data["cumsum"] = data[cause].cumsum()
    
    fig = px.bar(data, x="year", y=cause, color=cause, color_continuous_scale="reds")
    fig.update_coloraxes(showscale=False)
    
    fig.add_scatter(
        x=data["year"], y=data["cumsum"],
        yaxis="y2", name="Somme cumulée",
        line=dict(width=2, color='firebrick'),
    )
    
    if cause == "nkill":
        title = "Évolution du nombre de décès dus<br>à l'activité terroriste"
    if cause == "nwound":
        title = f"Évolution du nombre de blessés dus<br> à l'activité terroriste"
    if cause == "casualties":
        title = f"Évolution du nombre de blessés dus<br> à l'activité terroriste"
    if cause == "size":
        title = f"Évolution du nombre d'attaque<br>terroriste"
    
    fig.update_layout(
        **update_layout_simple,
        bargap=.1,
        showlegend=False,
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(title="Incidence", showgrid=False),
        yaxis2=dict(
            title="Somme cumulée", showgrid=False,
            anchor="free",
            overlaying="y",
            side="right",
            position=1
        ),

        font=dict(family="serif", color="white"),
        height=450,
        title={
            "text": (
                    f"<b>{title}</b><br />"
                    f"<sup style='color:silver'>{geo}: 1970 à 2017</sup>"
                ),
            "font": {"family": "serif", "size": 30, "color": "white"},
            "x": 0.98,
                "y": 0.93,
                "xanchor": "right",
                "yanchor": "top",
        },
    )

    
    return fig





@callback(
    Output("share", "children"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def share_of(range_date, geo, cause, group, attack, target, weapon):
    colors = ['rgb(239,59,44)', 'rgb(103,0,13)',]
    rel_abs = "relative"
    df = raw_data.copy()
    
    def group_data(df):
        if cause == "nkill":
            title = "Part de décès en pourcentage dans le nombre<br>total de décès dus au terrorisme"
            title_pie = "Repartition Pourcentage du<br>nombre de décès"
            df = df.groupby(["year"], as_index=False)[cause].sum()
        if cause == "nwound":
            title = "Part de blessés en pourcentage dans le nombre<br>total de blessés dus au terrorisme"
            title_pie = "Repartition Pourcentage du<br>nombre de blessés"
            df = df.groupby(["year"], as_index=False)[cause].sum()
        if cause == "casualties":
            title = "Part de victimes en pourcentage dans le nombre<br>total de victimes dus au terrorisme"
            title_pie = "Repartition Pourcentage<br>du nombre de victimes"
            df = df.groupby(["year"], as_index=False)[cause].sum()
        if cause == "size":
            title = "Part des attacques en pourcentage dans le nombre<br>total des attacques dus au terrorisme"
            title_pie = "Repartition Pourcentage du<br>nombre d'attaque terroriste"
            df = df.groupby(["year"], as_index=False).size()
            
        return df, title, title_pie
    
    data = data_date_filter(range_date)
    data = data_geo_filter(data, geo)
    data = data_filter(data, group, attack, target, weapon) 
    
    if geo == "Monde" or geo == "Les autres pays":
        children =[]
    else:
        
        if geo in list(raw_data.continent.unique()):
            df = df[df.continent != geo]
        if geo in list(data.region.unique()):
            df = df[df.region != geo]
        if geo in countries_most_affected:
            df = df[df.country != geo]
            
        data, title, title_pie = group_data(data)
        data.rename(columns={cause: geo}, inplace=True)
        df, _, _ = group_data(df)
        df.rename(columns={cause: "Le reste du monde"}, inplace=True)
                        
        merged_data = pd.merge(data, df, on="year")
        fig = absolute_relative_figure(merged_data, colors, rel_abs, title)
        
        dframe = merged_data.set_index("year").sum().reset_index()
        
        fig2 = go.Figure(go.Pie(
                labels=dframe["index"], values=dframe[0],
                textposition="outside", textinfo="label+percent", 
                textfont=dict(size=13.6, family="Lato"),
                marker=dict(colors=colors),
                insidetextorientation='radial', 
                pull = [.2]+[0] * 10, # hole=.5
            ))
                    
        fig2.update_layout(
            height=450,
            template="plotly_dark",
            showlegend=False,
            margin=dict(autoexpand=True, l=0, r=0, t=80),
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            title={
                "text": (
                        f"<b>{title_pie}</b><br />"
                        f"<sup style='color:silver'>En comparaison au reste du monde"
                    ),
                "font": {"family": "serif", "size": 30, "color": "white"},
                "x": 0.93,
                "y": 0.86,
                "xanchor": "right",
                "yanchor": "top",
            },
        )

            
        children = [
            html.Div(className="col-lg-7", children=[
                dcc.Loading(dcc.Graph(id="share-graph", figure=fig), color="firebrick", type="dot"),
            ]),
            
            html.Div(className="col-lg-5", children=[
                dcc.Loading(dcc.Graph(id="share-dist", figure=fig2), color="firebrick", type="dot"),
            ]),
            
            html.Div(className="mt-3", children=[
                
                dcc.Markdown(
                    "Dans l'ensemble, le nombre d'attaques terroristes dans le monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflitsrégionaux et internationaux. Au cours de cette période, des groupes terroristes tels qu'Al-Qaïda et l'Étatislamique (ISIS) sont devenus des acteurs mondiaux majeurs du terrorisme, lançant des attaques à l'échelleinternationale et inspirant des cellules terroristes dans de nombreux pays.",
                                            
                    className="preambule_text",
                ),
                
            ]),
    
        ]
    
    return children