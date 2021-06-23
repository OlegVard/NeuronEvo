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
            if reference[0] == 0:
                out1 = abs(out1)
            else:
                out2 = abs(out2)
            f_list.append(out1 + out2)
        fitness_list.append(f_list)

    net_obj.data_iter += 1
    return fitness_list


def find_best(fitt_list):
    min_list = []
    for i_iter in range(len(fitt_list)):
        min_list.append(min(fitt_list[i_iter]))

    min_error = min(min_list)
    min_index_x = min_list.index(min_error)
    min_index_y = fitt_list[min_index_x].index(min_error)
    return min_index_x, min_index_y


def find_best_in_species(fit_species):
    to_new_pop = min(fit_species)
    new_index = fit_species.index(to_new_pop)
    return new_index


def final_forward(net, best_person, final=False):
    right_count = 0
    data_i = net.data_iter
    net.data_iter = 400
    for i_iter in range(50):
        best_out1, best_out2, ref = net.forward(best_person, test=True)
        if round(best_out1) == ref[0] and round(best_out2) == ref[1]:
            right_count += 1
            if final:
                print(best_out1, best_out2)
        net.data_iter += 1
    net.data_iter = data_i
    return right_count / 50


for i in range(1000):
    fit_list = cell_funk(population, net)
    best_index_x, best_index_y = find_best(fit_list)
    best = fit_list[best_index_x][best_index_y]
    acc = final_forward(net, population[best_index_x][best_index_y])
    if acc >= 0.8:
        acc = final_forward(net, population[best_index_x][best_index_y], final=True)
        print('Алгоритм завершен на ', i, 'итерации. Точность =', acc)
        name = 'final' + str(i) + '.gv'
        population[best_index_x][best_index_y].render(name)
        break
    else:
        new_pop = []
        for j in range(len(population)):
            new_pop.append(population[j][find_best_in_species(fit_list[j])])

        if len(population[best_index_x]) == 1:
            continue
        elif len(population[best_index_x]) == 2:
            if fit_list[best_index_x][0] > fit_list[best_index_x][1]:
                new_pop.append(Genome.crossover(population[best_index_x][0], population[best_index_x][1]))
            else:
                new_pop.append(Genome.crossover(population[best_index_x][1], population[best_index_x][0]))
        else:
            for j in range(len(population[best_index_x])):
                parent1 = random.choice(population[best_index_x])
                parent2 = random.choice(population[best_index_x])
                while parent1 == parent2:
                    parent2 = random.choice(population[best_index_x])
                if fit_list[best_index_x][population[best_index_x].index(parent1)] \
                        > fit_list[best_index_x][population[best_index_x].index(parent2)]:
                    new_pop.append(Genome.crossover(parent2, parent1))
                else:
                    new_pop.append(Genome.crossover(parent1, parent2))

        for j in range(len(new_pop)):
            mutate = random.randint(0, 1)
            if random.random() < 0.2:
                if mutate == 1:
                    new_pop[j].mutate_connection()
                else:
                    new_pop[j].mutate_node()

        pop = []
        for _ in range(len(population)):
            pop.append([])
        for j in range(len(new_pop)):
            Genome.types_division(population, new_pop[j], len(population))
            if new_pop[j].species > len(population):
                pop.append([new_pop[j]])
            else:
                pop[new_pop[j].species].append(new_pop[j])

        if i % 10 == 0:
            print('Итерация', i, 'Лучший', best)
            name = 'iteration' + str(i) + '.gv'
            population[best_index_x][best_index_y].render(name)

        population.clear()
        for j in range(len(pop)):
            if len(pop[j]) != 0:
                population.append(pop[j])
