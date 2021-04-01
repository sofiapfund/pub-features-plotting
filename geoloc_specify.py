#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 08:05:42 2021

@author: sofiapfund
"""

# - Plot geolocation of different tumor type samples across the years - #

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors
import matplotlib.cm as cmx
from pymongo import MongoClient


### 1) Connect to MongoDB and load publication collection:

client = MongoClient() 
cl = client['progenetix'].publications 


### 2) Get information about sample geolocation & tumor type for publications of a specific subset of years:

# Required function argument: list() object indicating the wanted subsed of years as integers

def get_info(years): 
    c = []
    #tumor_type =[]
    for year in years:
        for obj in cl.find({"year" : str(year)}): 
            coord = obj["provenance"]["geo_location"]["geometry"]["coordinates"]
            #tumor = obj["cancertype"]
            if coord != 0 and coord != [0, 0]:
                c.append([coord, year])
                #tumor_type.append(tumor)
    
    return c #, tumor_type

uniq = [2018, 2019, 2020]
coordinates = get_info(uniq)


#### 3) Plot the information: 

# Required function arguments: 1. projection region, 2. samples geolocations, 3. tumor type(s)
# Note on projection region: must be float or integer from -180 to 180 (lon); resp. from -90 to 90 (lat)
# Check out: https://matplotlib.org/basemap/api/basemap_api.html

def plot_geoloc(llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon, coordinates): #tumor_type

    plt.figure(figsize=(14,8))
    
    map = Basemap(projection='cyl', llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat, llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon) 
    map.drawmapboundary(color="white") 
    map.fillcontinents(color="white") 
    map.drawcoastlines(linewidth=0.5)
    map.drawcountries()
    
    def takeFirst(elem):
        return elem[1]
    
    coordinates.sort(key=takeFirst) ### sort samples coordinates by year of publication
    
    lons = []
    lats = []
    years = []
    for coord_pair in coordinates:
        lons.append(coord_pair[0][0])
        lats.append(coord_pair[0][1])
        years.append(int(coord_pair[1]))
    
    x, y = map(lons, lats)
    
    #tumor_type = # list to be used as a marker (extracted from mongoDB)
    
    colorMap = plt.get_cmap('tab10')
    cNorm  = colors.Normalize(vmin=0, vmax=len(uniq))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=colorMap)
    
    for line in coordinates:
        for i in range(len(uniq)):
            if line[1] == uniq[i]: #uniq = list that specifies the selected years
                map.scatter(line[0][0], line[0][1], s=80, color=scalarMap.to_rgba(i), label=uniq[i], marker="o", alpha=0.5, zorder=1.5)
    
    # Avoid repeating labels:
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    
    plt.title("Map of the geographic distribution of genome screening experiments", fontsize=12, fontweight="bold", y=1.1)
    n_pub = len(coordinates)
    plt.text(-177, -30, f"n(publications): {n_pub}", fontsize=10)
    plt.text(-110, -80, "Fig. 1. Map of the geographic distribution of genome screening experiments performed in the years 2018, 2019 and 2020." + "\n" + "The first author affiliation location proxy was used to plot the data. Cylindrical projection of the world map.", fontsize=10)
    
    plt.show()
    
    return map

print(plot_geoloc(-60, 80, -180, 180, coordinates)) 




    
