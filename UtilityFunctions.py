import math
import random


class Utility:
    @staticmethod
    def floydWarshal(graph, size):

        dist = [[math.inf for i in range(len(graph[0]))] for j in range(len(graph))]

        path = [[i for i in range(size)] for j in range(size)]
        # for i in range(size):
        #     for j in range(i,size):
        #         #print(i,j,"test")
        #         if(i<j):
        #             path[i][j]=(i+1)%size
        #             # path[j][i]=(j+1)%size
        #         elif(i>j):
        #             path[i][j]=(i-1)%size
        #             # path[j][i]=(j-1)%size
        #         else:
                    # path[i][j]=i

        for i in range(len(graph)):
            dist[i][i] = 0

        for i in range(size):
            for j in range(size):
                if graph[i][j] == 1:
                    dist[i][j] = 1
                    dist[j][i] = 1
                    # path[i][j] = j
                    # path[j][i] = i

        # print("--------------------dist--------------")
        # Utility.printGrid(dist)
        for k in range(size):
            for i in range(size):
                for j in range(size):
                    if(dist[i][k]== math.inf or dist[k][j]== math.inf):
                        continue
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        dist[j][i] = dist[i][k] + dist[k][j]
                        if(graph[i][k]==1):
                            path[i][j] = k
                        # path[k] = j
                            path[j][i] = k
                    # else:
                    #     if(i<j):
                    #         path[i][j] = i+1
                    #         path[j][i] = i+1
                    #     elif(i>j):
                    #         path[i][j] = i-1
                    #         path[j][i] = i-1
                        # path[k] = i
                        # path[i][k] = k
                        # path[k][i] = i
                        # path[j][k] = k
                        # path[k][j] = j
        print("--------------------dist--------------")
        Utility.printGrid(dist)

        for i in range(len(graph)):
            dist[i][i] = 0
        # for i in range(size):
        #     for j in range(size):
        #         if(graph[i][j]==1):

 
        return path, dist


    @staticmethod
    def movePredator(agentPos, predPos, path):
        # print(path[predPos][agentPos],"test path")
        return path[predPos][agentPos]

    @staticmethod
    def movePredator_dum(predPos, graph,dist):
        moves = []
        minmovedist=99999999
        minmove=9999999
        for i in range(len(graph[predPos])):
            if graph[predPos][i] == 1:
                if(dist[predPos][i]<minmovedist):
                    minmovedist=dist[predPos][i]
                    minmove=i       
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
        # for i in range(len(grid[0])):
        #     print(",".join(i),end="  ")
        # print()
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                print(grid[row][col], end = ", ")
            print()
