#import asyncio
import threading
import time
import django
import json
from lobbychessserver.settings import SECRET_KEY
import jwt
from .game_state import State
from .menu import main_menu

django.setup()


class Timer:
    #time1={'base':100,'add':5}
    def __init__(self,game,time1=None,time2=None):
        self.game=game
        self.state=game.state
        self.timers = game.state.timers
        game.state.timers[0]=time1
        game.state.timers[1]=time2

        self.running=[False,False]

    def start_ticking(self,team):
        self.stop_ticking((team+1)%2)
        #print(f"{self.timers[0]['base']} y {0}, {self.timers[1]['base']} y {1}")
        if self.timers[team]:
            self.timers[(team+1)%2]['base']+=self.timers[(team+1)%2]['add']
            self.running[team]=True
            thread=threading.Thread(target=ticking,args=(self,team))
            thread.start()

    def stop_ticking(self,team):
        self.running[team]=False


def ticking(self,team):
    while self.running[team]:
        time.sleep(0.1)
        self.timers[team]['base'] -= 0.1
        if self.timers[team]['base'] <= 0:
            self.state.endgame=True
            self.game.start_closing()
            self.stop_ticking(team)
    #print(f'thread stopped {team}')

def create_game(time1=None,time2=None):
    if not games:
        id=1
    else:
        id=max(games.keys())+1
    games[id]=FreeGame(id,time1,time2)
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
    #timers={0:None,1:None}
    #state  #figurespos
            #turn
            #hodi
    on_connection = []
    on_move = []
    on_chat_message = []
    events=[]
    def __init__(self,id,time1=None,time2=None):
        self.state=State(self)
        self.state.timer = Timer(self,time1,time2)
        #self.state.timer = Timer(self)
        self.id=id
        self.started=False
        #self.timer=Timer(self,{'base':100,'add':5},{'base':100,'add':5})
        #main_menu.update()

    def start_closing(self):
        print(f'closing {self.id}')
        my_thread = threading.Thread(target=test1, args=(self,))
        my_thread.start()

    def on_close(self):
        for key,value in self.websockets.items():
            value.close()
        if self in self.games.values():
            print(f'closed {self.id}')
            self.games.pop(self.id,None)
            #main_menu.update()

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
        #print(websocket.team)
        if websocket.team != None:
            self.players.pop(websocket.team)
            self.on_player_joined()

    def get_players_payloads(self):
        dict={}
        for key,value in self.players.items():
            dict[key]=value.payload
        return dict
    def get_players_payloads2(self):
        dict={0:{},1:{}}
        for ws in self.players.values():
            dict[ws.team]=ws.payload
        return dict
    def on_player_joined(self):
        for identifier, ws in self.websockets.items():
            ws_send(ws,'connection','player_connected',None,self.get_players_payloads())
    def load_game(self, websocket):

        if self.id_in_players(websocket,0,0,['loadgame', 'ok', websocket.payload, {'team': 0,'figs':self.state.get_loaded_state()}]):
            get_timers(self, websocket)
            return
        if self.id_in_players(websocket,1,1,['loadgame', 'ok', websocket.payload, {'team': 1,'figs':self.state.get_loaded_state()}]):
            get_timers(self, websocket)
            return
        else:
            ws_send(websocket, 'loadgame', 'viewer',websocket.payload, {'figs':self.state.get_loaded_state()})
            ws_send(websocket, 'connection', 'player_connected', None, self.get_players_payloads())
            get_timers(self, websocket)


    def new_game(self, websocket):
        if self.id_in_players(websocket,0,0,['startgame', 'ok', websocket.payload, {'team': 0}]):
            get_timers(self, websocket)
            return
        if self.id_in_players(websocket,1,1,['startgame', 'ok', websocket.payload, {'team': 1}]):
            get_timers(self, websocket)
            return
        else:
            ws_send(websocket, 'startgame', 'viewer', websocket.payload)
            ws_send(websocket, 'connection', 'player_connected', None, self.get_players_payloads())
            get_timers(self, websocket)

    def id_in_players(self,websocket,id,team,data_to_send):
        if id not in self.players:
            websocket.team = team
            self.players[id] = websocket
            ws_send(websocket, *data_to_send)
            self.on_player_joined()
            main_menu.update()
            return True

def get_timers(self,websocket,message=None):
    ws_send(websocket, 'timers','get_timers',None, {'timers':self.state.timer.timers,'turn':self.state.turn})
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
    if not self.started:
        self.started=True
        main_menu.update()
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
            while id in self.websockets:
                id = str(id)+'clone'
            websocket.identifier = id
            self.websockets[id] = websocket
    except:
        if self.games[self.id].websockets.keys():
            id = min(min(self.websockets.keys()),0)-1
        else:
            id=-1
        payload={'username':f'guest{-1*id}','email':'','account':{'user':id,'rating':0}}
        websocket.payload=payload
        self.games[self.id].websockets[id]=websocket
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
    timers=[get_timers]
    def __init__(self,id,time1=None,time2=None):
        super().__init__(id,time1,time2)
        self.games=games
        self.websockets={}
        self.players={}
        self.events = [("connection",self.on_connection),("move",self.on_move),('chat_mess',self.on_chat_message),('timers',self.timers)]

class gameDict(dict):
    def __setitem__(self,key,value):
        super().__setitem__(key,value)
        main_menu.update()
        print(f'game {key} hosted')
    def pop(self,key,f=None):
        super().pop(key,f)
        main_menu.update()
        print(f'game {key} unhosted')


games = gameDict()
all_games = {'free':games}
main_menu.games = all_games