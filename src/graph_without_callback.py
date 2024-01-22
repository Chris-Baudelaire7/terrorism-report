import plotly.express as px
import plotly.graph_objects as go
from data_preparation import *
from utils import *
import plotly.figure_factory as ff
import numpy as np


def quincenal_average():
    dfr1 = raw_data.groupby(["year"], as_index=False)["nkill"].sum()
    dfr2 = raw_data.groupby(["year"], as_index=False)["nwound"].sum()
    dfr3 = raw_data.groupby(["year"], as_index=False).size()
    dfr = pd.merge(dfr1, dfr2, on="year")
    dfr = pd.merge(dfr, dfr3, on="year")
    dfr['year'] = pd.to_datetime(dfr['year'], format='%Y')
    dfr.set_index('year', inplace=True)
    dfr = dfr.resample('5A').mean().astype(int).reset_index()
    dfr = dfr[["year", "size", "nwound", "nkill"]]
    dfr['year'] = dfr['year'].dt.year


    fig = go.Figure()

    colors=['rgb(254,224,210)', 'rgb(103,0,13)', 'rgb(203,24,29)']
    marker_colors=['white', "crimson", 'orangered']
    marker_symbol=['circle', "diamond", 'square']
    positions=["bottom center", "top left", "top right"]
    columns=list(dfr.columns[1:])

    for col, color, mcolor, pos, symbol in zip(columns, colors, marker_colors, positions, marker_symbol):
        fig.add_scatter(
            x=dfr["year"], y=dfr[col],
            mode="lines+markers+text",
            text=dfr[col],
            line=dict(color=color),
            marker=dict(size=13, symbol=symbol),
            textposition=pos,
            textfont=dict(size=11), #color=mcolor
            name=col
        )

    fig.add_vrect(
        x0="2000", x1="2015",
        line_width=0, fillcolor="red", opacity=.16,
    )
    
    fig.add_vrect(
        x0="1995", x1="2000",
        line_width=0, fillcolor="lightyellow", opacity=.16,
    )
    
    fig.add_vrect(
        x0="1970", x1="1995",
        line_width=0, fillcolor="red", opacity=.16,
    )

    fig.add_vrect(
        x0="2015", x1="2020",
        line_width=0, fillcolor="lightyellow", opacity=.16,
    )

    fig.add_vline(
        x="2000",
        line_width=.6, line_color="white",
    )

    fig.add_vline(
        x="2015",
        line_width=.6, line_color="white",
    )
    
    fig.add_vline(
        x="1995",
        line_width=.6, line_color="white",
    )

    fig.add_vline(
        x="2020",
        line_width=.6, line_color="white",
    )


    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=100),
        template="plotly_dark",
        hovermode="x",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font={"family": "Lato", "size": 14},
        height=500,
        xaxis=dict(title=None, showgrid=False, nticks=20),
        yaxis=dict(visible=False),
        title={
            "text": (
                    f"<b>Moyenne quinquennale du nombre<br> d'attaque, de blessés et de décès</b><br />"
                    f"<sup style='color:silver'>Moyenne calculée sur une période de 5 ans "
                ),
            "font": {"family": "serif", "size": 30, "color": "white"},
            "x": 0.92,
            "y": 0.96,
            "xanchor": "right",
            "yanchor": "top",
        },
        legend=dict(orientation="h", x=.4,),
        annotations=[
            dict(
                x=2005, y=28000,
                text="Période connaissant<br> une forte augmentation<br>de l'activité terrorites",
                showarrow=False,
                xanchor="center",
                yanchor="middle",
                ax=-100, ay=-30
            ),
            dict(
                x=2017.5, y=17000,
                text="Période connaissant<br> une baisse de<br>l'activité terrorites",
                showarrow=False,
                xanchor="center",
                yanchor="middle",
                # arrowwidth=1,
                # arrowhead=2,
                # arrowcolor="white",
                ax=0, ay=40
            ),
            dict(
                x=1997.5, y=18000,
                text="Période connaissant<br> une baisse<br>de l'activité terrorites",
                showarrow=False,
                xanchor="center",
                yanchor="middle",
                ax=-100, ay=-30
            ),
            dict(
                x=1980, y=18000,
                text="Période connaissant<br> une legère augmentation<br>de l'activité terrorites",
                showarrow=False,
                xanchor="center",
                yanchor="middle",
                ax=-100, ay=-30
            ),
        ]
    )

    return fig




