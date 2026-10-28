import random
import numpy as np

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

# 1. Create a simple student dataset
# Columns: Study hours, Attendance, Previous score
X = np.array([
    [2, 50, 35],
    [3, 60, 40],
    [4, 65, 45],
    [5, 75, 55],
    [6, 80, 65],
    [7, 85, 70],
    [8, 90, 80],
    [9, 95, 90],
    [2, 55, 30],
    [6, 70, 60],
    [7, 80, 75],
    [3, 50, 38]
])

# 0 = Fail, 1 = Pass
y = np.array([0, 0, 0, 1, 1, 1, 1, 1,
              0, 1, 1, 0])

features = [
    "Study Hours",
    "Attendance",
    "Previous Score"
]

# 2. Genetic Algorithm settings
POPULATION_SIZE = 8
GENERATIONS = 10
MUTATION_RATE = 0.1
N_FEATURES = len(features)

random.seed(42)
np.random.seed(42)

cv = StratifiedKFold(
    n_splits=3, shuffle=True, random_state=42
)

# 3. Fitness function
def fitness(chromosome):
    selected = np.flatnonzero(chromosome)

    if len(selected) == 0:
        return 0

    model = DecisionTreeClassifier(max_depth=2)

    accuracy = cross_val_score(
        model,
        X[:, selected],
        y,
        cv=cv,
        scoring="accuracy"
    ).mean()

    # Reward accuracy and fewer features
    return 0.9 * accuracy + 0.1 * (
        1 - len(selected) / N_FEATURES
    )

# 4. Generate a random chromosome
def create_chromosome():
    chromosome = np.random.randint(0, 2, N_FEATURES)

    if chromosome.sum() == 0:
        chromosome[random.randrange(N_FEATURES)] = 1

    return chromosome

# 5. Select the best of three random candidates
def select_parent(population):
    candidates = random.sample(population, 3)
    return max(candidates, key=fitness).copy()

# 6. Crossover
def crossover(p1, p2):
    point = random.randint(1, N_FEATURES - 1)

    c1 = np.concatenate([p1[:point], p2[point:]])
    c2 = np.concatenate([p2[:point], p1[point:]])

    return c1, c2

# 7. Mutation
def mutate(chromosome):
    child = chromosome.copy()

    for i in range(N_FEATURES):
        if random.random() < MUTATION_RATE:
            child[i] = 1 - child[i]

    if child.sum() == 0:
        child[random.randrange(N_FEATURES)] = 1

    return child

# 8. Initialize population
population = [
    create_chromosome()
    for _ in range(POPULATION_SIZE)
]

best_solution = None
best_fitness = -1

# 9. Evolve the population
for generation in range(GENERATIONS):
    scores = [fitness(c) for c in population]
    order = np.argsort(scores)[::-1]

    population = [population[i] for i in order]
    scores = [scores[i] for i in order]

    if scores[0] > best_fitness:
        best_fitness = scores[0]
        best_solution = population[0].copy()

    print(
        f"Generation {generation + 1}: "
        f"Fitness = {best_fitness:.4f}"
    )

    # Preserve the best solution
    new_population = [best_solution.copy()]

    while len(new_population) < POPULATION_SIZE:
        p1 = select_parent(population)
        p2 = select_parent(population)

        c1, c2 = crossover(p1, p2)

        new_population.append(mutate(c1))

        if len(new_population) < POPULATION_SIZE:
            new_population.append(mutate(c2))

    population = new_population

# 10. Display the best solution
selected = np.flatnonzero(best_solution)

print("\n===== BEST SOLUTION =====")
print("Selected features:")

for i in selected:
    print("-", features[i])

print("Number of features:", len(selected))
print("Best fitness:", round(best_fitness, 4))

# Evaluate the selected features
final_model = DecisionTreeClassifier(max_depth=2)
final_model.fit(X[:, selected], y)

print("Training accuracy:",
      round(final_model.score(X[:, selected], y) * 100, 2),
      "%")

print("Total features:", N_FEATURES)
print("Best chromosome:", "".join(map(str, best_solution.astype(int))))
print("Selected features:", int(best_solution.sum()))