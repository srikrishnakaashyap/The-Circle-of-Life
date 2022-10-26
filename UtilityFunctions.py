import math
import random
import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np

class Utility:
    @staticmethod
    def floydWarshal(graph, size):

        dist = [[math.inf for i in range(len(graph[0]))] for j in range(len(graph))]

        path = [[-1 for i in range(size)] for j in range(size)]

        for i in range(len(graph)):
            dist[i][i] = 0

        for i in range(size):
            for j in range(size):
                if graph[i][j] == 1:
                    dist[i][j] = 1
                    dist[j][i] = 1


        # print("--------------------dist--------------")
        # Utility.printGrid(dist)
        for k in range(size):
            for i in range(size):
                for j in range(size):

                    if dist[i][k] == math.inf or dist[k][j] == math.inf:
                        continue

                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        dist[j][i] = dist[i][k] + dist[k][j]

        # print("--------------------dist--------------")
        # Utility.printGrid(dist)

        return path, dist

    @staticmethod
    def movePredator(agentPos, predPos, path):
        # print(path[predPos][agentPos],"test path")
        return path[predPos][agentPos]

    @staticmethod
    def movePredatorWithoutPath(agentPos, predPos, graph, dist):
        neighbours = Utility.getNeighbours(graph, predPos)
        agentNeighbourDistance = {}

        for i in range(len(neighbours)):
            agentNeighbourDistance[neighbours[i]] = dist[neighbours[i]][agentPos]

        return sorted(agentNeighbourDistance.items(), key=lambda x: x[1])[0][0]

    @staticmethod
    def movePredator_dum(predPos, graph, dist):
        moves = []
        minmovedist = 99999999
        minmove = 9999999
        for i in range(len(graph[predPos])):
            if graph[predPos][i] == 1:
                if dist[predPos][i] < minmovedist:
                    minmovedist = dist[predPos][i]
                    minmove = i
        return minmove

    @staticmethod
    def getNeighbours(graph, start):
        neighbours = []

        for index, elem in enumerate(graph[start]):
            if elem == 1:
                neighbours.append(index)

        return neighbours

    @staticmethod
    def movePrey(preyPos, graph):
        moves = [preyPos]
        for i in range(len(graph[preyPos])):
            if graph[preyPos][i] == 1:
                moves.append(i)
        return random.choice(moves)

    @staticmethod
    def printGrid(grid):
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                print(grid[row][col], end=", ")
            print()

    @staticmethod
    def visualizeGrid(graph,agentPos,predPos,preyPos):
        ngraph=np.array(graph)
        rows, cols = np.where(ngraph == 1)
        edges = zip(rows.tolist(), cols.tolist())
        G=nx.cycle_graph(50)
        G.add_edges_from(edges) 
        color_map = []
        for node in G:
            if node == agentPos:
                color_map.append('blue')
            elif node == predPos: 
                color_map.append('red')
            elif node == preyPos: 
                color_map.append('yellow')
            else:
                color_map.append('grey')
        pos=nx.circular_layout(G)
        ax=plt.gca()
        ax1=plt.gcf()
        ax1.set_size_inches(17,17)
        for edge in G.edges():
            source, target = edge
            rad = 0.8
            arrowprops=dict(lw=1,arrowstyle="-",color='black',connectionstyle=f"arc3,rad={rad}",linestyle= '-',alpha=0.6,)
            ax.annotate("",xy=pos[source],
                        xytext=pos[target],
                        arrowprops=arrowprops
                    )
        nx.draw(G, pos, font_size=15,node_size=1000, node_color=color_map,with_labels=True,font_family="sans-serif", width=0)
        # plt.figure(figsize=(10,10))
        plt.show()
        # plt.pause(9)

