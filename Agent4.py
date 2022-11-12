from GenerateGraph import GenerateGraph

import random
from UtilityFunctions import Utility
import time
from copy import copy


class Agent4:
    def __init__(self):
        self.generateGraph = GenerateGraph()

    def findNodeToScout(self):
        options = []
        maxiValue = max(self.beliefArray)

        for i, j in enumerate(self.beliefArray):
            if j == maxiValue:
                options.append(i)

        if len(options) > 0:
            return random.choice(options)

    def dfs(self, currNode, visited, graph, degree, newBeliefArray):

        neighbours = Utility.getNeighbours(graph, currNode)

        for j in neighbours:
            self.beliefArray[currNode] += newBeliefArray[j] * (1 / (degree[j] + 1))
            if j not in visited:
                visited.add(j)
                self.dfs(j, visited, graph, degree, newBeliefArray)

    def updateBeliefArray2(self, agentPos, preyPos, predPos, graph, dist, degree):

        nextTimeStepBeliefArray = [0 for i in range(len(self.beliefArray))]

        scoutNode = self.findNodeToScout()

        if scoutNode == preyPos:
            nextTimeStepBeliefArray[scoutNode] = 1
        else:

            scoutNodeNeighbours = Utility.getNeighbours(graph, scoutNode)

            currentNodeNeighbours = Utility.getNeighbours(graph, agentPos)

            for i in range(len(nextTimeStepBeliefArray)):

                piNext = 0

                iNeighbours = Utility.getNeighbours(graph, i)

                iNeighbours.append(i)

                for j in iNeighbours:
                    piNext += self.beliefArray[j] / (degree[j] + 1)

                # nextProb = 0

                mulFactor = 1
                if i in scoutNodeNeighbours:
                    mulFactor *= 1 - (
                        self.beliefArray[scoutNode] / (degree[scoutNode] + 1)
                    )
                if i in currentNodeNeighbours:
                    mulFactor *= 1 - (
                        self.beliefArray[agentPos] / (degree[agentPos] + 1)
                    )

                nextProb = piNext * mulFactor

                nextTimeStepBeliefArray[i] = nextProb

        self.beliefArray = copy(nextTimeStepBeliefArray)

    def updateBeliefArray3(self, agentPos, preyPos, predPos, graph, dist, degree):

        nextTimeStepBeliefArray = [0 for i in range(len(self.beliefArray))]

        neighbours = Utility.getNeighbours(graph, agentPos)

        for n in neighbours:
            self.beliefArray[n] += self.beliefArray[agentPos] / degree[agentPos]

        self.beliefArray[agentPos] = 0

        scoutNode = self.findNodeToScout()

        if scoutNode == preyPos:
            nextTimeStepBeliefArray[scoutNode] = 1
        else:

            neighbours = Utility.getNeighbours(graph, scoutNode)

            for n in neighbours:
                self.beliefArray[n] += self.beliefArray[scoutNode] / degree[scoutNode]

            for i in range(len(nextTimeStepBeliefArray)):

                if i != scoutNode and i != agentPos:

                    neighbours = Utility.getNeighbours(graph, i)
                    neighbours.append(i)

                    for n in neighbours:
                        nextTimeStepBeliefArray[n] += self.beliefArray[i] / (
                            degree[i] + 1
                        )

        self.beliefArray = copy(nextTimeStepBeliefArray)

    def updateBeliefArray(self, agentPos, preyPos, predPos, graph, dist, degree):

        newBeliefArray = copy(self.beliefArray)
        scoutNode = self.findNodeToScout()

        if self.scoutForPrey(scoutNode, preyPos):
            newBeliefArray = [0] * len(dist)
            newBeliefArray[scoutNode] = 1
            self.beliefArray = copy(newBeliefArray)
        else:

            totalProbability = 1 - (
                self.beliefArray[scoutNode] + self.beliefArray[agentPos]
            )

            # print(totalProbability, self.beliefArray)
            testbeliefArray = [0] * len(self.beliefArray)
            for i in range(len(self.beliefArray)):
                if i == scoutNode or i == agentPos:
                    testbeliefArray[i] = 0
                else:
                    testbeliefArray[i] = self.beliefArray[i] + (
                        (1 / (len(self.beliefArray) - 2))
                        * (self.beliefArray[scoutNode] + self.beliefArray[agentPos])
                    )  # / totalProbability
            # print(sum(testbeliefArray), "test")
            # Addition Step
            newBeliefArray = [0] * len(self.beliefArray)
            for i in range(len(self.beliefArray)):
                neighbours = Utility.getNeighbours(graph, i)
                neighbours.append(i)
                # print(i,neighbours,"check neighbours")
                for n in neighbours:
                    # print(1/(degree[n]+1),"degree")
                    newBeliefArray[n] += testbeliefArray[i] * (1 / (degree[i] + 1))
            # print(sum(newBeliefArray),"test new belief")
            self.beliefArray = copy(newBeliefArray)
            # every val / tot
            # for i in range(len(self.beliefArray)):
            #     self.beliefArray[i] = self.beliefArray[i] / totalProbability

    def predictPreyPos(self):
        options = []
        maxiValue = max(self.beliefArray)

        for i, j in enumerate(self.beliefArray):
            if j == maxiValue:
                options.append(i)

        if len(options) > 0:
            return random.choice(options)

    def scoutForPrey(self, node, preyPos):
        return node == preyPos

    def moveAgent(
        self, agentPos, predictedPreyPos, preyPos, predPos, graph, dist, degree
    ):

        agentNeighbours = Utility.getNeighbours(graph, agentPos)

        neighboursPreyDistance = []
        neighboursPredatorDistance = []

        currPreyDist = dist[agentPos][predictedPreyPos]
        currPredDist = dist[agentPos][predPos]

        for index, elem in enumerate(agentNeighbours):
            neighboursPreyDistance.append(dist[elem][predictedPreyPos])
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

    def agent3(
        self,
        graph,
        path,
        dist,
        agentPos,
        preyPos,
        predPos,
        degree,
        runs=100,
        visualize=False,
    ):

        while runs > 0:

            if visualize:
                # wait for a second
                Utility.visualizeGrid(graph, agentPos, predPos, preyPos)
                # time.sleep(10)

            # print(agentPos, preyPos, predPos)
            if agentPos == predPos:
                return False, 3, 100 - runs, agentPos, predPos, preyPos

            if agentPos == preyPos:
                return True, 0, 100 - runs, agentPos, predPos, preyPos

            self.updateBeliefArray3(agentPos, preyPos, predPos, graph, dist, degree)

            predictedPreyPosition = self.predictPreyPos()

            # move agent
            agentPos = self.moveAgent(
                agentPos,
                predictedPreyPosition,
                preyPos,
                predPos,
                graph,
                dist,
                degree,
            )

            # check pred
            if agentPos == predPos:
                return False, 4, 100 - runs, agentPos, predPos, preyPos

            # check prey
            if agentPos == preyPos:
                return True, 1, 100 - runs, agentPos, predPos, preyPos

            # move prey
            preyPos = Utility.movePrey(preyPos, graph)

            if agentPos == preyPos:
                return True, 2, 100 - runs, agentPos, predPos, preyPos

            # move predator
            # predPos = Utility.movePredator(agentPos, predPos, path)
            predPos = Utility.movePredatorWithoutPath(agentPos, predPos, graph, dist)

            runs -= 1

        return False, 5, 100, agentPos, predPos, preyPos

    def executeAgent(self, size):

        graph, path, dist, degree = self.generateGraph.generateGraph(size)

        counter = 0

        stepsCount = 0
        for _ in range(100):

            agentPos = random.randint(0, size - 1)
            preyPos = random.randint(0, size - 1)
            predPos = random.randint(0, size - 1)

            self.beliefArray = [1 / (size) for i in range(size)]

            # print("INITIAL BELIEF ARRAY SUM ", sum(self.beliefArray))

            # self.beliefArray[agentPos] = 0

            self.updateBeliefArray3(agentPos, preyPos, predPos, graph, dist, degree)

            result, line, steps, agentPos, predPos, preyPos = self.agent3(
                graph, path, dist, agentPos, preyPos, predPos, degree, 100, False
            )

            print(result, agentPos, predPos, preyPos)
            counter += result
            stepsCount += steps
        # print(self.agent1(graph, path, dist, agentPos, preyPos, predPos))
        # print(result, line)

        return counter, stepsCount / 100


if __name__ == "__main__":

    agent3 = Agent4()
    counter = 0
    stepsArray = []
    for _ in range(30):

        result, steps = agent3.executeAgent(50)
        counter += result
        stepsArray.append(steps)
    print("SUCCESS RATE", counter / 30, stepsArray)
