from collections import defaultdict
from copy import copy
from GenerateGraph import GenerateGraph
import random
from UtilityFunctions import Utility


class Agent5:
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

    def agent5(
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
        self.updateBeliefArray(agentPos, preyPos, predPos, graph, dist, degree)
        while runs > 0:

            if visualize:
                # wait for a second
                Utility.visualizeGrid(graph, agentPos, predPos, preyPos)
    
            if agentPos == predPos:
                return False, 3, 100 - runs, agentPos, predPos, preyPos

            if agentPos == preyPos:
                return True, 0, 100 - runs, agentPos, predPos, preyPos
            print(self.beliefArray,"input belief")
            scoutnode=self.findNodeToScout()
            self.updateBeliefArray(scoutnode, preyPos, predPos, graph, dist, degree)
            print(self.beliefArray,"after scout")
            predictedPredPosition = self.predictPredPos()
            # move agent
            agentPos = self.moveAgent(agentPos, preyPos, predictedPredPosition, graph, dist)
            self.NormalizeBeliefArray(agentPos, preyPos, predPos, graph, dist, degree)
            print(agentPos, preyPos, predPos, predictedPredPosition, sum(self.beliefArray))
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
            predPos = Utility.movePredator_dum(agentPos, predPos, graph, dist)

            runs -= 1

        return False, 5, 100, agentPos, predPos, preyPos

    def findNodeToScout(self):
        options = []
        maxiValue = max(self.beliefArray)

        for i, j in enumerate(self.beliefArray):
            if j == maxiValue:
                options.append(i)

        if len(options) > 0:
            return random.choice(options)

    def updateBeliefArray(self, agentPos, preyPos, predPos, graph, dist, degree):

        nextTimeStepBeliefArray = [0 for i in range(len(self.beliefArray))]

        scoutNode = agentPos

        if scoutNode == predPos:
            nextTimeStepBeliefArray[scoutNode] = 1
        else:
            nextTimeStepBeliefArray[scoutNode] = 0
            for i in range(len(nextTimeStepBeliefArray)):
                if(i!=scoutNode):
                    nextTimeStepBeliefArray[i] = self.beliefArray[i] / (1 - self.beliefArray[scoutNode])

            # print("sum before distributing: ", sum(nextTimeStepBeliefArray))
        self.beliefArray = copy(nextTimeStepBeliefArray)

    def NormalizeBeliefArray(self, agentPos, preyPos, predPos, graph, dist, degree):
        nextTimeStepBeliefArray2 = [0 for i in range(len(self.beliefArray))]
        randombeliefarray=[0.4*self.beliefArray[i] for i in range(len(self.beliefArray))]
        intelligentbeliefarray = [0.6 * self.beliefArray[i] for i in range(len(self.beliefArray))]
        
        for i in range(len(self.beliefArray)):
          #normalising 0.6 of the belief to intelligent choices
            neighbours = Utility.getNeighbours(graph, i)
            neighbourDistanceMap = defaultdict(list)
            for n in neighbours:
                neighbourDistanceMap[dist[n][agentPos]].append(n)
            minimumDistanceList = neighbourDistanceMap.get(min(neighbourDistanceMap), [])
            for intelligent_choice in minimumDistanceList:
                nextTimeStepBeliefArray2[intelligent_choice] += intelligentbeliefarray[i]/(len(minimumDistanceList))
          #normalising 0.4 ot the remaining belief to random choices      
            neighbours = Utility.getNeighbours(graph, i)
            neighbours.append(i)
            for neighbor in neighbours:
                nextTimeStepBeliefArray2[i] += randombeliefarray[neighbor] / (degree[neighbor] + 1)
                
        self.beliefArray = copy(nextTimeStepBeliefArray2)
        self.updateBeliefArray(agentPos, preyPos, predPos, graph, dist, degree)

    def predictPredPos(self):
        options = []
        maxiValue = max(self.beliefArray)

        for i, j in enumerate(self.beliefArray):
            if j == maxiValue:
                options.append(i)

        if len(options) > 0:
            return random.choice(options)

    def scoutForPredator(self, node, predPos):
        return node == predPos

    def executeAgent(self, size):

        graph, path, dist, degree = self.generateGraph.generateGraph(size)

        counter = 0

        stepsCount = 0
        for _ in range(1):
            agentPos = random.randint(0, size - 1)
            preyPos = random.randint(0, size - 1)
            predPos = random.randint(0, size - 1)

            self.beliefArray = [0 for i in range(size)]
            self.beliefArray[predPos] = 1
            result, line, steps, agentPos, predPos, preyPos = self.agent5(
                graph, path, dist, agentPos, preyPos, predPos, degree, 100, False
            )

            print(result, agentPos, predPos, preyPos)
            counter += result
            stepsCount += steps

        return counter, stepsCount / 100


if __name__ == "__main__":

    agent5 = Agent5()
    counter = 0
    stepsArray = []
    for _ in range(1):

        result, steps = agent5.executeAgent(50)
        counter += result
        stepsArray.append(steps)
    print(counter/30, stepsArray)
