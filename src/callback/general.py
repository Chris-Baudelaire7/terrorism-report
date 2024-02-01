import time
import datetime
import pydeck as pdk
import plotly.figure_factory as ff
import plotly.express as px
import dash
import dash_echarts
import dash_bootstrap_components as dbc

from dash import Input, Output, callback, ctx, html
from dash.exceptions import PreventUpdate

from data_preparation import *
from utils import *
from components import *




































@callback(
    Output("dist-fig", "figure"),
    Input("range-slider", "value"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def global_incidlkjhgfence_timeseries(range_date, cause, group, attack, target, weapon):
    df = data_date_filter(range_date)
    dr = data_filter(df, group, attack, target, weapon)

    if cause == "nwound" or cause == "nkill":
        title = "Nombre journalier de décès dus à l'activité terroriste" if cause == "nkill" else \
                "Nombre journalier de blessés dus à l'activité terroriste"
    else:
        title = "Évolution du nombre d'attaque terroriste par jour"
        
    dr['date'] = pd.to_datetime(dr[['year', 'month', 'day']], errors='coerce')
    
    data_victim = dr.groupby(["date"], as_index=False)[["nkill", "nwound"]].sum()
    data_count = dr.groupby(["date"], as_index=False).size()
    data = pd.merge(data_victim, data_count, on="date")
    data["victim"] = data["nkill"] + data["nwound"]
    data["cumsum"] = data[cause].cumsum()
        
    x = data[cause].values
    hist_data = [x]
    group_labels = ['Cas journalier'] 
    
    fig = ff.create_distplot(hist_data, group_labels, bin_size=1, histnorm="", show_curve=False,
                             show_rug=False, curve_type="normal", colors=["firebrick"])
    
    fig.update_layout(
        **{"paper_bgcolor":"rgba(0,0,0,0)",
        "plot_bgcolor":"rgba(0,0,0,0)",
        "hovermode":"x",
        "margin":dict(l=0, r=0, t=0, b=0)},
        bargap=.1,
        font={"family": "serif", "size": 14},
        height=300,
        #margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        yaxis=dict(title="Frequence", showgrid=False),
        xaxis=dict(title="Nombre d'attaque par jour"),
        title={
            "text": (
                    f"<b>Frequence des cas</b><br />"
                    f"<sup style='color:silver'>Le terrorisme dans le monde "
                ),
            "font": {"family": "serif", "size": 25, "color": "black"},
            "x": 0.98,
            "y": 0.75,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig




@callback(
    Output("daily", "children"),
    Input("range-slider", "value"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def global_incidlkjhgfence_timeseries(range_date, cause, group, attack, target, weapon):
    df = data_date_filter(range_date)
    dr = data_filter(df, group, attack, target, weapon)

    if cause == "nwound" or cause == "nkill":
        title = "Nombre journalier de décès dus à l'activité terroriste" if cause == "nkill" else \
                "Nombre journalier de blessés dus à l'activité terroriste"
    else:
        title = "Évolution du nombre d'attaque terroriste par jour"
        
    dr['date'] = pd.to_datetime(dr[['year', 'month', 'day']], errors='coerce')
    
    data_victim = dr.groupby(["date"], as_index=False)[["nkill", "nwound"]].sum()
    data_count = dr.groupby(["date"], as_index=False).size()
    data = pd.merge(data_victim, data_count, on="date")
    data["victim"] = data["nkill"] + data["nwound"]
    data["cumsum"] = data[cause].cumsum()

        
    option = {
        "title": {
            "text": title,
            "subtext": 'Feature Sample: Gradient Color, Shadow, Click Zoom',
            "left": '1%',
        },
        "tooltip": {
            "trigger": 'axis'
        },
        "grid": {
            "left": '5%',
            "right": '10%',
            "bottom": '10%'
        },
        "xAxis": {
            "data": data['date']
        },
        "yAxis": {},

        "toolbox": {
            "right": 10,

            "feature": {
                "dataZoom": {
                    "yAxisIndex": 'none'
                },
                "dataZoom": [
                    {
                        "type": 'inside'
                    },
                    {
                        "type": 'slider'
                    }
                ],
                "dataView": {"show": True, "readOnly": True},
                "magicType": {"show": True, "type": ['line', 'bar']},
                "restore": {"show": True},
                "saveAsImage": {"show": True}
            },
        },



        "dataZoom": [
            {
                "startValue": '1990-11-22T00:00:00',
                "endValue": '1994-09-21T00:00:00'
            },
            {
                "type": 'inside'
            }
        ],
        "visualMap": {
            "top": 50,
            "right": 10,
            "pieces": [
                {
                    "gt": 0,
                    "lte": 10,
                    "color": '#93CE07'
                },
                {
                    "gt": 10,
                    "lte": 20,
                    "color": '#FBDB0F'
                },
                {
                    "gt": 20,
                    "lte": 30,
                    "color": '#FC7D02'
                },
                {
                    "gt": 30,
                    "lte": 40,
                    "color": '#FD0100'
                },
                {
                    "gt": 40,
                    "lte": 80,
                    "color": '#AA069F'
                },

            ],
            "outOfRange": {
                "color": 'red'
            }
        },
        "series": {
            "name": 'Daily Cases',
            "type": 'line',
            "data": data[cause],
            "markLine": {
                "silent": True,
                "lineStyle": {
                    "color": '#333'
                },
                "emphasis": {
                    "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": 'rgba(0, 0, 0, 1)'
                    }
                },
                "data": [
                    {
                        "yAxis": 10
                    },
                    {
                        "yAxis": 20
                    },
                    {
                        "yAxis": 30
                    },
                    {
                        "yAxis": 40
                    },
                    {
                        "yAxis": 80
                    }
                ]
            }
        }
    }

    children = [
        dash_echarts.DashECharts(option=option, style={"width": '100%', "height": '500px'})
    ]
    
   
    return children


@callback(
    Output("echart", "children"),
    Input("range-slider", "value"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def global_incidlkjhgfence_timeseries(range_date, cause, group, attack, target, weapon):
    df = data_date_filter(range_date)
    dr = data_filter(df, group, attack, target, weapon)

    if cause == "nwound" or cause == "nkill":
        title = "Nombre de décès dus à l'activité terroriste par année" if cause == "nkill" else \
                "Nombre de blessés dus à l'activité terroriste par année"
    else:
        title = "Évolution du nombre d'attaque terroriste par année"

    data_victim = dr.groupby(["year"], as_index=False)[["nkill", "nwound"]].sum()
    data_count = dr.groupby(["year"], as_index=False).size()
    data = pd.merge(data_victim, data_count, on="year")
    data["victim"] = data["nkill"] + data["nwound"]
    data["cumsum"] = data[cause].cumsum()
    
    dt = data[[cause, cause, "year"]].copy()
    df = data.copy()

    data = data[[cause, cause, "year"]].copy()
    

    data = [data.columns.tolist()] + data.values.tolist()
    
    option = {
        
        "title": {
            "text": title,
            "subtext": 'Feature Sample: Gradient Color, Shadow, Click Zoom'
        },

        "toolbox": {
            "show": True,
            "feature": {
                "dataView": { "show": True, "readOnly": True },
                "magicType": { "show": True, "type": ['line', 'bar'] },
                "restore": { "show": True },
                "saveAsImage": { "show": True }
            },
        },

        'tooltip': {
            'trigger': 'axis',
            "axisPointer": {
                "type": 'cross',
                "crossStyle": {
                    "color": '#999'
                }
            }
        },
        "calculable": True,
        "xAxis": {
            "type": 'category',
            "name": "year",
            "axisTick": {
                "alignWithLabel": True
            },
            "data": df["year"]
        },
        "yAxis": [
            {
                "type": 'value', 
                "alignTicks": True,
            },
            {
                "type": 'value', 
                "position": 'right', 
                "alignTicks": True,
                "axisLine": {
                    "show": False,
                    
                },
            },
        ],
        "visualMap": [
            {
                "orient": 'horizontal',
                "left": 'center',
                "min": df[cause].min(),
                "max": df[cause].max(),
                "text": ['High Score', 'Low Score'],
                "inRange": {
                    "color": px.colors.sequential.Reds
                }
            }
        ],
  
        "series": [
            {
                "type": 'bar',
                "color": "brown",
                "name": 'Event Occured',
                "encode": {
                    "x": df["year"],
                    "y": cause
                },
                "data": df[cause],
                
                "markPoint": {
                    "data": [
                        {"type": 'max', "name": 'Max'},
                        {"type": 'min', "name": 'Min'}
                    ]
                },
                "markLine": {
                    "data": [{"type": 'average', "name": 'Avg'}],
                    
                }
            },
            
            {
                "name": 'Cumulative sum',
                "color": "red",
                "type": 'line',
                "yAxisIndex": 1,
                "markPoint": {
                    "data": [
                        {"type": 'max', "name": 'Max'},
                        {"type": 'min', "name": 'Min'}
                    ]
                },
                "data": df["cumsum"],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": 'rgba(0, 0, 0, 1)'
                    }
                }
            }
        ],

    }
    
    children = [
        dash_echarts.DashECharts(option=option, style={
            "width": '100%',
            "height": '500px',
        })
    ]

    return children



@callback(
    Output("by-continent", "children"),
    Input("range-slider", "value"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
    Input("choice_serie_type_continent", "value"),
)
def continent_timerseries(range_date, cause, group, attack, target, weapon, graph):
    # fiter data
    data = data_date_filter(range_date)
    data = data_filter(data, group, attack, target, weapon)

    colors = ['rgb(255,245,240)', 'rgb(252,187,161)', 'rgb(251,106,74)', 'rgb(203,24,29)', 'rgb(103,0,13)']
    cols_continent = ["Oceania", "Europe", "America", "Asia", "Africa"]

    if cause == "nwound" or cause == "nkill":
        data = data.groupby(["year", "continent"], as_index=False)[cause].sum()
    else:
        data = data.groupby(["year", "continent"], as_index=False).size()

    data = data.pivot_table(index="year", columns="continent", values=cause)
    data = data[cols_continent]
    data = data.fillna(0).reset_index()
    
    if graph == "absolue":
        pass
    else:
        data[data.columns[1:]] = round(
            data[data.columns[1:]].apply(calculate_percentage, axis=1), 2)
    
    option = {
        "color": colors,
        "title": {
            "text": 'Gradient Stacked Area Chart'
        },
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'cross',
                "label": {
                    "backgroundColor": '#6a7985'
                }
            }
        },
        "legend": {
            "data": list(data.columns)[1:],
            "top": 40
        },
        
        "toolbox": {
            "show": True,
            "feature": {
                "dataView": { "show": True, "readOnly": True },
                "magicType": { "show": True, "type": ['line', 'bar'] },
                "restore": { "show": True },
                "saveAsImage": { "show": True }
            },
        },
        "grid": {
            "left": '0%',
            "right": '0%',
            "bottom": '0%',
            "containLabel": True
        },
        "xAxis": [
            {
                "type": 'category',
                "boundaryGap": False,
                "data": data["year"]
            }
        ],
        "yAxis": [
            {
                "type": 'value'
            }
        ],
        "series": [
            {
                "name": continent,
                "type": 'line',
                "stack": 'Total',
                "smooth": False,
                "lineStyle": {
                    "width": 0
                },
                "showSymbol": False,
                "areaStyle": {
                    "opacity": 1,

                },
               
                "emphasis": {
                    "focus": 'series',
                    "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": 'rgba(0, 0, 0, 1)'
                    }
                },
                "data": data[continent]
            }
            
            for continent in cols_continent

        ]
    }
    
    children = [
        dash_echarts.DashECharts(option=option, style={"width": '100%', "height": '400px'})
    ]

    return children


@callback(
    Output("by-region", "children"),
    Input("range-slider", "value"),
    Input("cause", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
    Input("choice_serie_type_region", "value"),
)
def continent_timerseries(range_date, cause, group, attack, target, weapon, graph):
    # fiter data
    data = data_date_filter(range_date)
    data = data_filter(data, group, attack, target, weapon)

    colors = px.colors.sequential.Blues[::-2] + px.colors.sequential.Reds[1:]
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

    if graph == "absolue":
        pass
    else:
        data[data.columns[1:]] = round(
            data[data.columns[1:]].apply(calculate_percentage, axis=1), 2)

    option = {
        #"color": color,
        "title": {
            "text": 'Gradient Stacked Area Chart'
        },
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'cross',
                "label": {
                    "backgroundColor": '#6a7985'
                }
            }
        },
        "legend": {
            "data": list(data.columns)[1:],
            "top": 40, "left": 35
        },

        "toolbox": {
            "show": True,
            "feature": {
                "dataView": {"show": True, "readOnly": True},
                "magicType": {"show": True, "type": ['line', 'bar']},
                "restore": {"show": True},
                "saveAsImage": {"show": True}
            },
        },
        "grid": {
            "left": '0%',
            "right": '0%',
            "bottom": '0%',
            "containLabel": True
        },
        "xAxis": [
            {
                "type": 'category',
                "boundaryGap": False,
                "data": data["year"]
            }
        ],
        "yAxis": [
            {
                "type": 'value'
            }
        ],
        "series": [
            
            {
                "name": region,
                "type": 'line',
                "color": color,
                "stack": 'Total',
                "smooth": False,
                "lineStyle": {
                    "width": 0
                },
                "showSymbol": False,
                "areaStyle": {
                    "opacity": 1,

                },
                "emphasis": {
                    "focus": 'series',
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": 'rgba(0, 0, 0, 1)'
                    }
                },
                "data": data[region]
            }
            
            for region, color in zip(cols_region, colors)
           
        ]
    }

    children = [
        dash_echarts.DashECharts(id="graph-echart", option=option, style={"width": '100%', "height": '400px'})
    ]

    return children




@callback(
    Output("world-top-affected-rest-of-world", "children"),
    Output("world-top-affected-rest-of-world2", "children"),
    Input("cause", "value"),
)
def world_top_affected_rest_of_world(cause):
    def group_data(dframe):
        if cause == "nwound" or cause == "nkill":
            df = dframe.groupby(["year", "country"], as_index=False)[
                cause].sum()
            df_world = raw_data.groupby(["year"], as_index=False)[cause].sum()
        else:
            df = dframe.groupby(["year", "country"], as_index=False).size()
            df_world = raw_data.groupby(["year"], as_index=False).size()
        return df, df_world

    def figure(start_date):
        if start_date == raw_data.year.min():
            filtered_date = raw_data.copy()
        else:
            filtered_date = raw_data[raw_data.year >= start_date]

        name = "Iraq, Afghanista, Pakistan<br>India, Syria & Nigeria"
        most_affected = filtered_date[filtered_date.country.isin(
            ["Iraq", "Afghanistan", "Pakistan", "India", "Syria", "Nigeria"])]
        most_affected, _ = group_data(most_affected)
        most_affected = pd.pivot_table(
            most_affected, index="year", columns="country", values=cause)
        most_affected = most_affected.sum(
            axis=1).reset_index().rename(columns={0: name})
        rest_of_world = filtered_date[~filtered_date.country.isin(
            ["Iraq", "Afghanistan", "Pakistan", "India", "Nigeria"])]
        rest_of_world, _ = group_data(rest_of_world)
        rest_of_world = pd.pivot_table(
            rest_of_world, index="year", columns="country", values=cause)
        rest_of_world = rest_of_world.sum(axis=1).reset_index().rename(
            columns={0: "Le reste du monde"})
        _, world = group_data(filtered_date)
        world = world.rename(columns={cause: "Monde entier"})
        data = pd.merge(most_affected, rest_of_world, on="year")
        data = pd.merge(data, world, on="year")
        l = data.iloc[:, 1:].sum().reset_index()
        l = pd.pivot_table(l, columns="index", values=0).iloc[:, [2, 1, 0]]

        colors = ['rgb(103,0,13)', 'rgb(203,24,29)', 'rgb(251,106,74)',]

        option = {
            "tooltip": {
                "trigger": 'axis',
                "axisPointer": {
                    "type": 'shadow'
                }
            },
            "legend": {},

            "yAxis": {
                "type": 'value'
            },
            "xAxis": {
                "type": 'category',
                "data": ['Mon']
            },
            "series": [
                {
                    "color": color,
                    "type": 'bar',
                    "stack": 'total',
                    "label": {
                        "show": True
                    },
                    "emphasis": {
                        "focus": 'series',
                        "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": 'rgba(0, 0, 0, 1)'
                        }
                    },
                    "data": l[col]
                }

                for col, color in zip(list(l.columns[:]), colors)

            ]
        }

        children = [
            dash_echarts.DashECharts(option=option, style={
                                     "width": '100%', "height": '400px'})
        ]

        return children

    children1 = figure(2004)
    children2 = figure(raw_data.year.min())

    return children1, children2


