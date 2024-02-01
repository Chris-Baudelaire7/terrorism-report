from dash import Input, Output, callback, clientside_callback, State
import dash_echarts
import dash
import plotly.express as px
from data_preparation import *
from utils import *





def choropleth():
    COLUMN = ["code", "flag", "flag_country", "country"]
    
    data_victim = raw_data.groupby(COLUMN, as_index=False)[["nkill", "nwound"]].sum()
    data_count = raw_data.groupby(COLUMN, as_index=False).size()
    data = pd.merge(data_victim, data_count, on=COLUMN)
    data["victim"] = data["nkill"] + data["nwound"]
    
    fig = px.choropleth(
        data,
        locations='code',
        color="victim",
        color_continuous_scale="reds",
        #custom_data=['Entity', 'Continent']
    )

    fig.update_geos(
        projection_type='orthographic',
        projection_rotation_lon=-170,  # 110
        projection_rotation_lat=20,
        showocean=True,
        oceancolor='#87CEEB',
        showcoastlines=True,
        coastlinecolor='#333333',
        coastlinewidth=1,
        showland=True,
        landcolor='#4B4B4B',  # couleur continent
        showlakes=False,
        lakecolor='#202E78',  # couleur lac
        showcountries=False,
        countrycolor='white',
        bgcolor='rgba(0,0,0,0)',
        showframe=False
    )

    fig.update_layout(
        height=550,
        margin={"autoexpand":True, "r": 0, "t": 0, "l": 0, "b": 15},
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        coloraxis_showscale=False,
        hoverlabel=dict(
            bgcolor='rgba(11, 6, 81, 0.8)',
            bordercolor='rgba(11, 6, 81, 0.8)',
            font=dict(
                color='white'
            )
        ),
        title={
            "text": (
                f"<b>Total Victims as a 8, December 2023</b><br />"
            ),
            "font": {"family": "serif", "size": 15, "color": "black"},
            "x": 0.51,
            "y": 0,
            "xanchor": "center",
            "yanchor": "bottom",
        },
    )

    fig.update_traces(
        marker_line_width=1,
        marker_line_color='white',
        hovertemplate=None,
        #hoverinfo='none'
    )
        
    return fig


clientside_callback(
    """
    function(_, figure) {
        let rotation_lon = figure.layout.geo.projection.rotation.lon;
        let rotation_lat = figure.layout.geo.projection.rotation.lat;

        if (rotation_lon <= -180) {
            rotation_lon = 180;
        }

        if (rotation_lon >= 180) {
            rotation_lon = -180;
        }

        if (rotation_lat >= 90) {
            rotation_lat = 90;
        } else if (rotation_lat <= -90) {
            rotation_lat = -90;
        }

        if (Math.abs(0 - rotation_lat) < 0.01) {
            rotation_lat = 0;
        }

        const updatedFigure = Object.assign({}, figure);
        updatedFigure.layout.geo.projection.rotation.lon = rotation_lon + 1;
        updatedFigure.layout.geo.projection.rotation.lat = rotation_lat;

        return updatedFigure;
    }
    """,
    Output('choropleth', 'figure'),
    Input('choropleth-interval', 'n_intervals'),
    State('choropleth', 'figure'),
    prevent_initial_call=True
)
