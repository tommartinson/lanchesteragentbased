from mesa.visualization.ModularVisualization import ModularServer
from .model import BattleFieldModel
from .SimpleContinuousModule import SimpleCanvas
from .model import RedSoldier, BlueSoldier



def agent_portrayal(agent):
    portrayal = {"Shape": "circle","Filled": "true","r": 0.5}
    
    if type(agent) is RedSoldier:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    
    
    if type(agent) is BlueSoldier:
        portrayal["Color"] = "blue"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
    
    
    return portrayal


# create grid (numx,numy,pixelsx,pixelsy)
grid = SimpleCanvas(agent_portrayal,500, 500)


server = ModularServer(BattleFieldModel, [grid], "Lanchester Model")
server.port = 8521
