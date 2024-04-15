from NEAT_standard.genome.gene import Gene

class GeneNEAT(Gene):
    """
    Class for representing a gene in stnadard NEAT algorithm.
    Implementation based on 
    https://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf

    Gene_NEAT is a class that works as abstract class representing general gene.

    params:
    __innovation_number: int    nothing more than id that is necessary to diffrentiate gene nodes and connection nodes.


    
    """
    __innovation_number: int

    def __init__(self, innovation_number: int):
        self.__innovation_number = innovation_number

    @property
    def innovation_number(self) -> int:
        return self.__innovation_number
    

    @innovation_number.setter
    def innovation_number(self, inn_number):
        self.innovation_number = inn_number


    def __str__(self) -> str:
        return f'NEAT gene in: {self.innovation_number}'
    
    def __repr__(self) -> str:
        return self.__str__()