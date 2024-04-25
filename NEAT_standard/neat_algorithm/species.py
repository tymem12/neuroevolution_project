from NEAT_standard.neat_algorithm.individual import Individual
from data_structures.sorted_set import SortedSet

class Specie:
    __individuals : SortedSet[Individual]
    __representative : Individual
    __score : float

    def __init__(self, repr : Individual):
        self.__representative = repr
        self.__individuals = SortedSet(lambda ind : ind.score) # storing using score ???
        self.__representative.specie(self)
        self.__individuals.add_sorted(self.__representative)
        
    @property
    def individuals(self) -> SortedSet[Individual]:
        return self.__individuals

    @individuals.setter
    def individuals(self, individuals : SortedSet[Individual]):
        self.__individuals = individuals

    @property
    def representative(self) -> Individual:
        return self.__representative
    
    @representative.setter
    def represenative(self, representative : Individual):
        self.__representative = representative

    @property
    def score(self) -> float:
        return self.__score 
    
    @score.setter
    def score(self, score : float):
        self.__score = score