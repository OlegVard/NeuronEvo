from enum import Enum


class NodeType(Enum):
    Input = 0
    Hidden = 1
    Output = 2


class Node:
    def __init__(self, node_type, node_id):
        self.type = node_type
        self.id = node_id


class Connections:
    def __init__(self, input_node, output_node, weight, state, innovation):
        self.input_n = input_node
        self.output = output_node
        self.weight = weight
        self.state = state
        self.innovation = innovation
