#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 21:18:12 2021

@author: sofiapfund
"""

# - Map of the geographic distribution of genome screening experiments using the first author affiliation location proxy. - #

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
from matplotlib import animation
import numpy as np
from pymongo import MongoClient

client = MongoClient() 
cl = client['progenetix'].publications 

### 1) Get data:
rows = []
for pub in cl.find({"year": {"$regex": r"\d{4}"}}):
    coord = pub["provenance"]["geo_location"]["geometry"]["coordinates"]
    year = pub["year"]
    genomes = pub["counts"]["genomes"]
    if coord != [] and coord !=[0,0] and year != None and genomes != None:
        rows.append([coord, int(year), int(genomes)])

### 2) Sort data in chronological order:
def takeFirst(elem):
     return elem[1]
rows.sort(key=takeFirst)

### 3) Make dataframe with all the data:
df = pd.DataFrame(rows, columns=["Coordinates", "Years", "Genomes"])
uniq = list(set(df["Years"]))
df["yr_genome_sum"] = df.groupby(["Years"])["Genomes"].transform(sum)
uniq_genomes = list(set(df["yr_genome_sum"])) # total amount of samples for each unique year

### 4) Plot geolocation of tumor samples across the years:
fig, ax = plt.subplots(figsize=(14,8))
x_vals = []
y_vals = []

my_map = Basemap(projection='cyl', llcrnrlat=-60, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180)
my_map.drawcoastlines(linewidth=0.5)
my_map.drawcountries()
my_map.fillcontinents(color = 'darkkhaki', lake_color='lightblue')
my_map.drawmapboundary(color= "black", linewidth=0.5, fill_color='#3cb9e0') 

scatter = ax.scatter(x_vals,y_vals, color="red", s=30, alpha=0.3, zorder=1.5)
ax.set_title("Geographic distribution of genome screening experiments from 1993 to 2020.", fontweight="bold", y=1.05, fontsize=14)

cities = [["New York", -73.935242, 40.730610], ["London", -0.118092, 51.509865], ["New Delhi", 77.216721, 28.644800], 
          ["Hong Kong", 114.177216, 22.302711], ["Sydney", 151.209900, -33.865143], ["São Paulo", -46.625290, -23.533773],
          ["Lagos", 3.406448, 6.465422]]
for city in cities:
    plt.plot(city[1], city[2], "wo", markersize=3)
    ax.annotate(city[0], (city[1]+0.5, city[2]+1.0), fontweight="bold", color="white")

samples = 0
def update(t):
    global x_vals, y_vals, intensity, samples
    
    for coord_pair in rows:
        if int(coord_pair[1]) == uniq[t]:
            new_xvals, new_yvals = coord_pair[0][0], coord_pair[0][1] # lons, lats
            x_vals.append(new_xvals)
            y_vals.append(new_yvals)

        # Put new values in your plot
        scatter.set_offsets(np.c_[x_vals,y_vals])
    
    # Set title and add sample information (how many)
    samples += uniq_genomes[t]
    plt.xlabel("Year: " + str(uniq[t]) + "\n" + f"Samples: {samples}", fontsize=12, fontweight="bold", labelpad=15)
       
ani = animation.FuncAnimation(fig, update, frames=len(uniq), interval=1500, repeat=False)

plt.show()
