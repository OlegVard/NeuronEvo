import random
from Genome import Genome
from Genes import Connections, Node, NodeType
from Data import get_data
import math


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
        data = self.data[self.data_iter]
        if self.data_iter > 500:
            self.data_iter = 0
        sum_matrix = [0.0] * len(net.nodes)
        data_iter = 0
        for i in range(len(net.nodes)):
            sum_matrix[i] = [0.0] * len(net.nodes)
        previous_node = -1
        for (i, conn) in net.connections.items():
            if not conn.state:
                continue
            in_node = conn.input_n - 1
            out_node = conn.output - 1
            if in_node < self.number_of_in and in_node != previous_node:
                x = data[data_iter] * conn.weight
                data_iter += 1
            elif in_node < self.number_of_in and in_node == previous_node:
                x = data[data_iter] * conn.weight
            else:
                x = sum(sum_matrix[in_node]) * conn.weight
            previous_node = in_node
            sum_matrix[out_node][in_node] = self.sigmoid(x)

        out1 = self.sigmoid(sum(sum_matrix[self.number_of_out + self.number_of_in - 2]))
        out2 = self.sigmoid(sum(sum_matrix[self.number_of_out + self.number_of_in - 1]))

        # self.back_propagation(net, sum_matrix, out1, out2)
        return out1, out2, data[-2:]

    def back_propagation(self, net, sum_matrix, out1, out2):
        lr_speed = 0.001    # weigh + correction * weigh_out * (1-last_act) * lr_speed
        result_data = self.data[-2:]
        error_1 = result_data[0] - out1
        correction_1 = error_1/out1
        error_2 = result_data[1] - out2
        correction_2 = error_2/out2
        index_list1 = []
        index_list2 = []
        for i in range(len(sum_matrix)):
            if sum_matrix[self.number_of_out+self.number_of_in - 2][i] != 0.0:
                index_list1.append(i + 1)
            if sum_matrix[self.number_of_out+self.number_of_in - 1][i] != 0.0:
                index_list2.append(i + 1)

        for (_, conn) in net.connections.items():
            if conn.input_n in index_list1 and conn.output == self.number_of_out + self.number_of_in - 1:
                conn.weight = conn.weight + correction_2 * out1 * (1 - out1) * lr_speed
            if conn.input_n in index_list2 and conn.output == self.number_of_out + self.number_of_in:
                conn.weight = conn.weight + correction_2 * out2 * (1 - out2) * lr_speed
        if len(net.nodes) == self.number_of_in + self.number_of_out:
            return
        else:
            correction = (correction_1 + correction_2) / 2
            count_of_hidden = len(net.nodes) - self.number_of_in - self.number_of_out
            index_list3 = []
            for i in range(count_of_hidden):
                temp_list = []
                for j in range(len(sum_matrix)):
                    if sum_matrix[self.number_of_out + self.number_of_in + i][j] != 0.0:    # косяк
                        temp_list.append(j+1)
                index_list3.append(temp_list)

            for i in range(len(index_list3)):
                for (_, conn) in net.connections.items():
                    if conn.input_n in index_list3[i] and conn.output > self.number_of_out + self.number_of_in:
                        out3 = self.sigmoid(sum(sum_matrix[self.number_of_out + self.number_of_in + i]))
                        conn.weight = conn.weight + correction * out3 * (1 - out3) * lr_speed
            return

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))
