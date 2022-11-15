from collections import defaultdict
from copy import copy

from GenerateGraph import GenerateGraph
import random
from UtilityFunctions import Utility


class Agent7:
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

    def agent7(
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
        self.updateBeliefArrayPred(agentPos, preyPos, predPos, graph, dist, degree)
        self.updateBeliefArrayPrey(agentPos, preyPos, predPos, graph, dist, degree)
        while runs > 0:

            if visualize:
                # wait for a second
                Utility.visualizeGrid(graph, agentPos, predPos, preyPos)

            if agentPos == predPos:
                return False, 3, 100 - runs, agentPos, predPos, preyPos

            if agentPos == preyPos:
                return True, 0, 100 - runs, agentPos, predPos, preyPos
            # print(self.beliefArrayPred,"input belief of predator")
            # print(self.beliefArrayPrey, "input belief of prey")
            if (self.beliefArrayPred.count(0)!=49):
                scoutnode=self.findNodeToScoutPred(agentPos,dist)
                # print("test1")
            else:
                scoutnode=self.findNodeToScoutPrey()
                # print("test2")
            self.updateBeliefArrayPred(scoutnode, preyPos, predPos, graph, dist, degree)
            self.updateBeliefArrayPrey(scoutnode, preyPos, predPos, graph, dist, degree)
            # print(self.beliefArrayPred,"after scout of predator")
            # print(self.beliefArrayPrey, "after scout of prey")
            predictedPredPosition = self.predictPredPos(agentPos,dist)
            predictedPreyPosition = self.predictPreyPos()
            # move agent
            agentPos = self.moveAgent(agentPos, predictedPreyPosition, predictedPredPosition, graph, dist)
            self.NormalizeBeliefArrayPred(agentPos, preyPos, predPos, graph, dist, degree)
            self.NormalizeBeliefArrayPrey(agentPos, preyPos, predPos, graph, dist, degree)
            print(agentPos, preyPos, predPos, predictedPredPosition, sum(self.beliefArrayPred))
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
            predPos = Utility.movePredator_dum(agentPos, predPos, graph, dist)

            runs -= 1

        return False, 5, 100, agentPos, predPos, preyPos

    def findNodeToScoutPred(self,agentPos,dist):
        options = []
        maxiValue = max(self.beliefArrayPred)

        for i, j in enumerate(self.beliefArrayPred):
            if j == maxiValue:
                options.append(i)
        options_same_probabilty=[]
        mini=999999
        for c in options:
            if(dist[agentPos][c]<mini):
                mini=dist[agentPos][c]
        for c in options:
            if(dist[agentPos][c]==mini):
                options_same_probabilty.append(c)
        if len(options_same_probabilty) > 0:
            return random.choice(options_same_probabilty)

    def findNodeToScoutPrey(self):
        options = []
        maxiValue = max(self.beliefArrayPrey)

        for i, j in enumerate(self.beliefArrayPrey):
            if j == maxiValue:
                options.append(i)

        if len(options) > 0:
            return random.choice(options)


    def updateBeliefArrayPrey(self, agentPos, preyPos, predPos, graph, dist, degree):

        nextTimeStepBeliefArrayPrey = [0 for i in range(len(self.beliefArrayPrey))]

        scoutNode = agentPos
        scoutCondition=self.scoutForPrey(scoutNode,preyPos)

        if scoutCondition:
            nextTimeStepBeliefArrayPrey[scoutNode] = 1
        else:
            nextTimeStepBeliefArrayPrey[scoutNode] = 0
            for i in range(len(nextTimeStepBeliefArrayPrey)):
                if(i!=scoutNode):
                    nextTimeStepBeliefArrayPrey[i] = self.beliefArrayPrey[i] / (1 - self.beliefArrayPrey[scoutNode])

            # print("sum before distributing: ", sum(nextTimeStepBeliefArray))
        self.beliefArrayPrey = copy(nextTimeStepBeliefArrayPrey)

    def updateBeliefArrayPred(self, agentPos, preyPos, predPos, graph, dist, degree):

        nextTimeStepBeliefArrayPred = [0 for i in range(len(self.beliefArrayPred))]

        scoutNode = agentPos

        scoutCondition=self.scoutForPredator(scoutNode,predPos)

        if scoutCondition:
            nextTimeStepBeliefArrayPred[scoutNode] = 1
        else:
            if(self.beliefArrayPred[scoutNode]==1):
                nextTimeStepBeliefArrayPred = copy(self.beliefArrayPred)
            else:
                nextTimeStepBeliefArrayPred[scoutNode] = 0
                for i in range(len(nextTimeStepBeliefArrayPred)):
                    if(i!=scoutNode):
                        nextTimeStepBeliefArrayPred[i] = self.beliefArrayPred[i] / (1 - self.beliefArrayPred[scoutNode])

            # print("sum before distributing: ", sum(nextTimeStepBeliefArray))
        self.beliefArrayPred = copy(nextTimeStepBeliefArrayPred)

    def NormalizeBeliefArrayPrey(self, agentPos, preyPos, predPos, graph, dist, degree):
        nextTimeStepBeliefArrayPrey2 = [0 for i in range(len(self.beliefArrayPrey))]
        for i in range(len(self.beliefArrayPrey)):
            neighbours = Utility.getNeighbours(graph, i)
            neighbours.append(i)
            for neighbor in neighbours:
                nextTimeStepBeliefArrayPrey2[i] += self.beliefArrayPrey[neighbor] / (degree[neighbor] + 1)

        # print("sum after distributing: ", sum(nextTimeStepBeliefArray2))
        self.beliefArrayPrey = copy(nextTimeStepBeliefArrayPrey2)
        self.updateBeliefArrayPrey(agentPos, preyPos, predPos, graph, dist, degree)

    def NormalizeBeliefArrayPred(self, agentPos, preyPos, predPos, graph, dist, degree):
        nextTimeStepBeliefArrayPred2 = [0 for i in range(len(self.beliefArrayPred))]
        randombeliefarrayPred=[0.4*self.beliefArrayPred[i] for i in range(len(self.beliefArrayPred))]
        intelligentbeliefarrayPred = [0.6 * self.beliefArrayPred[i] for i in range(len(self.beliefArrayPred))]
        for i in range(len(self.beliefArrayPred)):
            neighbours = Utility.getNeighbours(graph, i)
            neighbourDistanceMap = defaultdict(list)
            for n in neighbours:
                neighbourDistanceMap[dist[n][agentPos]].append(n)
            minimumDistanceList = neighbourDistanceMap.get(min(neighbourDistanceMap), [])
            for intelligent_choice in minimumDistanceList:
                nextTimeStepBeliefArrayPred2[intelligent_choice] += intelligentbeliefarrayPred[i]/(len(minimumDistanceList))
            neighbours = Utility.getNeighbours(graph, i)
            # neighbours.append(i)
            for neighbor in neighbours:
                nextTimeStepBeliefArrayPred2[i] += randombeliefarrayPred[neighbor] / (degree[neighbor])
        self.beliefArrayPred = copy(nextTimeStepBeliefArrayPred2)
        self.updateBeliefArrayPred(agentPos, preyPos, predPos, graph, dist, degree)

    def predictPredPos(self,agentPos,dist):
        options = []
        maxiValue = max(self.beliefArrayPred)

        for i, j in enumerate(self.beliefArrayPred):
            if j == maxiValue:
                options.append(i)
        options_same_probabilty=[]
        mini=999999
        for c in options:
            if(dist[agentPos][c]<mini):
                mini=dist[agentPos][c]
        for c in options:
            if(dist[agentPos][c]==mini):
                options_same_probabilty.append(c)
        if len(options_same_probabilty) > 0:
            return random.choice(options_same_probabilty)

    def predictPreyPos(self):
        options = []
        maxiValue = max(self.beliefArrayPrey)

        for i, j in enumerate(self.beliefArrayPrey):
            if j == maxiValue:
                options.append(i)

        if len(options) > 0:
            return random.choice(options)

    def scoutForPredator(self, node, predPos):
        if(node == predPos):
            return random.choices([True,False],weights=(90,10),k=1)[0]
        else:
            return False


    def scoutForPrey(self, node, preyPos):
        if(node == preyPos):
            return random.choices([True,False],weights=(90,10),k=1)[0]
        else:
            return False

    def executeAgent(self, size):

        graph, path, dist, degree = self.generateGraph.generateGraph(size)

        counter = 0

        stepsCount = 0
        for _ in range(100):
            agentPos = random.randint(0, size - 1)
            preyPos = random.randint(0, size - 1)
            predPos = random.randint(0, size - 1)

            self.beliefArrayPred = [0 for i in range(size)]
            self.beliefArrayPred[predPos] = 1
            self.beliefArrayPrey = [1 / (size) for i in range(size)]
            result, line, steps, agentPos, predPos, preyPos = self.agent7(
                graph, path, dist, agentPos, preyPos, predPos, degree, 100, False
            )

            print(result, agentPos, predPos, preyPos)
            counter += result
            stepsCount += steps

        return counter, stepsCount / 100


if __name__ == "__main__":

    agent7 = Agent7()
    counter = 0
    stepsArray = []
    for _ in range(30):

        result, steps = agent7.executeAgent(50)
        counter += result
        stepsArray.append(steps)
    print(counter/30, stepsArray)
