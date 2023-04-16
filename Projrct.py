from Queue import *
from Node import *
from dataclasses import dataclass, field
from typing import Any
import math
from time import sleep
from dataclasses import dataclass, field
from typing import Any
from time import perf_counter
from functools import wraps
from AISearchAlgorithm import *
@dataclass
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)
class Searchalgorithm(AISearchAlgorithm):
    __slots__ = ('_Barricade' ,'_Food' , '_Pacman','_Branching_fuctor','_BoardBorder','_RootNode','_RootNodeForAStar','_ClosedList','_count' , '_countAStar' , '_countDFS' , '_countBFS')
    def __init__(self, Pacman , Food , Barricade , Branching_fuctor=4):
        self._Barricade = Barricade
        self._Food = Food
        self._Pacman = Pacman
        self._Branching_fuctor  = Branching_fuctor
        self._BoardBorder = [(0,0) , (20,20)]
        self._RootNode = self._making_node(None , self._Pacman)[0]
        self._RootNodeForAStar = self._making_nodeForAStar(None , self._Pacman)
        self._ClosedList =  []
        self._count = 0


    def time_calculation(func):
        @wraps(func)
        def wr_decorator(*args , **kwargs):
            start_time = perf_counter()
            value = func(*args , **kwargs)
            end_time= perf_counter()
            run_time = end_time - start_time
            print("the run time of " , func.__name__ ,"is:" , run_time)
            return value
        return wr_decorator


    @time_calculation
    def BFS(self)->None :
        _fringe = MYFIFOQueue(self)
        _addjacent  = self._adjacent_generator_for_BF1(self._RootNode);
        _fringe.PutInOrder(self._making_node(self._Pacman , _addjacent  ))
        while True:
            Checking_Node = _fringe.get()
            if(_fringe.empty()):
                #hamid jan agar koskhol nisti ke hasti inja hamoon jaei ke maeloom mish rahi nist
                #if your vigina is not stupid and ofcourse it is this is where we noticed there is no way
                pass
            if((Checking_Node.x , Checking_Node.y) not in self._ClosedList and self._barricade_checking(Checking_Node) and self._board_border(Checking_Node)):
                self._ClosedList.append((Checking_Node.x , Checking_Node.y))
                #hamid
                next(self)
                if self._goal_test(Checking_Node):
                    while True:
                        #hamid
                        Checking_Node = Checking_Node.parrent
                        if(Checking_Node == None):
                            break
                else:
                    self._expand(Checking_Node , _fringe)





    @time_calculation
    def DFS(self) -> None :
        _fringe = MYFIFOQueue(self)
        _addjacent  = self._adjacent_generator_for_BF1(self._RootNode);
        _fringe.PutInOrder(self._making_node(self._Pacman , _addjacent  ))
        while True:
            Checking_Node = _fringe.get()
            if(_fringe.empty()):
                #hamid jan agar koskhol nisti ke hasti inja hamoon jaei ke maeloom mish rahi nist
                #if your vigina is not stupid and ofcourse it is this is where we noticed there is no way
                pass
            if((Checking_Node.x , Checking_Node.y) not in self._ClosedList and self._barricade_checking(Checking_Node) and self._board_border(Checking_Node)):
                self._ClosedList.append((Checking_Node.x , Checking_Node.y))
                #hamid
                next(self)
                if self._goal_test(Checking_Node):
                    while True:
                        #hamid
                        Checking_Node = Checking_Node.parrent
                        if(Checking_Node == None):
                            break
                else:
                    self._expand(Checking_Node , _fringe)


    @time_calculation
    def AStar(self) ->None:
        _fringe = MYPriorityQueue(self)
        _addjacent  = self._adjacent_generator_for_BF1(self._RootNodeForAStar);
        _fringe.PutInOrder(self._making_nodeForAStar(self._Pacman , _addjacent  ))
        while True:
            Checking_Node = _fringe.get()[2]
            if(_fringe.empty()):
                #hamid jan agar koskhol nisti ke hasti inja hamoon jaei ke maeloom mish rahi nist
                #if your vigina is not stupid and ofcourse it is this is where we noticed there is no way
                print("KKKKKK")
                pass
            if((Checking_Node.x , Checking_Node.y) not in self._ClosedList and self._barricade_checking(Checking_Node) and self.board_border(Checking_Node)):
                self._ClosedList.append((Checking_Node.x , Checking_Node.y))
                #hamid
                next(self)
                if self._goal_test(Checking_Node):
                    while True:
                        #hamid
                        Checking_Node = Checking_Node.parrent
                        if(Checking_Node == None):
                            break
                else:
                    self._expandNodeForAStar(Checking_Node , _fringe)






    def _adjacent_generator_for_BF1(self , node)->list:
        _addjacant=[
        (node.x + 1 , node.y) ,
        (node.x  , node.y+1)  ,
        (node.x -1 , node.y) ,
        (node.x , node.y-1)

        ]
        return _addjacant
    def _board_border(self,Node)->bool:
        if(Node.x>self._BoardBorder[0][0] and Node.y>self._BoardBorder[0][1] and Node.x<self._BoardBorder[1][0] and Node.y<self._BoardBorder[1][1] ):
            return True

    def _making_node(self,parrent , *Address)->list:
        l = []
        for item in Address[0]:
            node  = Node()
            node.x = item[0]
            node.y = item[1]
            node.parrent =  parrent
            l.append(node)
        return l


    def _making_nodeForAStar(self,parrent , *Address)->list:
        l = []
        for item in Address[0]:
            node  = AStarNode()
            node.x = item[0]
            node.y = item[1]
            _food = self._Food[0]
            try:
                node.value = math.sqrt((item[0]-_food[0])**2 + (item[1]-_food[1])**2)+parrent.TravelledDistance+1
                node.TravelledDistance = parrent.TravelledDistance + 1
            except:
                node.value = math.sqrt((item[0]-_food[0])**2 + (item[1]-_food[1])**2)+1
                node.TravelledDistance = 1
            node.parrent =  parrent
            l.append(node)
        return l


    def _barricade_checking(self , node)->bool:
        if ((node.x , node.y)) not in self._Barricade:
            return True


    def _goal_test(self , node )->bool:
        if ((node.x,node.y)) in self._Food:
            return True


    def _expand(self , node , _fringe)->None:
        addjacent =self._making_node(node , self._adjacent_generator_for_BF1(node))
        for ChildNode in addjacent:
            if (ChildNode.x ,ChildNode.y)  not in self._ClosedList and self._barricade_checking(ChildNode) and self._board_border(ChildNode):
                _fringe.put(ChildNode)


    def _expandNodeForAStar(self , node , _fringe)->None:
        addjacent =self._making_nodeForAStar(node , self._adjacent_generator_for_BF1(node))
        for ChildNode in addjacent:
            if (ChildNode.x , ChildNode.y) not in self._ClosedList and self._barricade_checking(ChildNode) and self._board_border(ChildNode):
                _fringe.put(ChildNode)


    def __enter__(self):
        return self


    def __exit__(self , exc_type , exc_val , exc_tb ):
        return True


    def __next__(self):
        self._count+=1
        return self._count


if __name__ == '__main__':
    pass








