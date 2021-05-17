from Genes import NodeType, Node, Connections
import random
from copy import deepcopy


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

    def add_connection(self, connection):
        self.connections[connection.innovation] = connection

    def add_node(self, node):
        self.nodes[node.id] = node

    def mutate_node(self):
        conn = random.choice(list(self.connections.values()))
        inp = self.nodes[conn.inp]
        out = self.nodes[conn.out]

        conn.state = False

        new = Node(NodeType.hidden, self.node_innovations())
        to_new = Connections(inp.id, new.id, 1.0, True, self.connections_innovations())
        from_new = Connections(new.id, out.id, conn.weight, True, self.connections_innovations())

        self.add_node(new)
        self.add_connection(to_new)
        self.add_connection(from_new)

    def mutate_weights(self):
        for conn in self.connections.values():
            if random.random() < 0.5:
                conn.weight = conn.weight * random.random()
            else:
                conn.weight = random.random()

    @staticmethod
    def crossover(parent_a, parent_b):
        child = Genome()

        for(_, parent_node) in parent_a.nodes.items():
            child.add_node(deepcopy(parent_node))

        for(_, parent_conn) in parent_a.connections.items():
            if parent_conn.innovation in parent_b.connections:
                if random.random() < 0.5:
                    child_conn = deepcopy(parent_conn)
                else:
                    child_conn = deepcopy(parent_b.connections[parent_conn.innovation])
                child.add_connection(child_conn)
            else:
                child.add_connection(deepcopy(parent_conn))

        return child
