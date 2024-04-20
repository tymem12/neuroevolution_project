from __future__ import annotations
from typing import Iterable
from data_structures.sorted_set import SortedSet
from NEAT_standard.genome.genes_types import ConnectionGene, NodeGene
from settings.settingsParams import C1,C2,C3


class Genome:
    __connections : SortedSet[ConnectionGene]
    __nodes : SortedSet[NodeGene]

    def distance(self, g2 : Genome) -> float:
        highest_innovation_gene1 : int = self.__connections[-1].innovation_number()
        highest_innovation_gene2 : int = g2.__connections[-1].innovation_number()
        
        # we want ot gave in g1 the bigger innovation number
        g1 = self
        if highest_innovation_gene1 < highest_innovation_gene2:
            g1, g2 = g2, g1

        

        index_g1 : int = 0
        index_g2 : int = 0
        disjoint_genes: int = 0  #that are in one gene but not in another
        weight_diff : float = 0     
        matching_genes : int = 0

        while index_g1 < len(g1.connections()) and index_g2 < len(g2.connections()):
            gene1 : ConnectionGene = g1.connections[index_g1]
            gene2 : ConnectionGene = g2.connections[index_g2]
            in1 : int = gene1.innovation_number()
            in2 : int = gene2.innovation_number()

            if in1 == in2:
                matching_genes += 1
                weight_diff += abs(gene1.weight - gene2.weight)
                index_g1 += 1
                index_g2 += 1
            elif in1 > in2:
                disjoint_genes += 1
                index_g2 += 1
            else:
                disjoint_genes += 1
                index_g1 += 1

        weight_diff /= max(1, matching_genes)
        excess_genes = len(g1.connections) - index_g1


        N :int = min(g1.connections.size(), 1) if N < 20 else N

        return C1 * disjoint_genes / N + C2 * excess_genes / N + C3 * weight_diff


    @property
    def connections(self) -> SortedSet[ConnectionGene]:
        return self.__connections
    
    @connections.setter
    def connections(self, connections: SortedSet[ConnectionGene]):
        self.__connections = connections

    @property
    def nodes(self) -> SortedSet[NodeGene]:
        return self.__nodes
    
    @nodes.setter
    def nodes(self, nodes: SortedSet[NodeGene]):
        self.__nodes = nodes