@callback(
    Output("top-country-and-world", "children"),
    Input("cause", "value"),
)
def top_country_and_world(cause):
    COUNTRIES = ["Iraq", "Afghanistan",
                 "Pakistan", "India", "Syria", "Nigeria"]
    NAME = "Iraq, Afghanista, Pakistan, India, Syria & Nigeria"
    COLORS = ['rgb(103,0,13)', 'rgb(203,24,29)', 'rgb(251,106,74)',]

    def group_data(dframe):
        if cause == "nwound" or cause == "nkill":
            df = dframe.groupby(["year", "country"], as_index=False)[
                cause].sum()
            df_world = raw_data.groupby(["year"], as_index=False)[cause].sum()
        else:
            df = dframe.groupby(["year", "country"], as_index=False).size()
            df_world = raw_data.groupby(["year"], as_index=False).size()
        return df, df_world

    most_affected = raw_data[raw_data.country.isin(COUNTRIES)]
    most_affected, _ = group_data(most_affected)

    most_affected = pd.pivot_table(
        most_affected, index="year", columns="country", values=cause)
    most_affected = most_affected.sum(
        axis=1).reset_index().rename(columns={0: NAME})

    rest_of_world = raw_data[~raw_data.country.isin(
        ["Iraq", "Afghanistan", "Pakistan", "India", "Nigeria"])]
    rest_of_world, _ = group_data(rest_of_world)
    rest_of_world = pd.pivot_table(
        rest_of_world, index="year", columns="country", values=cause)
    rest_of_world = rest_of_world.sum(axis=1).reset_index().rename(
        columns={0: "Le reste du monde"})

    _, world = group_data(raw_data)
    world = world.rename(columns={cause: "Monde entier"})

    data = pd.merge(most_affected, rest_of_world, on="year")
    data = pd.merge(data, world, on="year")

    option = {
        "title": {
            "text": 'Stacked Line',
            "subtext": 'Feature Sample: Gradient Color, Shadow, Click Zoom',
            "left": '1%',
        },
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'shadow',
                "label": {
                    "backgroundColor": '#6a7985'
                }
            }
        },
        "toolbox": {
            "show": True,
            "feature": {
                "dataView": {"show": True, "readOnly": True},
                "magicType": {"show": True, "type": ['line', 'bar']},
                "restore": {"show": True},
                "saveAsImage": {"show": True}
            },
        },
        "legend": {
            "data": list(data.columns)[1:],
            "top": 70, "left": 60,
        },


        "xAxis": {
            "type": 'category',
            # "boundaryGap": False,
            "data": data["year"],
        },
        "yAxis": {
            "type": 'value',
        },
        "series": [
            {
                "name": name,
                "color": color,
                "type": 'line',
                "stack": 'Total',
                "data": data["Monde entier"],
                "emphasis": {
                    # "focus": 'series',
                    "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": 'rgba(0, 0, 0, 1)'
                    }
                },
                
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowColor": 'rgba(120, 36, 50, 0.5)',
                    "shadowOffsetY": 5,

                },
                
            }

            for name, color in zip(list(data.columns)[1:], COLORS)

        ]
    }

    children = [
        dash_echarts.DashECharts(option=option, style={
                                 "width": '100%', "height": '500px'})
    ]

    return children


