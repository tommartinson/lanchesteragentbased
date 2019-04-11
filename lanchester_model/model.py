from mesa import Agent, Model
from mesa.space import ContinuousSpace
import random
#Thomas Martinson
#SDSU
#CS558


class BattleFieldModel(Model):
    """A model  of an agent-based battle simulation using Lanchester’s Law. First assume it is
analogous to the continuous model whereby all troops are homogenous and jumbled together. At
combat start, each troop is put in a random position. A shooting occurs on each side at each time
step, if any enemies are left to kill. The soldier shooting shall be chosen randomly from among
the remaining troops. Thus each is equally likely to be the random shooter on his/her side. The
probability of killing an opposing troop is expressed in the lethality coefficients.
    """

    def __init__(self, N=200, width=20, height=20):
        self.num_agents = int(N/2)
        self.grid = ContinuousSpace(height, width, True)
        self.redAgentList = []
        self.blueAgentList = []
        self.turn = 1
        
        #redLethality = input("Enter Red team lethality coefficient")
        #blueLethality = input("Enter Blue team lethality coefficient")
        
        # Create Red and Blue agents
        for i in range(self.num_agents):
            a = RedSoldier(i, self)
            self.redAgentList.append(a)
            
            # add red soldier to random location on grid
            rx = self.random.randrange(self.grid.width)
            ry = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (rx, ry))
            
            b = BlueSoldier(i, self)
            self.blueAgentList.append(b)
            
            # add blue soldier to random location on grid
            bx = self.random.randrange(self.grid.width)
            by = self.random.randrange(self.grid.height)
            self.grid.place_agent(b, (bx, by))
            
     
        self.running = True
        

    def step(self):
        numRed = len(self.redAgentList)
        numBlue = len(self.blueAgentList)
        if ((numRed > 0) and (numBlue > 0)):
            if (self.turn == 1):
                print("Red Turn")
                self.redAgentList[random.randint(0,numRed-1)].step()
            
                self.turn = 0
            else:
                print("Blue Turn")
                self.blueAgentList[random.randint(0,numBlue-1)].step()
            
                self.turn = 1
        else:
            if(numRed == 0):
                print("Battle Over! Blue Team Wins.")
            else:
                print("Battle Over! Red Team Wins.")
            self.running = False
        
        
    
class RedSoldier(Agent):
    """ A red soldier."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def shoot(self):
        numBlue = len(self.model.blueAgentList) # num enemies left
        currDistance = 1000
        
        redPos = self.pos
        currClosestPos = redPos
        blueAgent = self.model.blueAgentList[0]
        for i in range (numBlue):
            bluePos = self.model.blueAgentList[i].pos
            
            if(self.model.grid.get_distance(redPos, bluePos)<currDistance):
                currDistance = self.model.grid.get_distance(redPos, bluePos)
                currClosestPos = bluePos
                blueAgent = self.model.blueAgentList[i]

        
        self.model.blueAgentList.remove(blueAgent) # remove blue soldier from database 
        self.model.grid.remove_agent(blueAgent) # remove blue soldier from grid

        print("\nRed soldier at",self.pos,"killed blue piece at ",currClosestPos)
        print("Red team size:",len(self.model.redAgentList))
        print("Blue team size:",len(self.model.blueAgentList))
            
            
            
    def step(self):
        # lethality coeff from 1-10 (10% to `100%)
        lethalityCoeff = 9
        randNum= random.randint(1,11)
        if(randNum < lethalityCoeff):
            self.shoot()
        
    
        
class BlueSoldier(Agent):
    """ A blue game piece."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def shoot(self):
        numRed = len(self.model.redAgentList) # num enemies left
        currDistance = 1000
        
        bluePos = self.pos
        currClosestPos = bluePos
        redAgent = self.model.redAgentList[0]
        for i in range (numRed):
            redPos = self.model.redAgentList[i].pos
            
            if(self.model.grid.get_distance(bluePos, redPos)<currDistance):
                currDistance = self.model.grid.get_distance(bluePos, redPos)
                currClosestPos = redPos
                redAgent = self.model.redAgentList[i]

        
        self.model.redAgentList.remove(redAgent) # remove blue soldier from database 
        self.model.grid.remove_agent(redAgent) # remove blue soldier from grid

        print("\nBlue soldier at",self.pos,"killed red soldier at ",currClosestPos)
        print("Red team size:",len(self.model.redAgentList))
        print("Blue team size:",len(self.model.blueAgentList))
                

    def step(self):
        # lethality coeff from 1-10 (10% to `100%)
        lethalityCoeff = 8
        randNum= random.randint(1,11)
        if(randNum < lethalityCoeff):
            self.shoot()
        
        
        
