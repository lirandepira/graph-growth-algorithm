import random
import collections
from fractions import Fraction

"""
Class Network: It models a network
  Composed of:
    - A list of object nodes
    - A list of object edges
    - m0: the number of initial nodes for the network (later on also the number of edge per new nodes)
"""


class Network:
    """
    Constructor:
      - initial_nodes_nb: the initial number of nodes that will be added to the network (m0)
    """
    def __init__(self, initial_nodes_nb):
        # Will be used to label each node uniquely
        self.node_label = 1
        # m0 is the number of edges per node
        # when adding node later on
        # we consider it stays equal to
        # the number of initial nodes
        self.m0 = initial_nodes_nb
        # List of existing nodes in the network
        self.node_list = []
        # List of existing edges in the network
        self.edge_list = []
        # t is the time evolution index for average degree
        self.t = 0

        # Average degree history needs to be recorded every
        # Time a node is added.
        # The key to this ordered dictionary is time t
        # The value is the average degree at that time
        self.average_degree_history = collections.OrderedDict()

        # Node initialization: we need to create initial_nodes_nb nodes
        # Constructor first initialize all the nodes needed for the start
        for count in range(0, initial_nodes_nb):
            new_node = Node(self.node_label)
            # Ensure we increment the label after adding the node
            self.node_label = self.node_label + 1
            self.node_list.append(new_node)

        # Now that we have every nodes in the graph,
        # We need to build edges to link them
        # let's browse the list of nodes
        # and link each node with the previous one
        # so that no node is isolated
        previous_node = None
        for node in self.node_list:
            if previous_node is not None:
                edge = Edge(previous_node, node)
                self.edge_list.append(edge)
            # set previous node to current node
            # to link it to the next one
            previous_node = previous_node

        # Calculate average degree for t = 0
        self.calculate_average_degree()

    """
    Adding a certain number of edges to a node
    Edges will be randomly created
    This function is only called after initialization
    of the network
    """
    def add_random_edges(self, node, number_of_edges):
        possible_nodes= []
        # First construct the list of possible nodes
        # That can be linked to that node
        # Before we were using a copy of the list of nodes
        # in the list possible_nodes.
        # That was working but if the list was big
        # The creation time was exponentional
        # Now we just pick m0 + 1 random nodes
        # (+1 just in case we picked up node in it
        for edge_count in range(0, number_of_edges+1):
            possible_node = random.choice(self.node_list)
            possible_nodes.append(possible_node)

        # The list cannot contain the node itself of course
        # Remove uses the redefined equals method for nodes
        # If a node label is equal to another node label
        # then the nodes are equal
        if possible_nodes.__contains__(node):
            possible_nodes.remove(node)

        # We need to add the remaining edges to random nodes
        for countEdge in range(0, number_of_edges):
            # possible nodes is already randomized
            # just take the first element and then remove it from the list
            linked_node = possible_nodes[0]
            edge = Edge( node, linked_node)
            self.edge_list.append(edge)
            # the linked node cannot be picked up for another link
            possible_nodes.remove(linked_node)

    """
    Add a nodes (to use only after constructor)
    When adding a node we need to automatically
    Add m0 edges to it
    """
    def add_node(self):
        # Create a node
        new_node = Node(self.node_label)
        self.node_list.append(new_node)
        self.node_label = self.node_label + 1
        # Build m0 edges from that node
        self.add_random_edges(new_node, self.m0)
        # Take a snapshot of the average degree at that very moment
        # The snapshot will be used when drawing the plot
        self.calculate_average_degree()

    """
    Calculate degree distribution
    Of a network (used to draw the degree distribution function)
    """
    def get_degree_distribution(self):
        degree_distribution = {}
        # The total number of nodes is used in the calculation for the degree distribution
        number_of_nodes = len(self.node_list)
        # Inspect every nodes in the network to retrieve how many edges they have
        for node in self.node_list:
            number_of_edges = len(node.edge_list)
            # current count for degree x is either the existing count or 0
            count = degree_distribution.setdefault(number_of_edges, Fraction(0))
            # degree distribution for degree x is:
            # the current count (existing/total + 1/total)
            # We use fraction here as it is better displayed on the graph
            degree_distribution[number_of_edges] = count+Fraction(1, number_of_nodes)
        # Once every nodes have been browsed
        # Degree distribution is calculated
        # We return a sorted by key dictionary to get
        # degree_distribution[1]
        # the degree_distributon[2] and so on in order for plotting the graph
        return collections.OrderedDict(sorted(degree_distribution.items()))

    """
    The average degree at a time t is equal to the total number of
    edges * 2 divided by the number of nodes
    """
    def calculate_average_degree(self):
        self.average_degree_history[self.t] = Fraction(2*len(self.edge_list),len(self.node_list))
        # Increment t to get it ready for the next snapshot
        self.t = self.t+1


"""
Class Node: It modelizes a node
  Composed of:
    - A unique label (incremented int)
    - A list of edge that comes out of that node
        Note that the list of edges is automatically filled
        when creating an edge
"""


class Node:

    """
    Constructor:
      - label: the unique label for the node
    """
    def __init__(self, label):
        self.label = label
        self.edge_list = []

    """
    Equals function: used to compare node with each others
    And therefore used when removing nodes from list
    Or checking whether a node is equal to another
    """
    def __eq__(self, other):
        # A node is equal to another node only if its
        # unique label is the same
        return self.label == other.label

    """
    Add an edge to a node.
    This function is automatically called when we create an edge
    It allows to know automatically the list of edges that link that nodes
    """
    def add_edge(self, edge):
        self.edge_list.append(edge)


"""
Class Edge: It modelizes an edge
  Composed of:
    - Two nodes
"""


class Edge:

    """
        Constructor:
          - node1: the first node object to link
          - node2: the second node object to link
    """
    def __init__(self, node1, node2):
        self.node1 = node1
        # Automatically inform node 1 it is linked with this edge
        self.node1.add_edge(self);
        self.node2 = node2
        # Automatically inform node 2 it is linked with this edge
        self.node2.add_edge(self);

    """
    Equals function: used to compare edges with each others
    And therefore used when removing edges from list
    Or checking whether a edges is equal to another (basically does it already exists?)
    """
    def __eq__(self, other):
        # An edge is equal to another edge if it links to the same nodes
        # The statements will use the equal function of the nodes
        # (if a node has the same label as another node it's the same)
        if other.node1 == self.node1:
            return other.node2 == self.node2
        elif other.node2 == self.node1:
            return other.node1 == self.node2
        return False
