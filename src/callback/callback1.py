from dash import Input, Output, callback, State
import plotly.express as px
import plotly.graph_objects as go
from data_preparation import *
from utils import *
import json
import plotly.figure_factory as ff
import numpy as np
from plotly.subplots import make_subplots
import datetime as dt
from statsmodels.nonparametric.smoothers_lowess import lowess



@callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(
    Output("dropdown-cause", "value"),
    Output("dropdown-group", "value"),
    Output("dropdown-attack", "value"),
    Output("dropdown-target", "value"),
    Output("dropdown-weapon", "value"),
    Input("reset", "n_clicks"),
    prevent_initial_call=True,
)
def reset_dropdown_value(n_clicks):
    if n_clicks:
        return "size", "All group", "All attack type", "All target", "All weapons"


@callback(
    Output('selected-data', 'children'),
    Input('country-map', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)



@callback(
    Output("country-timeseries", "figure"),
    Input("date-range-slider", "value"),
    Input("dropdown-cause", "value"),
    Input("dropdown-group", "value"),
    Input("dropdown-attack", "value"),
    Input("dropdown-target", "value"),
    Input("dropdown-weapon", "value"),
    Input("choice_serie_type_countries", "value"),
)
def country_timeseries(range_date, cause, group, attack, target, weapon, rel_abs):
    data = data_date_filter(range_date)
    data = data_filter(data, group, attack, target, weapon)
    
    def group_data(df):
        if cause == "nwound" or cause == "nkill":
            title = "Évolution du nombre de décès dus<br>à l'activité terroriste par pays" if cause == "nkill" else \
                "Évolution du nombre de blessés dus<br> à l'activité terroriste par année"
            df = df.groupby(["year", "country"], as_index=False)[cause].sum()
        else:
            title = "Évolution du nombre d'attaque<br>terroriste par pays"
            df = df.groupby(["year", "country"], as_index=False).size()
            
        return df, title
        
    most_affected = data[data.country.isin(["Iraq","Afghanistan","Pakistan","India","Syria", "Nigeria"])]
    most_affected, title = group_data(most_affected)
    most_affected = pd.pivot_table(most_affected, index="year", columns="country", values=cause)
    most_affected = most_affected.reset_index()

    rest_of_world = data[~data.country.isin(["Iraq","Afghanistan","Pakistan","India","Nigeria"])]
    rest_of_world, _ = group_data(rest_of_world)
    rest_of_world = pd.pivot_table(rest_of_world, index="year", columns="country", values=cause)
    rest_of_world = rest_of_world.sum(axis=1).reset_index().rename(columns={0:"rest of world"})

    df = pd.merge(most_affected, rest_of_world, on="year")
    df = df[["year", "Nigeria", "Syria", "India","Pakistan", "Afghanistan","Iraq", "rest of world",]]

    colors = ['grey','rgb(103,0,13)', 'rgb(165,15,21)',  'rgb(203,24,29)','rgb(251,106,74)','rgb(252,187,161)','rgb(255,245,240)'][::-1]
    
    
    fig = absolute_relative_figure(df, colors, rel_abs, title)
    
    return fig



@callback(
    Output("terrorist-killed", "figure"),
    Input("date-range-slider", "value"),
    Input("dropdown-group", "value"),
    Input("dropdown-attack", "value"),
    Input("dropdown-target", "value"),
    Input("dropdown-weapon", "value"),
)
def timeseries_terrorist_killed(range_date, group, attack, target, weapon):
    df = data_date_filter(range_date)
    data = data_filter(df, group, attack, target, weapon)
    
    data_nkiller = data.groupby("year", as_index=False)[["nkillter"]].sum()
    data_nkiller["cumsum"] = data_nkiller["nkillter"].cumsum()
    
    fig = px.bar(data_nkiller, x="year", y="nkillter", color="nkillter", color_continuous_scale="reds")
    fig.update_coloraxes(showscale=False)
    
    fig.add_scatter(
        x=data_nkiller["year"], y=data_nkiller["cumsum"],
        yaxis="y2", name="Somme cumulée",
        line=dict(width=2, color='whitesmoke'),
    )
    
    fig.update_layout(
        **update_layout_simple,
        bargap=.1,
        showlegend=False,
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(title="Nombre de terroriste tuées", showgrid=False),
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
                    f"<b>Evolution du nombre de terroriste<br>tués lors d'une attaque</b><br />"
                    f"<sup style='color:silver'>Évolution de 1970 à 2017"
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



@callback(
    Output("global-incidence-timeseries", "figure"),
    Input("date-range-slider", "value"),
    Input("dropdown-cause", "value"),
    Input("dropdown-group", "value"),
    Input("dropdown-attack", "value"),
    Input("dropdown-target", "value"),
    Input("dropdown-weapon", "value"),
)
def global_incidence_timeseries(range_date, cause, group, attack, target, weapon):
    df = data_date_filter(range_date)
    data = data_filter(df, group, attack, target, weapon)
    
    if cause == "nwound" or cause == "nkill":
        title = "Évolution du nombre de décès dus<br>à l'activité terroriste par année" if cause == "nkill" else \
                "Évolution du nombre de blessés dus<br> à l'activité terroriste par année"
    else:
        title = "Évolution du nombre d'attaque<br>terroriste par année"
                
    
    data_victim = data.groupby(["year"], as_index=False)[["nkill", "nwound"]].sum()
    data_count = data.groupby(["year"], as_index=False).size()
    merged_data = pd.merge(data_victim, data_count, on="year")
    merged_data["victim"] = merged_data["nkill"] + merged_data["nwound"]
    merged_data["cumsum"] = merged_data["size"].cumsum()
        
    fig = px.bar(merged_data, x="year", y=cause, color=cause, color_continuous_scale="reds")
    fig.update_coloraxes(showscale=False)
    
    fig.add_scatter(
        x=merged_data["year"], y=merged_data["cumsum"],
        yaxis="y2", name="Somme cumulée",
        line=dict(width=2, color='firebrick'),
    )
    
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
                    f"<sup style='color:silver'>Évolution de 1970 à 2017</sup>"
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





@callback(
    Output("by-region", "figure"),
    Input("date-range-slider", "value"),
    Input("dropdown-cause", "value"),
    Input("dropdown-group", "value"),
    Input("dropdown-attack", "value"),
    Input("dropdown-target", "value"),
    Input("dropdown-weapon", "value"),
    Input("choice_serie_type_region", "value"),
)
def region_timerseries(range_date, cause, group, attack, target, weapon, rel_abs):
    # fiter data
    data = data_date_filter(range_date)
    data = data_filter(data, group, attack, target, weapon)
    
    colors_region =  px.colors.sequential.Blues[::-2] +  px.colors.sequential.Reds[1:]
    cols_region = ['Middle East & North Africa', 'South Asia', 'Sub-Saharan Africa',
                   'South America', 'Central America & Caribbean', 'Southeast Asia',
                   'Eastern Europe', 'Western Europe', 'North America', 'East Asia',
                   'Central Asia', 'Australasia & Oceania'][::-1]
    
    if cause == "nwound" or cause == "nkill": 
        data = data.groupby(["year", "region"], as_index=False)[cause].sum()
    else:
        data = data.groupby(["year", "region"], as_index=False).size()
    
    
    data = data.pivot_table(index="year", columns="region", values=cause)
    data = data[cols_region]
    data = data.fillna(0).reset_index()
    
    fig = absolute_relative_figure(data, colors_region, rel_abs, "Repartion (en %) par region")
    
    return fig



@callback(
    Output("by-continent", "figure"),
    Input("date-range-slider", "value"),
    Input("dropdown-cause", "value"),
    Input("dropdown-group", "value"),
    Input("dropdown-attack", "value"),
    Input("dropdown-target", "value"),
    Input("dropdown-weapon", "value"),
    Input("choice_serie_type_continent", "value"),
)
def region_timerseries(range_date, cause, group, attack, target, weapon, rel_abs):
    # fiter data
    data = data_date_filter(range_date)
    data = data_filter(data, group, attack, target, weapon)
    
    colors_continent = ['rgb(255,245,240)','rgb(252,187,161)','rgb(251,106,74)','rgb(203,24,29)','rgb(103,0,13)']
    cols_continent = ["Oceania", "Europe", "America", "Asia", "Africa"]
    
    if cause == "nwound" or cause == "nkill": 
        data = data.groupby(["year", "continent"], as_index=False)[cause].sum()
    else:
        data = data.groupby(["year", "continent"], as_index=False).size()
    
    
    data = data.pivot_table(index="year", columns="continent", values=cause)
    data = data[cols_continent]
    data = data.fillna(0).reset_index()
    
    fig = absolute_relative_figure(data, colors_continent, rel_abs, "Repartition en par continent")
    
    return fig



@callback(
    Output("timeseries-by-category", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("category-select", "value"),
    Input("choice_serie_type_crt", "value"),
)
def global_incidence_timeseries(range_date, area, cause, category, rel_abs):
    def data_geo_filter(dataframe, area):
        if area == "Monde":
            data = dataframe.copy()
        elif area in list(dataframe.continent.unique()):
            data = dataframe[dataframe.continent == area]
        else: 
            data = dataframe[dataframe.region == area]
        # else:
        #     data = dataframe[dataframe.flag_country == area]
    
        return data

    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)
    
    
    colors = px.colors.sequential.Reds
    
    if category == "attacktype":
        subtitle = "par mode d'attaque"
    if category == "targtype":
        subtitle = "par cible visées"
    else:
        subtitle = "par armes utilisées"
    
    if cause == "nwound" or cause == "nkill":
        data = data.groupby(["year", category], as_index=False)[cause].sum()
        title = f"Évolution du nombre de décès<br> {subtitle}" if cause == "nkill" else \
                f"Évolution du nombre de blessés<br> {subtitle}"
    else:
        data = data.groupby(["year", category], as_index=False).size()
        title = "Évolution du nombre d'attaque<br> {subtitle}"
        
    data = data.pivot_table(index="year", columns=category, values=cause)
    data = data.fillna(0).reset_index()
        
    fig = absolute_relative_figure(data, colors, rel_abs, title)
    
    return fig


@callback(
    Output("global-rate", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def rate_func(range_date, area, cause, group, attack, target, weapon):
    # fiter data
    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)
    data = data_filter(data, group, attack, target, weapon)
    
    if cause == "nwound" or cause == "nkill": # ["nwound", "nkill"]
        data = data.groupby(["year"], as_index=False)[cause].sum()
        title = "Taux de croissance du nombre de<br>décès dû à l'activité terroriste" if cause == "nkill" else \
                "Taux de croissance du nombre de<br>blessés dû à l'activité terroriste"
    else:
        data = data.groupby(["year"], as_index=False).size()
        title = "Taux de croissance du nombre<br> d'attaque terroriste"
        
    data["rate"] = round((data[cause].pct_change()) * 100, 2)
    data["relative_rate"] = (data[cause].diff().fillna(0).astype(int)).apply(lambda x: "+" + str(x) if x>0 else str(x))
    data['text'] = data.apply(lambda row: f"{row['rate']}%", axis=1)

    data_rate = data.copy().iloc[1:, :]
        
    fig = px.bar(data_rate, x="year", y="rate", color="rate", color_continuous_scale="reds")
    
    fig.update_traces(
        text=data["relative_rate"],
        textposition="outside",
        textfont=dict(size=20, family="Lora")
    )
    
    fig.update_coloraxes(showscale=False)
    
    fig.update_layout(
        **update_layout_simple,
        yaxis=dict(showgrid=False, ticksuffix="%"),
        xaxis=dict(title=None, showgrid=False),
        height=450,
        title={
            "text": (
                    f"<b>{title}</b><br />"
                    f"<sup style='color:silver'>Le terrorisme dans le monde "
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



@callback(
    Output("period-distribution", "figure"),
    Input("date-range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
)
def period_distribution(range_date, area, cause):
    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)
    period = "dayofyear"
    
    data['date'] = pd.to_datetime(data[['year', 'month', 'day']], errors='coerce')
    data["dayofyear"] = data["date"].dt.dayofyear
    data = data[~((data["date"].dt.month == 2) & (data["date"].dt.day == 29))].copy()

    data["dayofyear"] = data["dayofyear"].where(
        ~((data["date"].dt.month > 2) & (data["date"].dt.is_leap_year)),
        data["dayofyear"] - 1,
    )
    
    data1 = data.groupby([period], as_index=False)[["nkill", "nwound", "casualties"]].sum()
    data2 = data.groupby([period], as_index=False).size()
    data = pd.merge(data1, data2, on=period)
        
    x = data[cause].values
    hist_data = [x]
    group_labels = ['distplot'] # name of the dataset
    
    fig = ff.create_distplot(hist_data, group_labels, bin_size=8, histnorm="", show_curve=False,
                             show_rug=False, curve_type="normal", colors=["firebrick"])

    fig.update_layout(
        **update_layout_simple,
        bargap=.1,
        font={"family": "serif", "size": 14},
        height=400,
        showlegend=False,
        yaxis=dict(title="Frequence", showgrid=False),
        xaxis=dict(title="Nombre d'attaque par jour"),
        title={
            "text": (
                    f"<b>Frequence du nombre d'attaque par jour</b><br />"
                    f"<sup style='color:silver'>Le terrorisme dans le monde "
                ),
            "font": {"family": "serif", "size": 25, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )
        
    return fig



@callback(
    Output("period-timeseries", "figure"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def all_days_in_year_timeseries(cause, group, attack, target, weapon):
    data = data_filter(df, group, attack, target, weapon)
    
    period="dayofyear"
    year=2020 # Choisir au hazard (il ne sera de toute les facons pas affiché)
    
    data['date'] = pd.to_datetime(data[['year', 'month', 'day']], errors='coerce')
    data["dayofyear"] = data["date"].dt.dayofyear
    data = data[~((data["date"].dt.month == 2) & (data["date"].dt.day == 29))].copy()

    data["dayofyear"] = data["dayofyear"].where(
        ~((data["date"].dt.month > 2) & (data["date"].dt.is_leap_year)),
        data["dayofyear"] - 1,
    )
        
    if cause == "nwound" or cause == "nkill":
        data = data.groupby([period], as_index=False)[cause].sum()
        title = f"Évolution du nombre de<br>décès par jour" if cause == "nkill" else \
                f"Évolution du nombre de<br>blessés par jour"
    else:
        data = data.groupby([period], as_index=False).size()
        title = f"Évolution du nombre d'attaques<br>terroriste par jour"
        
    data["date"] = data["dayofyear"].apply(
        lambda x: dt.datetime(year, 1, 1) + dt.timedelta(days=x - 1)
    )
    
    smoothed_values = lowess(
        data[cause],
        data["dayofyear"],
        is_sorted=True,
        frac=1 / 12,
    )

    data[f"{cause}_lowess"] = smoothed_values[:, 1]
    
    trace = {
        "type": "scatter",
        "x": data["date"],
        "y": data[cause],
        "line":dict(color="firebrick", width=1),
        "name": "Attaque terroriste"
    }
    
    fig = go.Figure(data=[trace])
    
    fig.add_scatter(
        x=data["date"], y=data[f"{cause}_lowess"],
        line=dict(color="rgb(251,106,74)", width=1.86),
        name="Lissage"
    )
        
    fig.update_coloraxes(showscale=False)

    months_with_days = {
        month: (
            dt.datetime(2020, month, 1),
            dt.datetime(
                2020, month, 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31
            ),
        )
        for month in range(1, 13)
    }

    # Loop over months and add a shape for each month
    for month, days in months_with_days.items():
        # Define background color
        bg_color = "black" if (month % 2) == 0 else "#111"

        fig.add_shape(
            type="rect",
            yref="paper",
            x0=days[0],
            x1=days[1],
            y0=0,
            y1=1,
            fillcolor=bg_color,
            layer="below",
            line_width=0,
        )
    
    fig.update_layout(
        **update_layout_simple,
        height=450,
        font=dict(size=14, family="serif"),
        legend=dict(
            orientation="h", x=.013, y=.87
        ),
        xaxis=dict(
            showgrid=False, 
            dtick="M1",
            tickformat="%B",
            hoverformat="%e %B",
            ticklabelmode="period",
            tickfont=dict(size=11, family="serif")
        ),
        yaxis=dict(showgrid=False),
        title={
            "text": (
                    f"<b>{title}</b><br />"
                    f"<sup style='color:silver'>Situtation globale dans le monde"
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
    Output("month-timeseries", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def month_timeseries(range_date, area, cause, group, attack, target, weapon):
    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)   
    data = data_filter(data, group, attack, target, weapon)  
      
    period="month"
    
    if cause == "nkill":
        title = "Évolution du nombre de<br>décès par mois"
    elif cause == "nwound":
        title = f"Évolution du nombre de<br>blessés par mois" 
    elif cause == "casualties":
        title = f"Évolution du nombre de<br>victimes par mois"    
    else:
        title = f"Évolution du nombre d'attaque<br>terroriste par mois" 
    
    data1 = data.groupby([period], as_index=False)[["nkill", "nwound", "casualties"]].sum() 
    data2 = data.groupby([period], as_index=False).size()
    data = pd.merge(data1, data2, on=period)
        
    data[period] = data[period].map(month_dict)
    
    data.dropna(inplace=True)
        
    fig = horizontal_bar_labels(data, period, cause, "firebrick")
    
    fig.update_layout(
        height=450,
        font=dict(size=14, family="serif"),
        title={
            "text": (
                    f"<b>{title}</b><br />"
                    f"<sup style='color:silver'>Situtation globale dans le monde"
                ),
            "font": {"family": "serif", "size": 22, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )
        
    return fig


@callback(
    Output("repartition-in-percent-by-month", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("select-category", "value"),
)
def repartition_in_percent_by_month(range_date, area, cause, column):  
    data = data_date_filter(range_date)
    data = data_geo_filter(df, area)   
    #data = data[data.month != 0]
    #data = df.copy()
    # data.dropna(inplace=True)
    
    if column == "targtype":
        x = "par cible"
        columns_to_group = targtype_to_group
        colorscale = ['rgb(103,0,13)', 'rgb(165,15,21)', 'rgb(203,24,29)', 
                      'rgb(239,59,44)', 'rgb(251,106,74)', 'rgb(252,146,114)']
    elif column == "attacktype":
        x = "par type d'attaque"
        columns_to_group = attacktype_to_group
        colorscale = ['rgb(103,0,13)', 'rgb(203,24,29)', 'rgb(251,106,74)']
    else:
        x = "armes utilisée"
        columns_to_group = weaptype_to_group
        colorscale = ['rgb(103,0,13)', 'rgb(203,24,29)', 'rgb(251,106,74)']
        
        
    if cause == "nkill" or cause == "nwound":
        val, aggfunc = cause, "sum"
        title = f"Distribution {x} du nombre de<br>décès par mois" if cause == "nkill" else \
                f"Distribution {x} du nombre de<br>blessés par mois"
    else:
        val, aggfunc = column, "count"
        title = f"Distribution {x} du nombre <br>d'attaque terroriste par mois"
        
        
    data = pd.crosstab(
        index=data["month"], 
        columns=data[column], 
        values=data[val] , 
        aggfunc=aggfunc, 
        normalize="index"
    )
    
    data = data * 100
    data['other'] = data[columns_to_group].sum(axis=1)
    data.drop(columns=columns_to_group, inplace=True)
    data['month'] = data.index.map(month_dict)
    data.reset_index(drop=True, inplace=True)
    data.set_index("month", inplace=True)
    data = round(data, 1)
    
    fig = dist_fig(data, colorscale, title)
    
    return fig




@callback(
    Output("serie-relative-absolue", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("slct-category", "value"),
)
def serie_rel_abs(range_date, area, cause, column): 
    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)   
    
    if column == "targtype":
        x = "par cible"
        columns_to_group = targtype_to_group
        colorscale = ['rgb(103,0,13)', 'rgb(165,15,21)', 'rgb(203,24,29)', 
                      'rgb(239,59,44)', 'rgb(251,106,74)', 'rgb(252,146,114)'] 
             
    elif column == "attacktype":
        x = "par type d'attaque"
        columns_to_group = attacktype_to_group
        colorscale = ['rgb(103,0,13)', 'rgb(203,24,29)', 'rgb(251,106,74)']  
            
    else:
        x = "armes utilisée"
        columns_to_group = weaptype_to_group
        colorscale = ['rgb(103,0,13)', 'rgb(203,24,29)', 'rgb(251,106,74)']  
                  
    if cause in ["nkill", "nwound", "casualties"]:
        val, aggfunc = cause, "sum"
        if cause == "nkill":
            title = f"Distribution {x} du nombre de<br>décès par mois" 
        elif cause == "casualties":
            title = f"Distribution {x} du nombre de<br>victimes par mois" 
        else:
            title = f"Distribution {x} du nombre de<br>blessés par mois"    
    else:
        val, aggfunc = column, "count"
        title = f"Distribution {x} du nombre <br>d'attaque terroriste par mois"   
        
    
    data = pd.crosstab(
        index=data["month"], 
        columns=data[column], 
        values=data[val] , 
        aggfunc=aggfunc, 
        normalize="index"
    )  
    
    data = data * 100
    data['other'] = data[columns_to_group].sum(axis=1)
    data.drop(columns=columns_to_group, inplace=True)
    data['month'] = data.index.map(month_dict)
    data.reset_index(drop=True, inplace=True)
    data.set_index("month", inplace=True)
    data = round(data, 1)  
                       
    fig = px.area(data, x=data.index, y=data.columns, color_discrete_sequence=colorscale)  
        
    for trace, color in zip(fig.data, colorscale):
        trace.update(fill='tonexty', mode='none', line=dict(color=color), fillcolor=color, opacity=1)              
        
    fig.update_layout(
        hovermode="closest",
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font={"family": "Lato", "size": 14},
        margin=dict(autoexpand=True, l=0, r=0, t=60),
        legend=dict(orientation="h", title=None),
        height=450,
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(ticksuffix="%", title=None, showgrid=False),
        title={
            "text": (
                    f"<b>{title}</b><br />"
                    f"<sup style='color:silver'>Série temporelle relative (1970-2017) "
                ),
            "font": {"family": "serif", "size": 30, "color": "white"},
            "x": 0.98,
                "y": 0.91,
                "xanchor": "right",
                "yanchor": "top",
        }
    )
    
    legend(fig)
    
    return fig 



@callback(
    Output("sankey-graph", "figure"),
    Input("selection", "value"),
    Input("cause", "value"),
)
def terrorist_group(columns, cause):
    group_list = []
    data = raw_data[raw_data["gname"] != "Unknown"]
    
    if cause == "nwound" or cause == "nkill": 
        group_list = data.groupby("gname")["nwound"].sum().nlargest(n=5).keys().to_list()
        title = "Évolution du nombre de<br>décès par mois" if cause == "nkill" else \
                "Évolution du nombre de<br>blessés par mois"
    else:
        group_list = data.groupby("gname").size().nlargest(n=5).keys().to_list()
        title = "Évolution du nombre d'attaque<br>terroriste par mois"

    data = raw_data[raw_data["gname"] != "Unknown"]
    data = data[data["gname"].isin(group_list)]

    data1 = (data.groupby(["gname",  columns], as_index=False)[["nkill", "nwound"]].sum())
    data2 = (data.groupby(["gname", columns], as_index=False).size())

    data = pd.merge(data1, data2, on=["gname", columns])
    data = data.sort_values(by=['gname', cause], ascending=[True, False])
    data = data.groupby('gname').head(5)

    nodes = pd.concat([data['gname'], data[columns]]).unique()
    node_indices = {node: i for i, node in enumerate(nodes)}

    data['gname'] = data['gname'].map(node_indices)
    data[columns] = data[columns].map(node_indices)

    fig = go.Figure(data=go.Sankey(
        node=dict(
            pad=70,
            thickness=10,
            line=dict(color="black", width=1),
            label=nodes,
            color="blue"
        ),
        link=dict(
            source=data['gname'],
            target=data[columns],
            value=data[cause]
        )
    ))

    fig.update_layout(
        font={"family": "Lato", "size": 14},
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=0, r=0, t=130),
        height=650,
        showlegend=False,
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
        
    return fig