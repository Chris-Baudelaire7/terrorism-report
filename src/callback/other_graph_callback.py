from dash import Input, Output, callback, State
import plotly.express as px
import plotly.graph_objects as go
from data_preparation import *
from utils import *


@callback(
    Output("country-map-by-year", "figure"),
    Input("dropdown-cause", "value"),
)
def country_map_by_year(cause):
    
    if cause == "nwound" or cause == "nkill":
        title = "Carte graphique du nombre total<br>de décès par pays" if cause == "nkill" else \
                "Carte graphique du nombre total<br>de blessés par pays"
    else:
        data_size = df.groupby(["year", "code", "country"], as_index=False).size()
        title = "Carte graphique du nombre total<br>d'incidence par pays"
    
    data_size = df.groupby(["year", "code", "country"], as_index=False).size()
    data_victim = df.groupby(["year", "code", "country"], as_index=False)[["nkill", "nwound"]].sum()
    
    data = pd.merge(data_size, data_victim, on=["year", "code", "country"])
    data["casualty"] = data["nkill"] + data["nwound"] + data["size"]
    data.fillna(0, inplace=True)

    fig = px.choropleth(data, locations="code",
                        color=cause, # lifeExp is a column of gapminder
                        hover_name="country", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Reds,
                        animation_frame='year')
    
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
            currentvalue={"prefix": "Nombre d'attaque terroriste en "},
            font=dict(family="serif", size=15, color="white"),
            #"),
        )],
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