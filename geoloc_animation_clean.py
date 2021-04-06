#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 21:18:12 2021

@author: sofiapfund
"""

# - Map of the geographic distribution of genome screening experiments using the first author affiliation location proxy. - #

import requests
import json
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
from matplotlib import animation
import numpy as np


def jprint(obj):
    text = json.dumps(obj, sort_keys= True, indent = 4)
    print(text)

    # 1) Select results:
    
response = requests.get("https://progenetix.org/services/publications/?method=details")
print(response.status_code)
publications = response.json()["response"]["results"]

c = []
for pub in publications:       
    coord = pub["provenance"]["geo_location"]["geometry"]["coordinates"]
    year = pub["year"]
    genomes = pub["counts"]["genomes"]
    if coord != [] and coord !=[0,0] and year != None and genomes != None:
        c.append([coord, year, genomes])

    # 2) Sort data in chronological order:

def takeFirst(elem):
     return elem[1]
c.sort(key=takeFirst)

    # 3) Plot geolocation of tumor samples across the years:

years = []
genomess = []
for coord_pair in c:
    years.append(int(coord_pair[1]))
    genomess.append(coord_pair[2])

uniq = list(set(years)) # 28 unique years

df = pd.DataFrame({"Years": years, "Genomes": genomess})
df["yr_genome_sum"] = df.groupby(["Years"])["Genomes"].transform(sum)
uniq_genomes = list(set(df["yr_genome_sum"])) # total amount of samples for each unique year

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

samples = 0
def update(t):
    global x_vals, y_vals, intensity, samples
    
    # Get intermediate points
    for coord_pair in c:
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
