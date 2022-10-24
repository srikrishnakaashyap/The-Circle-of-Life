import math
import random


class Utility:
    @staticmethod
    def floydWarshal(graph, size):

        dist = [[math.inf for i in range(len(graph[0]))] for j in range(len(graph))]
        # print(dist)
        path = [[i for i in range(size)] for j in range(size)]

        for i in range(len(graph)):
            dist[i][i] = 0

        for i in range(size):
            for j in range(size):
                if graph[i][j] == 1:
                    dist[i][j] = 1
                    path[i][j] = j
                    path[j][i] = i

        for k in range(size):
            for i in range(size):
                for j in range(size):

                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

                        path[i][j] = k
                        # path[k] = j
                        path[j][i] = k
                        # path[k] = i
                        path[i][k] = k
                        path[k][i] = i
                        path[j][k] = k
                        path[k][j] = j

        return path, dist

    @staticmethod
    def movePredator(agentPos, predPos, path):
        return path[predPos][agentPos]

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
