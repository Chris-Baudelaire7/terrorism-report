from dash import Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from data_preparation import *
from utils import *



    


@callback(
    Output("country-map", "figure"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def global_incidence_timeseries(cause, group, attack, target, weapon):
    data = data_filter(raw_data, group, attack, target, weapon)
    
    if cause == "nwound" or cause == "nkill":
        data = data.groupby(["code", "flag", "flag_country", "country"], as_index=False)[cause].sum()
        title = "Carte graphique du nombre total<br>de décès par pays" if cause == "nkill" else \
                "Carte graphique du nombre total<br>de blessés par pays"
    else:
        data = data.groupby(["code", "flag", "flag_country", "country"], as_index=False).size()
        title = "Carte graphique du nombre total<br>d'incidence par pays"
        
    data.fillna(0, inplace=True)
            
    fig = go.Figure(
        go.Choropleth(
            z=data[cause],
            locations=data["code"],
            colorscale=["black"]+ px.colors.sequential.Reds[1:],
            showscale=True,
            marker=dict(line=dict(width=.3, color="black")),
            customdata=data,
            colorbar=dict(
                orientation='h',
                y=0, len=.8, thickness=13
            ),
            zmin=0,
            zmax=data[cause].max()-20000,
        )
    )
    
    fig.update_layout(
        **update_layout_geo,
        dragmode="lasso",
        height=600,
        # template="plotly_dark",,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=90),
        title={
            "text": (
                    f"<b>{title}</b><br />"
                    f"<sup style='color:silver'>Nombre total entre 1970 et 2020"
                ),
            "font": {"family": "serif", "size": 30, "color": "black"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
        annotations = [dict(
        x=0.55,
        y=-0.08,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
            CIA World Factbook</a>',
        showarrow = False
    )]

    )
    
    
    
    
    
    return fig



@callback(
    Output("ranking", "figure"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
    Input("country-map", "selectedData"),
)
def ranking(cause, group, attack, target, weapon, selectedData):
    if selectedData:
        list_country = [point["customdata"][3] for point in selectedData["points"]]
        df = raw_data[raw_data["country"].isin(list_country)]
    else:
        df = raw_data.copy()
    
    data = data_filter(df, group, attack, target, weapon)
    
    if cause == "nwound" or cause == "nkill":
        data = data.groupby(["flag_country", "country"], as_index=False)[cause].sum()
        data = data.nlargest(columns=cause, n=10) if not selectedData else data.copy()
        title = "Top des pays par nombre de décès" if cause == "nkill" else \
                "Top des pays par nombre de blessés"
    
    else:
        data = data.groupby(["flag_country", "country"], as_index=False).size()
        data = data.nlargest(columns=cause, n=10) if not selectedData else data.copy()
        title = "Top des pays par nombre d'incidence"
        
    fig = px.bar(data, x=cause, y="flag_country", orientation="h", color=cause, color_continuous_scale="reds")
    fig.update_coloraxes(showscale=False)
    fig.update_yaxes(categoryorder='total ascending')
    
    fig.update_layout(
        **update_layout_simple,
        height=450,
        title={
            "text": (
                    f"<b>{title}</b><br />"
                    f"<sup style='color:silver'>situtation globale dans le monde"
                ),
            "font": {"family": "serif", "size": 18, "color": "black"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )
    
    legend(fig)
    
    return fig



@callback(
    Output("success-failure-attack", "figure"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def global_incidence_timeseries(group, attack, target, weapon):
    data = data_filter(raw_data, group, attack, target, weapon)
    
    data_failure = (data[data.success == 0]).groupby("year", as_index=False).size().rename(columns={"size": "failure"})
    data_success = (data[data.success == 1]).groupby("year", as_index=False).size().rename(columns={"size": "succes"})
    df = pd.merge(data_success, data_failure, on="year")
    
    fig = px.bar(df, x="year", y=["succes", "failure"], barmode="group")
    fig.update_coloraxes(showscale=False)
    
    fig.update_layout(
        **update_layout_simple,
        height=450,
        title={
            "text": (
                    f"<b>Attaques terroristes réussie vs échouées </b><br>"
                    f"<sup style='color:silver'>Le terrorisme dans le monde "
                ),
            "font": {"family": "serif", "size": 30, "color": "black"},
            "x": 0,
            "y": 0.93,
            
        },
        legend=dict(
            orientation='h', title=None, x=0, y=0.93,
        )
    )
    
    legend(fig)
    
    return fig


@callback(
    Output("suicid-attack", "figure"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def global_incidence_timeseries(group, attack, target, weapon):
    data = data_filter(raw_data, group, attack, target, weapon)
    
    data_failure = (data[data.suicide == 0]).groupby("year", as_index=False).size().rename(columns={"size": "No suicide"})
    data_success = (data[data.suicide == 1]).groupby("year", as_index=False).size().rename(columns={"size": "Suicide"})
    df = pd.merge(data_success, data_failure, on="year")
    
    fig = px.bar(df, x="year", y=["Suicide", "No suicide"], barmode="group")
    fig.update_coloraxes(showscale=False)
    
    fig.update_layout(
        **update_layout_simple,
        height=450,
        title={
            "text": (
                    f"<b>Attaques terroristes suicide vs non suicide </b><br>"
                    f"<sup style='color:silver'>Le terrorisme dans le monde "
                ),
            "font": {"family": "serif", "size": 30, "color": "black"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
            
        },
        legend=dict(
            orientation='h', title=None, x=0, y=0.93,
        )
    )
    
    legend(fig)
    
    return fig




@callback(
    Output("multiple-attack", "figure"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def global_incidence_timeseries(group, attack, target, weapon):
    data = data_filter(raw_data, group, attack, target, weapon)
    
    data_failure = (data[data.multiple == 0]).groupby("year", as_index=False).size().rename(columns={"size": "unique"})
    data_success = (data[data.multiple == 1]).groupby("year", as_index=False).size().rename(columns={"size": "Multiple"})
    df = pd.merge(data_success, data_failure, on="year")
    
    fig = px.bar(df, x="year", y=["Multiple", "unique"], barmode="group")
    fig.update_coloraxes(showscale=False)
    
    fig.update_layout(
        **update_layout_simple,
        height=450,
        title={
            "text": (
                    f"<b>Attaques terroristes multiple vs isolée </b><br>"
                    f"<sup style='color:silver'>Le terrorisme dans le monde "
                ),
            "font": {"family": "serif", "size": 30, "color": "black"},
            "x": 0,
            "y": 0.93,
            
        },
        legend=dict(
            orientation='h', title=None, x=0, y=0.93,
        )
    )
    
    legend(fig)
    
    return fig



@callback(
    Output("individual", "figure"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def global_incidence_timeseries(group, attack, target, weapon):
    data = data_filter(raw_data, group, attack, target, weapon)
    
    data_failure = (data[data.individual == 0]).groupby("year", as_index=False).size().rename(columns={"size": "À plusieurs"})
    data_success = (data[data.individual == 1]).groupby("year", as_index=False).size().rename(columns={"size": "Individuelle"})
    df = pd.merge(data_success, data_failure, on="year")
    
    fig = px.bar(df, x="year", y=["Individuelle", "À plusieurs"], barmode="group")
    fig.update_coloraxes(showscale=False)
    
    fig.update_layout(
        **update_layout_simple,
        height=450,
        title={
            "text": (
                    f"<b>Attaques terroristes individuelle vs à plusieurs </b><br>"
                    f"<sup style='color:silver'>Le terrorisme dans le monde "
                ),
            "font": {"family": "serif", "size": 30, "color": "black"},
            "x": 0,
            "y": 0.93,
            
        },
        legend=dict(
            orientation='h', title=None, x=0, y=0.93,
        )
    )
    
    legend(fig)
    
    return fig




def trace(df, n, cause, column, name, graph, test=True):
        mean, median=0, 0
        if cause == "nkill": 
            data = df.groupby([column], as_index=False)[cause].sum().sort_values(by=cause, ascending=False)
            data_bar = df.groupby([column], as_index=False)[cause].sum().sort_values(by=cause, ascending=False)
            mean = data_bar[cause].mean()
            title=f"""Repartition du nombre de décès par<br> {name}"""
            
        elif cause == "nwound": 
            data = df.groupby([column], as_index=False)[cause].sum().sort_values(by=cause, ascending=False)
            data_bar = df.groupby([column], as_index=False)[cause].sum().sort_values(by=cause, ascending=False)
            mean = data_bar[cause].mean()
            title=f"""Repartition du nombre de blessés par<br> {name}"""
        else:
            
            data = (df[column].value_counts(normalize=True) * 100).reset_index()
            data_bar = df.groupby([column], as_index=False).size().rename(columns={"size": "proportion"})
            title=f"""Repartition du nombre d'incidence<br> par {name}"""
            cause="proportion"
            mean = data_bar[cause].mean()
            
        data_bar = data_bar[data_bar[column] != "Unknown"]
        data_bar = data_bar.nlargest(columns=cause, n=10)
        data_bar = (data_bar.set_index(column)).rename(index=rename).reset_index()
            
        if test:
            other = data.iloc[n:][cause].sum()
            new_row = pd.DataFrame({column: ['Other'], cause: [other]})
            data = pd.concat([data.iloc[:n], new_row], ignore_index=True)
        else:
            data = data.nlargest(columns=cause, n=6)
                
        data = (data.set_index(column)).rename(index=rename).reset_index()
        
        if graph == "pie":
            fig = go.Figure(go.Pie(
                labels=data[column], values=data[cause],
                textposition="outside", textinfo="label+percent", 
                textfont=dict(size=13.6, family="Lato"),
                marker=dict(colors=px.colors.sequential.Reds_r),
                insidetextorientation='radial', 
                pull = [.2]+[0] * 10, # hole=.5
            ))
            
            fig.update_layout(
                height=450,
                    # template="plotly_dark",,
                    showlegend=False,
                    margin=dict(autoexpand=True, l=0, r=0, t=80),
                    plot_bgcolor="rgba(0, 0, 0, 0)",
                    paper_bgcolor="rgba(0, 0, 0, 0)",
                    title={
                    "text": (
                            f"<b>{title}</b>"
                        ),
                    "font": {"family": "serif", "size": 30, "color": "black"},
                    "x": 0.93,
                    "y": 0.86,
                    "xanchor": "right",
                    "yanchor": "top",
                },
            )
        else:
            data_bar["percent"] = (data_bar[cause] / data_bar[cause].sum()) * 100
            data_bar["percent_cumulate"] = data_bar["percent"].cumsum()
            
            fig = px.bar(data_bar, x=cause, y=column, orientation="h",
                         color=cause, color_continuous_scale="reds")
            fig.update_coloraxes(showscale=False)
            fig.update_yaxes(categoryorder='total ascending')
            
            fig.add_vline(
                x=mean, line=dict(dash="dot", width=1),
                annotation_text=f"Moyenne<br> avg={round(mean, 2)}",
                annotation_position="bottom right",
            )
            
            fig.update_layout(
                **update_layout_simple,
                height=450,
                xaxis=dict(title=None, showgrid=False),
                yaxis=dict(title=None, showgrid=False),
                #margin=dict(autoexpand=True, l=0, r=0, t=80, b=0),
                title={
                    "text": (
                            f"<b>{title}</b><br />"
                            f"<sup style='color:silver'>situtation globale dans le monde"
                        ),
                    "font": {"family": "serif", "size": 27, "color": "black"},
                    "x": 0.98,
                    "y": 0.93,
                    "xanchor": "right",
                    "yanchor": "top",
                },
            )
            
        legend(fig)
    
        return fig
    

@callback(
    Output("pie-weapon", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("graph-type", "value"),
)
def pie_weapon_graph(range_date, area, cause, graph):
    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)   
    df = data[data["weaptype1"] != "Unknown"]
    
    if cause == "nkill": n=4
    elif cause == "nwound": n=4
    else: n=4
            
    fig = trace(df, n, cause, "weaptype1", "type d'arme", graph, True)
        
    return fig


@callback(
    Output("pie-group", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("graph-type", "value"),
)
def pie_group_graph(range_date, area, cause, graph):
    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)   
    df = data[data["gname"] != "Unknown"]
    
    if cause == "nkill": n=3
    elif cause == "nwound": n=3
    else: n=4
            
    fig = trace(df, n, cause, "gname", "groupe", graph, False)
        
    return fig


@callback(
    Output("pie-attack", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("graph-type", "value"),
)
def pie_attack_graph(range_date, area, cause, graph):
    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)   
    df = data[data["attacktype"] != "Unknown"]
    
    if cause == "nkill": n=4
    elif cause == "nwound": n=4
    else: n=4
        
    fig = trace(df, n, cause, "attacktype", "mode d'attaque", graph, True)
        
    return fig



@callback(
    Output("pie-target", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("graph-type", "value"),
)
def pie_attack_graph(range_date, area, cause, graph):
    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)   
    df = data[data["targtype"] != "Unknown"]
    
    if cause == "nkill": n=5
    elif cause == "nwound": n=5
    else: n=5
            
    fig = trace(df, n, cause, "targtype", "cible", graph, True)
        
    return fig




@callback(
    Output("success-failure-map", "figure"),
    Input("dropdown-se", "value"),
)
def global_incidence_timeseries(cause):
    data = raw_data[raw_data.success == cause]
    data = data.groupby(["code", "country", "year"], as_index=False).size()
    
    if cause == 1:
        title="Attaque terroriste réussie par pays"
    if cause == 0:
        title="Attaque terroriste échouées par pays"
            
    fig = go.Figure(
        go.Choropleth(
            z=data["size"],
            locations=data["code"],
            colorscale="reds",
            showscale=False,
            # zmin=0, zmax=5300,
            marker=dict(line=dict(width=.3, color="black")),
            customdata=data
        )
    )

    fig.update_layout(
        **update_layout_geo,
        dragmode="lasso",
        # template="plotly_dark",,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0),
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
    
    legend(fig)
    
    return fig