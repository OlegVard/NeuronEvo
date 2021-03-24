import random


class Neuron:  # запись структуры сети в виде матрицы
    matrix = []
    size = 5

    def init_matrix(self):
        for i in range(self.size):
            small_matrix = []
            for j in range(self.size):
                if i == j:
                    small_matrix.append(0)
                    continue
                if random.random() >= 0.4:
                    small_matrix.append(round(random.random(), 2))
                else:
                    small_matrix.append(0)
            self.matrix.append(small_matrix)

        for i in range(self.size):  # для направлений
            for j in range(self.size):
                if self.matrix[i][j] != 0:
                    self.matrix[j][i] = 0

        return self.matrix


# для проверки пусть пока побудет тут
m = Neuron()
ma = m.init_matrix()
for i in range(5):
    print(ma[i])
