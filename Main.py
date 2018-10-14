import time

import FunctionsDraw
from Model import Network

# The list of networks to draw in the same graph
network_list=[]


style = FunctionsDraw.Style()

user_input = input("Number of different networks to draw (1 <= networks < "+str(len(style.colors)+1) +"):")
try:
    networks_nb = int(user_input)
except ValueError:
    print("Number of different networks is supposed to be an integer")
    exit(-1)

user_input = input("Number of nodes added during the experiment (1000 <= nodes <= 10000):")
try:
    nodes_added = int(user_input)
except ValueError:
    print("Number of nodes added is supposed to be an integer")
    exit(-1)

if nodes_added < 1000 or nodes_added > 10000:
    print("Number of nodes added is supposed to be between 1000 and 10000")
    exit(-1)

graph_nb = 1
m0_list = []

for count in range(0,networks_nb):
    user_input = input("Number of initial nodes (m0) for graph "+str(graph_nb)+":")
    graph_nb = graph_nb+1
    try:
        initial_nodes_nb = int(user_input)
    except ValueError:
        print("Number of initial nodes is supposed to be an integer")
        exit(-1)

    if m0_list.__contains__(initial_nodes_nb):
        print(str(initial_nodes_nb)+" is already planned to be drawn, ignoring it")
    else:
        m0_list.append(initial_nodes_nb)

start = time.time()

m0_list.sort()
for m0 in m0_list:
    # Initialize the network with a certain number of nodes
    network = Network(m0)
    # Add additional nodes
    for node_to_add in range(0, nodes_added):
        network.add_node()
    network_list.append(network)

network_creation_time = time.time()
print("Network creation Time "+str(network_creation_time - start)+" seconds")

# Call the drawing utility
FunctionsDraw.FunctionsDraw.draw_graph(network_list)

end = time.time()
print("PNG Generation Time "+str(end-network_creation_time)+" seconds")

print("Total Time "+str(end-start)+" seconds")
