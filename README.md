## graph-growth-algorithm
Remodel of the Barabasi-Albert algorithm, which takes into account only the principle of growth in a graph.


### Description of the algorithm
The Barabasi-Albert (BA) algorithm generates scale-free networks (graphs). It starts with m0 nodes,
and a number of links arbitrarily chosen so that each node has at least one link.
It relies on two main principles:
1. **Growth**
At each time step a new node is added with m (m ≤ m0) links that connect the new node to m nodes already in the network.
2. **Preferential Attachment**
The probability that a link of the new node connects to node i depends on the degree of the node.

In the 'remodel' of the algorithm, only the **growth** mechanism is taken into account.

### Architecture and Modeling
The process of thought can be described in the following steps:

1. Network initialization:
Using a for loop create a random number of nodes (m0) and add them to the list of nodes by labels.
Browse the list of nodes, check if there is a previous node, and add a link with the next node.
This way we ensure there are no isolated nodes.

2. Iterative process begins:
When adding a new node, m0 links are added to it.
The links are randomly added to the nodes (no preferential attachment).

3. Iterative process ends:
The algorithm accepts 1000 to 10000 nodes.
It ends when N nodes have been added.

4. Degree distribution:
Degree distribution is calculated after the network creation.

5. Time evolution of the average degree:
Average degree is calculated continuously ever since the creation of the network.

### User input:
- Number of different networks to draw (1 <= networks < 8):
- Number of nodes added during the experiment (1000 <= nodes <= 10000):
- Number of initial nodes (m0) for graph 1:
- Number of initial nodes (m0) for graph 2:
- Number of initial nodes (m0) for graph 3:
### Algorithm output:
- Network creation Time 1.25185489655 seconds
- PNG Generation Time 11.3400251865 seconds
- Total Time 12.5918800831 seconds
