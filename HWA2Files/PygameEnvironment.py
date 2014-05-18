from game import Game,Direction
from pybrain.rl.environments.episodic import EpisodicTask
import numpy
from pybrain.utilities import Named

class TwentyFortyEightEnvironment(EpisodicTask,Named):

    #The number of actions.
    action_list = (Direction.up,Direction.left,Direction.down,Direction.right)
    nactions = len(action_list)
    
    meansize = 1.0
    nsenses = 4*4
    indims = nsenses
    outdims = nactions
    printgame = False

    # number of steps of the current trial
    steps = 0

    # number of the current episode
    episode = 0
    
    resetOnSuccess = True
    
    done = 0
    
    game = None

    def __init__(self):
        self.nactions = len(self.action_list)
        self.reset()
        self.cumreward = 0
        self.lastscore = 0
        self.meanscore = 0

    def reset(self):
        self.StartEpisode()
        self.game = Game()
        self.done = 0
        self.startState = self.game.state
    
    def getObservation(self):
        if self.printgame:
            print "Game State:"
            print self.game.state.astype(numpy.uint32)
        #this is the input to the neural network
        #modify this function to change the observation representation
        return self.game.state.flatten()
        
    def performAction(self, action):
        #this is the output of the neural network
        #currently a move which doesn't change the board ends the game
        #this could be changed
        if len(action) == 4:
            action = [numpy.argmax(action)]
        if self.game.won or self.done:
            self.done += 1            
        else:
            lastgs = self.game.score
            moved = self.game.move(self.action_list[int(action[0])])
            if not moved or self.game.won:
                self.r = moved*-2.0
                self.done += 1
            else:
                self.r = self.game.score - lastgs
            self.cumreward += self.r
            
    def getReward(self):
        return self.r    

    def GetInitialState(self):
        self.StartEpisode()
        return self.startState.flatten()

    def StartEpisode(self):
        self.steps = 0
        self.cumreward = 0
        self.episode = self.episode + 1
        self.done = 0
        
    def isFinished(self):
        if self.done > 2 or self.game.won and self.resetOnSuccess:
            self.lastscore = self.cumreward
            self.meanscore = self.meansize*self.meanscore + (1.0-self.meansize)*self.cumreward
            return True
        return False
