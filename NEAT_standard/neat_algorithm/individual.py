from __future__ import annotations
from NEAT_standard.genome.genome import Genome
from NEAT_standard.neat_algorithm.species import Specie
from NEAT_standard.callculations.Calculator import Calculator

class Individual:
    __genome : Genome
    __score : float
    __specie : Specie
    __calculator : Calculator


    def __init__(self, calculator : Calculator):
        self.__calculator = calculator
        
    def distance(self, other : Individual) -> float:
        return self.genome.distance(other.genome)

    def mutate(self):
        self.genome.mutate()



    @property
    def genome(self) -> Genome:
        return self.__genome
    
    @genome.setter
    def genome(self, g : Genome):
        self.__genome = g

    @property
    def score(self) -> float:
        return self.__score
    
    @score.setter
    def score(self, score : float):
        self.__score = score

    @property
    def specie(self) -> Specie:
        return self.__specie
    
    @specie.setter
    def specie(self, specie : Specie):
        self.__specie = specie