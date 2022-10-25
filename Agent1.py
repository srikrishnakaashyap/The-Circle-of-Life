from GenerateGraph import GenerateGraph

import random
from UtilityFunctions import Utility


class Agent1:
    def __init__(self):
        self.generateGraph = GenerateGraph()

    def moveAgent(self, agentPos, preyPos, predPos, graph, dist):

        agentNeighbours = Utility.getNeighbours(graph, agentPos)

        neighboursPreyDistance = []
        neighboursPredatorDistance = []

        currPreyDist = dist[agentPos][preyPos]
        currPredDist = dist[agentPos][predPos]

        for index, elem in enumerate(agentNeighbours):
            neighboursPreyDistance.append(dist[elem][preyPos])
            neighboursPredatorDistance.append(dist[elem][predPos])

        options = []
        for i in range(len(neighboursPredatorDistance)):
            if (
                neighboursPreyDistance[i] < currPreyDist
                and neighboursPredatorDistance[i] > currPredDist
            ):
                options.append(agentNeighbours[i])

        # Break ties by choosing optimal choice for agent 2
        if len(options) > 0:
            return random.choice(options)

        for i in range(len(neighboursPredatorDistance)):
            if (
                neighboursPreyDistance[i] < currPreyDist
                and neighboursPredatorDistance[i] == currPredDist
            ):
                options.append(agentNeighbours[i])

        if len(options) > 0:
            return random.choice(options)

        for i in range(len(neighboursPredatorDistance)):
            if (
                neighboursPreyDistance[i] == currPreyDist
                and neighboursPredatorDistance[i] > currPredDist
            ):
                options.append(agentNeighbours[i])

        if len(options) > 0:
            return random.choice(options)

        for i in range(len(neighboursPredatorDistance)):
            if (
                neighboursPreyDistance[i] == currPreyDist
                and neighboursPredatorDistance[i] == currPredDist
            ):
                options.append(agentNeighbours[i])

        if len(options) > 0:
            return random.choice(options)

        for i in range(len(neighboursPredatorDistance)):
            if neighboursPredatorDistance[i] > currPredDist:
                options.append(agentNeighbours[i])

        if len(options) > 0:
            return random.choice(options)

        for i in range(len(neighboursPredatorDistance)):
            if neighboursPredatorDistance[i] == currPredDist:
                options.append(agentNeighbours[i])

        if len(options) > 0:
            return random.choice(options)

        return agentPos

    def agent1(self, graph, path, dist, agentPos, preyPos, predPos, runs=100):
        while runs > 0:
            print(agentPos,preyPos,predPos,"test")
            if agentPos == predPos:
                return False, 3

            if agentPos == preyPos:
                return True, 0

            # move agent
            agentPos = self.moveAgent(agentPos, preyPos, predPos, graph, dist)

            # check pred
            if agentPos == predPos:
                return False, 4

            # check prey
            if agentPos == preyPos:
                return True, 1

            # move prey
            preyPos = Utility.movePrey(preyPos, graph)

            if agentPos == preyPos:
                return True, 2

            # move predator
            #predPos = Utility.movePredator(agentPos, predPos, path)
            predPos = Utility.movePredator_dum(predPos, graph,dist)

        runs -= 1

        return False, 5

    def executeAgent(self, size):

        graph, path, dist = self.generateGraph.generateGraph(size)

        agentPos = random.randint(0, size - 1)
        preyPos = random.randint(0, size - 1)
        predPos = random.randint(0, size - 1)

        result, line = self.agent1(graph, path, dist, agentPos, preyPos, predPos)
        # print(self.agent1(graph, path, dist, agentPos, preyPos, predPos))
        print(result, line)

        return result


if __name__ == "__main__":

    agent1 = Agent1()

    agent1.executeAgent(20)
