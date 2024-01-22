import pandas as pd
import numpy as np
from constants import *
from src.utils import *


countries_most_affected = ["Iraq","Afghanistan","Pakistan","India","Syria", "Nigeria"]

def data_date_filter(range_date):
    df = raw_data[(raw_data["year"] >= range_date[0]) & (raw_data["year"] <= range_date[1])]
    return df


def data_filter(df, group, attack, target, weapon):
    data = df[
        (df["gname"] == group if group in terrorist_group else df["gname"]==df["gname"]) & 
        (df["attacktype"] == attack if attack in terrorist_attack else df["attacktype"]==df["attacktype"]) & 
        (df["targtype"] == target if target in terrorist_targtype else df["targtype"]==df["targtype"]) &
        (df["weaptype1"] == weapon if weapon in terrorist_weaptype else df["weaptype1"]==df["weaptype1"]) 
    ]
    return data


def data_geo_filter(dataframe, area):
    if area == "Monde":
        data = dataframe.copy()
    elif area in list(dataframe.continent.unique()):
        data = dataframe[dataframe.continent == area]
    elif area in list(dataframe.region.unique()):
        data = dataframe[dataframe.region == area]
    else:
        data = dataframe[dataframe.country == area]
    
    return data


# data
raw_data = pd.read_csv(
    'https://raw.githubusercontent.com/Chris-Baudelaire7/terrorism_report/main/src/data/terrorism_database.csv',
    engine="python",
    on_bad_lines="skip",
                 encoding='utf-8')
raw_data = raw_data.copy().iloc[:, 1:]
raw_data = render_codes_and_flag(raw_data, list(raw_data["country"].values), "country")


# Category
limites = [1, 5, 10, 20, float('inf')]
casualties_limit = [-1, 0, 5, 10, 20, 50, float('inf')]

etiquettes = ["1-5 décès", "6-10 décès", "11-20 décès", "plus de 20 décès"]
casualties_labels = ["0 décès", "1-5 victimes", "6-10 victimes", "11-20 victimes", "21-50 victimes", "plus de 50 décès"]


# New features
raw_data['nkill_categories'] = pd.cut(raw_data['nkill'], bins=limites, labels=etiquettes)
raw_data['continent'] = raw_data['region'].map(continent_mapping)
raw_data["month_name"] = raw_data['month'].map(month_dict)
raw_data["casualties"] = raw_data['nkill'] + raw_data['nwound']


# Renaming (because too long)
raw_data.set_index("weaptype1", inplace=True)
raw_data.rename(
    index={"Vehicle (not to include vehicle-borne explosives, i.e., car or truck bombs)": "Vehicle"},
    inplace=True
)
raw_data.reset_index(inplace=True)


# Removing unknown month
df = raw_data.copy()[(raw_data.month != 0) & (raw_data.day != 0)]
df['date'] = pd.to_datetime(df[['year', 'month', 'day']], errors='coerce')

columns_to_clean = ["attacktype", "gname", "targtype", "weaptype1"]

df_without_unknown = raw_data.copy()
df_without_unknown[columns_to_clean] = df_without_unknown[columns_to_clean].replace('Unknown', np.nan)


# List
terrorist_group = list(raw_data.gname.unique())
terrorist_attack = list(raw_data.attacktype.unique())
terrorist_targtype = list(raw_data.targtype.unique()) 
terrorist_weaptype = list(raw_data.weaptype1.unique())


