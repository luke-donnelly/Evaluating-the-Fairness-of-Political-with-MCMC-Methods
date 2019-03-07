from .constituency_map import Constituency_Map
import os,os.path
import shutil

class Confirmer:
    def __init__(self, population_low, population_high, isoparametric_target):
        self.population_low = population_low
        self.isoparametric_target = isoparametric_target
        self.population_high = population_high

    #examines the given map to see if its total population lies in the accepted range
    def check_population(self, con_map):
        check = True
        populations = con_map.get_populations()
        for population in populations:
            check = check and (self.population_low <= population) and (population <= self.population_high)
            if not check:
                break
        return check

    #checks the given map to see if its total isoparametric score lies in the accepted limit
    def check_isoparametric(self, con_map):
        check = True
        for isoparametric_score in con_map.get_all_isoparametric_scores():
            check = check and  (isoparametric_score <= self.isoparametric_target)
            if not check:
                break
        return check

    #returns a list of maps with valid population from a list of maps
    def validise_population(self, con_maps):
        valid_maps = []
        for con_map in con_maps:
            if self.check_population(con_map):
                valid_maps.append(con_map)

        return valid_maps

    #returns a list of maps with valid isoparametric score from a list of maps
    def validise_isoparametric(self, con_maps):
        valid_maps = []
        for con_map in con_maps:
            if self.check_isoparametric(con_map):
                valid_maps.append(con_map)

        return valid_maps
    #returns a list of valid maps from a list of maps
    def validise_maps(self, con_maps):
        valid_maps = []
        for con_map in con_maps:
            if self.check_population(con_map) and self.check_isoparametric(con_map):
                valid_maps.append(con_map)

        return valid_maps

    def read_constituency_map_from_file(self, con_map):
        f = open(con_map, "r")
        fl = f.readlines()
        id = fl[0].rstrip().split(",") 
        neighbours = [x.split(",") for x in fl[1].rstrip().split(";")]
        constituenciesID = fl[2].rstrip().split(",")
        constituenciesID = [int(x) for x in constituenciesID]
        lat = fl[3].rstrip().split(",") 
        lat = [float(x) for x in lat]
        lng = fl[4].rstrip().split(",") 
        lng = [float(x) for x in lng]
        electorate = fl[5].rstrip().split(",") 
        electorate = [int(x) for x in electorate]
        area = fl[6].rstrip().split(",") 
        area = [float(x) for x in area]
        borders = [x.split(",") for x in fl[7].rstrip().split(";")]
        unionist = fl[8].rstrip().split(",") 
        nationalist = fl[9].rstrip().split(",") 
        c = Constituency_Map(id, neighbours, constituenciesID, lat, lng, electorate, area, borders,unionist, nationalist)
        return c

    def read_constituency_from_file(self, con_map):
        f = open(con_map, "r")
        fl = f.readlines()
        id = fl[0].rstrip().split(",")
        constituenciesID = fl[1].rstrip().split(",")
        constituenciesID = [int(x) for x in constituenciesID]
        return id, constituenciesID

    def validise_population_from_file(self, con_maps_location):
        current_directory = os.getcwd()
        write_directory = os.path.join(current_directory, "constituency_maps_valid_pop")
       
        if os.path.exists(write_directory):
            shutil.rmtree(write_directory)
        if not os.path.exists(write_directory):
   	    	os.makedirs(write_directory)

        constituency_map_base = self.read_constituency_map_from_file(os.path.join(con_maps_location, "constituency_map_base.txt"))
        f = open(os.path.join(write_directory, "constituency_map_base.txt"), "w+")
        contents = constituency_map_base.contents_to_string()
        f.write(contents)
        f.close

        for i in range (len([name for name in os.listdir(con_maps_location) if os.path.isfile(os.path.join(con_maps_location, name))]) - 1):
            file_current = os.path.join(con_maps_location, "constituency_map " + str(i) +".txt")
            ids, constituencies = self.read_constituency_from_file(file_current)
            constituency_map_current = constituency_map_base.deep_copy()
            constituency_map_current.reassign_constituencies(ids, constituencies)
            if self.check_population(constituency_map_current):
                count = len([name for name in os.listdir(write_directory) if os.path.isfile(os.path.join(write_directory, name))])
                f = open(os.path.join(write_directory, "constituency_map " + str(count)) +".txt", "w+")
                contents = constituency_map_current.constituency_to_string()
                f.write(contents)
                f.close

    def validise_isoparametric_from_file(self, con_maps_location):
        current_directory = os.getcwd()
        write_directory = os.path.join(current_directory, "constituency_maps_valid_iso")
       
        if os.path.exists(write_directory):
            shutil.rmtree(write_directory)
        if not os.path.exists(write_directory):
   	    	os.makedirs(write_directory)

        constituency_map_base = self.read_constituency_map_from_file(os.path.join(con_maps_location, "constituency_map_base.txt"))
        f = open(os.path.join(write_directory, "constituency_map_base.txt"), "w+")
        contents = constituency_map_base.contents_to_string()
        f.write(contents)
        f.close

        for i in range (len([name for name in os.listdir(con_maps_location) if os.path.isfile(os.path.join(con_maps_location, name))]) - 1):
            file_current = os.path.join(con_maps_location, "constituency_map " + str(i) +".txt")
            ids, constituencies = self.read_constituency_from_file(file_current)
            constituency_map_current = constituency_map_base.deep_copy()
            constituency_map_current.reassign_constituencies(ids, constituencies)
            if self.check_isoparametric(constituency_map_current) and constituency_map_current.check_contiguous():
                count = len([name for name in os.listdir(write_directory) if os.path.isfile(os.path.join(write_directory, name))])
                f = open(os.path.join(write_directory, "constituency_map " + str(count)) +".txt", "w+")
                contents = constituency_map_current.constituency_to_string()
                f.write(contents)
                f.close

    def validise_map_from_file(self, con_maps_location):
        current_directory = os.getcwd()
        write_directory = os.path.join(current_directory, "constituency_maps_valid_total")
       
        if not os.path.exists(write_directory):
   	    	os.makedirs(write_directory)

        constituency_map_base = self.read_constituency_map_from_file(os.path.join(con_maps_location, "constituency_map_base.txt"))
        f = open(os.path.join(write_directory, "constituency_map_base.txt"), "w+")
        contents = constituency_map_base.contents_to_string()
        f.write(contents)
        f.close

        #check for population and isoparametric
        for i in range (len([name for name in os.listdir(con_maps_location) if os.path.isfile(os.path.join(con_maps_location, name))]) - 1):
            file_current = os.path.join(con_maps_location, "constituency_map " + str(i) +".txt")
            ids, constituencies = self.read_constituency_from_file(file_current)
            constituency_map_current = constituency_map_base.deep_copy()
            constituency_map_current.reassign_constituencies(ids, constituencies)
            if self.check_isoparametric(constituency_map_current) and self.check_population(constituency_map_current) and constituency_map_current.check_contiguous():
                count = len([name for name in os.listdir(write_directory) if os.path.isfile(os.path.join(write_directory, name))]) -1
                f = open(os.path.join(write_directory, "constituency_map " + str(count)) +".txt", "w+")
                contents = constituency_map_current.constituency_to_string()
                f.write(contents)
                f.close

        #check for distinct
        unique_directory = os.path.join(current_directory, "constituency_maps_valid_unique")

        if not os.path.exists(unique_directory):
   	    	os.makedirs(unique_directory)

        f = open(os.path.join(unique_directory, "constituency_map_base.txt"), "w+")
        contents = constituency_map_base.contents_to_string()
        f.write(contents)
        f.close

        for i in range (len([name for name in os.listdir(write_directory) if os.path.isfile(os.path.join(write_directory, name))]) - 1):
            f = open(os.path.join(write_directory, "constituency_map " + str(i)) +".txt", "r")
            old = f.read()
            f.close

            unique = True
            max = len([name for name in os.listdir(unique_directory) if os.path.isfile(os.path.join(unique_directory, name))]) - 1
            for j in range (max):
                f = open(os.path.join(unique_directory, "constituency_map " + str(j)) +".txt", "r")
                new = f.readlines()
                f.close

                if (old == new):
                    unique = False
                    break

            if(unique):
                f = open(os.path.join(unique_directory, "constituency_map " + str(max)) +".txt", "w+")
                f.write(old)
                f.close

        
            