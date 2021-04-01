#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 18:59:55 2021

@author: sofiapfund
"""

# - Map of the geographic distribution of genome screening experiments using the first author affiliation location proxy. - #

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from scipy.stats import gaussian_kde
from pymongo import MongoClient
import pprint as pp ### pretty print


### 1) Connect to MongoDB and load publication collection:

client = MongoClient() 
cl = client['progenetix'].publications 

### 2) Get information about sample geolocation:

c = []
n_pub = 0
aCGH = 0
cCGH = 0
WES = 0
WGS = 0
for pub in cl.find():
    #pp.pprint(pub)
    coord = pub["provenance"]["geo_location"]["geometry"]["coordinates"]
    if coord != [] and coord != [0, 0]:
            c.append(coord) 
            n_pub += 1
            #print(int(pub["counts"]["acgh"])) ### finish annotations in figure description!

WESWGS = WES + WGS

### 3) Plot sample density:

def sample_kde(samples_coordinates):

    plt.figure(figsize=(14,8))
    
    map = Basemap(projection='cyl', llcrnrlat=-60, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180) ### specify projection region
    map.drawmapboundary(color="white") ### fill_color='#3cb9e0'
    map.fillcontinents(color="white") ### lake_color='#1c94b9'
    map.drawcoastlines(linewidth=0.5)
    map.drawcountries()
    
    lons = []
    lats = []
    
    for coord_pair in samples_coordinates:
        lons.append(coord_pair[0])
        lats.append(coord_pair[1])
    
    x, y = map(lons, lats)
    
    cm = plt.cm.get_cmap('autumn_r') ### color map
    
    # Calculate the point density (Gaussian Kernel Desnsity)
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy) * 10000
    
    fig = map.scatter(x, y, marker='o', c=z, s=80, alpha=0.2, zorder=1.5, cmap=cm)
    
    # Add colorbar
    cb = plt.colorbar(fig, shrink=0.55)
    cb.set_label(r"Gaussian Kernel Density in (d x$10^{5}$)", rotation = 270, labelpad = 20)
    cb.ax.set_title("Sample Density", fontsize=10)
    
    plt.title("Map of the geographic distribution of genome screening experiments", fontsize=12, fontweight="bold", y=1.1)
    
    plt.text(-135, -100, "Figure 1. Map of the geographic distribution of genome screening experiments using the first author affiliation" + 
             "\n" + f"location proxy derived from {n_pub} publications registered in the Progenetix database, including {aCGH}" + 
             "\n" + f"genomic arrays, {cCGH} cCGH and {WESWGS} whole genome/exome-based cancer genome profiles." + 
             "\n" + "The map is rendered in a cylindrical projection (kernel density per square kilometer?).", fontsize=8)
    
    plt.show()
    
    return map

print(sample_kde(c))







