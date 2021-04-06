#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 08:12:20 2021

@author: sofiapfund
"""

import requests
import json
import matplotlib.pyplot as plt
import math
import pandas as pd
import seaborn as sns
import numpy as np

def jprint(obj):
    text = json.dumps(obj, sort_keys= True, indent = 4)
    print(text)

response = requests.get("https://progenetix.org/services/publications/?method=details")
print(response.status_code)

    # 1) Select results:

publications = response.json()["response"]["results"]
#jprint(publications)


    # 2) Extract data from progenetix objects:

data = []
for pub in publications:
    year = pub["year"]
    acgh = pub["counts"]["acgh"]
    ccgh = pub["counts"]["ccgh"]
    wes = pub["counts"]["wes"]
    wgs = pub["counts"]["wgs"]
        
    if year != None:
        data.append([year, acgh, ccgh, wes, wgs])


    # 3) Sort publications by year:
        
def takeFirst(elem):
    return elem[0]

data.sort(key=takeFirst)


    # 4) Create data objects:

objects = []
n_acgh = 0
n_ccgh = 0
n_wes = 0
n_wgs = 0

for pub in data:
    obj = []
    obj1 = []
    obj2 = []
    obj3 = []
    
    if pub[1] > 0:
        obj.append(pub[0]) # year
        obj.append(math.log10(pub[1])) # n_samples (log transformation)
        obj.append("aCGH") # technique
        objects.append(obj)
        n_acgh += pub[1]
        
    if pub[2] > 0:
        obj1.append(pub[0])
        obj1.append(math.log10(pub[2]))
        obj1.append("cCGH")
        objects.append(obj1)
        n_ccgh += pub[2]
        
    if pub[3] > 0:
        obj2.append(pub[0])
        obj2.append(math.log10(pub[3]))
        obj2.append("WES")
        objects.append(obj2)
        n_wes += pub[3]

    if pub[4] > 0:
        obj3.append(pub[0])
        obj3.append(math.log10(pub[4]))
        obj3.append("WGS")
        objects.append(obj3)
        n_wgs += pub[4]


    # 5) Create dataframe for plot: 
        
years = []
samples = []
tech = []
sizes = []
for obj in objects:
    years.append(obj[0])
    samples.append(obj[1])
    tech.append(obj[2])
    s = int((4.0 * obj[1]))**2 +15 # size depends on n of samples
    sizes.append(s)   

df = pd.DataFrame({"Year": years, "Samples": samples, "Technique": tech, "Sizes": sizes})


  # 6) Plot scatterplot with legend and jitter effect:

def jitter(values):
    new_values = []
    for v in values:
        v = float(v) + np.random.random()
        new_values.append(v)
    return new_values

#sns.stripplot(x="Year", y="Samples", hue= "Technique", size= df["Sizes"], data= df, dodge= True, alpha= 0.2, jitter= 1.25)

plt.figure(figsize=(10,6))

sns.scatterplot(x= jitter(df["Year"]), 
                y= jitter(df["Samples"]),
                hue= "Technique", data= df, s= df["Sizes"], alpha= 0.2)

#plt.xticks([2, 7, 12, 17, 22, 27], ['1995','2000','2005','2010', '2015', '2020'], fontsize=10) #rotation = 45
plt.yticks(fontsize=10)
plt.ylabel("Cancer Samples in Publication (log10 scale)")
plt.xlabel("Year of Publication")
plt.legend(fontsize=10)
plt.title("Number of tumor samples for each publication across the years", fontsize = 12, fontweight = "bold")


# 7) Add description to the figure (tot_genomes and n_pub are automatically updated):

tot_genomes = 0
for pub in publications:
    tot_genomes += pub["counts"]["genomes"]
    
n_pub = len(publications)

txt1 = f"n(samples): {tot_genomes}" + "\n" + f"n(publications): {n_pub}" + "\n" + f"n(aCGH): {n_acgh}" + "\n" + f"n(cCGH): {n_ccgh}" + "\n" + f"n(WES): {n_wes}" + "\n" + f"n(WGS): {n_wgs}" 

txt= f"Fig 1. Publication statistics for cancer genome screening studies. The graphic shows our assessment of publications reporting whole-genome screening of cancer samples, using molecular detection methods (chromosomal CGH, genomic arrays technologies, whole-exome and whole-genome sequencing)." + "\n" + f" For the years 1993-2020 we found {n_pub} publications reporting {tot_genomes} individual samples." + "\n" + " The y-axis and the size of the dots refer to the sample number in a non-linear way; the color codes indicate the technology used." 

plt.figtext(0.27, 0.71, txt1, wrap=True, horizontalalignment='left', fontsize=10) 

plt.show()














