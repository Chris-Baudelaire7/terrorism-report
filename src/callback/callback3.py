from dash import Input, Output, callback, State
import plotly.express as px
import plotly.graph_objects as go
from data_preparation import *
from utils import *

def render_pie(df, col, title, name1, name2, graph, metric):
    
    if graph == "pie":
        if metric == "size":
            data = df[col].value_counts().reset_index()
            metric = "count"
        else:
            data = df.groupby(col, as_index=False)[["nkill", "casualties"]].sum()
        
        data = data.set_index(col).rename(index={1:name1, 0:name2}).reset_index()
        
        fig = go.Figure(go.Pie(
            labels=data[col], values=data[metric],
            textposition="outside", textinfo="label+percent", 
            textfont=dict(size=15, family="Lato"),
            marker=dict(colors=px.colors.sequential.Reds_r), pull=[.2,0],
            insidetextorientation='radial', 
        ))

        fig.update_layout(
            height=450,
            # template="plotly_dark",,
            showlegend=False,
            margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            title={
                "text": (
                        f"<b>{title}</b><br />"
                    ),
                "font": {"family": "serif", "size": 30, "color": "black"},
                "x": 0.98,
                "y": 0.93,
                "xanchor": "right",
                "yanchor": "top",
            },
        )
        
    else:
        columns={1: name1, 0: name2}
        
        if metric == "size":
            data = df[col].value_counts().reset_index()
            dframe = df.groupby(["year", col], as_index=False).size()
        else:
            dframe = df.groupby(["year", col], as_index=False)[["nkill", "casualties"]].sum()
        
        dframe = pd.pivot_table(dframe, index="year", columns=col, values=metric).reset_index()
        dframe.rename(columns=columns, inplace=True)
        color_discrete_sequence=['rgb(239,59,44)', 'rgb(103,0,13)']
        
        fig = absolute_relative_figure(dframe, color_discrete_sequence, "relative", title)
        
    return fig


