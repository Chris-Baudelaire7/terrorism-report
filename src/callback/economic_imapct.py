from dash import Input, Output, callback
import dash_echarts
import plotly.express as px
from data_preparation import *
from utils import *


@callback(
    Output("series-damages", "children"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
    Input("select-property", "value"),
)
def global_incidence_timeseries(range_date, area, group, attack, target, weapon, damage):
    cause, damage = "size", int(damage)
    
    data = data_date_filter(range_date)
    data = data_geo_filter(data, area)
    data = data_filter(data, group, attack, target, weapon)

    data = data[data["property"] == damage].groupby("year", as_index=False).size()
    
    df = data.copy()

    data = data[[cause, cause, "year"]].copy()

    data = [data.columns.tolist()] + data.values.tolist()
    
    option = {
        
        "title": {
            "text": "title",
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
                
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": 'rgba(0, 0, 0, 1)'
                    }
                },
                
                "markPoint": {
                    "data": [
                        {"type": 'max', "name": 'Max'},
                        {"type": 'min', "name": 'Min'}
                    ]
                },
                "markLine": {
                    "data": [{"type": 'average', "name": 'Avg'}],
                    
                }
            }
        ]
    }
    
    children = [
        dash_echarts.DashECharts(option=option, style={
            "width": '100%',
            "height": '500px',
        })
    ]

    return children


@callback(
    Output("repartition-damages", "children"),
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

    data = data["property"].value_counts().reset_index()
    data.set_index("property", inplace=True)
    data.rename(index={1: "Dégâts matériels", 0: "Sans dégâts matériels", -9: "Inconnu"}, inplace=True)
    data = data.reset_index()
    data = data.to_dict(orient='records')
    data = [{"value": item["count"], "name": item["property"]} for item in data]

    colors = ['rgb(103,0,13)', 'rgb(203,24,29)', 'rgb(252,146,114)']
    
    option = {
        "title": {
            "text": 'Activités Terroristes avec/sans coût',
            "subtext": 'Taux en pourcentage',
            "left": 'center'
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
    Output("repartition-dollars", "children"),
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

    colors = ['rgb(254,224,210)', 'rgb(251,106,74)', 'rgb(203,24,29)', 'rgb(103,0,13)'][::-1]
    
    
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





def relationship():
    data_damage = raw_data[raw_data["property"] == 1].groupby(["year"], as_index=False).size()
    data_nkill = (raw_data[raw_data["property"] == 1]).groupby(["year"], as_index=False)[["nkill", "nwound"]].sum()
    data = pd.merge(data_nkill, data_damage, on="year")
    data["casualty"] = data["nkill"] + data["nwound"]
    result = data[["size", "casualty"]].values.tolist()

    option = {
  "dataset": [
    {
        "source": result
    },
    {
      "transform": {
        "type": 'ecStat:regression',
        #"config": { "method": 'polynomial', "order": 5 }
      }
    }
  ],
  "title": {
    "text": '18 companies net profit and main business income (million)',
    "subtext": 'By ecStat.regression',
    "sublink": 'https://github.com/ecomfe/echarts-stat',
    "left": 'center',
    "top": 16
  },
  "tooltip": {
    "trigger": 'axis',
    "axisPointer": {
      "type": 'cross'
    }
  },
  "xAxis": {
    "splitLine": {
      "lineStyle": {
        "type": 'dashed'
      }
    },
    "splitNumber": 20
  },
  "yAxis": {
    "min": -40,
    "splitLine": {
      "lineStyle": {
        "type": 'dashed'
      }
    }
  },
  "series": [
    {
      "name": 'scatter',
      "type": 'scatter',
      "symbolSize": 10,
      "markPoint": {
        "data": [
          { "type": 'max', "name": 'Max' },
          { "type": 'min', "name": 'Min' }
        ]
      }
    },
    {
      "name": 'line',
      "type": 'line',
      "smooth": True,
      "datasetIndex": 1,
      "symbolSize": 0.1,
      "symbol": 'circle',
      "label": { "show": True, "fontSize": 16 },
      "labelLayout": { "dx": -20 },
      "encode": { "label": 2, "tooltip": 1 }
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
