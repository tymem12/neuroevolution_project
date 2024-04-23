import random
import numpy as np
from __future__ import annotations
from typing import Iterable
from data_structures.sorted_set import SortedSet
from NEAT_standard.genome.genes_types import ConnectionGene, NodeGene
from neat_algorithm.NEAT import NEAT
from settings.settingsParams import C1,C2,C3,PROBABILITY_MUTATE_LINK, PROBABILITY_MUTATE_NODE,PROBABILITY_MUTATE_TOGGLE_LINK, PROBABILITY_MUTATE_WEIGHT_RANDOM, PROBABILITY_MUTATE_WEIGHT_SHIFT,WEIGHT_SHIFT_STRENGTH, WEIGHT_RANDOM_STRENGTH



class Genome:
    __connections : SortedSet[ConnectionGene]
    __nodes : SortedSet[NodeGene]
    __neat : NEAT

    def __init__(self, neat: NEAT):
        random.seed(123)
        self.__neat = neat

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

        while index_g1 < g1.connections.size and index_g2 < g2.connections.size():
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

    def mutate(self):
        if PROBABILITY_MUTATE_LINK > random.random():
            self.__mutate_link()
        if PROBABILITY_MUTATE_NODE > random.random():
            self.__mutate_node()
        if PROBABILITY_MUTATE_WEIGHT_SHIFT > random.random():
            self.__mutate_weight_shift()
        if PROBABILITY_MUTATE_WEIGHT_RANDOM > random.random():
            self.__mutate_weight_random()
        if PROBABILITY_MUTATE_TOGGLE_LINK > random.random():
            self.__mutate_link_toggle()

    def __mutate_link(self):
        # create the connection based on the nodes that alreay exists. So lets find the to nodes that are possible to connect and create connection betwwen
        # them  and add weight. But we need to use the x parameter mostly to distinguish shich one is in which layer.


        while True:
            from_node : NodeGene = self.nodes.get_random()
            to_node : NodeGene = self.nodes.get_random()

            # if nodes belongs to the same layer
            if from_node.x == to_node.x:
                continue
            

            # we create the connection with making sure that node from earlier layer is connectet to further layer
            connection : ConnectionGene
            if from_node.x < to_node.x:
                connection = ConnectionGene(from_node, to_node)
            else:
                connection = ConnectionGene(to_node, from_node)

            # if this connection exists already we start again
            if self.connections.contains(connection):
                continue

            # if connection does not exists we inform the NEAT that there is need for reating new Connection and updating the list
            # of all conections, 

            connection = self.neat.get_connection(connection.from_node, connection.to_node)
            connection.weight((np.clip(np.random.normal(0.5, 0.1), 0, 1) * 2 - 1) * WEIGHT_RANDOM_STRENGTH)

            self.connections.add_sorted(connection)
            break

            


    def __mutate_node(self):
        connection : ConnectionGene = self.connections.get_random()
        node_from : NodeGene = connection.from_node
        node_to : NodeGene = connection.to_node
        middle : NodeGene = self.neat.create_new_node()
        middle.x((node_from.x + node_to.x) / 2)
        middle.y((node_from.y + node_to.y) / 2)
        
        connection_f_m : ConnectionGene = self.neat.get_connection(node_from, middle)
        connection_m_t : ConnectionGene = self.neat.get_connection(middle, node_to)

        connection_f_m.weight(1)
        connection_m_t.weight(connection.weight)
        connection_m_t.enable(connection.enable)

        self.connections.remove(connection)
        self.connections.add_sorted(connection_f_m)
        self.connections.add_sorted(connection_m_t)
        self.nodes.add_sorted(middle)

    def __mutate_weight_shift(self):
        connection : ConnectionGene = self.connections.get_random()
        value : float = np.clip(np.random.normal(0.5, 0.1), 0, 1)
        connection.weight(connection.weight + (value * 2 - 1) * WEIGHT_RANDOM_STRENGTH)

    def __mutate_weight_random(self):
        connection : ConnectionGene = self.connections.get_random()
        value : float = np.clip(np.random.normal(0.5, 0.1), 0, 1)
        connection.weight((value * 2 - 1) * WEIGHT_RANDOM_STRENGTH)
    

    def __mutate_link_toggle(self):
        connection : ConnectionGene = self.connections.get_random()
        connection.enable(not connection.enable)

    



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

    @property
    def neat(self) -> NEAT:
        return self.__neat
    
    @neat.setter
    def neat(self, neat : NEAT):
        self.__neat = neat

def crossover(genome1: Genome, genome2: Genome) -> Genome:
    # we assume that genome1.innovation > genome2.innovation
    neat : NEAT = genome1.neat
    new_genome = neat.create_new_genome()

    idx_1: int = 0
    idx_2: int = 0

    while idx_1 < genome1.connections.size() and idx_2 < genome2.connections.size():
        connection1 : ConnectionGene = genome1.connections[idx_1]
        connection2 : ConnectionGene = genome2.connections[idx_2]
        innv_1 : int = connection1.innovation_number
        innv_2 : int = connection2.innovation_number

        if innv_1 == innv_2:
            new_genome.connections.add_sorted(connection1.copy() if random.random() > 0.5 else connection2.copy)
            idx_1 += 1
            idx_2 += 1
        elif innv_1 > innv_2:
            new_genome.connections.add_sorted(connection2.copy())  # test it
            idx_2 += 1
        else:
            new_genome.connections.add_sorted(connection1.copy())  # test it
            idx_1 += 1

    while idx_1 < genome1.connections.size():
        connection : ConnectionGene = genome1.connections[idx_1]
        new_genome.connections.add_sorted(connection.copy())
        idx_1 += 1

    for connection in new_genome.connections:
        new_genome.nodes.add_sorted(connection.from_node)
        new_genome.nodes.add_sorted(connection.to_node)

    return new_genome



        