def quincenal_aeverage():
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

    colors = ['rgb(254,224,210)', 'rgb(103,0,13)', 'rgb(203,24,29)']
    columns = list(dfr.columns[1:])

    option = {
        "title": {
            "text": 'Distribution of Electricity',
            "subtext": 'Fake Data'
        },


        "xAxis": {
            "type": 'category',
            "boundaryGap": False,
            "data": dfr["year"]
        },
        "yAxis": {
            "type": 'value',
            "axisLabel": {
                "formatter": '{value} W'
            },
            "axisPointer": {
                "snap": True
            }
        },

        "series": [
            {
                "name": col,
                "color": color,
                "type": 'line',
                "data": dfr[col],
                
                 "itemStyle": {
                    "shadowBlur": 10,
                    "shadowColor": 'rgba(120, 36, 50, 0.5)',
                    "shadowOffsetY": 5,
                
                },
                
                
                "markArea": {
                    "itemStyle": {
                        "color": 'rgba(255, 173, 177, 0.4)'
                    },
                    "data": [

                        [
                            {
                                "name": 'Evening Peak',
                                "xAxis": "1995"
                            },
                            {
                                "xAxis": "2000"
                            }
                        ],

                        [
                            {
                                "name": 'Eveningddd Peak',
                                "xAxis": "2015"
                            },
                            {
                                "xAxis": "2020"
                            }
                        ],

                    ]
                }
            }

            for col, color in zip(columns, colors)
        ]
    }

    children = [
        dash_echarts.DashECharts(option=option, style={
                                 "width": '100%', "height": '500px'})
    ]

    return children







