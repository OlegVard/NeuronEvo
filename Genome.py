from Genes import NodeType, Node, Connections
import random
from graphviz import Digraph
from copy import deepcopy
import os

os.environ["PATH"] += os.pathsep + "C:/Program Files/Graphviz/bin"


class Genome:
    def __init__(self):
        self.connections = {}
        self.nodes = {}
        self.conn_innovation = 0
        self.node_innovation = 0

    def connections_innovations(self):
        temp = self.conn_innovation
        self.conn_innovation += 1
        return temp

    def node_innovations(self):
        temp = self.node_innovation
        self.node_innovation += 1
        return temp

    def add_connection(self, conn):
        self.connections[conn.innovation] = conn

    def add_node(self, node):
        self.nodes[node.id] = node

    def mutate_node(self):
        conn_index = random.randint(1, len(self.connections))
        conn = self.connections.get(conn_index)
        while conn is None:
            conn_index = random.randint(1, len(self.connections))
            conn = self.connections.get(conn_index)

        inp = self.nodes[conn.input_n]
        out = self.nodes[conn.output]
        conn.state = False

        new = Node(NodeType.Hidden, self.node_innovations())
        to_new = Connections(inp.id,
                             new.id,
                             conn.weight * round(random.random(), 2),
                             True,
                             self.connections_innovations())
        from_new = Connections(new.id,
                               out.id,
                               conn.weight,
                               True,
                               self.connections_innovations())

        self.add_node(new)
        self.add_connection(to_new)
        self.add_connection(from_new)

    def mutate_connection(self):
        index_1 = random.choice(list(self.nodes.keys()))
        index_2 = random.choice(list(self.nodes.keys()))

        while index_1 == index_2:
            index_2 = random.choice(list(self.nodes.keys()))

        node_1 = self.nodes[index_1]
        node_2 = self.nodes[index_2]

        if node_1.type == NodeType.Input and node_2.type == NodeType.Input:
            index_2 = random.randint(10, len(self.nodes))
            node_2 = self.nodes[index_2]

        while node_1.type == NodeType.Output and node_2.type == NodeType.Output:
            index_1 = random.randint(1, len(self.nodes))
            node_1 = self.nodes[index_1]
            while index_1 == 10 or index_1 == 11:
                index_1 = random.randint(1, len(self.nodes))


        if node_1.type == NodeType.Hidden and node_2.type == NodeType.Input:
            node_1, node_2 = node_2, node_1

        if node_1.type == NodeType.Output and node_2.type == NodeType.Hidden:
            node_1, node_2 = node_2, node_1

        if node_1.type == NodeType.Output and node_2.type == NodeType.Input:
            node_1, node_2 = node_2, node_1

        for (_, conn) in self.connections.items():
            if (conn.input_n == node_1.id and conn.output == node_2.id) or \
                    (conn.input_n == node_2.id and conn.output == node_1.id):
                return

        self.add_connection(Connections(
            node_1.id,
            node_2.id,
            round(random.random(), 2),
            True,
            self.connections_innovations(),
        ))

    @staticmethod
    def crossover(parent_a, parent_b):
        child = Genome()
        child.node_innovation = parent_a.node_innovation
        child.conn_innovation = parent_a.conn_innovation

        for (_, parent_node) in parent_a.nodes.items():
            child.add_node(deepcopy(parent_node))

        for (_, parent_conn) in parent_a.connections.items():
            child.add_connection(deepcopy(parent_conn))

        for (_, parent_conn) in parent_b.connections.items():
            if parent_conn.innovation in parent_a.connections:
                if not child.already_connected(parent_conn):
                    if parent_conn.output in child.nodes.keys():
                        if parent_conn.input_n in child.nodes.keys():
                            if random.random() < 0.5:
                                child.add_connection(parent_conn)

        child.is_connected()

        return child

    def render(self, filename):
        dot = Digraph()

        for (i, node) in self.nodes.items():
            dot.node(str(i))

        for (i, conn) in self.connections.items():
            if conn.state:
                dot.edge(str(conn.input_n), str(conn.output), "{:.0f}, {:.2f}".format(conn.innovation, conn.weight))

        dot.render(filename)

    def already_connected(self, conn):
        flag = False
        if len(self.connections) == 0:
            return flag
        for (_, connection) in self.connections.items():
            if conn.input_n == connection.input_n and conn.output == connection.output:
                flag = True
                break
            else:
                flag = False
        return flag

    def is_connected(self):
        for (_, node) in self.nodes.items():
            flag_in = False
            flag_out = False
            for (_, conn) in self.connections.items():
                if node.type == NodeType.Input:
                    if conn.input_n == node.id:
                        flag_in = True
                        break
                elif node.type == NodeType.Output:
                    if conn.output == node.id:
                        flag_out = True
                        break
                else:
                    if conn.input_n == node.id:
                        flag_in = True
                    if conn.output == node.id:
                        flag_out = True
                        if flag_in:
                            break
            if node.type == NodeType.Input:
                if not flag_in:
                    self.add_connection(Connections(node.id,
                                                    random.randint(10, len(self.nodes)),
                                                    round(random.random()),
                                                    True,
                                                    self.connections_innovations()))
            elif node.type == NodeType.Output:
                if not flag_out:
                    index_in = random.randint(1, len(self.nodes))
                    while index_in == 11 or index_in == 10:
                        index_in = random.randint(1, len(self.nodes))
                    self.add_connection(Connections(index_in,
                                                    node.id,
                                                    round(random.random()),
                                                    True,
                                                    self.connections_innovations()))
            else:
                if not flag_in and not flag_out:
                    index_in = random.randint(1, 9)
                    index_out = random.randint(10, len(self.nodes))
                    self.add_connection(Connections(index_in,
                                                    node.id,
                                                    round(random.random()),
                                                    True,
                                                    self.connections_innovations()))
                    self.add_connection(Connections(node.id,
                                                    index_out,
                                                    round(random.random()),
                                                    True,
                                                    self.connections_innovations()))
