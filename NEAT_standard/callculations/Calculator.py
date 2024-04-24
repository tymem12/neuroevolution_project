from abc import ABC, abstractmethod

from NEAT_standard.genome.genome import Genome

class Calculator(ABC):
    """
    Abstract class that will work as the interface. The way of how to calculate the the inputs"""
    __genome : Genome

    @abstractmethod
    def __init__(self, genome : Genome):
        self.__genome = genome

    def create_structure(self):
        pass

    @abstractmethod
    def calculate(self):
        pass
