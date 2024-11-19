# Traveling Salesman Problem (TSP) - Genetic Algorithm
![Example image](https://github.com/telmobriones/Travelling-Salesman-Problem/blob/4335c2cbadfac266ef5429b38cf85180f57deb5a/adibidea.png)
## Overview

This project implements a **genetic algorithm** to solve the Traveling Salesman Problem (TSP) using some rudimentarily created datapoints of cities and towns from Euskal Herria (Basque Country). 
The algorithm aims to approximate the shortest possible route that visits each city once and returns to the starting point.

Key features include:
- **Visualization**: Displays the best found route over a map of Euskal Herria.
- **Customizable Parameters**: Adjust population size, mutation rate, and iterations.
- **Performance Analysis**: Tracks computation time and optimal distance for each run.

---

## Getting Started

### Prerequisites
To run this project, you need:
- **Python 3.7+**
- Libraries: `numpy`, `matplotlib`

Install the required libraries with:
```bash
pip install numpy matplotlib
```

### Files

- `ehmapa_garbia.png`: Map image used for route visualization. Ensure this file is in the same directory as the script.

---

## How It Works

### Genetic Algorithm Workflow:

1. **Initial Population**: Randomly generates routes.
2. **Fitness Evaluation**: Calculates fitness based on route distances.
3. **Selection**: Selects parent routes based on fitness (roulette wheel selection).
4. **Crossover**: Combines parts of parent routes to create new routes.
5. **Mutation**: Randomly swaps cities in a route to introduce variety.
6. **Optimization**: Repeats the process over multiple iterations to find the shortest route.

### Parameters

You can modify these parameters in the script to experiment with different configurations:

- `n_cities`: Number of cities in the dataset (default: 15).
- `n_population`: Number of candidate solutions per generation (default: 100).
- `mutation_rate`: Proportion of mutations applied to routes (default: 0.3).
- `iterations`: Number of generations to evolve (default: 10,000).
- `scale`: Distance scale (pixels to kilometers) based on map resolution (default: 2.076).

---

## Running the Program

Run the script with:
```bash
python tsp_genetic_algorithm.py
```
The program executes 10 tests, logging the shortest route and distance for each test. It also saves the route visualizations as `bidea_<test_number>.png`.

## Visualization

Each route is plotted over a map of Euskal Herria, with: 
- Cities marked as points.
- Routes displayed as arrows.
- Total distance and city names shown on the map.
