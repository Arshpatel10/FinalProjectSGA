from random import choices
import random


def generate_chromosome(length,bounds):
    return [random.uniform(bounds[0], bounds[1]) for _ in range(length)]

def generate_population(number,length,bounds):
    return [generate_chromosome(length, bounds) for _ in range(number)]

def selection(population, fitness, tournament_size=3):
    selected = random.sample(list(zip(population, fitness)), tournament_size)
    selected.sort(key=lambda x: x[1])  # Sort by fitness (lower is better)
    return selected[0][0]

def crossover(parent1, parent2,crossover_rate, length):
        if random.random() < crossover_rate:
            point = random.randint(1, length - 1)
            return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
        return parent1, parent2

# Mutation: Gaussian Mutation
def mutate(individual,mutation_rate,length,bounds):
    if random.random() < mutation_rate:
        index = random.randint(0, length - 1)
        individual[index] += random.gauss(0, 1)
        individual[index] = max(bounds[0], min(bounds[1], individual[index]))
    return individual

def de_Jong_Sphere(individual):
     return sum(x**2 for x in individual)

def evaluate_population(population):
        return [de_Jong_Sphere(ind) for ind in population]

def genetic_algorithm(population_size,length,generations,crossover_rate,mutation_rate,bounds):
    population = generate_population(population_size,length,bounds)
    for generation in range(generations):
        fitnesses = evaluate_population(population)
        next_population = []

        while len(next_population) < population_size:
            # Select parents
            parent1 = selection(population, fitnesses)
            parent2 = selection(population, fitnesses)

            # Crossover and mutation
            offspring1, offspring2 = crossover(parent1, parent2,crossover_rate,length)
            offspring1 = mutate(offspring1,mutation_rate,length,bounds)
            offspring2 = mutate(offspring2,mutation_rate,length,bounds)

            # Add to the next generation
            next_population.extend([offspring1, offspring2])

        population = next_population[:population_size]

        # Best solution in the current generation
        best_individual = min(population, key=de_Jong_Sphere)
        best_fitness = de_Jong_Sphere(best_individual)

        rounded_individual = [round(x, 5) for x in best_individual]
        rounded_fitness = round(best_fitness, 5)

        print(
            f"Generation {generation + 1}: Best Fitness = {rounded_fitness}, Best Individual = {rounded_individual}"
        )

    # Final best solution
    best_individual = min(population, key=de_Jong_Sphere)
    best_fitness = de_Jong_Sphere(best_individual)

    rounded_individual = [round(x, 5) for x in best_individual]
    rounded_fitness = round(best_fitness, 5)

    return rounded_individual, rounded_fitness


best_solution, best_value = genetic_algorithm(100,5,50,0.8,0.1,(-5.12, 5.12))
print(f"\nOptimal Solution: {best_solution}")
print(f"Optimal Fitness (Minimum Value): {best_value}")