def property_graph():
    data_damage = raw_data[raw_data["property"] == 1].groupby(["year"], as_index=False).size()
    data_nkill = (raw_data[raw_data["property"] == 1]).groupby(["year"], as_index=False)[["nkill", "nwound"]].sum()
    data = pd.merge(data_nkill, data_damage, on="year")
    data["casualty"] = data["nkill"] + data["nwound"]

    fig = px.scatter(data, x="size", y="casualty", size="casualty", color="casualty",
                    color_continuous_scale="reds", trendline="ols")
    fig.update_traces(
        marker=dict(line=dict(color="black"), opacity=1)
    )
    fig.update_coloraxes(showscale=False)

    fig.update_layout(
        hovermode="x",
        font={"family": "Lato", "size": 14},
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=0, r=0, b=30, t=10),
        height=450,
        xaxis=dict(title="Dégâts matériels enregistrés", showgrid=False, zeroline=False),
        yaxis=dict(title="Nombre de victime", showgrid=False, zeroline=False),
        title={
            "text": (
                    f"<b>Lien entre les dégâts matériels<br>et le nombre de victimes</b><br />"
                    f"<sup style='color:silver'>Les dégâts matériels ont-ils été suivis de victimes? "
                ),
            "font": {"family": "serif", "size": 30, "color": "white"},
            "x": 0.1,
                "y": 0.93,
                "xanchor": "left",
                "yanchor": "top",
        },
    )

    return fig



def country_map_by_year():

    df = pd.read_csv("/Users/new/Desktop/Terrorisme/data/terrorism-deaths-rate.csv")

    fig = px.choropleth(df, locations="Code",
                    color="Terrorism deaths per 100,000 people", # lifeExp is a column of gapminder
                    hover_name="Entity", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Reds,
                    animation_frame='Year')

    fig.update_coloraxes(showscale=False)

    for i, _ in enumerate(fig.frames):
        fig.frames[i].data

    fig.update_layout(
        **update_layout_geo,
        height=550,
        dragmode="lasso",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, b=0, t=0),
        sliders=[dict(
            y=.2,
            bgcolor="firebrick",
            bordercolor="black",
            borderwidth=4,
            currentvalue={"prefix": "Taux de décès en "},
            font=dict(family="serif", size=15, color="white"),
            #"),
        )],
        title={
            "text": (
                    f"<b>Taux de décès par 100 mille habitants</b><br />"
                    f"<sup style='color:silver'>situtation globale dans le monde"
                ),
            "font": {"family": "serif", "size": 32, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    fig["layout"]["updatemenus"] = [dict(
        buttons=[
            {
                "args": [None, {"frame": {"duration": 250, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 700,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                                "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        direction="right",
        showactive=False,
        type="buttons",
        pad=dict(r=10),
        font=dict(family="serif", size=12, color="white"),
        x=.1, y=0.1,
        bgcolor="black", bordercolor="firebrick", borderwidth=1
    )]

    return fig


def scatter_geo():
    data = raw_data.copy()[["country", "city", "latitude", "longitude", "nkill", "nwound"]]
    data["casualties"] = data["nkill"] + data["nwound"]
    data.fillna(0, inplace=True)
    data.sort_values(by="nkill", ascending=False, inplace=True)
    data.reset_index(drop=True, inplace=True)
    data = data[data.country == "Iraq"]

    mapbox_access_token = 'pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw'

    fig = go.Figure(go.Scattermapbox(
        lon = data['longitude'],
        lat = data['latitude'],
            mode = 'markers',
            marker = go.scattermapbox.Marker(
                #size = data['nkill'],
                color = data['nkill']/10,
            ),
        ))

    fig.update_layout(
            font={"family": "Lato", "size": 14},
            template="plotly_dark",
            margin=dict(l=0, r=0, t=0, b=0),
            autosize = True,
            hovermode = 'closest',
            height=300,
            width=400,
            showlegend=False,
            mapbox = dict(
                accesstoken = mapbox_access_token,
                center = {'lat': (data.latitude.min() + data.latitude.max())/2,
                        'lon': (data.longitude.min() + data.longitude.max())/2},
                bearing = 0,
                pitch = 40,
                zoom = 5,
                style = "dark", # try basic, dark, light, outdoors, or satellite.
            ),
        )


    return fig


