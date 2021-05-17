import random


class Neuron:
    def __init__(self, number_of_in, number_of_out, number_of_models):
        self.models = number_of_models
        self.number_of_in = number_of_in
        self.number_of_out = number_of_out