@callback(
    Output("pie-success", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("severity-metric-versus", "value"),
    Input("graph-type-versus", "value"),
)
def comparison(range_date, area, metric, graph):
    data_date = data_date_filter(range_date)
    data = data_geo_filter(data_date, area)   
    fig = render_pie(data, "success", "Taux d'attaque réusssie<br>échouées",
                     "Réussie", "Échouées", graph, metric)  
    return fig


@callback(
    Output("pie-suicide", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("severity-metric-versus", "value"),
    Input("graph-type-versus", "value"),
)
def comparison(range_date, area, metric, graph):
    data_date = data_date_filter(range_date)
    data = data_geo_filter(data_date, area)   
    fig = render_pie(data, "suicide", "Taux d'attaque suicide<br>vs non suicide",
                     "Suicide", "Non suicide", graph, metric)
    return fig


@callback(
    Output("pie-individual", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("severity-metric-versus", "value"),
    Input("graph-type-versus", "value"),
)
def comparison(range_date, area, metric, graph):
    data_date = data_date_filter(range_date)
    data = data_geo_filter(data_date, area)   
    fig = render_pie(
        data, "individual","Taux d'attaque en solo<br>vs à plusieurs", 
        "En solo", "À plusieurs", graph, metric
    )
    return fig


# @callback(
#     Output("pie-multiple", "figure"),
#     Input("range-slider", "value"),
#     Input("filter-geo", "value"),
#     Input("severity-metric-versus", "value"),
#     Input("graph-type-versus", "value"),
# )
# def comparison(range_date, area, metric, graph):
#     data_date = data_date_filter(range_date)
#     data = data_geo_filter(data_date, area)   
#     fig = render_pie(data, "multiple", "Taux d'attaque multiple<br>vs unique",
#                      "Multiple", "Unique", graph, metric)
#     return fig


@callback(
    Output("pie-crit", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("severity-metric-versus", "value"),
    Input("graph-type-versus", "value"),
)
def comparison(range_date, area, metric, graph):
    data_date = data_date_filter(range_date)
    data = data_geo_filter(data_date, area)   
    fig = render_pie(data, "crit1", "À but politique/religieux/<br>économique/social ou non",
                     "Oui", "Non", graph, metric)
    return fig




@callback(
    Output("graph", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"), # 
    Input("rel-abs-damage", "value"),
)
def update_graph_damage(range_date, area, rel_or_abs):
    data_date = data_date_filter(range_date)
    data_filter = data_geo_filter(data_date, area)   
  
    data_damage1 = data_filter[data_filter["property"] == 0].groupby("year", as_index=False).size()
    data_damage2 = data_filter[data_filter["property"] == 1].groupby("year", as_index=False).size()
    data_damage3 = data_filter[data_filter["property"] == -9].groupby("year", as_index=False).size()
    
    columns={"size": "Inconnu", "size_x": "Sans dégâts matériels", "size_y":"Avec dégâts matériels"}

    data = pd.merge(data_damage1, data_damage2, on="year")
    data = (pd.merge(data, data_damage3, on="year")).rename(columns=columns)
    data = data.copy()[["year", "Inconnu", "Sans dégâts matériels", "Avec dégâts matériels"]]
    
    color_discrete_sequence=['rgb(254,224,210)',  'rgb(203,24,29)', 'rgb(103,0,13)']
    
    title = "Repartion en pourcentage des attaques selon<br>qu'il y ait eu des coûts ou non" \
            if rel_or_abs == "relative" else \
            "Évolution des attaques selon qu'il y<br>ait eu des coûts ou non"
    
    fig = absolute_relative_figure(data, color_discrete_sequence, rel_or_abs, title)
        
    return fig







@callback(
    Output("attack-by-severity", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
    Input("severity-metric", "value"),
    Input("rel-abs", "value"),
)
def severity(range_date, area, group, attack, target, weapon, cause, rel_abs):
    # fiter data 
    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)
    data = data_filter(data, group, attack, target, weapon)
    
    if cause == "nkill":
        data = data.groupby(["year", "nkill_categories"], as_index=False).size()
        title = "Repartion des décès par classe de gravité"
        cause = "size"
    else:
        data = data.groupby(["year", "nkill_categories"], as_index=False)[[cause]].sum()
        title = "Repartion des victimes par classe de gravité"
        
    data = data.pivot_table(index="year", columns="nkill_categories", values=cause)
    data = data.fillna(0).reset_index()
    
    colors = ['rgb(252,187,161)','rgb(251,106,74)','rgb(203,24,29)','rgb(103,0,13)']
    
    fig = absolute_relative_figure(data, colors, rel_abs, title)
    
    return fig




@callback(
    Output("pie-severity", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("severity-metric", "value"),
    Input("weapon", "value"),
)
def pie_chart_severity(range_date, area, group, attack, target, cause, weapon):
    # fiter data
    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)
    data = data_filter(data, group, attack, target, weapon)
    
    if cause == "nkill":
        data = data['nkill_categories'].value_counts().reset_index()
        title = "Répartition entre les différentes<br>classes de décès"
        cause = "count"
    else:
        data = data.groupby(["nkill_categories"], as_index=False)[[cause]].sum()
        title = "Répartition entre les différentes<br>classes de victime"
        
    colors = ['rgb(252,187,161)','rgb(251,106,74)','rgb(203,24,29)','rgb(103,0,13)']
    
    fig = go.Figure(go.Pie(
            labels=list(data["nkill_categories"].values), values=data[cause],
            textposition="outside", textinfo="label+percent", 
            textfont=dict(size=15, family="serif"),
            marker=dict(colors=colors),
            insidetextorientation='radial', 
            pull=[0.16, 0, 0]
        ))

    fig.update_layout(
            height=455,
            # template="plotly_dark",,
            showlegend=False,
            margin=dict(autoexpand=True, l=0, r=0, t=80),
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            
            title={
          
                "text": (
                        f"<b>{title}</b><br />"
                        f"<sup style='color:silver'>Situation globale dans le monde"
                    ),
                "font": {"family": "serif", "size": 28, "color": "black"},
                "x": 0.93,
                "y": 0.91,
                "xanchor": "right",
                "yanchor": "top",
            },
        )
        
    return fig


@callback(
    Output("number-attack-with-damage-by-category", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("choose-category", "value"),
    Input("cost", "value"),
)
def number_attack_with_damage(range_date, area, category, cost):
    data_date = data_date_filter(range_date)
    data_geo = data_geo_filter(data_date, area)   
    
    data_f = data_geo[data_geo[category] != "Unknown"]
    data = (data_f[data_f["property"]==1])[category].value_counts().reset_index()
    df = (data_f[data_f["propextent_txt"]==cost])[category].value_counts().reset_index()
    
    def figure(dfr):
        dfr.rename(columns={"Vehicle (not to include vehicle-borne explosives, i.e., car or truck bombs)": "Vehicle"}, inplace=True)
        fig = px.bar(dfr.nlargest(columns="count", n=10), x="count", y=category, color="count", 
                     orientation="h", color_continuous_scale="reds", text="count")
        fig.update_coloraxes(showscale=False)
        fig.update_traces(
            textposition="auto",
            textfont=dict(family="serif", size=14)
        )
        fig.update_yaxes(categoryorder='total ascending')
        return fig
    
    fig1 = figure(data)
    fig2 = figure(df)
    
    def layout(title):
        return dict(
            height=455,
            # template="plotly_dark",,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(visible=False, showgrid=False),
            yaxis=dict(title=None, showgrid=False),
            margin=dict(autoexpand=True, l=0, r=0, t=100, b=0),
            title={
                "text": (
                        f"<b>{title}</b><br />"
                        f"<sup style='color:silver'>situtation globale dans le monde"
                    ),
                "font": {"family": "serif", "size": 30, "color": "black"},
                "x": 0.98,
                "y": 0.93,
                "xanchor": "right",
                "yanchor": "top",
            },
        )
    fig1.update_layout(**layout("Activités terrosriste ayant<br>causés des dommages"))
    fig2.update_layout(**layout("Evolution du nombre d'attaques<br>terroriste par gravité"))
    
    return fig2


