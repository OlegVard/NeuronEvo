# file for network
import random


class Neuron:   # запись структуры сети в виде матрицы
    matrix = []
    size = 5

    def init_matrix(self):
        i = 0
        j = 0
        while i < self.size:
            small_matr = []
            while j < self.size:
                if i == j:
                    small_matr.append(0)
                    j += 1
                    continue
                if random.random() >= 0.3:
                    small_matr.append(random.randint(0, 1))
                    j += 1
                else:
                    small_matr.append(0)
                    j += 1
            self.matrix.append(small_matr)
            i += 1
            j = 0
        return self.matrix


m = Neuron()
ma = m.init_matrix()
for i in range(5):
    print(ma[i])
