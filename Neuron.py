import random
from Genome import Genome
from Genes import Connections, Node, NodeType
from Data import get_data
import numpy as np


class Neuron:
    def __init__(self, number_of_in, number_of_out, number_of_models, data_iter=0):
        self.models = number_of_models
        self.number_of_in = number_of_in
        self.number_of_out = number_of_out
        self.data = get_data()
        self.data_iter = data_iter

    def create(self):
        population = []
        for i in range(self.models):
            a = Genome()
            for j in range(self.number_of_in + self.number_of_out):
                if j < self.number_of_in:
                    a.add_node(Node(NodeType.Input, a.node_innovations()))
                else:
                    a.add_node(Node(NodeType.Output, a.node_innovations()))
            for j in range(self.number_of_in):
                out = random.choice([self.number_of_in + 1, self.number_of_in + 2])
                a.add_connection(Connections(j + 1,
                                             out,
                                             round(random.random(), 2),
                                             True,
                                             a.connections_innovations()))
                if random.random() < 0.2:
                    if out == self.number_of_in + 1:
                        a.add_connection(Connections(j + 1,
                                                     self.number_of_in + 2,
                                                     round(random.random(), 2),
                                                     True,
                                                     a.connections_innovations()))
                    else:
                        a.add_connection(Connections(j + 1,
                                                     self.number_of_in + 1,
                                                     round(random.random(), 2),
                                                     True,
                                                     a.connections_innovations()))
            population.append(a)
        return population

    def forward(self, net):     # переделать
        data = self.data[self.data_iter]
        if self.data_iter > 500:
            self.data_iter = 0
        sum_matrix = [0.0] * len(net.nodes)
        data_iter = 0

        for i in range(len(net.nodes)):
            sum_matrix[i] = [0.0] * len(net.nodes)
        previous_list = []
        for (_, conn) in net.connections.items():
            if not conn.state:
                continue
            in_node = conn.input_n - 1
            out_node = conn.output - 1
            if in_node < self.number_of_in and in_node not in previous_list:
                data_iter += 1
                x = data[data_iter] * conn.weight
            elif in_node < self.number_of_in and in_node in previous_list:
                x = data[data_iter] * conn.weight
            else:
                x = np.sum(sum_matrix[in_node]) * conn.weight
            previous_list.append(in_node)
            sum_matrix[out_node][in_node] = self.sigmoid(x)

        out1 = self.sigmoid(np.sum(sum_matrix[self.number_of_out + self.number_of_in - 2]))
        out2 = self.sigmoid(np.sum(sum_matrix[self.number_of_out + self.number_of_in - 1]))

        return out1, out2, data[-2:]

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
