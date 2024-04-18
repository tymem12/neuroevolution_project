from NEAT_standard.genome.gene_neat import GeneNEAT
from __future__ import annotations

class NodeGene(GeneNEAT):

    #that is first idea to know which node belongs to which layer (x,y) parameters. We can diffrentiate which node
    __x : float
    __y : float



    def __init__(self, innovation_number: int) -> NodeGene:
        super().__init__(innovation_number)


    def __eq__(self, other:NodeGene) -> bool:
        return self.innovation_number == other.innovation_number
    
    def __str__(self) -> str:
        return f'node gene: {self.innovation_number}'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def x(self)-> float:
        return self.__x
    
    @x.setter
    def x(self, x: float):
        self.__x = x


    @property
    def y(self)-> float:
        return self.__y
    
    @y.setter
    def y(self, y: float):
        self.__y = y





class ConnectionGene(GeneNEAT):
    __from_node : NodeGene
    __to_node: NodeGene
    __weight: float
    __enable: bool

    def __init__(self, from_node: NodeGene, to_node: NodeGene) -> ConnectionGene:

        # it is worth to give a thought if I want to callculate the innovation numebr in constructor (max_nodes * from.inv + to.inv) and pass it
        # to super constructor or to dont callcualte it and just use dynamic creation 
        self.__from_node = from_node
        self.__to_node = to_node


    def __str__(self):
        return f'Connection node:\n\tfrom node inv: {self.from_node.innovation_number}\n\tto node inv: {self.to_node.innovation_number}\n\t weigh: {self.weight}\n\tenable: {self.enable}'

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: ConnectionGene) -> bool:
        return self.from_node == other.from_node and self.to_node == other.to_node
    

    
    @property
    def from_node(self) -> NodeGene:
        return self.__from_node
    
    @from_node.setter
    def from_node(self, from_node: NodeGene):
        self.__from_node = from_node

    
    @property
    def to_node(self) -> NodeGene:
        return self.__to_node
    
    @to_node.setter
    def to_node(self, to_node: NodeGene):
        self.__to_node = to_node

    @property
    def weight(self)-> float:
        return self.__weight
    
    @weight.setter
    def weight(self, weight: float):
        self.__weight = weight

    @property
    def enable(self) -> bool:
        return self.__enable
    
    @enable.setter
    def enable(self, enable: bool):
        self.__enable = enable
        



            