def line_race(area):
    cols = [["Income", "Country", "Year"]]

    df = raw_data.groupby(["year", area], as_index=False).size()
    for _, row in df.iterrows():
        cols.append([row['size'], row[area], row['year']])

    def get_countries():
        return list(set([e[1] for e in cols[1:]]))


    dataset_with_filters = [
        {
            "id": f"dataset_{country}",
            "fromDatasetId": "dataset_raw",
            "transform": {
                "type": "filter",
                "config": {
                    "and": [
                        {"dimension": "Year", "gte": 1970},
                        {"dimension": "Country", "=": country},
                    ]
                },
            },
        }
        for country in get_countries()
    ]

    series_list = [
        {
            "type": "line",
            "datasetId": f"dataset_{country}",
            "showSymbol": False,
            "name": country,
            "endLabel": {
                "show": True,
                "formatter": "line_race_formatter"
            },
            "labelLayout": {"moveOverlap": "shiftY"},
            "emphasis": {"focus": "series"},
            "encode": {
                "x": "Year",
                "y": "Income",
                "label": ["Country", "Income"],
                "itemName": "Year",
                "tooltip": ["Income"],
            },
        }
        for country in get_countries()
    ]

    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'shadow',
                "label": {
                    "backgroundColor": '#6a7985'
                }
            }
        },
        "toolbox": {
            "show": True,
            "feature": {
                "dataView": {"show": True, "readOnly": True},
                "magicType": {"show": True, "type": ['line', 'bar']},
                "restore": {"show": True},
                "saveAsImage": {"show": True}
            },
        },
        "animationDuration": 30000,
        "animation": True,
        "dataset": [{"id": "dataset_raw", "source": cols}] + dataset_with_filters,
        "title": {"text": "Income since 1950"},
        "tooltip": {"order": "valueDesc", "trigger": "axis"},
        "xAxis": {"type": "category", "nameLocation": "middle"},
        "yAxis": {"name": "Income"},
        #"grid": {"right": 140},
        "series": series_list,
    }
    
    
    children = [
        dash_echarts.DashECharts(
            option=option,
            id='line-race',
            style={
                "width": '100%',
                "height": '400px',
            },
            funs={
                "line_race_formatter":
                '''
            function(params){ 
                return params.value[3] + ': ' + params.value[0];
            }
            '''
            },
            fun_values=['line_race_formatter']
        ),
        
        dbc.Button('restart', color='success',
            id='line-race-button',
            style={
                'position': 'absolute',
                'height': 50, 'width': '5%',
                'top': '25%', 'right': '15%',
                'opacity': 0.8
            }
        )
    ]

    return children




