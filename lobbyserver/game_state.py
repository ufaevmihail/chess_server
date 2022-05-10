

class State:



    def __init__(self,game):
        self.game=game
        self.turn=0
        self.board = []
        self.turnList=[]
        self.endgame=False
        self.start_fig_params = [["roof", 0, 0, 0], ["konb", 1, 0, 0], ["slon", 2, 0, 0], ["king", 4, 0, 0],
                            ["ferz", 3, 0, 0],
                            ["slon", 5, 0, 0], ["konb", 6, 0, 0], ["roof", 7, 0, 0],
                            ["peshka", 0, 1, 0], ["peshka", 1, 1, 0], ["peshka", 2, 1, 0], ["peshka", 3, 1, 0],
                            ["peshka", 4, 1, 0], ["peshka", 5, 1, 0], ["peshka", 6, 1, 0],
                            ["peshka", 7, 1, 0],
                            ["roof", 0, 7, 1], ["konb", 1, 7, 1], ["slon", 2, 7, 1], ["king", 4, 7, 1],
                            ["ferz", 3, 7, 1],
                            ["slon", 5, 7, 1], ["konb", 6, 7, 1], ["roof", 7, 7, 1],
                            ["peshka", 0, 6, 1], ["peshka", 1, 6, 1], ["peshka", 2, 6, 1], ["peshka", 3, 6, 1],
                            ["peshka", 4, 6, 1], ["peshka", 5, 6, 1], ["peshka", 6, 6, 1],
                            ["peshka", 7, 6, 1]]
        self.kings= {}
        self.rooks=[[],[]]
        self.figures=[[],[]]
        for i in range(8):
            s=[]
            for j in range(8):
                s.append(None)
            self.board.append(s)
        for fig_p in self.start_fig_params:
            fig=get_figure(*fig_p,self.board,self.turnList,self)
            if fig.name=='roof':
                self.rooks[fig.team].append(fig)
            if fig.name=='king':
                self.kings[fig.team]=fig
            self.figures[fig.team].append(fig)
            self.board[fig_p[1]][fig_p[2]]=fig
        self.start_fig_params=None

    def get_loaded_state(self):
        figures=[]
        sledi=[]
        for stroka in self.board:
            for i in stroka:
                #sledpeshki?
                if i:
                    if i.type == 'sledpeshki':
                        sledi.append([i.px,i.py,i.peshka.px,i.peshka.py])
                    if i.type == 'figure':
                        figures.append([i.name,i.px,i.py,i.team,type(i).__name__,i.firstmove])
        return {'figures':figures,'turn':self.turn,'sledi':sledi,'lastmove':self.turnList[-1]}
    def move(self,turn):
        startx,starty = tuple(turn['startfield'])
        endx,endy=tuple(turn['endfield'])
        #if self.validate(startx,starty,endx,endy):
        self.board[startx][starty].make_move(endx,endy)
        self.check_matt_or_draw()
        for str in self.board:
            for field in str:
                if field and field.type == 'sledpeshki':
                    if field.peshka.team != self.turn % 2:
                        self.board[field.px][field.py]=None
                if field and field.type=='figure':
                    field.cantogofields=[]
        for key,king in self.kings.items():
            king.rokerate=True
        self.turn+=1
        #print('---------------------------')
        #for line in self.board:
         #   print(*line)

    def check_matt_or_draw(self):
        draw=True
        checkmat=False
        for figure in self.figures[self.turn %2]:
            figure.turnrule()
            king = self.kings[(self.turn+1)%2]
            if (king.px,king.py) in figure.cantogofields:
                checkmat=True
                f='бел' if self.turn%2 else 'черн'
                print(f'Шах {f}ым')
        for figure in self.figures[(self.turn+1)%2]:
            figure.turnrule()
            enemyfigurescantattackourking(figure)
            if len(figure.cantogofields)!=0:
                checkmat=False
                draw=False
                break
        if draw and not checkmat:
            print('ничья')
            self.endgame=True
            self.game.start_closing()
        if checkmat:
            print(f'Мат {f}ым')
            self.endgame=True
            self.game.start_closing()


    def validate(self,x,y,next_x,next_y):
        figure=self.board[x][y]
        if not figure or figure.type!='figure':
            return
        figure.turnrule()
        enemyfigurescantattackourking(figure)
        if (next_x,next_y) in figure.cantogofields:
            figure.cantogofields=[]
            return True




