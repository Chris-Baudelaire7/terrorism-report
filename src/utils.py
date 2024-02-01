import pycountry
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.express.colors import sample_colorscale
from plotly.subplots import make_subplots
from data_preparation import *


update_layout_simple = { 
    # "template":"plotly_dark",
    "paper_bgcolor":"rgba(0,0,0,0)",
    "plot_bgcolor":"rgba(0,0,0,0)",
    "hovermode":"x",
    "margin":dict(l=0, r=0, t=50),
}

update_layout_geo = {
    "geo":dict(
        showframe=False,
        showcoastlines=False,
        showlakes=False,
        showcountries=False,
        bgcolor="rgba(0,0,0,0)",
        resolution=50,
        projection = dict(type = 'hyperelliptical'),
            
        lonaxis = dict(
            showgrid = False,
            range = [-135, 155]
        ),
        lataxis = dict(
            showgrid = False,
            range = [-55, 73]
        )
            
    )
}


def render_codes_and_flag(df, input_countries, col_name):
    countries, flag = {}, {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3
        flag[country.name] = country.flag
    codes = [countries.get(country, '') for country in input_countries]
    drapeau = [flag.get(country, '') for country in input_countries]
    df['code'] = codes
    df['flag'] = drapeau
    df['flag_country'] =  df['flag'] + " " + df[col_name]
    return df


def calculate_percentage(df):
    total = df.sum()  
    return (df / total) * 100


def sorted_by(df, column, list_order):
    df_sorted = df.sort_values(by=column, key=lambda col: col.map(
        {v: k for k, v in enumerate(list_order)}))
    return df_sorted


def pos_neg(df, col):
    pos, neg = [], []
    for i in df[col].values:
        pos.append(i) if i > 0 else pos.append(None)
        neg.append(i) if i < 0 else neg.append(None)
    df['pos'] = pos
    df['neg'] = neg
    return df


def legend(fig):
    return fig.add_annotation(
        xref="paper", yref="paper",
        name="Data source",
        x=1, y=-0.23,
        xanchor="right",
        showarrow=False,
        text="<b>Data source:</b> <a style='color:royalblue' href='https://www.start.umd.edu/gtd/'>Global Terrorism Index (GTD)</a><br>"
        "<b>Author:</b> Chris Baudelaire .K, <a style='color:royalblue' href='https://www.start.umd.edu/gtd/'>https://M3-Analytics.com</a>",
        opacity=0.7,
        font=dict(size=12, family="serif")
    )


def get_colorscale(series: pd.Series):
    """
    Calculate colorscale for a given series of values.
    """

    # Get difference between year's value and mean of reference period
    diff = series.copy().to_numpy()

    # Create masks for above and below mean
    mask_above = diff > 0
    mask_below = diff < 0

    # Get absolute value of difference
    diff = abs(diff)

    # Create array of zeros with same shape as diff
    diff_norm = np.zeros_like(diff)

    # Calculate min and max for values above the mean
    if len(diff[mask_above]) > 0:
        max_above = np.nanmax(diff[mask_above])
        min_above = np.nanmin(diff[mask_above])

        # Normalize to 0-1
        diff_norm[mask_above] = (diff[mask_above] - min_above) / (max_above - min_above)

    # Calculate min and max for values below the mean
    if len(diff[mask_below]) > 0:
        max_below = np.nanmax(diff[mask_below])
        min_below = np.nanmin(diff[mask_below])

        # Normalize to 0-1
        diff_norm[mask_below] = (diff[mask_below] - min_below) / (max_below - min_below)

    # Create array of black colors with same shape as diff
    colors = np.full_like(diff, "rgb(255, 255, 255)", dtype="object")

    # Sample colors from colormaps, using normalized values
    colors[mask_above] = sample_colorscale("YlOrRd", diff_norm[mask_above])
    colors[mask_below] = sample_colorscale("YlGnBu", diff_norm[mask_below])

    return colors


def dist_fig(data, colorscale, title):
    
    top_labels = data.columns.tolist()
    x_data = data.values.tolist()
    y_data = data.index.tolist()

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colorscale[i],
                    line=dict(color="rgba(0,0,0,0)", width=2)
                )
            ))

    fig.update_layout(
        height=440,
        font=dict(family='serif', size=18, color='black'),
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.14, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        autosize=True,
        # template='plotly_dark',
        margin=dict(l=0, b=0, r=0, t=130),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        title={
            "text": (
                    f"<b>{title}</b><br />"
                    f"<sup style='color:silver'>Le terrorisme dans le monde "
                ),
            "font": {"family": "serif", "size": 30, "color": "black"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    ),
    

    annotations = []

    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='serif', size=15,
                                        color='black'),
                                showarrow=False, align='right'))
        # labeling the first percentage of each bar (x_axis)
        annotations.append(dict(xref='x', yref='y',
                                x=xd[0] / 2, y=yd,
                                text=str(xd[0]) + '%',
                                font=dict(family='serif', size=14,
                                        color='rgb(248, 248, 255)'),
                                showarrow=False))
        # labeling the first Likert scale (on the top)
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                    x=xd[0] / 2, y=1.1,
                                    text=top_labels[0],
                                    font=dict(family='serif', size=15,
                                        color='black'),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
                # labeling the rest of percentages for each bar (x_axis)
                annotations.append(dict(xref='x', yref='y',
                                        x=space + (xd[i]/2), y=yd,
                                        text=str(xd[i]) + '%',
                                        font=dict(family='serif', size=14,
                                                color='rgb(248, 248, 255)'),
                                        showarrow=False))
                # labeling the Likert scale
                if yd == y_data[-1]:
                    annotations.append(dict(xref='x', yref='paper',
                                            x=space + (xd[i]/2), y=1.1,
                                            text=top_labels[i],
                                            font=dict(family='serif', size=15,
                                        color='black'),
                                            showarrow=False))
                space += xd[i]

    fig.update_layout(annotations=annotations)

    return fig