@callback(Output('line-race', 'reset_id'), Input("line-race-button", "n_clicks"),)
def update_line_race(n_clicks):
    triggered = dash.callback_context.triggered
    # value = triggered[0]['value']
    prop_id, event = triggered[0]['prop_id'].split('.')
    if n_clicks:
        if 'line-race-button' in prop_id:
            dtime = datetime.datetime.now()
            int_time = int(time.mktime(dtime.timetuple()))
            return int_time
    raise PreventUpdate


@callback(
    Output("repartition-dollards", "children"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def repartition_damages(range_date, area, group, attack, target, weapon):
    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)
    data = data_filter(data, group, attack, target, weapon)

    data = data["propextent_txt"].value_counts().reset_index()

    colors = ['rgb(254,224,210)', 'rgb(251,106,74)',
              'rgb(203,24,29)', 'rgb(103,0,13)'][::-1]

    data = data.to_dict(orient='records')
    data = [{"value": item["count"], "name": item["propextent_txt"]}
            for item in data]

    option = {
        "title": {
            "text": 'Classes de dommages matériels en Dollars',
            "subtext": 'Taux en pourcentage',
            "left": 'center',
        },
        "tooltip": {
            "trigger": 'item'
        },
        "legend": {
            "orient": 'vertical',
            "left": 'left',
            'top': 'center'
        },
        "toolbox": {
            "show": True,
            "feature": {
                "mark": {"show": True},
                "dataView": {"show": True, "readOnly": False},
                "restore": {"show": True},
                "saveAsImage": {"show": True}
            }
        },
        "series": [
            {
                "name": 'Activités Terroristes',
                "type": 'pie',
                "color": colors,
                "radius": [50, 150],
                "center": ['50%', '50%'],
                "roseType": 'area',
                "itemStyle": {
                    "borderRadius": 8
                },
                "data": data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": 'rgba(0, 0, 0, 1)'
                    }
                }
            }
        ]
    }

    children = [
        dash_echarts.DashECharts(option=option, style={
            "width": '100%',
            "height": '400px',
        })
    ]

    return children




