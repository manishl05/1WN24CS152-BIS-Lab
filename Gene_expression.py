import random

population = [
    [4, 3, 3],
    [2, 5, 3],
    [5, 2, 3],
    [3, 4, 3]
]

def fitness(x):
    return x[0]*10 + x[1]*8 + x[2]*6

for i in range(10):

    population.sort(key=fitness, reverse=True)
    parent1 = population[0]
    parent2 = population[1]
    child = [parent1[0], parent2[1], parent2[2]]

    if random.random() < 0.1:
        child[0] -= 1
        child[1] += 1

    population[-1] = child

best = max(population, key=fitness)

print("Best Resource Allocation")
print("Project A:", best[0], "workers")
print("Project B:", best[1], "workers")
print("Project C:", best[2], "workers")
print("Maximum Benefit:", fitness(best))
