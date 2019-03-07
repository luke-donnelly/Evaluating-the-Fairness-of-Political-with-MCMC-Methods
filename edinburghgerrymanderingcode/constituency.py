from .ward import  Ward

class Constituency:
    def __init__(self, id, ideal_population):
        self.wards_of_constituency = []
        self.constituency_id = id
        self.ideal_population = ideal_population
        self.isoparametric_score = 0
        self.population_score = float(0)
        self.results = []

    #setters
    #------------------------------------------------------------------------
    #sets a ward to this constituency without changing score
    def initialise_ward(self, ward):
        if isinstance(ward, str):
            raise Exception("attempted to assign a string to a constituency")
        self.wards_of_constituency.append(ward)
        ward.set_constituency(self.constituency_id)

    #sets a ward to this constituency then changes score
    def assign_ward(self, ward):
        if isinstance(ward, str):
            raise Exception("attempted to assign a string to a constituency")
        self.wards_of_constituency.append(ward)
        ward.set_constituency(self.constituency_id)
        self.calculate_population_score()
        self.calculate_isoparametric_score()

    #getters
    #----------------------------------------------------------------------
    def get_total_pop(self):
        pop = 0
        for w in self.wards_of_constituency:
            pop += int(w.get_population())

        return pop

    def get_isoparametric_score(self):
        return self.isoparametric_score

    def get_population_score(self):
        return self.population_score

    def get_id(self):
        return self.constituency_id
        
    def get_results(self):
        return self.results

    def get_wasted_votes_n(self):
        return abs(self.nationalist - self.unionist)

    def get_wards(self):
        return self.wards_of_constituency

    #calculating_atributes
    #--------------------------------------------------------------------
    #calculates the length of edges of wards in this Constituency
    #adjacent to a different Constituency
    def calculate_boundary(self):
        
        boundary = 0
        for ward in self.wards_of_constituency:
            for neighbour in ward.get_neighbours():
                if neighbour.get_constituency() != ward.get_constituency() and neighbour.get_id() != "out":
                    boundary += float(ward.get_border(neighbour.get_id()))

        return boundary

    #calculates the sun of area of all wards in this Constituency
    def calculate_area(self):
        area = 0
        for ward in self.wards_of_constituency:
            area += ward.get_area()
        return area

    #calculates and stores the current isoparametric score to be used later
    def calculate_isoparametric_score(self):
        if self.calculate_area() != 0:
            self.isoparametric_score = (self.calculate_boundary()**2/self.calculate_area())
        else:
            self.isoparametric_score = 0

    #calculates and stores the current population score to be used later
    def calculate_population_score(self):
        self.population_score = float(0)
        self.population_score += self.get_total_pop()
        self.population_score = self.population_score/self.ideal_population
        self.population_score = (self.population_score - 1)**2

    #Generating
    #--------------------------------------------------------------------------------------------------
    #checks if a ward has a neighbour of a different constituency
    def on_boundary(self, ward):
	    neighbours_to_check = ward.get_neighbours()
	    for neighbour in neighbours_to_check:
		    if neighbour.get_constituency() != ward.get_constituency() and neighbour.get_id() != "out":
			    return True
	    return False

    #deletes a ward from the list, then updates the scores
    def remove_ward(self, ward):
        self.wards_of_constituency.remove(ward)
        self.calculate_population_score()
        self.calculate_isoparametric_score()

    #deletes a ward from the list without updating scores
    def deinitialise_ward(self, ward):
        self.wards_of_constituency.remove(ward)

    def clear(self):
        self.wards_of_constituency = []
    
    #analysis
    #-------------------------------------------------------------------------------------
    #calculates which party has the majority vote
    def run_election(self):
        self.unionist = 0
        self.nationalist = 0

        for ward in self.wards_of_constituency:
            self.unionist += int(ward.get_unionist())
            self.nationalist += int(ward.get_nationalist())

        if self.unionist > self.nationalist:
            self.results = [self.unionist, self.nationalist, 'U']
        elif self.nationalist > self.unionist:
            self.results = [self.unionist, self.nationalist, 'N']
        else:
            self.results = [self.unionist, self.nationalist, 'D']

    def get_nationalist_vote_fraction(self):
        if self.nationalist + self.unionist == 0:
            return 0

        return (float(self.nationalist)/float(self.nationalist + self.unionist))

    #returns the number of effective nationalist votes
    def get_n_ev(self):
        n = 0
        u = 0
        for w in self.wards_of_constituency:
            n += int(w.get_nationalist())
            u += int(w.get_unionist())
        if n > u:
            return n - u
        else:
            return n

    #returnes the number of effective unionist votes
    def get_u_ev(self):
        n = 0
        u = 0
        for w in self.wards_of_constituency:
            n += int(w.get_nationalist())
            u += int(w.get_unionist())
        if n < u:
            return u - n
        else:
            return u