@callback(
    Output("f", "children"),
    Output("f2", "children"),
    Input("cause", "value"),
)
def world_top_affected_rest_of_world(cause):
    
    colors = ['rgb(103,0,13)','rgb(203,24,29)','rgb(251,106,74)',]
    
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
             
        name = "Iraq, Afghanista, Pakistan India, Syria & Nigeria"
        most_affected = filtered_date[filtered_date.country.isin(
            ["Iraq", "Afghanistan", "Pakistan", "India", "Syria", "Nigeria"])]
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
        data = data.iloc[:, 1:].sum().reset_index()
        data = pd.pivot_table(data, columns="index", values=0).iloc[:, [2,1,0]]  
        data = data.T.reset_index()
        data = data.to_dict(orient='records')
        data = [{"value": item[0], "name": item["index"]}for item in data]
        
        option = {
            "title": {
                "text": 'Activité Terroriste avant/apres 2004 ',
                "subtext": 'Les plus touchés vs le reste du monde',
                "left": 'center',
            },
            "tooltip": {
                "trigger": 'item'
            },
            "legend": {
                "orient": 'vertical',
                "left": 'left',
                'top': 'bottom'
            },
            "toolbox": {
                "show": True,
                "feature": {
                    "mark": {"show": True},
                    "dataView": {"show": True, "readOnly": False},
                    "restore": {"show": True},
                    
                    "magicType" : {
                        "show": True, 
                        "type": ['pie', 'funnel'],
                        "option": {
                            "funnel": {
                                "x": '25%',
                                "width": '50%',
                                "funnelAlign": 'left',
                                "max": 1548
                            }
                        }
                    },
                    
                    "saveAsImage": {"show": True}
                }
            },
            "calculable" : True,
            "series": [
                {
                    "name": 'Activités Terroristes',
                    "type": 'pie',
                    "label": {"show": False, "position": "center"},
                    "color": colors,
                    "sort" : 'ascending', # for funnel
                    "roseType" : 'radius',
                    "radius": [50, 150],
                    "center": ['50%', '50%'],
                    "roseType": 'area',
                    "itemStyle": {
                        "borderRadius": 8
                    },
                    "data": data,
                    "emphasis": {
                        "label": {"show": True, "fontSize": "20", "fontWeight": "bold"},
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": 'rgba(0, 0, 0, 1)'
                        }
                    }
                }
            ]
        }
        
        children = [
             dash_echarts.DashECharts(option=option, style={"width": '100%', "height": '400px'})
        ]
        
        return children
        
    children1 = figure(2004)
    children2 = figure(raw_data.year.min())
    
    return children2, children1