def horizontal_bar_labels(df, key, value, color):
    data = df.to_dict("records")
    
    fig = make_subplots(
        rows=len(data),
        cols=1,
        subplot_titles=[x[key] for x in data],
        shared_xaxes=True,
        print_grid=False,
        vertical_spacing=(0.43 / len(data)),
    )
    
    # add bars for the categories
    for k, x in enumerate(data):
        fig.add_trace(dict(
            type='bar',
            orientation='h',
            y=[x[key]],
            x=[x[value]],
            text=["{:,.0f}".format(x[value])],
            hoverinfo='text',
            textposition='outside',
            marker=dict(color=color),
        ), k+1, 1)

    
    for x in fig["layout"]['annotations']:
        x['x'] = 0
        x['xanchor'] = 'left'
        x['align'] = 'left'
        x['font'] = dict(
            size=14,
        )

    for axis in fig['layout']:
        if axis.startswith('yaxis') or axis.startswith('xaxis'):
            fig['layout'][axis]['visible'] = False

    fig.update_layout(
        # template='plotly_dark',
        margin=dict(l=0, b=0, r=0, t=90),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    return fig



def absolute_relative_figure(df, list_colors, choice_graph, title):

    if choice_graph == "absolue":
        fig = px.area(df, x="year", y=df.columns, color_discrete_sequence=list_colors)
                
        for trace, color in zip(fig.data, list_colors):
            trace.update(fill='tonexty', mode='none', line=dict(color=color), fillcolor=color, opacity=1)
            
        hovermode = "x"
        y_axis=dict(title=None, showgrid=False)
        legende=dict(orientation="v", title=None, x=.03, y=.95)

    else:
        df[df.columns[1:]] = df[df.columns[1:]].apply(calculate_percentage, axis=1)
        fig = px.area(df, x="year", y=df.columns, color_discrete_sequence=list_colors)

        for trace, color in zip(fig.data, list_colors):
            trace.update(fill='tonexty', mode='none', line=dict(color=color), fillcolor=color, opacity=1)
            
        hovermode = "closest"
        y_axis=dict(ticksuffix="%", title=None, showgrid=False)
        legende=dict(orientation="h", title=None)
        
        for trace in fig.data:
            trace.update(line=dict(shape="spline", smoothing=.5, width=0))
                
    # else:
    #     df[df.columns[1:]] = df[df.columns[1:]].apply(calculate_percentage, axis=1)
    #     fig = px.bar(df, x="year", y=df.columns, barmode="stack", color_discrete_sequence=list_colors)

    #     # for trace, color in zip(fig.data, list_colors):
    #     #     trace.update(fill='tonexty', mode='none', line=dict(color=color), fillcolor=color, opacity=1)
            
    #     hovermode = "closest"
    #     y_axis=dict(ticksuffix="%", title=None, showgrid=False)
    #     legende=dict(orientation="h", title=None)


    fig.update_layout(
        hovermode=hovermode,
        # template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font={"family": "Lato", "size": 14},
        margin=dict(autoexpand=True, l=0, r=0, t=60),
        legend=legende,
        height=450,
        xaxis=dict(title=None, showgrid=False),
        yaxis=y_axis,
        title={
            "text": (
                    f"<b>{title}</b><br />"
                    f"<sup style='color:silver'>Série temporelle {choice_graph} (1970-2017) "
                ),
            "font": {"family": "serif", "size": 30, "color": "black"},
            "x": 0.98,
                "y": 0.91,
                "xanchor": "right",
                "yanchor": "top",
        }
    )
          
    return fig