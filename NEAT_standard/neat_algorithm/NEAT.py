from data_structures.sorted_set import SortedSet
from NEAT_standard.genome.genes_types import ConnectionGene, NodeGene
from NEAT_standard.genome.genome import Genome


class NEAT:
    __all_nodes: SortedSet[NodeGene]
    __all_connections: dict[ConnectionGene, int]
    __all_individuals: SortedSet # individuals
    __all_species: SortedSet # species
    __input_size: int
    __output_size: int
    __max_individual: int

    def __init__(self, input_size: int, output_size: int, max_individuals: int) -> None:
        self.reset_NEAT(input_size, output_size, max_individuals)
        

    
    
    def create_new_connection(self) -> ConnectionGene:
        pass

    def get_connection(self, node1 : NodeGene, node2: NodeGene) -> ConnectionGene:
        connection : ConnectionGene = ConnectionGene(node1, node2)
        if connection in self.__all_connections:
            connection.innovation_number(self.__all_connections.get(connection))
        else:
            connection.innovation_number(len(self.__all_connections))
            self.__all_connections[connection] = connection.innovation_number
        

    def create_new_genome(self) -> Genome:
        g : Genome =  Genome()
        for i in range(self.__input_size + self.__output_size):
            g.nodes.add_sorted(self.get_node(i))
        return g



    def create_new_node(self) -> NodeGene:
        node_gene : NodeGene =  NodeGene(self.__all_nodes.size())
        self.__all_nodes.add_sorted(node_gene)
        return node_gene
    
    def get_node(self, idx: int) -> NodeGene:
        if idx < self.__all_nodes.size():
            #return self.__all_nodes[idx]
            return NodeGene(idx)   #UWAGA TUTAJ MOZE BYC ROZNICA plus jeszcze z indexami miedzu ta klasa a genomem, neat, genetypa do porwonania
        else:
            return self.create_new_node()

   

    def reset_NEAT(self, input_size: int, output_size: int, max_individuals: int):

        self.__max_individual = max_individuals
        self.__output_size = output_size
        self.__input_size = input_size
        self.__all_connections.clear()
        self.__all_nodes.clear()
        self.__all_individuals.clear()
        self.__all_species.clear()


        # to creat new NEAT we need to create node for every input layer and also one node for every output layer. So the first
        for i in range(input_size):
            node_input: NodeGene = self.create_new_node()
            node_input.x(0.1)
            node_input.y((i + 1)/(input_size + 1))

        for i in range(output_size):
            node_output : NodeGene = self.create_new_node()
            node_output.x(0.9)
            node_output.y((i+1)/(output_size + 1))




