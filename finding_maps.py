#The code in this script is used to analyse a given sample of maps
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import edinburghgerrymanderingcode as gm
import sys
import time
from scipy.stats import norm
import os,os.path
import shutil
#sys.setrecursionlimit(1500)


#df = pd.read_csv("dummyData.csv")
#df['Neighbours'] = df.Neighbours.apply(lambda x: x.split(', '))
#df['ID'] = df['ID'].astype(str) 
#id = df['ID'].tolist()
#neighbours = df['Neighbours'].tolist()
#lat = df['Lat'].tolist()
#lng = df['Long'].tolist()
#constituencies = df['Initial'].tolist()
#electorate = df['Electorate'].tolist()

wards_df = pd.read_csv("WardsWithDataVotes.csv")
wards_df['NeighbourID'] = wards_df['NeighbourID'].astype(str)
wards_df['NeighbourID'] = wards_df.NeighbourID.apply(lambda x: x.split(','))
wards_df['CleanLengths'] = wards_df.CleanLengths.apply(lambda x: x.split(','))
wards_df['WardID'] = wards_df['WardID'].astype(str) 
#wards_df['Electorate'] = wards_df['Electorate'].astype(int)
id = wards_df['WardID'].tolist()
neighbours = wards_df['NeighbourID'].tolist()
borders = wards_df['CleanLengths'].tolist()
lat = wards_df['Lat'].tolist()
lng = wards_df['Lng'].tolist()
#constituencies = wards_df['InitialConstituency'].tolist()
constituencies = wards_df['Constituency'].tolist()
wards_df['Electorate'] = wards_df.Electorate.apply(lambda x: x.replace(',', ''))
electorate = wards_df['Electorate'].tolist()
area = wards_df['Area'].as_matrix()
plot_area = np.divide(area, 500000)
wards_df['Unionist'] = wards_df['Unionist'].astype(int)
unionist = wards_df['Unionist'].tolist()
wards_df['Nationalist'] = wards_df.Nationalist.apply(lambda x: x.replace(',', ''))
wards_df['Nationalist'] = wards_df['Nationalist'].astype(int)
nationalist = wards_df['Nationalist'].tolist()

constituenciesID = []
for c in constituencies:
    if c == 'Belfast East':
        constituenciesID.append(1)
    elif c == 'Belfast North':
        constituenciesID.append(2)
    elif c == 'Belfast South':
        constituenciesID.append(3)
    elif c == 'Belfast West':
        constituenciesID.append(4)
    elif c == 'Causeway':
       constituenciesID.append(5)
    elif c == 'East Antrim':
        constituenciesID.append(6)
    elif c == 'Fermanagh and South Tyrone':
        constituenciesID.append(7)
    elif c == 'Foyle':
        constituenciesID.append(8)
    elif c == 'Mid Antrim':
        constituenciesID.append(9)
    elif c == 'Mid Down':
        constituenciesID.append(10)
    elif c == 'Mid Ulster':
        constituenciesID.append(11)
    elif c == 'Newry and Armagh':
        constituenciesID.append(12)
    elif c == 'North Down':
        constituenciesID.append(13)
    elif c == 'South Antrim':
        constituenciesID.append(14)
    elif c == 'South Down':
        constituenciesID.append(15)
    elif c == 'Sperrin':
        constituenciesID.append(16)
    elif c == 'Upper Bann':
        constituenciesID.append(17)
    else:
        constituenciesID.append(18)
        print('oops')
        print(c)

#constituenciesID = []
#for c in constituencies:
#    if c == 'Belfast East':
#        constituenciesID.append(1)
#    elif c == 'North Down':
#        constituenciesID.append(13)
#    elif c == 'North Tyrone':
#        constituenciesID.append(16)
#    elif c == 'East Antrim':
#        constituenciesID.append(6)
#    elif c == 'West Antrim':
#        constituenciesID.append(9)
#    elif c == 'Belfast North West':
#        constituenciesID.append(2)
#    elif c == 'Glenshane':
#        constituenciesID.append(11)
#    elif c == 'South Antrim':
#        constituenciesID.append(14)
#    elif c == 'Belfast South West':
#        constituenciesID.append(4)
#    elif c == 'West Down':
#        constituenciesID.append(3)
#    elif c == 'Strangford':
#        constituenciesID.append(10)
#    elif c == 'Dalriada':
#        constituenciesID.append(5)
#    elif c == 'Fermanagh and South Tyrone':
#        constituenciesID.append(7)
#    elif c == 'Upper Bann and Blackwater':
#        constituenciesID.append(17)
#    elif c == 'Foyle':
#        constituenciesID.append(8)
#    elif c == 'Newry and Armagh':
#        constituenciesID.append(12)
#    elif c == 'South Down':
#        constituenciesID.append(15)
#    else:
#        constituenciesID.append(18)
  

#id = ["0","1","2","3"]
#neighbours = [["1","2"], ["0","3"], ["0","3"], ["1","2"]]
#constituencies = [0, 1, 1, 1]
#lat = [0, 0, 0.1, 0.1]
#lng = [0, 0.1, 0, 0.1]

map = gm.Constituency_Map(id, neighbours, constituenciesID, lat, lng, electorate, area, borders, unionist, nationalist)

ideal_electorate = 73974
isoparametric_limit = 70
popultaion_low = 69401
population_high = 78547
confirm = gm.confirmer.Confirmer(popultaion_low, population_high, isoparametric_limit)

n=1
nw = len(id)
nc = len(set(constituenciesID))
c_iso = 0.2
c_pop = 150
beta = 1
met_hast = gm.mhmc.MHMC(n, nw, nc, ideal_electorate, c_pop, c_iso, beta)

current_directory = os.getcwd()
distinct_directory = os.path.join(current_directory, "constituency_maps_distinct")

met_hast.run_distinct(map, n, 1, 0)

#map = confirm.read_constituency_map_from_file(os.path.join(distinct_directory, "constituency_map 40000.txt"))
#met_hast.run_distinct_linear(map, 60000, 0, 1, 40000)

#map = confirm.read_constituency_map_from_file(os.path.join(distinct_directory, "constituency_map 100000.txt"))
#met_hast.run_distinct(map, 20000, 1, 100001)

#confirm.validise_map_from_file(distinct_directory)