def get_figure(name,px,py,team,board,turnlist,state):
    if name == 'peshka':
        return Peshka(name,px,py,team,board,turnlist,state)
    elif name == 'king':
        return King(name,px,py,team,board,turnlist,state)
    else:
        return Figure(name,px,py,team,board,turnlist,state)
class Figure:
    def __init__(self,name,px,py,team,board,turnlist,state):
        self.type='figure'
        self.px=px
        self.py=py
        self.name = name
        self.team=team
        self.turnlist = turnlist
        self.board = board
        self.state=state
        self.firstmove = True
        self.turnrule=lambda:turnrules[name](self)
        self.cantogofields=[]
       # self.turnrule=turnrules[name]
    def make_move(self,px,py,tl=True):
        self.board[self.px][self.py]=None
        pred_fig = self.board[px][py]
        if pred_fig and pred_fig.type=='figure':
            self.state.figures[pred_fig.team].remove(pred_fig)
        self.board[px][py]=self
        if tl:
            self.turnlist.append([self.px,self.py,px,py])
        self.px=px
        self.py=py
        self.firstmove=False
        self.cantogofields=[]
        #for line in self.board:
         #   print(*line)
    def __repr__(self):
        f= 'w' if self.team==0 else 'b'
        return f'{f}{self.name}'

class Peshka(Figure):
    def make_move(self,px,py,tl=True):
        pred_py = self.py
        if self.board[px][py] and self.board[px][py].type=="sledpeshki":
            self.board[px][py].remove()
            sp=self.board[px][py]
            self.board[sp.peshka.px][sp.peshka.py]=None
        super().make_move(px,py)
        if abs(pred_py-self.py)==2:
            self.board[self.px][round((pred_py+self.py)/2)]=SledPeshki(self.px,round((pred_py+self.py)/2),self)
        if (self.team==0 and self.py==7) or (self.team==1 and self.py==0):
            self.board[self.px][self.py]=Figure("ferz", self.px, self.py, self.team,self.board,self.turnlist,self.state)


class SledPeshki:
    def __init__(self,px,py,peshka):
        self.name=''
        self.type = 'sledpeshki'
        self.peshka = peshka
        self.team = peshka.team
        self.px=px
        self.py=py
    def remove(self):
        self.peshka.state.figures[self.team].remove(self.peshka)

class King(Figure):
    def __init__(self,name,px,py,team,board,turnlist,state):
        super().__init__(name,px,py,team,board,turnlist,state)
        self.rokerate=True
    def make_move(self,px,py,tl=True):
        pred_px=self.px
        super().make_move(px,py)
        if abs(pred_px-self.px)==2:
            rooks=[]
            for stroka in self.board:
                for field in stroka:
                    if field and field.name=='roof' and field.team==self.team:
                        rooks.append(field)
            rook=min(rooks,key=lambda x: abs(x.px-self.px))
            rook.make_move(round((self.px+pred_px)/2),self.py,False)


def konbrule(this):
    k=(-1,-2,1,2)
    for i in k:
        for j in k:
            if abs(i)+abs(j)==3 and inBoard(this.px+i,this.py+j):
                field = this.board[this.px+i][this.py+j]
                if not field or field.type != 'figure':
                    this.cantogofields.append((this.px+i,this.py+j))
                else:
                    if field.team != this.team:
                        this.cantogofields.append((this.px+i,this.py+j))


def slonrule(obj):
    k=[1,-1]
    for i in k:
        for j in k:
            p=1
            while inBoard(obj.px+p*i,obj.py+p*j):
                field = obj.board[obj.px+p*i][obj.py+p*j]
                if not field or field.type != 'figure':
                    obj.cantogofields.append((obj.px+p*i,obj.py+p*j))
                else:
                    if field.team==obj.team:
                        break
                    else:
                        obj.cantogofields.append((obj.px+p*i,obj.py+p*j))
                        break
                p += 1
