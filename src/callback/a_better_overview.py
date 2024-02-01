# from dash import Input, Output, callback, State, html
# import dash_echarts
# import plotly.express as px
# import plotly.graph_objects as go
# from data_preparation import *
# from utils import *
# import json
# import plotly.figure_factory as ff
# import numpy as np
# from plotly.subplots import make_subplots
# import datetime as dt
# from statsmodels.nonparametric.smoothers_lowess import lowess


# @callback(
#     Output("country-timeseries", "figure"),
#     Input("range-slider", "value"),
#     Input("cause", "value"),
#     Input("group", "value"),
#     Input("attack", "value"),
#     Input("target", "value"),
#     Input("weapon", "value"),
#     Input("choice_serie_type_countries", "value"),
# )
# def country_timeseries(range_date, cause, group, attack, target, weapon, rel_abs):
#     data = data_date_filter(range_date)
#     data = data_filter(data, group, attack, target, weapon)

#     def group_data(df):
#         if cause == "nwound" or cause == "nkill":
#             title = "Évolution du nombre de décès dus<br>à l'activité terroriste par pays" if cause == "nkill" else \
#                 "Évolution du nombre de blessés dus<br> à l'activité terroriste par année"
#             df = df.groupby(["year", "country"], as_index=False)[cause].sum()
#         else:
#             title = "Évolution du nombre d'attaque<br>terroriste par pays"
#             df = df.groupby(["year", "country"], as_index=False).size()

#         return df, title

#     most_affected = data[data.country.isin(
#         ["Iraq", "Afghanistan", "Pakistan", "India", "Syria", "Nigeria"])]
#     most_affected, title = group_data(most_affected)
#     most_affected = pd.pivot_table(
#         most_affected, index="year", columns="country", values=cause)
#     most_affected = most_affected.reset_index()

#     rest_of_world = data[~data.country.isin(
#         ["Iraq", "Afghanistan", "Pakistan", "India", "Nigeria"])]
#     rest_of_world, _ = group_data(rest_of_world)
#     rest_of_world = pd.pivot_table(
#         rest_of_world, index="year", columns="country", values=cause)
#     rest_of_world = rest_of_world.sum(
#         axis=1).reset_index().rename(columns={0: "rest of world"})

#     df = pd.merge(most_affected, rest_of_world, on="year")
#     df = df[["year", "Nigeria", "Syria", "India",
#              "Pakistan", "Afghanistan", "Iraq", "rest of world",]]

#     colors = ['grey', 'rgb(103,0,13)', 'rgb(165,15,21)',  'rgb(203,24,29)',
#               'rgb(251,106,74)', 'rgb(252,187,161)', 'rgb(255,245,240)'][::-1]

#     fig = absolute_relative_figure(df, colors, rel_abs, title)

#     return fig



# @callback(
#     Output("world-top-affected-rest-of-world", "children"),
#     Output("world-top-affected-rest-of-world2", "children"),
#     Input("cause", "value"),
# )
# def world_top_affected_rest_of_world(cause):
#     def group_data(dframe):
#         if cause == "nwound" or cause == "nkill":
#             df = dframe.groupby(["year", "country"], as_index=False)[cause].sum()
#             df_world = raw_data.groupby(["year"], as_index=False)[cause].sum()
#         else:
#             df = dframe.groupby(["year", "country"], as_index=False).size()
#             df_world = raw_data.groupby(["year"], as_index=False).size()
#         return df, df_world
    
#     def figure(start_date):
#         if start_date==raw_data.year.min(): 
#             filtered_date = raw_data.copy()
#         else: 
#             filtered_date = raw_data[raw_data.year >= start_date]
        
#         name = "Iraq, Afghanista, Pakistan<br>India, Syria & Nigeria"
#         most_affected = filtered_date[filtered_date.country.isin(["Iraq","Afghanistan","Pakistan","India","Syria", "Nigeria"])]
#         most_affected, _ = group_data(most_affected)
#         most_affected = pd.pivot_table(most_affected, index="year", columns="country", values=cause)
#         most_affected = most_affected.sum(axis=1).reset_index().rename(columns={0:name})
#         rest_of_world = filtered_date[~filtered_date.country.isin(["Iraq","Afghanistan","Pakistan","India","Nigeria"])]
#         rest_of_world, _ = group_data(rest_of_world)
#         rest_of_world = pd.pivot_table(rest_of_world, index="year", columns="country", values=cause)
#         rest_of_world = rest_of_world.sum(axis=1).reset_index().rename(columns={0:"Le reste du monde"})
#         _, world = group_data(filtered_date)
#         world = world.rename(columns={cause:"Monde entier"})
#         data = pd.merge(most_affected, rest_of_world, on="year")
#         data = pd.merge(data, world, on="year")
#         l = data.iloc[:, 1:].sum().reset_index()
#         l = pd.pivot_table(l, columns="index", values=0).iloc[:, [2,1,0]]
        
#         colors = ['rgb(103,0,13)','rgb(203,24,29)','rgb(251,106,74)',]
        
#         option = {
#             "tooltip": {
#                 "trigger": 'axis',
#                 "axisPointer": {
#                 "type": 'shadow' 
#                 }
#             },
#             "legend": {},

#             "yAxis": {
#                 "type": 'value'
#             },
#             "xAxis": {
#                 "type": 'category',
#                 "data": ['Mon']
#             },
#             "series": [
#                 {
#                     "color": color,
#                     "type": 'bar',
#                     "stack": 'total',
#                     "label": {
#                         "show": True
#                     },
#                     "emphasis": {
#                         "focus": 'series'
#                     },
#                         "data": l[col]
#                 }
                
#                 for col, color in zip(list(l.columns[:]), colors)
                
#             ]
#         }
        
