"""
Created on Mon Nov 28 15:11:31 2022

@author: Telmo Briones
"""

import numpy as np
from textwrap import wrap
from matplotlib import pyplot as plt
from time import time


# Parametroak
n_cities = 15
n_population = 100
mutation_rate = 0.3
iterations = 10000
scale =2.076
image_path="ehmapa_garbia.png"

# Datuak
coordinates_list = [[110,129],[147,220],[270,116],[326,235],[360,75],[394,154],[452,137],[223,178],[337,406],[163,296],[346,163],[255,316],[151,154],[97,167],[204,120]]
names_list = np.array(['Bilbao','Gasteiz','Donostia','Iruña','Baiona','Donibane-Garazi','Maule','Beasain','Tutera','Zieko','Elizondo','Lodosa','Durango','Amurrio','Mutriku'])
cities_dict = { x:y for x,y in zip(names_list,coordinates_list) }


"""------------------------------------"""

# Function to compute the distance between two points
def compute_city_distance_coordinates(a,b):
    return (((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5)/scale

def compute_city_distance_names(city_a, city_b, cities_dict):
    return compute_city_distance_coordinates(cities_dict[city_a], cities_dict[city_b])

"""------------------------------------"""

# Lehenengo pausua: Hasierako populazioa sortu
def genesis(city_list, n_population):

    population_set = []
    for i in range(n_population):
        # Ausaz sortuko dugu soluzio posible berria
        sol_i = city_list[np.random.choice(list(range(n_cities)), n_cities, replace=False)]
        sol_i = np.append(sol_i, sol_i[0])
        population_set.append(sol_i)
    return np.array(population_set)

"""------------------------------------"""

def fitness_eval(city_list, cities_dict):
    total = 0
    for i in range(n_cities-1):
        a = city_list[i]
        b = city_list[i+1]
        total += compute_city_distance_names(a,b, cities_dict)
    return 1/total

def get_all_fitnes(population_set, cities_dict):
    fitnes_list = np.zeros(n_population)

    #Looping over all solutions computing the fitness for each solution
    for i in  range(n_population):
        fitnes_list[i] = fitness_eval(population_set[i], cities_dict)

    return fitnes_list

"""------------------------------------"""

# Gurasoen aukeraketa
def progenitor_selection(population_set,fitnes_list):
    total_fit = fitnes_list.sum()
    prob_list = fitnes_list/total_fit

    #Notice there is the chance that a progenitor. mates with oneself
    progenitor_list_a = np.random.choice(list(range(len(population_set))), len(population_set),p=prob_list, replace=True)
    progenitor_list_b = np.random.choice(list(range(len(population_set))), len(population_set),p=prob_list, replace=True)

    progenitor_list_a = population_set[progenitor_list_a]
    progenitor_list_b = population_set[progenitor_list_b]


    return np.array([progenitor_list_a,progenitor_list_b])

"""------------------------------------"""

# Gurasoen ugalketa
def mate_progenitors(prog_a, prog_b):
    offspring = prog_a[0:5]
    for city in prog_b:

        if not city in offspring:
            offspring = np.concatenate((offspring,[city]))
    return offspring

# Populazioa ugaldu
def mate_population(progenitor_list):
    new_population_set = []
    for i in range(progenitor_list.shape[1]):
        prog_a, prog_b = progenitor_list[0][i], progenitor_list[1][i]
        offspring = mate_progenitors(prog_a, prog_b)
        offspring = np.append(offspring, offspring[0])
        new_population_set.append(offspring)

    return new_population_set

"""------------------------------------"""

# Semearen mutazioa burutu
def mutate_offspring(offspring):
    for q in range(int(n_cities*mutation_rate)):
        a = np.random.randint(1,n_cities)
        b = np.random.randint(1,n_cities)

        offspring[a], offspring[b] = offspring[b], offspring[a]

    return offspring

# Populazioa mutatu
def mutate_population(new_population_set):
    mutated_pop = []
    for offspring in new_population_set:
        mutated_pop.append(mutate_offspring(offspring))
    return mutated_pop

"""------------------------------------"""

def showSol(best_solution, test_num):

    im = plt.imread(image_path)
    fig, ax = plt.subplots()
    ax.imshow(im)
    cities = best_solution[2].tolist()[0]

    city_names = ""
    x_data, y_data = [], []

    for city in cities:
        c_coords = cities_dict.get(city)
        city_names += str(city)+" ~ "
        x_data += [c_coords[0]]
        y_data += [c_coords[1]]
    city_names = city_names[:-3]
    city_names = "\n".join(wrap(city_names, width=65))
    u = np.diff(x_data)
    v = np.diff(y_data)
    pos_x = x_data[:-1] + u/2
    pos_y = y_data[:-1] + v/2
    norm = np.sqrt(u**2+v**2)

    ax.plot(x_data, y_data, color='blue', lw = 1.8)
    ax.quiver(pos_x, pos_y, u/norm, v/norm, color='blue', angles="xy", zorder=5, pivot="mid", width=0.002, headwidth=10, headlength=20 ,headaxislength=15)
    ax.scatter(x_data, y_data, s=25, zorder=10,color='black')
    ax.axis('off')


    text = "Distantzia = " + str(round(best_solution[1],2)) + " km"
    ax.text(10,350, text, fontsize = 8)
    ax.text(10,50, city_names, fontsize = 8)
    ax.text(10,370,"1 pixel : 2 km", fontsize = 8)
    if test_num != 0:
        plt.title("TEST nº"+str(test_num))
    else:
        plt.title("Travelling Salesman Problem")

    return plt, city_names

"""------------------------------------"""

def calculate(test_num):

    start_time = time()
    # Hasierako populazioa sortu
    population_set = genesis(names_list, n_population)

    fitness_list = get_all_fitnes(population_set,cities_dict)

    # Gurasoen aukeraketa zuzentasunaren arabera
    progenitor_list = progenitor_selection(population_set,fitness_list)

    # Populazio berria sortu
    new_population_set = mate_population(progenitor_list)

    # Populazioan mutazioak sortu
    mutated_pop = mutate_population(new_population_set)
    mutated_pop[0]

    best_solution = [-1,np.inf,np.array([])]

    for i in range(iterations):
        if i%1000==0 and i!=0: print(i, best_solution[1])
        fitnes_list = get_all_fitnes(mutated_pop,cities_dict)

        #Saving the best solution
        if 1/fitnes_list.max() < best_solution[1]:
            best_solution[0] = i
            best_solution[1] = 1/fitnes_list.max()
            best_solution[2] = np.array(mutated_pop)[fitnes_list.max() == fitnes_list]

        progenitor_list = progenitor_selection(population_set,fitnes_list)
        new_population_set = mate_population(progenitor_list)

        mutated_pop = mutate_population(new_population_set)

    plt, city_names = showSol(best_solution, test_num)

    elapsed_time = time() - start_time
    return best_solution, plt, city_names, elapsed_time


def main():

    for test_num in range(0,10):
        print("\n\n--------------TEST nº" + str(test_num+1) +"--------------")
        best_solution, plt, city_names, elapsed_time = calculate(test_num+1)
        print("\n",best_solution[0],"iterazioan aurkitu da biderik laburrena: \n", city_names)
        print("\nDistantzia totala: ", round(best_solution[1],2), "km\n")
        print("Denbora: %0.10f segundu" % elapsed_time)
        plt.savefig("bidea_"+str(test_num+1)+".png")
    # print("\n\n--------------TEST--------------")
    # best_solution, plt, city_names, elapsed_time = calculate(0)
    # print("\n",best_solution[0],"iterazioan aurkitu da biderik laburrena: \n", city_names)
    # print("\nDistantzia totala: ", round(best_solution[1],2), "km\n")
    # print("Denbora: %0.10f segundu" % elapsed_time)
    # plt.savefig("bidea_exekuzio_sinplea.png")


if __name__ == "__main__":
    main()


