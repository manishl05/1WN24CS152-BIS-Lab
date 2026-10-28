import random

# Number of vehicles on each road
vehicles = {
    "North-South": 80,
    "East-West": 40
}

# Generate random signal timings
population = []

for i in range(10):
    ns = random.randint(20, 60)
    ew = random.randint(20, 60)
    population.append([ns, ew])


# Calculate waiting time
def fitness(signal):
    ns_time, ew_time = signal

    # More green time means less waiting
    ns_wait = vehicles["North-South"] * (60 - ns_time)
    ew_wait = vehicles["East-West"] * (60 - ew_time)

    return ns_wait + ew_wait


# Genetic Algorithm
for generation in range(50):

    # Select the best signal timings
    population.sort(key=fitness)

    parent1 = population[0]
    parent2 = population[1]

    # Crossover
    child = [
        parent1[0],
        parent2[1]
    ]

    # Mutation
    if random.random() < 0.2:
        child[0] = random.randint(20, 60)

    if random.random() < 0.2:
        child[1] = random.randint(20, 60)

    # Replace worst solution
    population[-1] = child


# Best solution
best = min(population, key=fitness)

print("Optimal Traffic Signal Timing")
print("North-South Green Time:", best[0], "seconds")
print("East-West Green Time:", best[1], "seconds")
print("Minimum Waiting Time:", fitness(best))
