#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 08:12:20 2021

@author: sofiapfund
"""

import matplotlib.pyplot as plt
import math
import pandas as pd
import seaborn as sns
import numpy as np
from pymongo import MongoClient

### 1) Connect to MongoDB and load publication collection:

client = MongoClient() 
cl = client['progenetix'].publications 

data = []
for pub in cl.find({"year": {"$regex": r"\d{4}"}}):
    year = pub["year"]
    acgh = pub["counts"]["acgh"]
    if acgh != None and acgh != "":
        int_acgh = int(acgh)
    ccgh = pub["counts"]["ccgh"]
    if ccgh != None and ccgh != "":
        int_ccgh = int(ccgh)
    wes = pub["counts"]["wes"]
    if wes != None and wes != "":
        int_wes = int(wes)
    wgs = pub["counts"]["wgs"]
    if wgs != None and wgs != "":
        int_wgs = int(wgs)
    
    data.append([year, int_acgh, int_ccgh, int_wes, int_wgs])

### 2) Sort publications by year:
        
def takeFirst(elem):
    return elem[0]

data.sort(key=takeFirst)

### 3) Calculate dot size:

def dot_size(log_samples):
    size = int(4.0 * log_samples)**2 +15
    return size

### 4) Create data objects:

rows = []
n_acgh = 0
n_ccgh = 0
n_wes = 0
n_wgs = 0
for pub in data:
    if pub[1] > 0:
        n_acgh += pub[1]
        rows.append([pub[0], math.log10(pub[1]), "aCGH", dot_size(math.log10(pub[1]))]) # year - n_samples (log transformation) - technique - dot size    
    if pub[2] > 0:
        n_ccgh += pub[2]
        rows.append([pub[0], math.log10(pub[2]), "cCGH", dot_size(math.log10(pub[2]))])    
    if pub[3] > 0:
        n_wes += pub[3]
        rows.append([pub[0], math.log10(pub[3]), "WES", dot_size(math.log10(pub[3]))])
    if pub[4] > 0:
        n_wgs += pub[4]
        rows.append([pub[0], math.log10(pub[4]), "WGS", dot_size(math.log10(pub[4]))])


### 5) Create dataframe for plot: 
 
df = pd.DataFrame(rows, columns=["Year", "Samples", "Technique", "Sizes"])

### 6) Plot scatterplot with legend and jitter effect:

def jitter(values):
    new_values = []
    for v in values:
        v = float(v) + np.random.random()
        new_values.append(v)
    return new_values


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


### 7) Add description to the figure (tot_genomes and n_pub are automatically updated):

tot_genomes = n_acgh + n_ccgh + n_wes + n_wgs # tot nr of samples
n_pub = cl.count_documents({"year": {"$regex": r"\d{4}"}}) # tot nr of publications
#txt1 = f"n(samples): {tot_genomes}" + "\n" + f"n(publications): {n_pub}" 
#plt.figtext(0.27, 0.71, txt1, wrap=True, horizontalalignment='left', fontsize=10) 

#txt2= f"Fig 1. Publication statistics for cancer genome screening studies. The graphic shows our assessment of publications reporting whole-genome screening of cancer samples, using molecular detection methods (chromosomal CGH, genomic arrays technologies, whole-exome and whole-genome sequencing)." 
#+ "\n" + f" For the years 1993-2020 we found {n_pub} publications reporting {tot_genomes} individual samples." 

plt.show()

''' 
Notes:
    - the y-axis and the size of the dots refer to the sample number in a !non-linear! way;
    - the color codes indicate the technology used;
    - a figure description can be added with plt.figtext(x, y, text);
'''