def enemyfigurescantattackourking(this):
    this.state.board[this.px][this.py]=None
    cantogofieldscopy = this.cantogofields.copy()
    for fld in cantogofieldscopy:
        afigure = this.board[fld[0]][fld[1]]
        this.board[fld[0]][fld[1]]=this
        for figure in this.state.figures[(this.team+1)%2]:
            figure.turnrule()
            if this.name=='king':
                if fld in figure.cantogofields:
                    this.cantogofields.remove(fld)
                    #break не надо этого делать
            ourking = this.state.kings[this.team]
            if (ourking.px,ourking.py) in figure.cantogofields:
                this.state.kings[this.team].rokerate=False
                if fld != (figure.px,figure.py) and this.name != 'king':
                    this.cantogofields.remove(fld)
                   # break
                #figure.cantogofields=[]
            figure.cantogofields=[]
        this.board[fld[0]][fld[1]]=afigure
    this.state.board[this.px][this.py]=this

def roofrule(obj):
    v=([1,0],[-1,0],[0,1],[0,-1])
    for t in v:
        i=t[0]
        j=t[1]
        p=1
        while inBoard(obj.px+p*i,obj.py+p*j):
            field = obj.board[obj.px+p*i][obj.py+p*j]
            if not field or field.type != 'figure':
                obj.cantogofields.append((obj.px+p*i,obj.py+p*j))
            else:
                if field.team == obj.team:
                    break
                else:
                    obj.cantogofields.append((obj.px+p*i,obj.py+p*j))
                    break
            p+=1

def ferzrule(obj):
    slonrule(obj)
    roofrule(obj)

def kingrule(this):
    v=[-1,0,1]
    for i in v:
        for j in v:
            if inBoard(this.px+i,this.py+j) and abs(i)+abs(j) != 0:
                field=this.board[this.px+i][this.py+j]
                if not field or field.type != 'figure' or field.team != this.team:
                    this.cantogofields.append((this.px+i,this.py+j))
    rokerate(this)
def rokerate(king):
    if king.firstmove and king.state.kings[(king.team+1)%2].rokerate:
        #print(king.state.rooks[king.team].__dict__)
        for rook in king.state.rooks[king.team]:
            if rook.firstmove:
                if noFiguresBetween(king,rook):
                   # print('1111')
                    x=-2 if king.px>rook.px else 2
                    if rokerateNotUnderAttack(king,rook):
                      #  print('2222')
                        king.cantogofields.append((king.px+x,king.py))
def rokerateNotUnderAttack(king,rook):
    z=king.px-2 if king.px > rook.px else king.px+2
    t=min(z,king.px)
    k=max(z,king.px)
    for fig in king.state.figures[(king.team+1)%2]:
        if fig.name!='king':
            fig.turnrule()
            for i in range(t,k+1):
                fld = (i,king.py)
                if (fld in fig.cantogofields):
                    return False
    return True
def noFiguresBetween(king,rook):
    mi=min([king,rook],key=lambda el: el.px).px
    ma=max([king,rook],key=lambda el: el.px).px
    for i in range(mi+1,ma):
        if king.board[i][king.py] != None and king.board[i][king.py].type == 'figure':
            return False
    return True

def peshkarule(this):
    v= 1 if this.team==0 else -1
    if inBoard(this.px,this.py+v) and (not this.board[this.px][this.py+v] or this.board[this.px][this.py+v].type != 'figure'):
        this.cantogofields.append((this.px,this.py+v))
        if this.firstmove and (not this.board[this.px][this.py+2*v] or this.board[this.px][this.py+2*v].type != 'figure'):
            this.cantogofields.append((this.px,this.py+2*v))
    for i in [1,-1]:
        f=this.px+i
        k=this.py+v
        if inBoard(f,k):
            if this.board[this.px+i][this.py+v]!= None and this.board[this.px+i][this.py+v].team != this.team:
                this.cantogofields.append((this.px+i,this.py+v))
           # elif this.board[this.px+i][this.py+v]


def inBoard(x,y):
    return x>-1 and x<8 and y>-1 and y<8

turnrules={'konb':konbrule,'slon':slonrule,'ferz':ferzrule,'king':kingrule,'peshka':peshkarule,'roof':roofrule}
'''class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)'''
#for stroka in self.board:
         #   print(*[(figure.name, figure.team) if figure else None for figure in stroka])