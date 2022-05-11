#from .sockets_deals import games
import json
class Menu:
    def __init__(self):
        self.games={'free':{}}
        self.websockets=[]
    def handler(self,websocket):
        self.websockets.append(websocket)

    def update(self):
        games={}
        for key,gamedicts in self.games.items():
            games[key]={'started':{},'notstarted':{}}
            for id,game in gamedicts.values():
                if game.started:
                    games[key]['started']=game.id
                else:
                    game[key]['notstarted']=game.id
        for ws in self.websockets:
            ws.send(json.dumps({'games':games}))

main_menu=Menu()