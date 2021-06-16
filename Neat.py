from Neuron import Neuron
from Genome import Genome
import random

net = Neuron(9, 2, 10)
population = [net.create()]


def cell_funk(persons, net_obj):
    fitness_list = []
    for person in persons:
        f_list = []
        for one in person:
            out1, out2, reference = net_obj.forward(one)
            out1 = reference[0] - out1
            out2 = reference[1] - out2
            fitness = (out1 + out2) / 2
            f_list.append(abs(fitness))
        fitness_list.append(f_list)

    net_obj.data_iter += 1
    return fitness_list


def find_best(fit_list):
    min_list = []
    for i in range(len(fit_list)):
        min_list.append(min(fit_list[i]))

    min_error = min(min_list)
    min_index_x = min_list.index(min_error)
    min_index_y = fit_list[min_index_x].index(min_error)
    return min_index_x, min_index_y


for i in range(10000000):
    fit_list = cell_funk(population, net)
    best_index_x, best_index_y = find_best(fit_list)
    best = fit_list[best_index_x][best_index_y]
    if best < 1.0e-3:
        print('Алгоритм завершен')
        population[best_index_x][best_index_y].render('final.gv')
        break
    else:
        new_pop = []
        for j in range(len(population)):
            if len(population[j]) == 1:
                continue
            elif len(population[j]) == 2:
                if fit_list[j][0] > fit_list[j][1]:
                    new_pop.append(Genome.crossover(population[j][0], population[j][1]))
                else:
                    new_pop.append(Genome.crossover(population[j][1], population[j][0]))
            else:
                for n in range(len(population[j])):
                    parent1 = random.choice(population[j])
                    parent2 = random.choice(population[j])
                    while parent1 == parent2:
                        parent2 = random.choice(population[j])
                    if fit_list[j][population[j].index(parent1)] > fit_list[j][population[j].index(parent2)]:
                        new_pop.append(Genome.crossover(parent2, parent1))
                    else:
                        new_pop.append(Genome.crossover(parent1, parent2))

        for j in range(len(new_pop)):
            mutate = random.randint(0, 1)
            if random.random() < 0.25:
                if mutate == 0:
                    new_pop[j].mutate_connection()
                else:
                    new_pop[j].mutate_node()

        for j in range(len(new_pop)):
            Genome.types_division(population, new_pop[j], len(population))
            if new_pop[j].species > len(population):
                population.append([new_pop[j]])
            else:
                population[new_pop[j].species].append(new_pop[j])

        if i % 10 == 0:
            print('iteration', i, 'best', best, 'species', population[best_index_x][best_index_y].species)
            name = 'iteration' + str(i) + 'species' + str(population[best_index_x][best_index_y].species) + '.gv'
            population[best_index_x][best_index_y].render(name)
