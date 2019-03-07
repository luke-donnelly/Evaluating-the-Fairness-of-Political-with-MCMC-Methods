import copy
import random as r
import numpy as np
import gc
import time
import os,os.path
import shutil

#import ward	
#import constituency_map

class MHMC:
	#many of these are not used
	def __init__(self, num_iterations, num_wards, num_constituencies, ideal_electorate, c_pop, c_iso, beta):
		self.n = num_iterations
		self.num_wards = num_wards
		self.num_constituencies = num_constituencies
		self.ideal_electorate = ideal_electorate
		self.c_pop = c_pop
		self.c_iso = c_iso
		self.beta = beta
	#private functionality
	#----------------------------------------------------------------------------------------------------
	def energy(self, x):
		p_score = x.get_population_score()
		i_score = x.get_isoparametric_score()
		score = self.c_pop * p_score
		score = score + self.c_iso * i_score
		return score

	def f(self, x, y):
		y = np.exp(-self.beta*(self.energy(x) - self.energy(y)))
		return y

	#returnes a valid random neighbour to a given ward
	def choose_neighbour(self, border_ward):
		neighbours_constituency = []
		for neighbour in border_ward.get_neighbours():
			if (neighbour.get_constituency() != 18):
				neighbours_constituency.append(neighbour.get_constituency())

		dif_constituency = False
		while not dif_constituency:
			i = r.randint(0, len(neighbours_constituency)-1)
			prop_constituency = neighbours_constituency[i]
			if prop_constituency != border_ward.get_constituency():
				dif_constituency = True
			
			del neighbours_constituency[i]
			
		return prop_constituency

	#swaps the constituency of a ward, updating all associated scores
	def swap(self, ward, old_constituency, new_constituency):
		ward.set_constituency(new_constituency.get_id())
		old_constituency.remove_ward(ward)
		new_constituency.assign_ward(ward)

	#public functionality
	#----------------------------------------------------------------------------------------------------
	#MHMC algorithm, running untill N different steps have occured and storing all valid maps to file
	def run_distinct(self, x0, N, beta, count):
		name_count = count
		self.beta = beta
		previous = x0.deep_copy()
		print("done")
		step = 0

		current_directory = os.getcwd()
		complete_directory = os.path.join(current_directory, "constituency_maps_distinct")
		if not os.path.exists(complete_directory):
   			os.makedirs(complete_directory)

		name = "constituency_map_base.txt"

		contents = previous.contents_to_string()
		print("writing map")
		with open(os.path.join(complete_directory, name), 'w+') as f:
			f.write(contents)
			f.seek(0)
			f.close()
		print("map wrote")
		t0 = time.time()
		while step < N:

			x = previous.deep_copy()
			boundary = x.wards_on_boundary()

			prop_swap_ward = boundary[r.randint(0,len(boundary)-1)]
			while prop_swap_ward.get_id() == "out":
				prop_swap_ward = boundary[r.randint(0,len(boundary)-1)]


			new_constituency = x.get_constituencies()[self.choose_neighbour(prop_swap_ward)]
			old_constituency = x.get_constituencies()[prop_swap_ward.get_constituency()]
			self.swap(prop_swap_ward, old_constituency, new_constituency)
			ar = self.f(x, previous)

			contiguous = x.check_contiguous()

			if ar >= 1 and contiguous:
				step = step + 1
				name = "constituency_map " + str(name_count) + ".txt"
				name_count = name_count+1
				contents = previous.constituency_to_string()
				with open(os.path.join(complete_directory, name), 'w+') as f:
					f.write(contents)
					f.seek(0)
					f.close()

				previous = x

			elif r.uniform(0,1)<ar and contiguous:
				step = step + 1
				name = "constituency_map " + str(name_count) + ".txt"
				name_count = name_count+1
				contents = previous.constituency_to_string()
				with open(os.path.join(complete_directory, name), 'w+') as f:
					f.write(contents)
					f.seek(0)
					f.close()

				previous = x
			gc.collect()
		t1 = time.time()
		print(t1-t0)