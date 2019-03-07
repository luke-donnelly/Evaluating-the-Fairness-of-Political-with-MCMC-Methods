#The code in this script is used to generate a sample of maps.
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




wards_df = pd.read_csv("WardsWithDataVotes.csv")
area = wards_df['Area'].as_matrix()
plot_area = np.divide(area, 500000)
#
#
current_directory = os.getcwd()
maps_directory = os.path.join(current_directory, "constituency_maps_valid_total_4")
new_map_directory = os.path.join(current_directory, "constituency_maps_distinct")
graphs_directory = os.path.join(current_directory, "analytical_data")

analyser = gm.Election_Results(new_map_directory)
#analyser.read_eight_histogram_of_n(graphs_directory, plot_area)
#map = analyser.read_constituency_map_from_file(os.path.join(new_map_directory, "constituency_map_base.txt"))
#plt.scatter(map.display_graph()[1], map.display_graph()[0], c=map.display_graph()[2], cmap = 'nipy_spectral', s = plot_area)
#plt.xlabel('Longitude', fontsize=14)
#plt.ylabel('Latitude', fontsize=14)
#plt.savefig("old prop map")
#plt.cla()
#analyser.examples_histogram_of_n()
#analyser.display_examples_histogram_of_n(graphs_directory, plot_area)
#map = analyser.run_election_from_file(os.path.join(maps_directory, "constituency_map 0.txt"))
#graph_maps = []
#graph_maps.append(map.display_graph())


#n = 5
#fig, ax = plt.subplots()
#ax.scatter(graph_maps[0][1], graph_maps[0][0], c=graph_maps[0][2], cmap = 'nipy_spectral', s = plot_area)
#def update(i):
#    map = analyser.run_election_from_file(os.path.join(maps_directory, "constituency_map " + str(i) + ".txt"))
#    return ax.scatter(map.display_graph()[0][1], map.display_graph()[0][0], c=map.display_graph()[0][2], cmap = 'nipy_spectral', s = plot_area)
#
#anim = FuncAnimation(fig, update, frames=n, interval=20, repeat_delay = 2000)
#plt.show()


#analyser.histogram_of_n()
analyser.animate(plot_area)
#analyser.box_plot()
#analyser.isoparametric_score_convergence()

#current_directory = os.getcwd()
#analyser.display_box(graphs_directory, maps_directory, new_map_directory)

#analyser.evp()
#analyser.display_evp(graphs_directory, maps_directory, new_map_directory)
