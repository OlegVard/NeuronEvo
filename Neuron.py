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
            population.append(a)
        return population

    def forward(self, net, test=False):     # поиск в ширину в обратную сторону
        data = self.data[self.data_iter]
        if self.data_iter > 500 and not test:
            self.data_iter = 0
        sum_matrix = [0.0] * len(net.nodes)
        x = 0
        for i in range(len(net.nodes)):
            sum_matrix[i] = [0.0] * len(net.nodes)
        sort_conn_list = self.sort_connections(net)
        for (i, conn) in net.connections.items():
            if not conn.state:
                continue
            in_node = sort_conn_list[i-1][0] - 1
            out_node = sort_conn_list[i-1][1] - 1
            weigh = self.find_weigh(net, in_node+1, out_node+1)
            if in_node < self.number_of_in:
                x = data[in_node] * weigh
            else:
                if (np.sum(sum_matrix[in_node])) == 0:
                    sort_conn_list.append(sort_conn_list.pop(i-1))
                else:
                    x = np.sum(sum_matrix[in_node]) * weigh
            sum_matrix[out_node][in_node] = self.sigmoid(x)

        out1 = self.sigmoid(np.sum(sum_matrix[self.number_of_out + self.number_of_in - 2]))

        return out1, data[-1:]

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def sort_connections(net):
        conn_list = []
        for (_, conn) in net.connections.items():
            conn_list.append([conn.input_n, conn.output])
        conn_list.sort()
        return conn_list

    @staticmethod
    def find_weigh(net, in_node, out_node):
        for (_, conn) in net.connections.items():
            if conn.input_n == in_node and conn.output == out_node:
                return conn.weight
