from Neuron import Neuron
from Genome import Genome
import random

net = Neuron(9, 2, 10)
population = net.create()


def cell_funk(persons, net_obj):
    fitness_list = []
    for person in persons:
        for one in person:
            out1, out2, reference = net_obj.forward(one)
            out1 = reference[0] - out1
            out2 = reference[1] - out2
            fitness = (out1 + out2) / 2
            fitness_list.append([abs(fitness)])

    net_obj.data_iter += 1
    return fitness_list


def _cell_funk(persons, net_obj):
    fitness_list = []
    for person in persons:
        out1, out2, reference = net_obj.forward(person)
        out1 = reference[0] - out1
        out2 = reference[1] - out2
        fitness = (out1 + out2) / 2
        fitness_list.append([abs(fitness)])

    net_obj.data_iter += 1
    return fitness_list


for i in range(10000000):
    fit_list = _cell_funk(population, net)
    best = min(fit_list)
    best_index = fit_list.index(best)
    if best[0] < 1.0e-3:
        print('Алгоритм завершен')
        population[best_index].render('final.gv')
        break
    else:
        new_pop = []
        for j in range(net.models):
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            while parent1 == parent2:
                parent2 = random.choice(population)
            if fit_list[population.index(parent1)] > fit_list[population.index(parent2)]:
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

        if i % 50 == 0:
            print('iteration', i, 'best', best)
            name = 'iteration' + str(i) + '.gv'
            population[best_index].render(name)
        for _ in range(4):
            new_pop.append(population.pop(best_index))
            fit_list.remove(best)
            best = min(fit_list)
            best_index = fit_list.index(best)

        population = new_pop