@callback(
    Output('continent-div', 'children'),
    Input('continent-race-chart', 'value'),
)
def update_graph(opt):
    if opt == 'chart':
        return [
            html.Div(id="by-continent"),
            choice_serie_type('choice_serie_type_continent')
        ]
    else:
        return line_race("continent")



@callback(
    Output('region-div', 'children'),
    Input('region-race-chart', 'value'),
)
def update_graph(opt):
    if opt == 'chart':
        return [
            html.Div(id="by-region"),
            choice_serie_type('choice_serie_type_region')
        ]
    else:
        return line_race("region")




  
def  performance():
    gaugeData = [
        {
            "value": 20,
            "name": 'Africa',
            "title": {
                "offsetCenter": ['0%', '-70%']
            },
            "detail": {
                "valueAnimation": True,
                "offsetCenter": ['0%', '-55%']
            }
        },
        
        {
            "value": 40,
            "name": 'Asia',
            "title": {
                "offsetCenter": ['0%', '-40%']
            },
            "detail": {
                "valueAnimation": True,
                "offsetCenter": ['0%', '-25%']
            }
        },
        
        {
            "value": 60,
            "name": 'America',
            "title": {
                "offsetCenter": ['0%', '-10%']
            },
            "detail": {
                "valueAnimation": True,
                "offsetCenter": ['0%', '5%']
            }
        },
        
        
        {
            "value": 80,
            "name": 'Europe',
            "title": {
                "offsetCenter": ['0%', '20%']
            },
            "detail": {
                "valueAnimation": True,
                "offsetCenter": ['0%', '35%']
            }
        },
        
        {
            "value": 100,
            "name": 'Oceania',
            "title": {
                "offsetCenter": ['0%', '50%']
            },
            "detail": {
                "valueAnimation": True,
                "offsetCenter": ['0%', '65%']
            }
        }
    ]

    option = {
        "series": [
        {
            "type": 'gauge',
            "startAngle": 90,
            "endAngle": -270,
            "pointer": {
            "show": False
            },
            "progress": {
            "show": True,
            "overlap": False,
            "roundCap": True,
            "clip": False,
            "itemStyle": {
                "borderWidth": 0,
                "borderColor": 'rgba(0, 0, 0, 0)',
            }
            },
            "axisLine": {
            "lineStyle": {
                "width": 30
            }
            },
            "splitLine": {
            "show": False,
            "distance": 0,
            "length": 10
            },
            "axisTick": {
            "show": False
            },
            "axisLabel": {
            "show": False,
            "distance": 150
            },
            "data": gaugeData,
            "title": {
            "fontSize": 12
            },
            "detail": {
            "width": 50,
            "height": 12,
            "fontSize": 12,
            "color": 'inherit',
            "borderColor": 'inherit',
            "borderRadius": 15,
            "borderWidth": 1,
            "formatter": '{value}%'
            }
        }
        ]
    }
    
    children = [
            dash_echarts.DashECharts(option=option, style={
                "width": '100%',
                "height": '400px',
            })
        ]

    return children



