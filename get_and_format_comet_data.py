import json
import requests
import os

name = input("Name of Comet: ").lower()
url = f"https://theskylive.com/objects/{name}/chartdata_dg.json"

try:
    os.mkdir(name)
except:
    pass

filename = f"{name}/{name}"

# saving data
data = requests.get(url).text

f = open(filename + "_raw.txt", "w")
f.write(data)
f.close()


# reading in the data
f = open(filename + "_raw.txt", "r")
original = f.readlines()
f.close()


# removing uncessary lines
lines = original[16:]


formatted_lines = []

for i in lines:
    formatted = i.replace('"__rawdata":[', "")
    formatted_lines.append(formatted)

formatted_lines = formatted_lines[:-1]



total = []
distance = []

for line in formatted_lines:
    x = line.replace("\n", "")[:-1]
    y = x.replace("[", "").replace("]", "")
    x, y, z  = y.split(",")
    
    
    date = x.replace("_d('", "").replace("')", "")
    
    total.append(date + "," + z)
    distance.append(z)
    
    

f = open(filename + "_formatted.csv", "w")

for i in total:
    f.write(i.strip() + "\n")

f.close()

f = open(filename + "_formatted_distance_only.txt", "w")

for i in distance:
    f.write(i + "\n")

f.close()
    

