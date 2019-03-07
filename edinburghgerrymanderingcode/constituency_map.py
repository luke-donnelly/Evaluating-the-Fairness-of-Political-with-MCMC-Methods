import numpy as np

# import ward from file
from .ward import Ward
from .constituency import Constituency
#import edinburghgerrymanderingcode as gm
#import ward


class Constituency_Map:

	#Input
	#id_list 			- a list of each id for each ward
	#neighbours_list 	- a list of each list of neighbours id for a eacch ward
	#constituencies		- a list of each constituencies id for each ward
	#lats				- a list of each latitute for each ward
	#lngs				- a list of each longitude for each ward
	#electorate			- ***
	#
	#Fields
	#ward_id			- a list of id for each ward stored
	#ward_dict			- a dict of key ward id and value corresponding ward
	#constituencies_id  - a list of id for each constituency stored
	#constituencies_dict- a dict of key constituency id and value corresponding constituency (class not value)
	def __init__(self, id_list, neighbours_list, constituencies, lats, lngs, electorate, area, borders, unionist, nationalist):
		self.ward_id = id_list
		self.ward_dict = {}
		self.constituencies_id  = []
		self.constituencies_dict = {}

		for i in range(len(id_list)):
			self.ward_dict[id_list[i]] = Ward(id_list[i], lats[i], lngs[i], electorate[i], area[i], unionist[i], nationalist[i])

		for i in range(len(id_list)):
			if self.ward_dict[id_list[i]].get_id() != 'out':
				for j in range(len(neighbours_list[i])):
					self.ward_dict[id_list[i]].add_neighbour(self.ward_dict[neighbours_list[i][j]])	
					self.ward_dict[id_list[i]].add_border(neighbours_list[i][j], borders[i][j])

			self.ward_dict[id_list[i]].set_constituency(constituencies[i])
			self.ward_dict[id_list[i]].finish_init()

		self.ideal_population = 74769
		for c in constituencies:
			if c not in self.constituencies_id:
				self.constituencies_id.append(c)
				self.constituencies_dict[c] = Constituency(c, self.ideal_population)

		for c in self.constituencies_id:
			for w in self.ward_id:
				if self.ward_dict[w].get_constituency() == c:
					self.constituencies_dict[c].initialise_ward(self.ward_dict[w])
			self.constituencies_dict[c].calculate_isoparametric_score()
			self.constituencies_dict[c].calculate_population_score()
		
	#getters
	#----------------------------------------------------------------------------------------------------
	def get_constituencies(self):
		return self.constituencies_dict

	def get_id_list(self):
		return self.ward_id

	def get_neighbours(self, ward):
		return self.get_ward(ward).get_neighbours()

	def get_ward(self, ward):
		if isinstance(ward, str):
			return self.ward_dict[ward]
		else:
			return ward

	def get_wards(self):
		return self.ward_dict
	
	#private functionality
	#----------------------------------------------------------------------------------------------------
	def on_boundary(self, ward):
		return self.constituencies_dict[self.get_ward(ward).get_constituency()].on_boundary(self.get_ward(ward))

	#public functionality
	#---------------------------------------------------------------------------------------------------
	#creates a list of wards that have a neighbour that is in a different constituency
	def wards_on_boundary(self):
		boundary = []
		for id_to_check in self.get_id_list():
			if self.on_boundary(id_to_check) and id_to_check not in boundary:
				boundary.append(self.get_ward(id_to_check))
		return boundary
	

	#graphing functionality
	#---------------------------------------------------------------------------------------------------
	#proof of concept, no longer in use
	def display_array(self, n, m):
		array_to_display = [[0 for k in range(m)] for l in range(n)]
		for i in range(0,n):
			for j in range(0,m):
				array_to_display[i][j] = (self.get_ward(str(i*n + j))).get_constituency()
		return array_to_display

	#gives the information needed to display a map graphicly
	def display_graph(self):
		lats = []
		lngs = []
		c = []
		for id in self.ward_id:
			c.append(self.get_ward(id).get_constituency())
			lats.append(self.get_ward(id).get_lat())
			lngs.append(self.get_ward(id).get_lng())
		return lats, lngs, c

	#Analysing functionality
	#---------------------------------------------------------------------------------
	#calculates the total population score of this map and returns it
	def get_population_score(self):
		population_score = float(0)
		for constituency_id in self.constituencies_id:
			if constituency_id != 18:
				population_score = population_score + self.constituencies_dict[constituency_id].get_population_score()

		population_score = population_score**(0.5)
		return population_score

	#calculates the total isoparametric score of this map and returns it
	def get_isoparametric_score(self):
		score = 0
		for constituency_id in self.constituencies_id:
			if constituency_id != 18:
				score = score + self.constituencies_dict[constituency_id].get_isoparametric_score()
		return score
		
	#returnes the population of each constituency in the map
	def get_populations(self):
		populations = []
		for constituency_id in self.constituencies_id:
			if constituency_id != 18:
				populations.append(self.constituencies_dict[constituency_id].get_total_pop())

		return populations

	#gives the ispparametric score of each constituency in the map
	def get_all_isoparametric_scores(self):
		isoparametric_scores = []
		for constituency_id in self.constituencies_id:
			if constituency_id != 18:
				self.constituencies_dict[constituency_id].calculate_isoparametric_score()
				isoparametric_scores.append(self.constituencies_dict[constituency_id].get_isoparametric_score())

		return isoparametric_scores

	#runs an election in each constituency
	def run_election(self):
		for i in self.constituencies_id:
			self.constituencies_dict[i].run_election()

	#gives the total number of nationalist constituencys
	def get_nationalist_seats(self):
		nationalist_seats = 0
		for i in self.constituencies_id:
			if self.constituencies_dict[i].get_results()[2] == 'N':
				nationalist_seats += 1
		return nationalist_seats

	#gives the fraction of each constituency which voted nationalist
	def get_nationalist_vote_fraction(self):
		nationalist_vote_fraction_per_district = []
		for i in self.constituencies_id:
			nationalist_vote_fraction_per_district.append(self.constituencies_dict[i].get_nationalist_vote_fraction())

		return nationalist_vote_fraction_per_district


	#Gives the nationalist effective vote percentage
	def get_n_evp(self):
		n_ev = 0
		total_pop = 0
		for i in self.constituencies_id:
			n_ev += self.constituencies_dict[i].get_n_ev()
			total_pop += self.constituencies_dict[i].get_total_pop()
		return float(n_ev)/float(total_pop)

	#Gives the unionist effective vote percentage
	def get_u_evp(self):
		u_ev = 0
		total_pop = 0
		for i in self.constituencies_id:
			u_ev += self.constituencies_dict[i].get_u_ev()
			total_pop += self.constituencies_dict[i].get_total_pop()

		return float(u_ev)/float(total_pop)


	#Gives the number of nationalist wasted votes
	def get_wasted_votes_n(self):
		wasted_votes_n = 0
		for i in self.constituencies_id:
			wasted_votes_n += self.constituencies_dict[i].get_wasted_votes_n()

		return wasted_votes_n

	#generating functionality
	#---------------------------------------------------------------------
	#reassignes every ward to a new constituency, then recalculates the associated scores
	def reassign_constituencies(self, ids, constituencies):

		for c in self.constituencies_id:
			self.constituencies_dict[c].clear()

		for i in range(len(ids)):
			self.constituencies_dict[constituencies[i]].initialise_ward(self.ward_dict[ids[i]])

		for c in self.constituencies_id:		
			self.constituencies_dict[c].calculate_isoparametric_score()
			self.constituencies_dict[c].calculate_population_score()

	def check_contiguous(self):
		for c in self.constituencies_id:
			con = self.constituencies_dict[c]

			if len(con.get_wards()) == 0:
				return True

			blob = [con.get_wards()[0].get_id()]
			count_previous = 0
			count_next = len(blob)
			while count_previous < count_next:
				ward = self.ward_dict[blob[count_previous]]
				for neighbour in ward.get_neighbours():
					if neighbour.get_constituency() == c and not (neighbour.get_id() in blob):
						blob.append(neighbour.get_id())
						count_next = count_next + 1
				count_previous = count_previous + 1

			if (len(blob) != len(con.get_wards())):
				return False
		return True


	#storage functionality
	#----------------------------------------------------------------------
	#creates an exact copy of the current map without any shared references
	def deep_copy(self):
		id_list = self.ward_id
		neighbours_list = []
		constituencies = []
		lats = []
		lngs = []
		electorate = []
		area = []
		borders_list = []
		unionist = []
		nationalist = []
		for i in id_list:
			current_neighbours = []
			current_borders = []
			for neighbour in self.ward_dict[i].get_neighbours():
				current_neighbours.append(neighbour.get_id())
				current_borders.append(self.ward_dict[i].get_border(neighbour.get_id()))

			neighbours_list.append(current_neighbours)
			borders_list.append(current_borders)
			constituencies.append(self.ward_dict[i].get_constituency())
			lats.append(self.ward_dict[i].get_lat())
			lngs.append(self.ward_dict[i].get_lng())
			electorate.append(self.ward_dict[i].get_electorate())
			area.append(self.ward_dict[i].get_area())
			unionist.append(self.ward_dict[i].get_unionist())
			nationalist.append(self.ward_dict[i].get_nationalist())
			
		return Constituency_Map(id_list, neighbours_list, constituencies, lats, lngs, electorate, area, borders_list, unionist, nationalist)

	#give the Constituency_Map in a form that it can be read from file
	def contents_to_string(self):
		id_list = self.ward_id
		neighbours_list = []
		constituencies = []
		lats = []
		lngs = []
		electorate = []
		area = []
		borders_list = []
		unionist = []
		nationalist = []
		for i in id_list:
			current_neighbours = []
			current_borders = []
			for neighbour in self.ward_dict[i].get_neighbours():
				current_neighbours.append(neighbour.get_id())
				current_borders.append(self.ward_dict[i].get_border(neighbour.get_id()))

			current_neighbours_string = ",".join(str(e) for e in current_neighbours)
			current_borders_string = ",".join(str(e) for e in current_borders)

			neighbours_list.append(current_neighbours_string)
			borders_list.append(current_borders_string)

			constituencies.append(str(self.ward_dict[i].get_constituency()))
			lats.append(str(self.ward_dict[i].get_lat()))
			lngs.append(str(self.ward_dict[i].get_lng()))
			electorate.append(str(self.ward_dict[i].get_electorate()))
			area.append(str(self.ward_dict[i].get_area()))
			unionist.append(str(self.ward_dict[i].get_unionist()))
			nationalist.append(str(self.ward_dict[i].get_nationalist()))

		id_list_string = ",".join(str(e) for e in id_list)
		neighbours_list_string = ";".join(str(e) for e in neighbours_list)
		constituencies_string = ",".join(str(e) for e in constituencies)
		lats_string = ",".join(str(e) for e in lats)
		lngs_string = ",".join(str(e) for e in lngs)
		electorate_string = ",".join(str(e) for e in electorate)
		area_string = ",".join(str(e) for e in area)
		borders_list_string = ";".join(str(e) for e in borders_list)
		unionist_string = ",".join(str(e) for e in unionist)
		nationalist_string = ",".join(str(e) for e in nationalist)
		return (id_list_string + "\n" + neighbours_list_string + "\n" + constituencies_string + "\n" + lats_string + "\n" + lngs_string + "\n" + electorate_string + "\n" + area_string + "\n" + borders_list_string + "\n" + unionist_string + "\n" + nationalist_string)
		
	#gives a string which can reasign all the wards of a map to new constituencies
	def constituency_to_string(self):
		id_list = self.ward_id
		constituencies = []
		for i in id_list:
			constituencies.append(str(self.ward_dict[i].get_constituency()))

		id_list_string = ",".join(str(e) for e in id_list)
		constituencies_string = ",".join(str(e) for e in constituencies)
		return (id_list_string + "\n" + constituencies_string)