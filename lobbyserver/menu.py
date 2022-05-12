#from .sockets_deals import games
import json

class Menu:
    def __init__(self):
        self.games={'free':{}}
        self.websockets=[]
    def handler(self,websocket):
        self.websockets.append(websocket)
    def make_games_dict(self):
        games = {}
        for key, gamedicts in self.games.items():
            games[key] = {'started': [], 'notstarted': []}
            for id, game in gamedicts.items():
                games[key]['started']=[]
                games[key]['notstarted']=[]
                if game.started:
                    games[key]['started'].append([id,game.get_players_payloads2()])
                else:
                    games[key]['notstarted'].append([id,game.get_players_payloads2()])
        return games
    def update(self):
        games=self.make_games_dict()
        for ws in self.websockets:
            ws.send(json.dumps({'games':games}))

main_menu=Menu()