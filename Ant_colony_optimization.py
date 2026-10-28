
import random

distance = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

N = len(distance)
NUM_ANTS = 10
ITERATIONS = 100

ALPHA = 1.0   
BETA = 2.0       
RHO = 0.5         
Q = 100           

pheromone = [[0.1 for j in range(N)] for i in range(N)]

best_tour = []
best_distance = float('inf')

def calculate_distance(tour):
    total = 0

    for i in range(len(tour) - 1):
        total += distance[tour[i]][tour[i + 1]]

    total += distance[tour[-1]][tour[0]]

    return total

def select_next_city(current, unvisited):
    probabilities = []

    for city in unvisited:
        trail = pheromone[current][city] ** ALPHA
        visibility = (1 / distance[current][city]) ** BETA
        probabilities.append(trail * visibility)

    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]

    return random.choices(
        list(unvisited), weights=probabilities, k=1
    )[0]

for iteration in range(ITERATIONS):
    all_tours = []

    for ant in range(NUM_ANTS):
        start = random.randrange(N)
        tour = [start]
        unvisited = set(range(N))
        unvisited.remove(start)

        current = start

        while unvisited:
            next_city = select_next_city(current, unvisited)
            tour.append(next_city)
            unvisited.remove(next_city)
            current = next_city

        tour_length = calculate_distance(tour)
        all_tours.append((tour, tour_length))

        if tour_length < best_distance:
            best_distance = tour_length
            best_tour = tour[:]

    for i in range(N):
        for j in range(N):
            pheromone[i][j] *= (1 - RHO)

    for tour, length in all_tours:
        deposit = Q / length

        for i in range(N):
            city1 = tour[i]
            city2 = tour[(i + 1) % N]

            pheromone[city1][city2] += deposit
            pheromone[city2][city1] += deposit

print("Best tour:")

for city in best_tour:
    print(city, end=" -> ")

print(best_tour[0])
print("Minimum distance:", best_distance)