#         children = [
#             dash_echarts.DashECharts(option=option, style={"width": '100%', "height": '400px'})
#         ]

#         return children
    
#     children1 = figure(2004)
#     children2 = figure(raw_data.year.min())
    
#     return children1, children2


# @callback(
#     Output("top-country-and-world", "children"),
#     Input("cause", "value"),
# )
# def top_country_and_world(cause):
#     COUNTRIES = ["Iraq", "Afghanistan",  "Pakistan", "India", "Syria", "Nigeria"]
#     NAME = "Iraq, Afghanista, Pakistan, India, Syria & Nigeria"
#     COLORS = ['rgb(103,0,13)', 'rgb(203,24,29)', 'rgb(251,106,74)',]
    
#     def group_data(dframe):
#         if cause == "nwound" or cause == "nkill":
#             df = dframe.groupby(["year", "country"], as_index=False)[cause].sum()
#             df_world = raw_data.groupby(["year"], as_index=False)[cause].sum()
#         else:
#             df = dframe.groupby(["year", "country"], as_index=False).size()
#             df_world = raw_data.groupby(["year"], as_index=False).size()
#         return df, df_world

#     most_affected = raw_data[raw_data.country.isin(COUNTRIES)]
#     most_affected, _ = group_data(most_affected)

#     most_affected = pd.pivot_table(most_affected, index="year", columns="country", values=cause)
#     most_affected = most_affected.sum(axis=1).reset_index().rename(columns={0: NAME})

#     rest_of_world = raw_data[~raw_data.country.isin(["Iraq", "Afghanistan", "Pakistan", "India", "Nigeria"])]
#     rest_of_world, _ = group_data(rest_of_world)
#     rest_of_world = pd.pivot_table( rest_of_world, index="year", columns="country", values=cause)
#     rest_of_world = rest_of_world.sum(axis=1).reset_index().rename(columns={0: "Le reste du monde"})

#     _, world = group_data(raw_data)
#     world = world.rename(columns={cause: "Monde entier"})

#     data = pd.merge(most_affected, rest_of_world, on="year")
#     data = pd.merge(data, world, on="year")

#     option = {
#         "title": {
#             "text": 'Stacked Line',
#             "subtext": 'Feature Sample: Gradient Color, Shadow, Click Zoom',
#             "left": '1%',
#         },
#         "tooltip": {
#             "trigger": 'axis',
#             "axisPointer": {
#                 "type": 'shadow',
#                 "label": {
#                     "backgroundColor": '#6a7985'
#                 }
#             }
#         },
#         "toolbox": {
#             "show": True,
#             "feature": {
#                 "dataView": {"show": True, "readOnly": True},
#                 "magicType": {"show": True, "type": ['line', 'bar']},
#                 "restore": {"show": True},
#                 "saveAsImage": {"show": True}
#             },
#         },
#         "legend": {
#             "data": list(data.columns)[1:],
#             "top": 70, "left": 60,
#         },


#         "xAxis": {
#             "type": 'category',
#             #"boundaryGap": False,
#             "data": data["year"],
#         },
#         "yAxis": {
#             "type": 'value',
#         },
#         "series": [
#             {
#                 "name": name,
#                 "color": color,
#                 "type": 'line',
#                 "stack": 'Total',
#                 "data": data["Monde entier"]
#             }

#             for name, color in zip(list(data.columns)[1:], COLORS)

#         ]
#     }

#     children = [
#         dash_echarts.DashECharts(option=option, style={"width": '100%', "height": '500px'})
#     ]

#     return children


# def quincenal_aeverage():
#     dfr1 = raw_data.groupby(["year"], as_index=False)["nkill"].sum()
#     dfr2 = raw_data.groupby(["year"], as_index=False)["nwound"].sum()
#     dfr3 = raw_data.groupby(["year"], as_index=False).size()
#     dfr = pd.merge(dfr1, dfr2, on="year")
#     dfr = pd.merge(dfr, dfr3, on="year")
#     dfr['year'] = pd.to_datetime(dfr['year'], format='%Y')
#     dfr.set_index('year', inplace=True)
#     dfr = dfr.resample('5A').mean().astype(int).reset_index()
#     dfr = dfr[["year", "size", "nwound", "nkill"]]
#     dfr['year'] = dfr['year'].dt.year

#     colors = ['rgb(254,224,210)', 'rgb(103,0,13)', 'rgb(203,24,29)']
#     columns = list(dfr.columns[1:])

#     option = {
#         "title": {
#             "text": 'Distribution of Electricity',
#             "subtext": 'Fake Data'
#         },


#         "xAxis": {
#             "type": 'category',
#             "boundaryGap": False,
#             "data": dfr["year"]
#         },
#         "yAxis": {
#             "type": 'value',
#             "axisLabel": {
#                 "formatter": '{value} W'
#             },
#             "axisPointer": {
#                 "snap": True
#             }
#         },

#         "series": [
#             {
#                 "name": col,
#                 "color": color,
#                 "type": 'line',
#                 "data": dfr[col],
#                 "markArea": {
#                     "itemStyle": {
#                         "color": 'rgba(255, 173, 177, 0.4)'
#                     },
#                     "data": [

#                         [
#                             {
#                                 "name": 'Evening Peak',
#                                 "xAxis": "1995"
#                             },
#                             {
#                                 "xAxis": "2000"
#                             }
#                         ],

#                         [
#                             {
#                                 "name": 'Eveningddd Peak',
#                                 "xAxis": "2015"
#                             },
#                             {
#                                 "xAxis": "2020"
#                             }
#                         ],

#                     ]
#                 }
#             }

#             for col, color in zip(columns, colors)
#         ]
#     }

#     children = [
#         dash_echarts.DashECharts(option=option, style={"width": '100%', "height": '500px'})
#     ]

#     return children
