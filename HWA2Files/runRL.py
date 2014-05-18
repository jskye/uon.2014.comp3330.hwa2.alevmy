
#import the RL libraries
from scipy import *
import sys, time,pickle

from PygameEnvironment import TwentyFortyEightEnvironment
from pybrain.rl.learners.valuebased import ActionValueNetwork
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import NFQ, SARSA
from pybrain.rl.experiments import EpisodicExperiment
from pybrain.rl.environments import Task

#set the learning time
learning_eps = 20

#set the batch size
games_per_ep = 25

# make the environment
environment = TwentyFortyEightEnvironment()
environment.meansize = 1.0/games_per_ep

#the task is the game this time
task = environment

#make the reinforcement learning agent (use a network because inputs are continuous)
controller = ActionValueNetwork(task.nsenses,task.nactions)

#use Q learning for updating the table (NFQ is for networks)
learner = NFQ()

agent = LearningAgent(controller, learner)



#set up an experiment
experiment = EpisodicExperiment(task, agent)

meanscores = []
m = 0.0
for i in xrange(learning_eps):
    print i
    experiment.doEpisodes(games_per_ep)
    meanscores.append(task.meanscore)
    if meanscores[-1] > m:
        m = meanscores[-1]
        f = open("bestRL.pkl",'w')
        pickle.dump(agent,f)
        f.close()
    agent.learn()
    agent.reset()

import matplotlib.pyplot as plt
plt.plot(meanscores)

plt.title("Mean Agent Score Per Batch")
plt.show()

"""
#get the best action at each state
finalactions = controller.params.reshape(environment.nsenses,environment.nactions).argmax(1).reshape(4,4)

import matplotlib.pyplot as plt

#make arrows for directions of the best movements
#these are the arrow locations
px = [[j+0.5 for j in xrange(4)] for i in xrange(4)]
py = [[i+0.5]*4 for i in xrange(4)]

#this are the arrow directions
ax = [[0.]*4 for i in xrange(4)]
ay = [[0.]*4 for i in xrange(4)]
for i in xrange(4):
    for j in xrange(4):
        if finalactions[i][j] == 0:
            ay[i][j] += 1.
        elif finalactions[i][j] == 1:
            ax[i][j] -= 1.
        elif finalactions[i][j] == 2:
            ay[i][j] -= 1.
        elif finalactions[i][j] == 3:
            ax[i][j] += 1.
        

#put colours according to how close we are to the goal
plt.pcolor(controller.params.reshape(environment.nsenses,environment.nactions).max(1).reshape(4,4))


plt.quiver(px,py,ax,ay)
plt.title("Reinforcement Learning Training Result")
plt.show()
"""



