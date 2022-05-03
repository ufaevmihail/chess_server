import json
from channels.generic.websocket import WebsocketConsumer
from .sockets_deals import games, test1
import threading

class GameConsumer(WebsocketConsumer):
    game=None
    identifier=None
    team=None
    def connect(self):
        try:
            self.game = games[int(self.scope['url_route']['kwargs']['game_id'])]
            self.accept()
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