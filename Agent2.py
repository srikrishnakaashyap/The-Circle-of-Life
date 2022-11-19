from GenerateGraph import GenerateGraph
import random
from UtilityFunctions import Utility
import time


class Agent2:
    def __init__(self):
        self.generateGraph = GenerateGraph()

    def nextbeliefArray(self, beliefArray, graph, degree, preyPos):
        # def perculateBeliefArray(self, graph, degree):
        nextTimeStepBeliefArray2 = [0 for i in range(len(beliefArray))]
        for i in range(len(beliefArray)):
            neighbours = Utility.getNeighbours(graph, i)
            neighbours.append(i)
            for neighbor in neighbours:
                nextTimeStepBeliefArray2[i] += beliefArray[neighbor] / (
                    degree[neighbor] + 1
                )

        # print("sum after distributing: ", sum(nextTimeStepBelief
        return nextTimeStepBeliefArray2

    def calculateHeuristic(
        self, agentPos, preyPos, predPos, nextPreyPositions, dist, beliefArray, graph
    ):
        agentNeighbours = Utility().getNeighbours(graph, agentPos)
        agentNeighbours.append(agentPos)

        heuristics = {}
        for n in agentNeighbours:

            currheuristic = 0
            for i in nextPreyPositions:

                neighbourPredDsitance = dist[n][predPos] + 1

                deno = (neighbourPredDsitance + 0.1) ** 10

                currheuristic += dist[n][i] * (1 - beliefArray[i]) / deno

            heuristics[n] = currheuristic

        return heuristics

    def agent2(
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

            # print(agentPos, predPos, preyPos)

            if visualize:
                # wait for a second
                Utility.visualizeGrid(graph, agentPos, predPos, preyPos)
                # time.sleep(10)

            # print(agentPos, preyPos, predPos)
            if agentPos == predPos:
                return False, 3, 100 - runs, agentPos, predPos, preyPos

            if agentPos == preyPos:
                return True, 0, 100 - runs, agentPos, predPos, preyPos

            beliefArray = [0 for i in range(len(graph))]

            beliefArray[preyPos] = 1

            nextTimeStepBeliefArray = self.nextbeliefArray(
                beliefArray, graph, degree, preyPos
            )

            # nextTimeStepBeliefArray = beliefArray

            # nextTimeStepBeliefArray = self.nextbeliefArray(
            #     nextTimeStepBeliefArray, graph, degree, preyPos
            # )

            print(nextTimeStepBeliefArray, sum(nextTimeStepBeliefArray))

            # nextTimeStepBeliefArray = self.nextbeliefArray(
            #     nextTimeStepBeliefArray, graph, degree, preyPos
            # )

            nextPreyPositions = []
            for i, j in enumerate(nextTimeStepBeliefArray):
                if j != 0:
                    nextPreyPositions.append(i)

            heuristicMap = self.calculateHeuristic(
                agentPos,
                preyPos,
                predPos,
                nextPreyPositions,
                dist,
                nextTimeStepBeliefArray,
                graph,
            )

            # move agent
            agentPos = sorted(heuristicMap.items(), key=lambda x: x[1])[0][0]

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

        predCatch = 0

        for _ in range(100):

            agentPos = random.randint(0, size - 1)
            preyPos = random.randint(0, size - 1)
            predPos = random.randint(0, size - 1)

            result, line, steps, agentPos, predPos, preyPos = self.agent2(
                graph, path, dist, agentPos, preyPos, predPos, degree, 100, False
            )

            print(result, agentPos, predPos, preyPos)
            counter += result
            stepsCount += steps

            if not result:
                predCatch += 1
        # print(self.agent1(graph, path, dist, agentPos, preyPos, predPos))
        # print(result, line)

        return counter, stepsCount / 100, predCatch


if __name__ == "__main__":

    agent1 = Agent2()
    counter = 0
    stepsArray = []
    successArray = []
    predCatch = []
    for _ in range(30):

        result, steps, catches = agent1.executeAgent(50)
        successArray.append(result)
        # counter += result
        stepsArray.append(steps)
        predCatch.append(catches)
        # print(catches)

    # print(predCatch)
    print(successArray)
    print(stepsArray)