def map_config(style):
    map_config = {
        "api_keys": {'mapbox': access_api_token},
        "map_provider": 'mapbox',
        "map_style": style
    }
    return map_config

def deck():
    # constants
    COLS = ["longitude", "latitude", "location"]
    
    # data preparation
    data_sum = raw_data.groupby(COLS, as_index=False)[["nkill", "nwound"]].sum()
    data_occurence = raw_data.groupby(["longitude", "latitude", "location"], as_index=False).size()
    data = pd.merge(data_sum, data_occurence, on=COLS)
    data["metric"] = data["nkill"] + data["nwound"] + data["size"]

    # Setting the viewport location
    initial_view_state = pdk.data_utils.compute_view(data[["longitude", "latitude"]])
    initial_view_state.zoom = 1.6
    initial_view_state.pitch = 50
    #initial_view_state.bearing = 20

    # Define the layer to display on a map
    hexagonlayer = pdk.Layer(
        "HexagonLayer",
        data=data,
        get_position=["longitude", "latitude"],
        get_elevation="size",
        elevation_scale=1,
        elevation_range=[500000, 5000000],
        pickable=True,
        radius=20000,
        extruded=True,
        auto_highlight=True,
    )
    
    maps = pdk.Deck(
        layers=[hexagonlayer],
        initial_view_state=initial_view_state,
        **map_config("light")
    )
    
    return maps


def perf():
    dataStyle = {
        "normal": {
            "label": {"show": False},
            "labelLine": {"show": False}
        }
    }

    placeHolderStyle = {
        "normal": {
            "color": 'rgba(0,0,0,0)',
            "label": {"show": False},
            "labelLine": {"show": False}
        },
        "emphasis": {
            "color": 'rgba(0,0,0,0)'
        }
    }
    option = {
        "title": {
            "text": '你幸福吗？',
            "subtext": 'From ExcelHome',
            "sublink": 'http://e.weibo.com/1341556070/AhQXtjbqh',
            "x": 'center',
            "y": 'center',
            "itemGap": 20,
            "textStyle": {
                "color": 'rgba(30,144,255,0.8)',
                "fontFamily": '微软雅黑',
                "fontSize": 35,
                "fontWeight": 'bolder'
            }
        },
        "tooltip": {
            "show": True,
            "formatter": "{a} <br/>{b} : {c} ({d}%)"
        },
        "legend": {
            "orient": 'vertical',
            # "x" : document.getElementById('main').offsetWidth / 2,
            "y": 45,
            "itemGap": 12,
            "data": ['68%的人表示过的不错', '29%的人表示生活压力很大', '3%的人表示“我姓曾”']
        },

        "series": [
            {
                "name": '1',
                "type": 'pie',
                "clockWise": False,
                "radius": [125, 150],
                "itemStyle": dataStyle,
                "data": [
                    {
                        "value": 68,
                        "name": '68%的人表示过的不错'
                    },
                    {
                        "value": 32,
                        "name": 'invisible',
                        "itemStyle": placeHolderStyle
                    }
                ]
            },
            {
                "name": '2',
                "type": 'pie',
                "clockWise": False,
                "radius": [100, 125],
                "itemStyle": dataStyle,
                "data": [
                    {
                        "value": 29,
                        "name": '29%的人表示生活压力很大'
                    },
                    {
                        "value": 71,
                        "name": 'invisible',
                        "itemStyle": placeHolderStyle
                    }
                ]
            },
            {
                "name": '3',
                "type": 'pie',
                "clockWise": False,
                "radius": [75, 100],
                "itemStyle": dataStyle,
                "data": [
                    {
                        "value": 3,
                        "name": '3%的人表示“我姓曾”'
                    },
                    {
                        "value": 97,
                        "name": 'invisible',
                        "itemStyle": placeHolderStyle
                    }
                ]
            }
        ]
    }
    
    children = [
            dash_echarts.DashECharts(option=option, style={
                "width": '100%',
                "height": '400px',
            })
        ]

    return children
