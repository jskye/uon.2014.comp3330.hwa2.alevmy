
#import the RL libraries
from scipy import *
import sys, time,pickle

from PygameEnvironment import TwentyFortyEightEnvironment
from pybrain.tools.shortcuts import buildNetwork
from pybrain.optimization import GA #HillClimber
from pybrain.rl.agents import OptimizationAgent
from pybrain.rl.experiments import EpisodicExperiment
from pybrain.rl.environments import Task

#set the learning time
learning_eps = 100

#set the batch size
games_per_ep = 50

population_size = 20


# make the environment
environment = TwentyFortyEightEnvironment()
environment.meansize = 1.0/(population_size*games_per_ep)

#the task is the game this time
task = environment

#create our network
controller = buildNetwork(task.nsenses, 20, task.nactions)

#use a Genetic Algorithm
#all the commented out lines are options you can play with
learner = GA(populationSize=population_size
            , topProportion=0.2
            , elitism=False
            , eliteProportion=0.5
            , mutationProb=0.1
            , mutationStdDev=0.3
            , tournament=False
            , tournamentSize=2
            )

agent = OptimizationAgent(controller, learner)



#set up an experiment
experiment = EpisodicExperiment(task, agent)

meanscores = []
for i in xrange(learning_eps):
    print i
    experiment.doEpisodes(games_per_ep)
    meanscores.append(learner.bestEvaluation)

f = open("bestEvo.pkl",'w')
pickle.dump(learner.bestEvaluable,f)
f.close()

import matplotlib.pyplot as plt
plt.plot(meanscores)

plt.title("Best Agent Score vs Generations:")
plt.show()




