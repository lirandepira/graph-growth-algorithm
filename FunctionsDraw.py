import random
import matplotlib
from datetime import datetime
# Use only due to MACOS issue
# Remove on other OS
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

"""
Class Style: automatically assigns a combination of colour and marker type
When drawing the different networks
"""


class Style(object):

    def __init__(self):
        self.colors = ['g', 'r', 'c', 'm', 'y', 'k', 'b']
        self.markers = ["8", "o", "v", "s", "*", "+", "x"]

    def get_color(self):
        color = random.choice(self.colors)
        self.colors.remove(color)
        return color

    def get_marker_style(self):
        marker = random.choice(self.markers)
        self.markers.remove(marker)
        return marker


"""
Class FunctionsDraw: contains the static method allowing to plot two graphs:
    - graph1: degree distribution
    - graph2: average degree evolution
"""


class FunctionsDraw(object):

    """
    draw_graph: will plot the 2 graphs based on multiple network which were built before
    """
    @staticmethod
    def draw_graph(network_list):
        style = Style()
        xindex = []
        # Create a figure and ensure
        # It has a high resolution
        # so that the png contains all the details
        fig=plt.figure(1)
        fig.set_size_inches(150,45)
        fig.set_dpi(100)
        # Figure will get 2 graphs
        # one for degree distribution
        # the second for average degree over time
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212)

        # Legend will be added to the graph to know which mark correspond to which m0
        legend = []
        for network in network_list:
            # Decide the unique combination of colour and marker which will be used for the network
            color = style.get_color()
            marker = style.get_marker_style()

            # Plot the degree distribution
            distribution = network.get_degree_distribution()

            # Little trick to get a mark on the x axis only if there is a degree distribution
            # some networks might have no distribution for degree 2
            # but in the end we need to ensure every degree from every network have a tick
            # so we discover every possible degrees
            for key in distribution:
                if not (xindex.__contains__(key)):
                    xindex.append(key)

            # We can simply draw the distribution plot using the scatter function (using points, not lines)
            # we have first the list of x coordinates
            # then their associated y values
            # and finally the color and marker options
            # we draw it on first graph (ax1)
            ax1.scatter(distribution.keys(), distribution.values(), color=color, marker=marker)

            # ax2 is less
            ax2.scatter(network.average_degree_history.keys(), network.average_degree_history.values(), color=color, marker=marker)

            # save the initial number of nodes into the legend list
            legend.append('m0=' + str(network.m0))

        # Now we can sort it by numbers so that the list of ticks is ordered
        # And we set the tix to the first x axis
        xindex.sort()
        ax1.set_xticks(xindex)

        # Set ax1 title and legend
        ax1.set_title("degree distribution")
        ax1.legend(legend,
                   scatterpoints=1,
                   loc='lower left',
                   ncol=3,
                   fontsize=8)

        # Set ax2 title and legend
        ax2.set_title("Average degree over time")
        ax2.legend(legend,
                   scatterpoints=1,
                   loc='lower left',
                   ncol=3,
                   fontsize=8)

        # Sets the figure main title
        fig.suptitle("Parameters: Iterations "+str(max(network_list[0].average_degree_history)))

        # Save the result in a big png (with date and hour)
        plt.savefig('result-'+datetime.now().strftime("%Y%m%d%H%M%S")+".png")
