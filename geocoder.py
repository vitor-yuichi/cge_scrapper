import googlemaps
from datetime import datetime
import pandas as pd
import numpy as np

gmaps = googlemaps.Client(key=GEOCODING_API)

def geocode_result(all_floods):
    lat = geocode_result[0]['geometry']['location']['lat']
    long = geocode_result[0]['geometry']['location']['lng']


    lat_list = []
    long_list = []
    for index, row in all_floods.iterrows():
        geocode_result = gmaps.geocode(row['geoadress'])
        lat = geocode_result[0]['geometry']['location']['lat']
        long = geocode_result[0]['geometry']['location']['lng']
        lat_list.append(lat)
        long_list.append(long)
        all_floods.at[index, 'lat'] = lat
        all_floods.at[index, 'lng'] = long
    all_floods.to_excel('finished.xlsx')
        