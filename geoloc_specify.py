#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 08:05:42 2021

@author: sofiapfund
"""

# - Plot geolocation of different tumor type samples across the years - #

import os
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors
import matplotlib.cm as cmx
from pymongo import MongoClient

#path = os.path.dirname(mpl_toolkits.basemap.__file__) # get path
#print(path)
os.environ['PROJ_LIB'] = '/Users/sofiapfund/.conda/envs/untitled/lib/python3.7/site-packages/mpl_toolkits/basemap'

##############################################################################
##############################################################################
##############################################################################

# Get information about sample geolocation & tumor type for publications of a specific subset of years (list()):

def get_info(years, cancer): 
    
    # Connect to MongoDB and load publication collection:
    client = MongoClient() 
    cl = client['progenetix'].publications 
    
    # Extract information:
    c = []
    for year in years:
        for obj in cl.find({ '$and': [{"year" : str(year)}, {'sample_types': {'$exists': True}}] }): 
            if type(obj['provenance']) == list:
                coord = obj["provenance"][0]["geo_location"]["geometry"]["coordinates"]
            else:
                coord = obj["provenance"]["geo_location"]["geometry"]["coordinates"]
            tumor = obj["sample_types"]
            for typ in tumor:
                label = typ['label']
                if coord != [] and coord != [0, 0] and label == cancer:
                    c.append([coord, year, typ['id'], typ['counts']])
    
    return c 

##############################################################################

# Plot the information: 

# Required function arguments: coordinates of the projection region.
# Coordinates must be given as float or as integer from -180 to 180 (lon); resp. from -90 to 90 (lat).
# Check out: https://matplotlib.org/basemap/api/basemap_api.html

def plot_geoloc(llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon):

    plt.figure(figsize=(14,8))
    
    map = Basemap(projection='cyl', llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat, llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon) 
    map.drawmapboundary(color="white") 
    map.fillcontinents(color="white") 
    map.drawcoastlines(linewidth=0.5)
    map.drawcountries()
    
    def takeFirst(elem): # function needed for sorting
        return elem[1]
    
    coordinates = get_info(years, cancer)
    coordinates.sort(key=takeFirst) # sort samples coordinates by year of publication
    
    lons = []
    lats = []
    n_samples = 0
    ncit = ''
    for coord_pair in coordinates:
        lons.append(coord_pair[0][0])
        lats.append(coord_pair[0][1])
        n_samples += coord_pair[3]
        ncit = coord_pair[2]
    
    x, y = map(lons, lats)
        
    colorMap = plt.get_cmap('tab10')
    cNorm  = colors.Normalize(vmin=0, vmax=len(years))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=colorMap)
    
    for line in coordinates:
        for i in range(len(years)):
            if line[1] == years[i]: 
                map.scatter(line[0][0], line[0][1], s=80, color=scalarMap.to_rgba(i), label=years[i], marker="o", alpha=0.7, zorder=1.5)
    
    # Avoid repeating labels:
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    
    # Add descriptions:
    plt.title(f"Map of the geographic distribution of genome screening experiments of {cancer} ({ncit}) cancer samples.", fontsize=12, fontweight="bold", y=1.1)
    n_pub = len(coordinates)
    y = len(years)
    plt.text(-177, -37, f"n(publications): {n_pub}" + "\n" + f"n(samples): {n_samples}", fontsize=10, fontstyle='oblique')
    plt.text(-115, -80, f"Fig. 1. Map of the geographic distribution of genome screening experiments performed in the last {y} years." + "\n" + "The first author affiliation location proxy was used to plot the data. Cylindrical projection of the world map.", fontsize=10)
    
    plt.show()
    
    plt.savefig("geoloc_specify.png", dpi=300)
    
    return map

##############################################################################

years = [2020, 2021]
cancer = "Neuroblastoma" 
coordinates = get_info(years, cancer)
print(coordinates)

print(plot_geoloc(-60, 80, -180, 180)) 

##############################################################################
##############################################################################
##############################################################################


    
