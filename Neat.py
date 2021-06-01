from Neuron import Neuron
from Genome import Genome

net = Neuron(9, 2, 10)
population = net.create()


def cell_funk(persons, net_obj):
    fitness_list = []
    j = 1
    for person in persons:
        out1, out2, reference = net_obj.forward(person)
        out1 = reference[0] - out1
        out2 = reference[1] - out2
        fitness = out1 + out2 / 2
        fitness_list.append([abs(fitness)])

        j += 1
    net_obj.data_iter += 1
    return fitness_list


for i in range(4):
    fit_list = cell_funk(population, net)
    best = min(fit_list)
    best_index = fit_list.index(best)
    if best == 0 or best[0] < 2.0e-16:
        print('Алгоритм завершен')
        population[best_index].render('final.gv')
    pass
print(cell_funk(population, net))
