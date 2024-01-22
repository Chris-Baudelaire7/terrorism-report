from dash import Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from data_preparation import *
from utils import *



@callback(
    Output("top-country-and-world", "figure"),
    Input("dropdown-cause", "value"),
)
def top_country_and_world(cause):
    
    def group_data(dframe):
        if cause == "nwound" or cause == "nkill":
            title = "Évolution du nombre de décès dus<br>à l'activité terroriste par pays" if cause == "nkill" else \
                "Évolution du nombre de blessés dus<br> à l'activité terroriste par année"
            df = dframe.groupby(["year", "country"], as_index=False)[cause].sum()
            df_world = raw_data.groupby(["year"], as_index=False)[cause].sum()
        else:
            title = "Évolution du nombre d'attaque<br>terroriste par pays"
            df = dframe.groupby(["year", "country"], as_index=False).size()
            df_world = raw_data.groupby(["year"], as_index=False).size()
            
        return df, df_world, title
    
    name = "Iraq, Afghanista, Pakistan<br>India, Syria & Nigeria"
    most_affected = raw_data[raw_data.country.isin(["Iraq","Afghanistan","Pakistan","India","Syria", "Nigeria"])]
    most_affected, _, title = group_data(most_affected)
    most_affected = pd.pivot_table(most_affected, index="year", columns="country", values=cause)
    most_affected = most_affected.sum(axis=1).reset_index().rename(columns={0:name})

    rest_of_world = raw_data[~raw_data.country.isin(["Iraq","Afghanistan","Pakistan","India","Nigeria"])]
    rest_of_world, _, _ = group_data(rest_of_world)
    rest_of_world = pd.pivot_table(rest_of_world, index="year", columns="country", values=cause)
    rest_of_world = rest_of_world.sum(axis=1).reset_index().rename(columns={0:"Le reste du monde"})
    
    _, world, _ = group_data(raw_data)
    world = world.rename(columns={cause:"Monde entier"})

    data = pd.merge(most_affected, rest_of_world, on="year")
    data = pd.merge(data, world, on="year")

    colors = ['rgb(203,24,29)',  'rgb(254,224,210)',"grey"]
    fig = px.line(data, x="year", y=data.columns[1:])
    for trace, color in zip(fig.data, colors):
        trace.update(mode='lines', line=dict(color=color, width=3))

    fig.update_layout(
            font={"family": "serif", "size": 14},
            legend=dict(x=0.07, y=.95),
            template="plotly_dark",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            hovermode="x",
            margin=dict(l=0, r=0, t=100),
            xaxis=dict(title=None, showgrid=False),
            yaxis=dict(title=None, showgrid=False),
            height=450,
            title={
                "text": (
                        f"<b>Region touchées par les grands<br>groupes de terreurs</b><br />"
                        f"<sup style='color:silver'>Le terrorisme dans le monde "
                    ),
                "font": {"family": "serif", "size": 32, "color": "white"},
                "x": 0.98,
                "y": 0.93,
                "xanchor": "right",
                "yanchor": "top",
            },
        )
    
    legend(fig)
    
    return fig


@callback(
    Output("world-top-affected-rest-of-world", "figure"),
    Output("world-top-affected-rest-of-world2", "figure"),
    Input("dropdown-cause", "value"),
)
def world_top_affected_rest_of_world(cause):
    def group_data(dframe):
        if cause == "nwound" or cause == "nkill":
            df = dframe.groupby(["year", "country"], as_index=False)[cause].sum()
            df_world = raw_data.groupby(["year"], as_index=False)[cause].sum()
        else:
            df = dframe.groupby(["year", "country"], as_index=False).size()
            df_world = raw_data.groupby(["year"], as_index=False).size()
        return df, df_world
    
    def figure(start_date):
        if start_date==raw_data.year.min(): 
            filtered_date = raw_data.copy()
        else: 
            filtered_date = raw_data[raw_data.year >= start_date]
        
        name = "Iraq, Afghanista, Pakistan<br>India, Syria & Nigeria"
        most_affected = filtered_date[filtered_date.country.isin(["Iraq","Afghanistan","Pakistan","India","Syria", "Nigeria"])]
        most_affected, _ = group_data(most_affected)
        most_affected = pd.pivot_table(most_affected, index="year", columns="country", values=cause)
        most_affected = most_affected.sum(axis=1).reset_index().rename(columns={0:name})
        rest_of_world = filtered_date[~filtered_date.country.isin(["Iraq","Afghanistan","Pakistan","India","Nigeria"])]
        rest_of_world, _ = group_data(rest_of_world)
        rest_of_world = pd.pivot_table(rest_of_world, index="year", columns="country", values=cause)
        rest_of_world = rest_of_world.sum(axis=1).reset_index().rename(columns={0:"Le reste du monde"})
        _, world = group_data(filtered_date)
        world = world.rename(columns={cause:"Monde entier"})
        data = pd.merge(most_affected, rest_of_world, on="year")
        data = pd.merge(data, world, on="year")
        l = data.iloc[:, 1:].sum().reset_index()
        l = pd.pivot_table(l, columns="index", values=0).iloc[:, [2,1,0]]
        
        colors = [ 'rgb(103,0,13)','rgb(203,24,29)','rgb(251,106,74)',]
        
        fig = go.Figure()
        
        for col, color in zip(list(l.columns),colors):
            fig.add_bar(
                y=l.index, x=l[col], name=col, orientation="h",
                marker=dict(color=color),
                texttemplate='%{x:f}' + "<br>"+ f"{col}", textposition='inside',
                hoverinfo="skip",
                textfont=dict(size=14)
            )

        fig.update_layout(
            barmode="stack",
            font={"family": "serif", "size": 14},
            showlegend=False,
            template="plotly_dark",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showticklabels=False,zeroline=False),
            height=60,
        )
        
        return fig
    
    fig1 = figure(raw_data.year.min())
    fig2 = figure(2004)
    
    return fig1, fig2
    


@callback(
    Output("country-map", "figure"),
    Input("dropdown-cause", "value"),
    Input("dropdown-group", "value"),
    Input("dropdown-attack", "value"),
    Input("dropdown-target", "value"),
    Input("dropdown-weapon", "value"),
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
            colorscale=["white"]+ px.colors.sequential.Reds[1:],
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
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=90),
        title={
            "text": (
                    f"<b>{title}</b><br />"
                    f"<sup style='color:silver'>Nombre total entre 1970 et 2020"
                ),
            "font": {"family": "serif", "size": 30, "color": "white"},
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
            "font": {"family": "serif", "size": 18, "color": "white"},
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
            "font": {"family": "serif", "size": 30, "color": "white"},
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
            "font": {"family": "serif", "size": 30, "color": "white"},
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
            "font": {"family": "serif", "size": 30, "color": "white"},
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
            "font": {"family": "serif", "size": 30, "color": "white"},
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
                    template="plotly_dark",
                    showlegend=False,
                    margin=dict(autoexpand=True, l=0, r=0, t=80),
                    plot_bgcolor="rgba(0, 0, 0, 0)",
                    paper_bgcolor="rgba(0, 0, 0, 0)",
                    title={
                    "text": (
                            f"<b>{title}</b>"
                        ),
                    "font": {"family": "serif", "size": 30, "color": "white"},
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
                    "font": {"family": "serif", "size": 27, "color": "white"},
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
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0),
        title={
            "text": (
                    f"<b>{title}</b><br />"
                    f"<sup style='color:silver'>situtation globale dans le monde"
                ),
            "font": {"family": "serif", "size": 30, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )
    
    legend(fig)
    
    return fig