import random
from Genome import Genome
from Genes import Connections, Node, NodeType
import math


class Neuron:
    def __init__(self, number_of_in, number_of_out, number_of_models, data, data_iter=0):
        self.models = number_of_models
        self.number_of_in = number_of_in
        self.number_of_out = number_of_out
        self.data = data
        self.data_iter = data_iter

    def create(self):
        population = []
        for i in range(self.models):
            a = Genome()
            for j in range(self.number_of_in + self.number_of_out):
                if j < self.number_of_in:
                    a.add_node(Node(NodeType.Input, j + 1))
                else:
                    a.add_node(Node(NodeType.Output, j + 1))
                a.node_innovation += 1
            for j in range(self.number_of_in):
                out = random.choice([self.number_of_in + 1, self.number_of_in + 2])
                a.add_connection(Connections(j + 1,
                                             out,
                                             round(random.random(), 2),
                                             True,
                                             a.conn_innovation + 1))
                a.conn_innovation += 1
                if random.random() < 0.2:
                    if out == self.number_of_in + 1:
                        a.add_connection(Connections(j + 1,
                                                     self.number_of_in + 2,
                                                     round(random.random(), 2),
                                                     True,
                                                     a.conn_innovation + 1))
                        a.conn_innovation += 1
                    else:
                        a.add_connection(Connections(j + 1,
                                                     self.number_of_in + 1,
                                                     round(random.random(), 2),
                                                     True,
                                                     a.conn_innovation + 1))
                        a.conn_innovation += 1
            a.conn_innovation += 1
            a.node_innovation += 1
            population.append(a)
        return population

    def forward(self, net):
        data = self.data
        self.data_iter += 1
        sum_out_1 = []
        sum_out_2 = []
        sum_hidden = []

        for (i, conn) in net.connections.items():
            x = data[i - 1] * conn.weight
            if conn.output == self.number_of_in + self.number_of_out:
                sum_out_1.append(self.sigmoid(x))
            elif conn.output == self.number_of_in + self.number_of_out - 1:
                sum_out_2.append(self.sigmoid(x))
            else:
                sum_hidden.append(self.sigmoid(x))
        out1 = sum(sum_out_1)
        out2 = sum(sum_out_2)


        fitness1 = data[self.number_of_in + self.number_of_out - 1] - out1
        fitness2 = data[self.number_of_in + self.number_of_out - 2] - out2
        return fitness1, fitness2

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))
