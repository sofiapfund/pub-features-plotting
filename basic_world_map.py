#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 17:36:49 2021

@author: sofiapfund
"""

# - Plotting of the World Map - #

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors
import matplotlib.cm as cmx

##############################################################################
##############################################################################
##############################################################################

# Required function arguments: coordinates of the locations I want to pot and coordinates of the projection region.
# Coordinates must be given as float or as integer from -180 to 180 (lon); resp. from -90 to 90 (lat).
# Check out: https://matplotlib.org/basemap/api/basemap_api.html

# In case of problems with Basempa, try:
# import os
# path = os.path.dirname(mpl_toolkits.basemap.__file__)
# os.environ['PROJ_LIB'] = f'{path}'

##############################################################################

def plot_geoloc(my_coordinates, llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon):

    plt.figure(figsize=(14,8))
    
    map = Basemap(projection='cyl', llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat, llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon) 
    map.drawmapboundary(color="black", linewidth=0.5, fill_color='#3cb9e0') 
    map.fillcontinents(color='darkkhaki', lake_color='lightblue') 
    map.drawcoastlines(linewidth=0.5)
    map.drawcountries()
     
    labels=['Location 1', 'Location 2', 'Location 3']
    colorMap = plt.get_cmap('tab10')
    cNorm  = colors.Normalize(vmin=0, vmax=len(labels))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=colorMap)
    
    for i, pair in enumerate(my_coordinates):
        map.scatter(pair[0], pair[1], s=50, color=scalarMap.to_rgba(i), marker='o', alpha=0.9, zorder=1.5, label=labels[i])

    # Add cities:
    cities = [["New York", -73.935242, 40.730610], ["London", -0.118092, 51.509865], ["New Delhi", 77.216721, 28.644800], 
                ["Hong Kong", 114.177216, 22.302711], ["Sydney", 151.209900, -33.865143], ["São Paulo", -46.625290, -23.533773],
                ["Lagos", 3.406448, 6.465422]]
    
    for city in cities:
        plt.plot(city[1], city[2], "wo", markersize=3)
        plt.annotate(city[0], (city[1]+0.5, city[2]+1.0), fontweight="bold", color="white")
    
    # Add descriptions:
    plt.title('Title', fontsize=14, fontweight="bold", y=1.05)

    plt.legend(fontsize=10)
   
    plt.text(-30, -70, 'Figure description.', fontsize=10)
    
    plt.show()
    plt.savefig("basic_world_map.png", dpi=300)
    
    return map

##############################################################################

coordinates = [[-100.01, 40.71], [8.69, 49.41], [35.69, 20.41]]
print(plot_geoloc(coordinates, -60, 80, -180, 180)) 

##############################################################################
##############################################################################
##############################################################################