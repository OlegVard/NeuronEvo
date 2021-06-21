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
        self.conn_innovation = 1
        self.node_innovation = 1
        self.species = 0

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
        while conn is None or not conn.state:
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
                self.mutate_connection()
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

        for conn in parent_a.connections.values():
            try:
                conn2 = parent_b.connections[conn.innovation]
            except KeyError:
                child.add_connection(deepcopy(conn))
            else:
                child.add_connection(Connections(conn.input_n,
                                                 conn.output,
                                                 (conn.weight + conn2.weight) / 2,
                                                 Genome.T_or_F(conn.state, conn2.state),
                                                 conn.innovation))

        return child

    def render(self, filename):
        dot = Digraph()

        for (i, node) in self.nodes.items():
            dot.node(str(i))

        for (i, conn) in self.connections.items():
            if conn.state:
                dot.edge(str(conn.input_n), str(conn.output), "{:.0f}, {:.2f}".format(conn.innovation, conn.weight))

        dot.render(filename)

    @staticmethod
    def T_or_F(a, b):
        if a and b:
            return a
        elif a and not b:
            return a
        elif not a and b:
            return a
        else:
            return b

    @staticmethod
    def types_division(type_a, type_b, num_types):
        c1, c2, c3 = 0.3, 0.3, 0.3
        Bt = 0.20
        for i in range(num_types):
            N = max((len(type_a[i][0].connections), len(type_b.connections)))
            B = (c1 * Genome.excess_genes(type_a[i][0], type_b) +
                 c2 * Genome.disjoint_genes(type_a[i][0], type_b)) / N + \
                c3 * Genome.match_genes(type_a[i][0], type_b)
            if Bt > B:
                type_b.species = i
                return
        type_b.species = num_types + 1

    @staticmethod
    def match_genes(a, b):
        match_gene = 0
        result = 0
        max_a = len(a.connections.keys())
        max_b = len(b.connections.keys())
        max_all = max(max_a, max_b)

        for i in range(max_all + 1):
            if i in a.connections and i in b.connections:
                match_gene += 1
                result += (a.connections[i].weight + b.connections[i].weight) / 2
        return result / match_gene

    @staticmethod
    def disjoint_genes(a, b):
        disjoint_genes = 0

        max_a = len(a.connections.keys())
        max_b = len(b.connections.keys())
        max_all = max(max_a, max_b)

        for i in range(max_all + 1):
            if (i not in a.connections and i in b.connections and max_a > i) or\
                    (i in a.connections and i not in b.connections and max_b > i):
                disjoint_genes += 1

        return disjoint_genes

    @staticmethod
    def excess_genes(a, b):
        excess_genes = 0

        max_a = len(a.connections.keys())
        max_b = len(b.connections.keys())
        indices = max(max_a, max_b)

        for i in range(indices + 1):
            if (i not in a.connections and i in b.connections and max_a < i) \
                    or (i in a.connections and i not in b.connections and max_b < i):
                excess_genes += 1

        return excess_genes
