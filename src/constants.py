timeout = 200

mapbox_access_token = 'pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw'

scale = ['rgb(103,0,13)','rgb(203,24,29)','rgb(251,106,74)', 'rgb(252,146,114)','rgb(253,219,199)','rgb(255,245,240)']
 
columns = [
    'iyear', 'imonth', 'iday', 'extended', 'country_txt', 'region_txt',
    'provstate', 'city', 'latitude', 'longitude', 'location', 'summary',
    'multiple', 'success', 'suicide', 'attacktype1_txt', 'targtype1_txt',
    'targsubtype1_txt', 'corp1', 'target1', 'natlty1_txt', 'crit1', 'nkillter',
    'targsubtype2_txt', 'gname', 'gsubname', 'guncertain1', 'individual',
    'claimmode_txt', 'weaptype1_txt', 'weapsubtype1_txt', 'weaptype2_txt',
    'weapsubtype2_txt', 'weapdetail', 'nkill', 'nwound', 'propextent_txt',
     'property', 'propextent', 'propvalue',
]

dict_rename = {
    "iyear": "year", "imonth":"month", "iday":"day", "country_txt":"country", "region_txt":"region",
    "attacktype1_txt":"attacktype", "targtype1_txt":"targtype", "targsubtype1_txt":"targsubtype",
    "corp1":"corp", "target1":"target", "natlty1_txt":"natlty", "targsubtype2_txt":"targsubtype2",
    "guncertain1":"guncertain", "claimmode_txt":"claimmode", "weaptype1_txt":"weaptype1", 
    "weaptype2_txt":"weaptype2", "weapsubtype2_txt": "weapsubtype2", "weapsubtype1_txt":"weapsubtype1"
}

new_name_country = {
    "Bolivia": "Bolivia, Plurinational State of", 
    "Bosnia-Herzegovina": "Bosnia and Herzegovina",
    "Brunei": "Brunei Darussalam",
    "Czech Republic": "Czechia",
    "Ivory Coast": "Côte d'Ivoire",
    "Democratic Republic of the Congo": "Congo, The Democratic Republic of the",
    "East Germany (GDR)":"Germany",
    "West Germany (FRG)":"Germany"
}

rename={
    "Vehicle (not to include vehicle-borne explosives, i.e., car or truck bombs)": "Vehicle",
    "Islamic State of Iraq and the Levant (ISIL)": "I.S.I.L",
    "Liberation Tigers of Tamil Eelam (LTTE)": "L.T.T.E",
    "Farabundo Marti National Liberation Front (FMLN)": "F.M.L.N",
    "Nicaraguan Democratic Force (FDN)": "F.D.N",
    "Revolutionary Armed Forces of Colombia (FARC)": "F.A.R.C",
    "Kurdistan Workers' Party (PKK)": "P.K.K",
    "New People's Army (NPA)": "N.P.A",
    "Shining Path (SL)": "S.L",
    "Irish Republican Army (IRA)": "I.R.A",
    "Tehrik-i-Taliban Pakistan (TTP)": "T.T.P",
    "Hostage Taking (Kidnapping)": "Kidnapping",
    "Hostage Taking (Barricade Incident)": "Barricade Incident",
    "Bombing/Explosion": "Explosion<br>Bombing",
    "Private Citizens & Property": "Private<br>Citizens<br>& Property",
    "Government (General)": "Government<br>(General)",
    "Religious Figures/Institutions": "Religious<br>Figures<br>(Institutions)",
    "Armed Assault":"Armed<br>Assault",
    "Unarmed Assault":"Unarmed<br>Assault",
    "Aum Shinri Kyo": "Aum<br>Shinri<br>Kyo",
    "Al-Qaida in Iraq": "Al-Qaida<br>in Iraq",
    "Boko Haram": "Boko<br>Haram"
}

month_dict = {
    1: 'Janvier',
    2: 'Février',
    3: 'Mars',
    4: 'Avril',
    5: 'Mai',
    6: 'Juin',
    7: 'Juillet',
    8: 'Août',
    9: 'Septembre',
    10: 'Octobre',
    11: 'Novembre',
    12: 'Décembre',
}

continent_mapping = {
    'Central America & Caribbean': 'America',
    'North America': 'America',
    'Southeast Asia': 'Asia',
    'Western Europe': 'Europe',
    'East Asia': 'Asia',
    'South America': 'America',
    'Eastern Europe': 'Europe',
    'Sub-Saharan Africa': 'Africa',
    'Middle East & North Africa': 'Africa',
    'Australasia & Oceania': 'Oceania',
    'South Asia': 'Asia',
    'Central Asia': 'Asia'
}



targtype_to_group=[
       "Educational Institution", "Abortion Related", "Airports & Aircraft", "Educational Institution",
       "Food or Water Supply", "Government (Diplomatic)", "Journalists & Media",
       "Journalists & Media", "Maritime",  "Other", "Tourists", "NGO", "Telecommunication",
       "Terrorists/Non-State Militia", "Violent Political Party","Unknown","Utilities","Transportation",
       "Religious Figures/Institutions"
]

attacktype_to_group=[
       "Hijacking","Unknown","Unarmed Assault","Hostage Taking (Barricade Incident)",
       "Facility/Infrastructure Attack","Hostage Taking (Kidnapping)", "Assassination"
]

weaptype_to_group = ["Biological","Chemical","Fake Weapons","Other","Radiological", "Melee", "Unknown","Incendiary",
      "Sabotage Equipment","Vehicle"]

