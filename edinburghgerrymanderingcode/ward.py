from .ward_data import Ward_Data

class Ward:
	#def __init__(self, id):
	#	self.neighbours = []
	#	self.id = id
	#	self.constituency = -1
	#	return
		
	def __init__(self, id, lat, lng, electorate, area, unionist, nationalist):
		self.ward_data = Ward_Data(id, lat, lng, electorate, area, unionist, nationalist)
		self.neighbours = []
		self.neighbours_border = {}
		self.finished_init = False

	#getters
	#----------------------------------------------------------------------------------------------------
	def get_neighbours(self):
		return self.neighbours

	def get_id(self):
		return self.ward_data.get_id()

	def get_lat(self):
		return self.ward_data.get_lat()

	def get_lng(self):
		return self.ward_data.get_lng()

	def get_electorate(self):
		return self.ward_data.get_electorate()

	def get_constituency(self):
		return self.constituency

	def get_population(self):
		return self.ward_data.get_electorate()

	def get_area(self):
		return self.ward_data.get_area()

	def get_border(self, neighbour):
		return self.neighbours_border[neighbour]

	def get_unionist(self):
		return self.ward_data.get_unionist()

	def get_nationalist(self):
		return self.ward_data.get_nationalist()

	#setters
	#----------------------------------------------------------------------------------------------------
	def set_constituency(self, constituency):
		self.constituency = constituency

	#restrict the changing of any graphing changes
	def finish_init(self):
		self.finished_init = True

	#Generating Functions
	#----------------------------------------------------------------------------------------------------
	#gives this ward a new set of neighbours
	def add_neighbours(self, neighbours):
		if not self.finish_init:
			for n in neighbours:
				if n not in self.neighbours:
					self.neighbours.append(n)
		else:
			print("cannot assign neighbours, ward has finished initialising")

	#gives this ward a new neighbour	
	def add_neighbour(self, neighbour):
		if not self.finished_init:
			if neighbour not in self.neighbours:
				self.neighbours.append(neighbour)
		else:
			print("cannot assign neighbours, ward has finished initialising")

	#stores the length of the border between this ward and one of its neighbours
	def add_border(self, neighbour, border):
		#if not self.finish_init:
		self.neighbours_border[neighbour] = border
		#else:
		#	print("cannot assign borders, ward has finished initialising")

	#adds a neighbour and a border between it at the same time
	def add_neighbour_new(self, neighbour, border):
		self.add_neighbour(neighbour)
		self.add_border(neighbour, border)