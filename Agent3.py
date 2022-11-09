from GenerateGraph import GenerateGraph

import random
from UtilityFunctions import Utility
import time


class Agent3:
    def __init__(self):
        self.generateGraph = GenerateGraph()

    def updateBeliefArray(self, agentPos, preyPos, predPos, graph, dist):
        pass

    def scoutForPrey(self, node, preyPos):
        return node == preyPos

    def moveAgent(self, agentPos, preyPos, predPos, graph, dist, degree):

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

            print(agentPos, predPos, preyPos)

            if visualize:
                # wait for a second
                Utility.visualizeGrid(graph, agentPos, predPos, preyPos)
                # time.sleep(10)

            # print(agentPos, preyPos, predPos)
            if agentPos == predPos:
                return False, 3, 100 - runs, agentPos, predPos, preyPos

            if agentPos == preyPos:
                return True, 0, 100 - runs, agentPos, predPos, preyPos

            # move agent
            agentPos = self.moveAgent(agentPos, preyPos, predPos, graph, dist, degree)

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
        for _ in range(1):

            agentPos = random.randint(0, size - 1)
            preyPos = random.randint(0, size - 1)
            predPos = random.randint(0, size - 1)

            if agentPos == predPos:
                continue

            if agentPos == preyPos:
                counter += 1
                continue

            self.belief_array = [1 / (size - 1) for i in range(size)]

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

    agent3 = Agent3()
    counter = 0
    stepsArray = []
    for _ in range(1):

        result, steps = agent3.executeAgent(50)
        counter += result
        stepsArray.append(steps)
    # print(counter/30, stepsArray)
