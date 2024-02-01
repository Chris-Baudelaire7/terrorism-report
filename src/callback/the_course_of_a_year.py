from dash import Input, Output, callback, State, html
import dash_echarts
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


# month-timeseries


@callback(
    Output("echarts", "children"),
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
    
    period = "month"
    label_option = {
        'show': True,
        'position': 'insideRight',
        'verticalAlign': 'middle',
        'fontSize': 16,
    }

    data1 = data.groupby([period], as_index=False)[["nkill", "nwound", "casualties"]].sum()
    data2 = data.groupby([period], as_index=False).size()
    data = pd.merge(data1, data2, on=period)
    
    data[period] = data[period].map(month_dict)
    data.dropna(inplace=True)

    df = data[["size", "size", "month"]].copy()

    df = [df.columns.tolist()] + df.values.tolist()
    
    option = {
        "dataset": {
            "source": df
        },
        
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'shadow'
            }
        },

        "grid": {"containLabel": True},
        "xAxis": {"name": 'size'},
        "yAxis": {"type": 'category'},
        "visualMap": {
            "orient": 'horizontal',
            "left": 'center',
            "min": data["size"].min(),
            "max": data["size"].max(),

            "text": ['High Score', 'Low Score'],
            "dimension": 0,
            "inRange": {
                "color": px.colors.sequential.Reds
            }
        },
        "series": [
            {
                "type": 'bar',
                "showBackground": True,
                'label': label_option,
                "encode": {
                    "x": 'size',
                    "y": 'month'
                }
            }
        ]
    }
    
    children = [
        dash_echarts.DashECharts(id='echadrts', option=option, style={
            "width": '100%',
            "height": '500px',
        }),
    ]
    
    return children

        
