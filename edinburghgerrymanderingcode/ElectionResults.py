import numpy as np
import matplotlib.pyplot as plt
import edinburghgerrymanderingcode as gm
import os,os.path
import shutil
from .constituency_map import Constituency_Map
from matplotlib.animation import FuncAnimation

class Election_Results:

    def __init__(self, maps_location):
        self.maps_location = maps_location
        self.map_count = len([name for name in os.listdir(self.maps_location) if os.path.isfile(os.path.join(self.maps_location, name))]) - 1
        self.base_map = self.read_constituency_map_from_file(os.path.join(self.maps_location, "constituency_map_base.txt"))

    #Calculating functions
    #===================================================================
    #Stores data for a box plot showing the efective vote percentage of both unionists and nationalists
    def evp(self):
        n_evp = []
        u_evp = []
        for i in range(self.map_count - 1):
            map = self.run_election_from_file(os.path.join(self.maps_location, "constituency_map " + str(i) +".txt"))
            map.run_election()
            n_evp.append(map.get_n_evp())
            u_evp.append(map.get_u_evp())

        n_evp_str = ','.join([str(e) for e in n_evp])
        u_evp_str = ','.join([str(e) for e in u_evp])

        data = n_evp_str + "\n" + u_evp_str

        current_directory = os.getcwd()
        complete_directory = os.path.join(current_directory, "analytical_data")
        if not os.path.exists(complete_directory):
            os.makedirs(complete_directory)
            
        f = open(os.path.join(complete_directory, "evp_data.txt"), "w+")
        f.write(data)
        f.close

        plt.plot(n_evp)
        plt.show()

        plt.plot(u_evp)
        plt.show()
    
    #stores a list of 10 maps for each of the 6 - 10 constituencys won by nationalists. Should be a script
    def examples_histogram_of_n(self):
        maps6 = []
        maps7 = []
        maps8 = []
        maps9 = []
        maps10 = []
        for i in range(self.map_count - 1):
            map = self.run_election_from_file(os.path.join(self.maps_location, "constituency_map " + str(i) +".txt"))
            map.run_election()
            if(len(maps6) < 10 and map.get_nationalist_seats() == 6):
                maps6.append(map.deep_copy())
            elif(len(maps7) < 10 and map.get_nationalist_seats() == 7):
                maps7.append(map.deep_copy())
            elif(len(maps8) < 10 and map.get_nationalist_seats() == 8):
                maps8.append(map.deep_copy())
            elif(len(maps9) < 10 and map.get_nationalist_seats() == 9):
                maps9.append(map.deep_copy())
            elif(len(maps10) < 10 and map.get_nationalist_seats() == 10):
                maps10.append(map.deep_copy())

            if(len(maps6) == 10 and len(maps7) == 10 and len(maps8) == 10 and len(maps9) == 10 and len(maps10) == 10):
                break

        current_directory = os.getcwd()
        complete_directory = os.path.join(current_directory, "analytical_data")
        if not os.path.exists(complete_directory):
            os.makedirs(complete_directory)
            
        for i in range(len(maps6)):
            write_str = maps6[i].contents_to_string()
            f = open(os.path.join(complete_directory, "map6 " + str(i) + ".txt"), "w+")
            f.write(write_str)
            f.close
        for i in range(len(maps7)):
            write_str = maps7[i].contents_to_string()
            f = open(os.path.join(complete_directory, "map7 " + str(i) + ".txt"), "w+")
            f.write(write_str)
            f.close
        for i in range(len(maps8)):
            write_str = maps8[i].contents_to_string()
            f = open(os.path.join(complete_directory, "map8 " + str(i) + ".txt"), "w+")
            f.write(write_str)
            f.close
        for i in range(len(maps9)):
            write_str = maps9[i].contents_to_string()
            f = open(os.path.join(complete_directory, "map9 " + str(i) + ".txt"), "w+")
            f.write(write_str)
            f.close
        for i in range(len(maps10)):
            write_str = maps10[i].contents_to_string()
            f = open(os.path.join(complete_directory, "map10 " + str(i) + ".txt"), "w+")
            f.write(write_str)
            f.close

    #Stores the data needed to show a histogram of how many maps had a given number of nationalist seats
    def histogram_of_n(self):
        num = []
        for i in range(self.map_count - 1):
            map = self.run_election_from_file(os.path.join(self.maps_location, "constituency_map " + str(i) +".txt"))
            map.run_election()
            num.append(map.get_nationalist_seats())

        current_directory = os.getcwd()
        complete_directory = os.path.join(current_directory, "analytical_data")
        if not os.path.exists(complete_directory):
            os.makedirs(complete_directory)
            
        num_str = ",".join([str(e) for e in num])
        f = open(os.path.join(complete_directory, "histogram_data.txt"), "w+")
        f.write(num_str)
        f.close
        
        plt.hist(num, bins=17)
        plt.show()

    #gives 10 spaced examples of maps with 8 nationalist seats. Should be a script
    def eight_histogram_of_n(self):
        maps8 = []
        map_index = []
        for i in range(10):
            for j in range(int(i*(self.map_count - 1)/10), int((i+1)*(self.map_count - 1)/10)):
                map = self.run_election_from_file(os.path.join(self.maps_location, "constituency_map " + str(j) +".txt"))
                map.run_election()
                if (map.get_nationalist_seats() == 8):
                    maps8.append(map.deep_copy())
                    map_index.append(j)
                    break

        current_directory = os.getcwd()
        complete_directory = os.path.join(current_directory, "analytical_data")
        if not os.path.exists(complete_directory):
            os.makedirs(complete_directory)
            
        for i in range(len(maps8)):
            write_str = maps8[i].contents_to_string()
            f = open(os.path.join(complete_directory, "nmap8 " + str(i) + ".txt"), "w+")
            f.write(write_str)
            f.close
        print([str(e) for e in map_index])

    #stores data needed to show how isoparimetric score varies over the maps generated
    def isoparametric_score_convergence(self):
        scores = []
        for i in range(self.map_count - 1):
            map = self.run_election_from_file(os.path.join(self.maps_location, "constituency_map " + str(i) +".txt"))
            map.run_election()
            scores.append(map.get_isoparametric_score())

        scores_str = ",".join(str(e) for e in scores)

        current_directory = os.getcwd()
        complete_directory = os.path.join(current_directory, "analytical_data")
        if not os.path.exists(complete_directory):
            os.makedirs(complete_directory)
            
        f = open(os.path.join(complete_directory, "isoparametric_score_data.txt"), "w+")
        f.write(scores_str)
        f.close

        plt.plot(scores)
        plt.show()

    #stores data needed to show a box plot showing, for each consistency, the fraction of the vote that is nationalist
    #much of the code here is unecasery
    def box_plot(self):
        scores = []
        for i in range(self.map_count - 1):
            map = self.run_election_from_file(os.path.join(self.maps_location, "constituency_map " + str(i) +".txt"))
            map.run_election()
            scores.append(map.get_nationalist_vote_fraction())

        sorted_scores = []

        sorted_centre = []
        sorted_leftout = []
        sorted_rightout= []
        #sorted_sd = []
        for s in range(18):
            current_lowest = []
            current_Q1 = []
            current_Q3 = []
            current_mean = 0
            current_Q1_mean = 0
            current_Q3_mean = 0

            current_centre = []
            current_leftout = []
            current_rightout = []

            for s in scores:
                current_lowest.append(min(s))
                s.remove(min(s))

            sorted_scores.append(current_lowest)
            current_mean = np.mean(current_lowest)


            for n in current_lowest:
                if n <= current_mean:
                    current_Q1.append(n)
            current_Q1_mean = np.mean(current_Q1)

            for n in current_lowest:
                if n >= current_mean:
                    current_Q3.append(n)
            current_Q3_mean = np.mean(current_Q3)

            for n in current_lowest:
                if n < current_Q1_mean:
                    current_leftout.append(n)
                elif n >= current_Q1_mean and n <= current_Q3_mean:
                    current_centre.append(n)
                elif n > current_Q3_mean:
                    current_rightout.append(n)

            sorted_centre.append(current_centre)
            sorted_leftout.append(current_leftout)
            sorted_rightout.append(current_rightout)

        sorted_scores = [[float(s) for s in l] for l in sorted_scores]
        sorted_centre = [[float(s) for s in l] for l in sorted_centre]
        sorted_leftout = [[float(s) for s in l] for l in sorted_leftout]
        sorted_rightout = [[float(s) for s in l] for l in sorted_rightout]

        sorted_scores_str_list = []
        for score in sorted_scores:
            current_score_str = ",".join(str(e) for e in score)
            sorted_scores_str_list.append(current_score_str)

        sorted_scores_str_final = ";".join(str(e) for e in sorted_scores_str_list)

        sorted_centre_str_list = []
        for centre in sorted_centre:
            sorted_centre_str = ",".join(str(e) for e in centre)
            sorted_centre_str_list.append(sorted_centre_str)

        sorted_centre_str_final = ";".join(str(e) for e in sorted_centre_str_list)

        sorted_leftout_str_list = []
        for leftout in sorted_leftout:
            sorted_leftout_str = ",".join(str(e) for e in leftout)
            sorted_leftout_str_list.append(sorted_leftout_str)

        sorted_leftout_str_final = ";".join(str(e) for e in sorted_leftout_str_list)

        sorted_rightout_str_list = []
        for rightout in sorted_rightout:
            sorted_rightout_str = ",".join(str(e) for e in rightout)
            sorted_rightout_str_list.append(sorted_rightout_str)

        sorted_rightout_str_final = ";".join(str(e) for e in sorted_rightout_str_list)

        contents = sorted_scores_str_final + "\n" + sorted_centre_str_final + "\n" + sorted_leftout_str_final + "\n" + sorted_rightout_str_final
        current_directory = os.getcwd()
        complete_directory = os.path.join(current_directory, "analytical_data")
        if not os.path.exists(complete_directory):
            os.makedirs(complete_directory)
            
        f = open(os.path.join(complete_directory, "boxplot_data.txt"), "w+")
        f.write(contents)
        f.close

        fig, axs = plt.subplots(1, 18)
        for i in range(17):
            data = np.concatenate((sorted_scores[i], sorted_centre[i], sorted_leftout[i], sorted_rightout[i]))
            axs[i].boxplot(data)
        plt.axis('off')
        plt.show()
    
    #Displaying functions
    #=============================================================================
    #displays a histogram representing the probability distribution of effective vote percentage for nationalists and
    #unionists, as well as the initial and final proposals.
    def display_evp(self, evp_location, new_map_location, old_map_location):
        f = open(os.path.join(evp_location, "evp_data.txt"), "r")
        fl = f.readlines()
        f.close

        new_map = self.run_election_from_file(os.path.join(new_map_location, "constituency_map 0.txt"))
        new_map.run_election()
        new_map_evp_n = new_map.get_n_evp()
        new_map_evp_u = new_map.get_u_evp()

        old_map = self.read_constituency_map_from_file(os.path.join(old_map_location, "constituency_map_base.txt"))
        old_map.run_election()
        old_map_evp_n = old_map.get_n_evp()
        old_map_evp_u = old_map.get_u_evp()


        n_str = fl[0].rstrip().split(",")
        u_str = fl[1].rstrip().split(",")

        n = [float(x) for x in n_str]
        u = [float(x) for x in u_str]

        fig, axs = plt.subplots(1, 1)
        axs.set_ylim([0,52])
        axs.set_xlim([0.18,0.44])
        plt.xlabel('Nationalist EVP', fontsize=18)
        plt.ylabel('Probability Density', fontsize=16)
        plt.scatter(old_map_evp_n, 3, color= "red", zorder = 2, alpha= 0.8, label = "Initial Proposals")
        plt.scatter(new_map_evp_n, 6, color= "black", zorder = 2, alpha= 1, label = "Final Proposals")
        plt.hist(n, bins = 1500, zorder = 1, color = "blue", density=True)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plt.savefig("n_hist_set")
        plt.close()
        #plt.show()
        

        fig, axs = plt.subplots(1, 1)
        axs.set_ylim([0,52])
        axs.set_xlim([0.18,0.44])
        plt.xlabel('Unionist EVP', fontsize=18)
        plt.ylabel('Probability Density', fontsize=16)
        plt.scatter(old_map_evp_u, 3, color= "red", zorder = 2, alpha= 0.8, label = "Initial Proposals")
        plt.scatter(new_map_evp_u, 6, color= "black", zorder = 2, alpha= 1, label = "Final Proposals")
        plt.hist(u, bins = 1500, zorder = 1, color = "blue", density=True)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plt.savefig("u_hist_var")
        plt.close()
        #plt.show()

    #displays the box plot generated above
    def display_box(self, box_data_location, new_map_location, old_map_location):
        f = open(os.path.join(box_data_location, "boxplot_data.txt"), "r")
        fl = f.readlines()
        f.close

        new_map = self.run_election_from_file(os.path.join(new_map_location, "constituency_map 0.txt"))
        new_map.run_election()
        new_map_score = new_map.get_nationalist_vote_fraction()

        old_map = self.read_constituency_map_from_file(os.path.join(old_map_location, "constituency_map_base.txt"))
        old_map.run_election()
        old_map_score = old_map.get_nationalist_vote_fraction()

        new_map_score.sort()
        del new_map_score[0]

        old_map_score.sort()
        del old_map_score[0]

        scores_str = [x.split(",") for x in fl[0].rstrip().split(";")]
        #print(rightout_str[1])
        del scores_str[0]


        scores = [[float(x) for x in score] for score in scores_str] 

        fig, axs = plt.subplots(1, 1)
        data = []
        for i in range(17):
            data.append(scores[i])

        axs.set_ylim([0,1])
        axs.boxplot(data, showfliers=False)

        plt.xlabel('Most Unionist To Most Nationalist Constituencies', fontsize=15)
        plt.ylabel('Nationalist Vote Percentage', fontsize=13)

        for i in range(16):
            plt.scatter(i+1, new_map_score[i], color='black', alpha= 0.65)
            plt.scatter(i+1, old_map_score[i], color='red', alpha= 0.65)
            
        plt.scatter(17, old_map_score[16], color='red', alpha= 0.65, label = "Initial Proposals")
        plt.scatter(17, new_map_score[16], color='black', alpha= 0.65, label = "Final Proposals")
        
        
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plt.savefig("box_plot")
        plt.show()


    #animates the given distribution of maps.
    def animate(self, plot_area):
        self.fig2, self.ax2 = plt.subplots()
        self.plot_area = plot_area
        anim = FuncAnimation(self.fig2, self.update, frames=self.map_count, interval=0.2, repeat_delay = 2000)
        plt.show()

    #def display_isoparametric(self, iso_location, new_map_location, old_map_location):
    #    f = open(os.path.join(iso_location, "isoparametric_score_data.txt"), "r")
    #    fl = f.readlines()
    #    f.close
    #
    #    new_map = self.run_election_from_file(os.path.join(new_map_location, "constituency_map 0.txt"))
    #    new_map.run_election()
    #    new_map_evp_n = new_map.get_n_evp()
    #
    #    old_map = self.read_constituency_map_from_file(os.path.join(old_map_location, "constituency_map_base.txt"))
    #    old_map.run_election()
    #    old_map_evp_n = old_map.get_n_evp()
    #    old_map_evp_u = old_map.get_u_evp()

    #displays the corresponding stored files above
    #should be in a script
    def read_eight_histogram_of_n(self, examples_loaction, plot_area):
        maps8 = []
        for i in range(10):
            maps8.append(self.read_constituency_map_from_file(os.path.join(examples_loaction, "nmap8 " + str(i) + ".txt")))
 
        for i in range(10):
            plt.scatter(maps8[i].display_graph()[1], maps8[i].display_graph()[0], c=maps8[i].display_graph()[2], cmap = 'nipy_spectral', s = plot_area)
            plt.xlabel('Longitude', fontsize=14)
            plt.ylabel('Latitude', fontsize=14)
            plt.savefig("histogram 6 n " + str(i))
            plt.cla()
            
    #displays the corresponding stored examples above
    #should be in a script
    def display_examples_histogram_of_n(self, examples_loaction, plot_area):
        maps6 = []
        maps7 = []
        maps8 = []
        maps9 = []
        maps10 = []
        for i in range(10):
            maps6.append(self.read_constituency_map_from_file(os.path.join(examples_loaction, "map6 " + str(i) + ".txt")))
            maps7.append(self.read_constituency_map_from_file(os.path.join(examples_loaction, "map7 " + str(i) + ".txt")))
            maps8.append(self.read_constituency_map_from_file(os.path.join(examples_loaction, "map8 " + str(i) + ".txt")))
            maps9.append(self.read_constituency_map_from_file(os.path.join(examples_loaction, "map9 " + str(i) + ".txt")))
            maps10.append(self.read_constituency_map_from_file(os.path.join(examples_loaction, "map10 " + str(i) + ".txt")))

        plt.scatter(maps6[9].display_graph()[1], maps6[9].display_graph()[0], c=maps6[9].display_graph()[2], cmap = 'nipy_spectral', s = plot_area)
        plt.xlabel('Longitude', fontsize=14)
        plt.ylabel('Latitude', fontsize=14)
        plt.savefig("histogram 6 n")
        plt.cla()

        plt.scatter(maps7[9].display_graph()[1], maps7[9].display_graph()[0], c=maps7[9].display_graph()[2], cmap = 'nipy_spectral', s = plot_area)
        plt.xlabel('Longitude', fontsize=14)
        plt.ylabel('Latitude', fontsize=14)
        plt.savefig("histogram 7 n")
        plt.cla()

        plt.scatter(maps8[9].display_graph()[1], maps8[9].display_graph()[0], c=maps8[9].display_graph()[2], cmap = 'nipy_spectral', s = plot_area)
        plt.xlabel('Longitude', fontsize=14)
        plt.ylabel('Latitude', fontsize=14)
        plt.savefig("histogram 8 n")
        plt.cla()

        plt.scatter(maps9[9].display_graph()[1], maps9[9].display_graph()[0], c=maps9[9].display_graph()[2], cmap = 'nipy_spectral', s = plot_area)
        plt.xlabel('Longitude', fontsize=14)
        plt.ylabel('Latitude', fontsize=14)
        plt.savefig("histogram 9 n")
        plt.cla()

        plt.scatter(maps10[9].display_graph()[1], maps10[9].display_graph()[0], c=maps10[9].display_graph()[2], cmap = 'nipy_spectral', s = plot_area)
        plt.xlabel('Longitude', fontsize=14)
        plt.ylabel('Latitude', fontsize=14)
        plt.savefig("histogram 10 n")
        plt.cla()


        #maps6, index 2
        #maps7, index 2
        #
        #maps9, index 2
        #maps10, index 2



        




#Private functions
#====================================================================
    def update(self, i):
        map = self.run_election_from_file(os.path.join(self.maps_location, "constituency_map " + str(i) + ".txt"))
        self.ax2.cla()
        self.ax2.scatter(map.display_graph()[1], map.display_graph()[0], c=map.display_graph()[2], cmap = 'nipy_spectral', s = self.plot_area)
        self.ax2.set_title(i+1, fontsize=20)
        #ax2.axis('equal')
        #self.ax2.set_axis_off()
        return self.ax2

    def run_election_from_file(self, file_current):
        ids, constituencies = self.read_constituency_from_file(file_current)
        constituency_map_current = self.base_map.deep_copy()
        constituency_map_current.reassign_constituencies(ids, constituencies)
        return constituency_map_current

    def read_constituency_from_file(self, con_map):
        f = open(con_map, "r")
        fl = f.readlines()
        id = fl[0].rstrip().split(",")
        constituenciesID = fl[1].rstrip().split(",")
        constituenciesID = [int(x) for x in constituenciesID]
        return id, constituenciesID

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
