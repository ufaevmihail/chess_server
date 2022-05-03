#import asyncio
import threading
import time
import django
import websockets
import json
from lobbychessserver.settings import SECRET_KEY
import jwt
from .game_state import State
django.setup()




def create_game():
    if not games:
        id=1
    else:
        id=max(games.keys())+1
    games[id]=FreeGame(id)
    return id

def joinGame(id):
    if id in games:
        return True

def test1(game):
    time.sleep(2)
    if game in games.values():
        time.sleep(30)
        if game.condition_to_end():
            game.on_close()
            return


class Game:
    players= {}
    websockets={}    #{userid:websocket}
    state=None
    #state  #figurespos
            #turn
            #hodi
    on_connection = []
    on_move = []
    on_chat_message = []
    events=[]
    def __init__(self,id):
        self.state=State(self)
        self.id=id

    def start_closing(self):
        print(f'closing {self.id}')
        my_thread = threading.Thread(target=test1, args=(self,))
        my_thread.start()

    def on_close(self):
        for key,value in self.websockets.items():
            value.close()
        if self in games.values():
            print(f'closed {self.id}')
            games.pop(self.id)

    def condition_to_end(self):
        if not self.players or self.state.endgame:
            return True

    def handler(self,websocket,msge):
        '''while websocket.open:
            try:
                msge = await websocket.recv()
            except websockets.exceptions.ConnectionClosedOK:
                break'''
        message = json.loads(msge)
        for etype, list_handlers in self.events:
            if message["type"] == etype:
                for handler in list_handlers:
                    handler(self,websocket, message)

    def on_disconnect(self,websocket):
        if websocket.team != None:
            self.players.pop(websocket.team)
            self.on_player_joined()

    def get_players_payloads(self):
        dict={}
        for key,value in self.players.items():
            dict[key]=value.payload
        return dict
    def on_player_joined(self):
        for identifier, ws in self.websockets.items():
            ws_send(ws,'connection','player_connected',None,self.get_players_payloads())
    def load_game(self, websocket):
        if self.id_in_players(websocket,0,0,['loadgame', 'ok', websocket.payload, {'team': 0,'figs':self.state.get_loaded_state()}]):
            return
        if self.id_in_players(websocket,1,1,['loadgame', 'ok', websocket.payload, {'team': 1,'figs':self.state.get_loaded_state()}]):
            return
        else:
            ws_send(websocket, 'loadgame', 'viewer', {'figs':self.state.get_loaded_state()})
    def new_game(self, websocket):
        if self.id_in_players(websocket,0,0,['startgame', 'ok', websocket.payload, {'team': 0}]):
            return
        if self.id_in_players(websocket,1,1,['startgame', 'ok', websocket.payload, {'team': 1}]):
            return
        else:
            ws_send(websocket, 'startgame', 'viewer', websocket.payload)


    def id_in_players(self,websocket,id,team,data_to_send):
        if id not in self.players:
            websocket.team = team
            self.players[id] = websocket
            ws_send(websocket, *data_to_send)
            self.on_player_joined()
            return True
def chat_message(self,websocket,message):
    for identifier, ws in self.websockets.items():
     #   if identifier != id:
        ws_send(ws,'chat_mess',message['content'],websocket.payload)

def move_done(self, websocket,message):
    if websocket not in self.players.values():
        return
    id = websocket.payload['account']['user']
    turn = {"startfield":message['startfield'],'endfield':message['endfield'],"swt":message["swt"]}
    if not self.state.validate(*turn['startfield'],*turn['endfield']):
        print('chtoto ne to')
        ws_send(websocket,'reload_page')
        return
    self.state.move(turn)
    for identifier,ws in self.websockets.items():
       # if identifier != id:
        if websocket != ws:
            ws_send(ws,'move_done','',websocket.payload,turn)


def start_game(self,websocket,message):
    try:
        payload = jwt.decode(message['token'],SECRET_KEY,algorithms=["HS256"])
        websocket.payload = payload
        id = payload['account']['user']
        if id not in self.websockets:
            websocket.identifier=id
            self.websockets[id] = websocket
        else:
            id = str(id)+'clone'
            websocket.identifier = id
            self.websockets[id] = websocket
    except:
        if games[self.id].websockets.keys():
            id = min(min(self.websockets.keys()),0)-1
        else:
            id=-1
        payload={'username':f'guest{-1*id}','email':'','account':{'user':id,'rating':0}}
        websocket.payload=payload
        games[self.id].websockets[id]=websocket
        websocket.identifier=id
    if self.state.turnList:
        self.load_game(websocket)
    else:
        self.new_game(websocket)


def ws_send(ws, type, content='', senderPayload=None, data=None):
    if data is None:
        data = {}
    if senderPayload is None:
        senderPayload = {}
    return ws.send(json.dumps({'type':type,'content':content,'usersender':senderPayload,'data':data}))

class FreeGame(Game):
    on_connection = [start_game]
    on_move = [move_done]
    on_chat_message=[chat_message]
    def __init__(self,id):
        super().__init__(id)
        self.websockets={}
        self.players={}
        self.events = [("connection",self.on_connection),("move",self.on_move),('chat_mess',self.on_chat_message)]

#{id:game()}
#games={1:FreeGame()}
games={}