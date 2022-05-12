import json
from channels.generic.websocket import WebsocketConsumer
from .sockets_deals import games, test1
from .menu import main_menu
import threading
import time
def test2(ws):
    time.sleep(0.5)
    ws.send(json.dumps({'type': 'on_open'}))
def t3(ws):
    test2(ws)
    ws.send(json.dumps({'games':main_menu.make_games_dict()}))

class MenuConsumer(WebsocketConsumer):

    def connect(self):
        main_menu.handler(self)
        self.accept()
        my_thread = threading.Thread(target=t3, args=(self,))
        my_thread.start()
    def disconnect(self,close_code):
        main_menu.websockets.remove(self)

class GameConsumer(WebsocketConsumer):
    game=None
    identifier=None
    team=None
    def connect(self):
        try:
            self.game = games[int(self.scope['url_route']['kwargs']['game_id'])]
            self.accept()
            #self.send(json.dumps({'type': 'on_open'}))
            #print('ya tut')
            my_thread = threading.Thread(target=test2, args=(self,))
            my_thread.start()
        except:
            self.close()

    def disconnect(self, close_code):
        if self.identifier:
            self.game.websockets.pop(self.identifier)
            #if self in self.game.players.values():
             #   self.game.on_player_joined()
             #   self.game.players.pop(self.identifier)
            self.game.on_disconnect(self)
            #if self.team != None:
              #  self.game.players.pop(self.team)
            if not self.game.players and self.game.id in games.keys():
                #games.pop(self.game.id)
                self.game.start_closing()
                #thread = threading.Thread(target=test1, args=(self.game,))
                #thread.start()

    def receive(self, text_data):
        self.game.handler(self,text_data)
        #games[int(self.scope['url_route']['kwargs']['game_id'])].handler(self,text_data)
        '''text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))'''