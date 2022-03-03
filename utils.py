import numpy as np
from queue import PriorityQueue
from collections import deque

class Product:
    def __init__(self, aName):
        self.theName = aName
        self.theOrderBook = OrderBook()

# TODO: might have to add some quick way to answer
# the question "how many orders in the last second?"
# Currently this data structure just quickly tells us
# how long ago the (n - 50)th order was if we are on
# the nth order
class Stopwatch:

    def __init__(self, aSize):
        self.theTimestamps = np.zeros(aSize)
        self.theSize = aSize
        self.theCount  = 0
        self.theLastTimestamp = 0

    def getSize(self):
        return self.theSize

    def getCount(self):
        return self.theCount

    # TODO: Watch out for how the exchange does timestamping.
    # e.g. if one aggressive order trades through multiple passive orders
    # does each trade caused by this get the same timestamp?
    def doTimestamp(self, aTimestamp):
        self.theCount += 1
        myLastTimestamp = self.theTimestamps[self.theLastTimestamp]
        self.theLastTimestamp = (self.theLastTimestamp + 1) % self.theSize
        self.theTimestamps[self.theLastTimestamp] = aTimestamp
        return aTimestamp - myLastTimestamp

class Trader:

    def __init__(self, aName):
        self.theName = aName
        self.thePositions = {}
        self.theStopwatch = Stopwatch(50)
        self.theActiveOrders = {}

    def getPosition(self, aProductName):
        return self.thePositions[aProductName]

    def changePosition(self, aProductName, aChange):
        self.thePositions[aProductName] += aChange

    def addProduct(self, aProductName):
        self.thePositions[aProductName] = 0

    def addOrder(self, aOrder):
        self.theActiveOrders[aOrder.theId] = aOrder

    def removeOrder(self, aOrder):
        self.theActiveOrders.pop(aOrder.theId)

        

class ExchangeInfo:

    def __init__(self, aOurName):
        self.theOurName = aOurName
        self.theProducts = {}
        self.theTraders = {}

    def addTrader(self, aTraderName):
        self.theTraders[aTraderName] = Trader(aTraderName)

    def addProduct(self, aProductName):
        self.theProducts[aProductName] = Product(aProductName)
        for myTrader in self.theTraders.items():
            myTrader.addProduct(aProductName)

    def addOrder(self, aProductName, aOrder):
        if(aProductName not in self.theProducts.keys()):
            self.addProduct(aProductName)
        if(aOrder.theTraderName not in self.theTraders.keys()):
            self.addTrader(aOrder.theTraderName)

        self.theTraders[aOrder.theTraderName].addOrder(aOrder)
        self.theProducts[aProductName].theOrderBook.addOrder(aOrder)
  
    def amendOrder(self, aOrder, aVolumeChange):

        self.theTraders[aOrder.theTraderName]. \
            theActiveOrders[aOrder.theId]. \
            changeVolume(aVolumeChange)   
    

class Level:

    def __init__(self, aPrice, aNullLevel):
        self.thePrice = aPrice
        self.theTotalVolume = 0
        self.theMyVolume = 0
        self.theSize = 0
        self.theColour = 1 # 1 = red, 0 = black
        self.theFirstOrder = None
        self.theLastOrder = None
        self.theParentLevel = None
        self.theLeftChildLevel = aNullLevel
        self.theRightChildLevel = aNullLevel

    def addOrder(self, aOrder):
        if(self.theFirstOrder == None):
            self.theLastOrder = aOrder
            self.theLastOrder = aOrder
        else:
            aOrder.setPreviousOrder(self.theLastOrder)
            self.theLastOrder.setNextOrder(aOrder)
            self.theLastOrder = aOrder

        self.theSize += 1
        self.theTotalVolume += aOrder.getVolume()
        if(aOrder.getIsMine()):
            self.theMyVolume += aOrder.getVolume()

    def removeOrder(self, aOrder):
        if(aOrder.getPreviousOrder() != None):
            aOrder.getPreviousOrder().setNextOrder(aOrder.getNextOrder())            
        if(aOrder.getNextOrder() != None):
            aOrder.getNextOrder().setPreviousOrder(aOrder.getPreviousOrder())

        self.theSize -= 1
        self.theTotalVolume -= aOrder.getVolume()
        if(aOrder.getIsMine()):
            self.theMyVolume -= aOrder.getVolume()

    def changeOrderVolume(self, aOrder, aVolumeChange):
        if(aVolumeChange == -aOrder.getVolume()):
            self.removeOrder(aOrder)
        else:
            aOrder.changeVolume(aVolumeChange)
            self.theTotalVolume += aVolumeChange
            if(aOrder.getIsMine()):
                self.theMyVolume += aVolumeChange

    def setColour(self, aColour):
        self.theColour = aColour 

    def changeTotalVolume(self, aChange):
        self.theTotalVolume += aChange

    def changeMyVolume(self, aChange):
        self.theMyVolume += aChange

    def setFirstOrder(self, aOrder):
        self.theFirstOrder = aOrder
    
    def setLastOrder(self, aOrder):
        self.theLastOrder = aOrder

    def setParentLevel(self, aLevel):
        self.theParentLevel = aLevel

    def setLeftChildLevel(self, aLevel):
        self.theLeftChildLevel = aLevel
    
    def setRightChildLevel(self, aLevel):
        self.theRightChildLevel = aLevel

    def incSize(self):
        self.theSize += 1

    def decSize(self):
        self.theSize -= 1

    def changeSize(self, aChange):
        self.theSize += aChange

    def getColour(self):
        return self.theColour

    def getFirstOrder(self):
        return self.theFirstOrder

    def getLastOrder(self):
        return self.theLastOrder

    def getParentLevel(self):
        return self.theParentLevel

    def getLeftChildLevel(self):
        return self.theLeftChildLevel

    def getRightChildLevel(self):
        return self.theRightChildLevel

    def getPrice(self):
        return self.thePrice

    def getTotalVolume(self):
        return self.theTotalVolume

    def getMyVolume(self):
        return self.theMyVolume

    def getSize(self):
        return self.theSize

class Order: 

    def __init__(self, aPrice, aTimestamp, aVolume, aTraderName, aSide, aId, aIsMine):
        self.thePrice = aPrice
        self.theTimestamp = aTimestamp
        self.theVolume = aVolume
        self.theTraderName = aTraderName
        self.theSide = aSide # True = buy, False = sell
        self.theId = aId
        self.theNextOrder = None
        self.thePreviousOrder = None
        self.theIsMine = aIsMine
        self.theLevel = None
        
    def changeVolume(self, aChange):
        self.theVolume -= aChange

    def setPreviousOrder(self, aOrder):
        self.thePreviousOrder = aOrder

    def setNextOrder(self, aOrder):
        self.theNextOrder = aOrder

    def setLevel(self, aLevel):
        self.theLevel = aLevel

    def getPreviousOrder(self):
        return self.thePreviousOrder

    def getNextOrder(self):
        return self.theNextOrder
        
    def getPrice(self):
        return self.thePrice

    def getTimestamp(self):
        return self.theTimestamp

    def getVolume(self):
        return self.theVolume

    def getTraderName(self):
        return self.theTraderName

    def getSide(self):
        return self.theSide

    def getId(self):
        return self.theId

    def getIsMine(self):
        return self.theIsMine

    def getLevel(self):
        return self.theLevel

class OrderBook:

    def __init__(self):
        self.theOrders = {}
        self.theLevels = {}

        self.theNullLevel = Level(0, None)
        self.theNullLevel.theColour = 0

        self.theBidLevelTree = self.theNullLevel
        self.theAskLevelTree = self.theNullLevel
        self.theLowestAsk = None
        self.theHighestBid = None

    def initialzieLevels(self, aPriceLevelList):
        for myPrice in aPriceLevelList:
            self.addNewLevel(myPrice)

    def addOrder(self, aOrder):
        self.theOrders[aOrder.getId()] = aOrder

        myOrderPrice = aOrder.getPrice()
        if(not myOrderPrice in self.theLevels):
            myLevel = self.addNewLevel(aOrder.thePrice)
        else:
            myLevel = self.theLevels[myOrderPrice]
            # if level has size zero, it is not in the tree
            # and must be added again
        self.addExistingLevel(myLevel, aOrder.theSide)

        aOrder.setLevel(myLevel)
        myLevel.addOrder(aOrder)       

    def addExistingLevel(self, aLevel, aSide):
        # we have to add the level to the tree 
        if(aSide): # aSide = True is buy side
            if(self.theBidLevelTree == self.theNullLevel):
                # initialize tree
                aLevel.theColour = 0
                self.theBidLevelTree = aLevel
                self.theHighestBid = aLevel                
            else:
                # add to tree
                self.insertLevel(aLevel, aSide)  
                self.updateHighestBidAfterAdd(aLevel)              
        else:
            if(self.theAskLevelTree == self.theNullLevel):
                #initialize tree
                self.theAskLevelTree = aLevel
                self.theLowestAsk = aLevel
            else:
                # add to tree
                self.insertLevel(aLevel, aSide)  
                self.updateLowestAskAfterAdd(aLevel)      

    def updateHighestBidAfterAdd(self, aLevel):
        # we have added 'aLevel' to the tree
        # we want to check if it is the new highest bid
        if(self.theHighestBid.thePrice < aLevel.thePrice):
            self.theHighestBid = aLevel

    def updateLowestAskAfterAdd(self, aLevel):
        # we have added 'aLevel to the tree
        # we want to check if it is the lowest ask
        if(self.theLowestAsk.thePrice > aLevel.thePrice):
            self.theLowestAsk = aLevel

    def updateHighestBidBeforeRemove(self, aLevel):

        # we have removed 'aLevel' from the tree
        # if aLevel was the highest bid, we must
        # find the new highest bid
        # there are two possibilities:
        # 1. The max bid is a right child
        #    --> take the parent as the new max,
        #    --> or the max of the left subtree
        #
        # 2. The max bid is the root
        #    --> take the max of the left subtree
        if(aLevel != self.theHighestBid):
            return
        elif(aLevel.theParentLevel is not None):
            if(aLevel.theLeftChildLevel == self.theNullLevel):
                self.theHighestBid = aLevel.theParentLevel
            else:
                self.theHighestBid = self.maximum(aLevel.theLeftChildLevel)
        else:
            if(aLevel.theLeftChildLevel != self.theNullLevel):
                self.theHighestBid = self.maximum(aLevel.theLeftChildLevel)
            else:
                return None

    def updateLowestAskBeforeRemove(self, aLevel):
        # we have removed 'aLevel' from the tree
        # if aLevel was the lowest , we must
        # find the new lowest ask
        # there are two possibilities:
        # 1. The min ask is a left child
        #    --> take the parent as the new min,
        #    --> or the min of the right subtree
        #
        # 2. The min ask is the root
        #    --> take the min of the right subtree
        if(aLevel != self.theLowestAsk):
            return
        elif(aLevel.theParentLevel is not None):
            if(aLevel.theRightChildLevel == self.theNullLevel):
                self.theLowestAsk = aLevel.theParentLevel
            else:
                self.theLowestAsk = self.minimum(aLevel.theRightChildLevel)
        else:
            if(aLevel.theRightChild != self.theNullLevel):
                self.theLowestAsk = self.minimum(aLevel.theRightChildLevel)
            else:
                return None

    def addNewLevel(self, aPrice):
        myNewLevel = Level(aPrice, self.theNullLevel)        
        self.theLevels[aPrice] = myNewLevel
        return myNewLevel

    def removeOrder(self, aId):
        myOrder = self.theOrders[aId]
        mySide = myOrder.theSide
        myPrice = myOrder.thePrice
        myLevel = self.theLevels[myPrice]
        myLevel.removeOrder(myOrder)
        if(myLevel.theSize == 0):
            if(mySide):
                self.updateHighestBidBeforeRemove(myLevel)
            else:
                self.updateLowestAskBeforeRemove(myLevel)
            self.removeLevel(myLevel, mySide)            

    def changeOrderVolume(self, aId, aVolumeChange):
        myOrder = self.theOrders[aId]
        self.theLevels[myOrder.getPrice()].changeOrderVolume(myOrder, aVolumeChange)

    def getHighestBidLevel(self):
        return self.theHighestBidLevel

    def getLowestAskLevel(self):
        return self.theHighestAskLevel

    def leftRotate(self, aLevel, aSide):
        myOldRightChild = aLevel.theRightChildLevel                                   
        aLevel.theRightChildLevel = myOldRightChild.theLeftChildLevel                                
        if(myOldRightChild.theLeftChildLevel != self.theNullLevel):
            myOldRightChild.theLeftChildLevel.theParentLevel = aLevel

        myOldRightChild.theParentLevel = aLevel.theParentLevel                             
        if(aLevel.theParentLevel == None):  
            if(aSide):                          
                self.theBidLevelTree = myOldRightChild 
            else:
                self.theAskLevelTree = myOldRightChild                                               
        elif(aLevel == aLevel.theParentLevel.theLeftChildLevel):
            aLevel.theParentLevel.theLeftChildLevel = myOldRightChild
        else:  
            aLevel.theParentLevel.theRightChildLevel = myOldRightChild
        myOldRightChild.theLeftChildLevel = aLevel
        aLevel.theParentLevel = myOldRightChild

    def rightRotate(self, aLevel, aSide):
        myOldLeftChild = aLevel.theLeftChildLevel                         
        aLevel.theLeftChildLevel = myOldLeftChild.theRightChildLevel       
        if(myOldLeftChild.theRightChildLevel != self.theNullLevel):
            myOldLeftChild.theRightChildLevel.theParentLevel = aLevel

        myOldLeftChild.theParentLevel = aLevel.theParentLevel              
        if(aLevel.theParentLevel == None):                                 
            if(aSide):
                self.theBidLevelTree = myOldLeftChild                      
            else:
                self.theAskLevelTree = myOldLeftChild
        elif(aLevel == aLevel.theParentLevel.theRightChildLevel):
            aLevel.theParentLevel.theRightChildLevel = myOldLeftChild
        else:
            aLevel.theParentLevel.theLeftChildLevel = myOldLeftChild
        myOldLeftChild.theRightChildLevel = aLevel
        aLevel.theParentLevel = myOldLeftChild

    def insertLevel(self, aNewLevel, aSide):
        y = None
        if(aSide): # True = buy, False = Sell
            x = self.theBidLevelTree
        else:
            x = self.theAskLevelTree

        while(x != self.theNullLevel):                
            y = x
            if(aNewLevel.thePrice < x.thePrice):
                x = x.theLeftChildLevel
            else:
                x = x.theRightChildLevel

        aNewLevel.theParentLevel = y                             
        if(y == None):                              
            if(aSide):
                self.theBidLevelTree = aNewLevel
            else:
                self.theAskLevelTree = aNewLevel
        elif(aNewLevel.thePrice < y.thePrice):
            y.theLeftChildLevel = aNewLevel
        else:
            y.theRightChildLevel = aNewLevel

        if(aNewLevel.theParentLevel == None):                   
            aNewLevel.theColour = 0
            return

        if(aNewLevel.theParentLevel.theParentLevel == None):                  
            return

        self.fixInsert(aNewLevel, aSide)                         

    def fixInsert(self, aLevel, aSide):   
        while(aLevel.theParentLevel.theColour == 1):                      
            if(aLevel.theParentLevel == aLevel.theParentLevel.theParentLevel.theRightChildLevel): 
                u = aLevel.theParentLevel.theParentLevel.theLeftChildLevel            
                if(u.theColour == 1):                       
                    u.theColour = 0                      
                    aLevel.theParentLevel.theColour = 0
                    aLevel.theParentLevel.theParentLevel.theColour = 1       
                    aLevel = aLevel.theParentLevel.theParentLevel            
                else:
                    if(aLevel == aLevel.theParentLevel.theLeftChildLevel):               
                        aLevel = aLevel.theParentLevel
                        self.rightRotate(aLevel, aSide)                      
                    aLevel.theParentLevel.theColour = 0
                    aLevel.theParentLevel.theParentLevel.theColour = 1
                    self.leftRotate(aLevel.theParentLevel.theParentLevel, aSide)
            else:                                        
                u = aLevel.theParentLevel.theParentLevel.theRightChildLevel                 
                if(u.theColour == 1):                        
                    u.theColour = 0                          
                    aLevel.theParentLevel.theColour = 0
                    aLevel.theParentLevel.theParentLevel.theColour = 1           
                    aLevel = aLevel.theParentLevel.theParentLevel               
                else:
                    if(aLevel == aLevel.theParentLevel.theRightChildLevel):          
                        aLevel = aLevel.theParentLevel
                        self.leftRotate(aLevel, aSide)                        
                    aLevel.theParentLevel.theColour = 0
                    aLevel.theParentLevel.theParentLevel.theColour = 1
                    self.rightRotate(aLevel.theParentLevel.theParentLevel, aSide)   

            if(aSide):          
                if(aLevel == self.theBidLevelTree):                           
                    break
            else:
                if(aLevel == self.theBidLevelTree):                           
                    break

        if(aSide):
            self.theBidLevelTree.theColour = 0   
        else:
            self.theAskLevelTree.theColour = 0                       

    def removeLevel(self, aLevel, aSide):
        y = aLevel
        y_original_color = y.theColour                         
        if(aLevel.theLeftChildLevel == self.theNullLevel):                           
            x = aLevel.theRightChildLevel                               
            self.__rb_transplant(aLevel, aLevel.theRightChildLevel, aSide)          
        elif(aLevel.theRightChildLevel == self.theNullLevel) :                      
            x = aLevel.theLeftChildLevel                                    
            self.__rb_transplant(aLevel, aLevel.theLeftChildLevel, aSide)           
        else:                                            
            y = self.minimum(aLevel.theRightChildLevel)                
            y_original_color = y.theColour                
            x = y.theRightChildLevel
         
            if(y.theParentLevel == aLevel):               
                x.theParentLevel = y                            
            else:
                self.__rb_transplant(y, y.theRightChildLevel, aSide)
                y.theRightChildLevel = aLevel.theRightChildLevel
                y.theRightChildLevel.theParentLevel = y

            self.__rb_transplant(aLevel, y, aSide)
            y.theLeftChildLevel = aLevel.theLeftChildLevel
            y.theLeftChildLevel.theParentLevel = y
            y.theColour = aLevel.theColour
        if(y_original_color == 0):                       
            self.fixDelete(x, aSide)

        aLevel.theParentLevel = self.theNullLevel
        aLevel.theRightChildLevel = None
        aLevel.theLeftChildLevel = None
        
    def fixDelete(self, aLevel, aSide):
        if(aSide):
            myRoot = self.theBidLevelTree
        else:
            myRoot = self.theAskLevelTree

        while(aLevel != myRoot and aLevel.theColour == 0):     
            if(aLevel == aLevel.theParentLevel.theLeftChildLevel):                
                s = aLevel.theParentLevel.theRightChildLevel   
                if(s.theColour == 1):               
                    s.theColour = 0                      
                    aLevel.theParentLevel.theColour = 1             
                    self.leftRotate(aLevel.theParentLevel, aSide)                 
                    s = aLevel.theParentLevel.theRightChildLevel
                if(s.theLeftChildLevel.theColour == 0 and s.theRightChildLevel.theColour == 0):
                    s.theColour = 1                     
                    aLevel = aLevel.theParentLevel
                else:
                    if(s.theRightChildLevel.theColour == 0):            
                        s.theLeftChildLevel.theColour = 0               
                        s.theColour = 1                 
                        self.rightRotate(s, aSide)                     
                        s = aLevel.theParentLevel.theRightChildLevel

                    s.theColour = aLevel.theParentLevel.theColour
                    aLevel.theParentLevel.theColour = 0                  
                    s.theRightChildLevel.theColour = 0
                    self.leftRotate(aLevel.theParentLevel, aSide)             
                    aLevel = myRoot
            else:                                     
                s = aLevel.theParentLevel.theLeftChildLevel                      
                if(s.theColour == 1):                         
                    s.theColour = 0                      
                    aLevel.theParentLevel.theColour = 1                  
                    self.rightRotate(aLevel.theParentLevel, aSide)               
                    s = aLevel.theParentLevel.theLeftChildLevel

                if(s.theRightChildLevel.theColour == 0 and s.theRightChildLevel.theColour == 0):
                    s.theColour = 1
                    aLevel = aLevel.theParentLevel
                else:
                    if(s.theLeftChildLevel.theColour == 0):                
                        s.theRightChildLevel.theColour = 0                 
                        s.theColour = 1
                        self.leftRotate(s, aSide)                     
                        s = aLevel.theParentLevel.theLeftChildLevel

                    s.theColour = aLevel.theParentLevel.theColour
                    aLevel.theParentLevel.theColour = 0
                    s.theLeftChildLevel.theColour = 0
                    self.rightRotate(aLevel.theParentLevel, aSide)
                    aLevel = myRoot
        aLevel.theColour = 0


    def __rb_transplant(self, u, v, aSide):
        
        if(u.theParentLevel == None):
            if(aSide):
                self.theBidLevelTree = v
            else:
                self.theAskLevelTree = v
        elif(u == u.theParentLevel.theLeftChildLevel):
            u.theParentLevel.theLeftChildLevel = v
        else:
            u.theParentLevel.theRightChildLevel = v
        v.theParentLevel = u.theParentLevel

    def minimum(self, aLevel):
        while(aLevel.theLeftChildLevel != self.theNullLevel):
            aLevel = aLevel.theLeftChildLevel
        return aLevel
        
    def maximum(self, aLevel):
        while(aLevel.theRightChildLevel != self.theNullLevel):
            aLevel = aLevel.theRightChildLevel
        return aLevel

    def sum(self, aLevel, aTotal):
        if(aLevel == self.theNullLevel):
            return aTotal
        else: 
            return aLevel.thePrice + \
                sum(aLevel.theLeftChildLevel) + \
                sum(aLevel.theRightChildLevel)

    def sumFirstN(self, aLevel, N):
        myTotal = 0
        myLevelStack = deque()
        myLevel = aLevel
        myIndex = 0
        while(myLevelStack or myLevel != self.theNullLevel):
    
            if(myLevel != self.theNullLevel):
                myLevelStack.append(myLevel)
                myLevel = myLevel.theLeftChildLevel
            else:
                myLevel = myLevelStack.pop()
                myTotal += myLevel.thePrice
                myIndex += 1
                if(myIndex == N):
                    return myTotal
    
                myLevel = myLevel.theRightChildLevel
            
        return myTotal
 
    # Function to generate string expressing tree
    def __expressCall ( self , node , indent , last ) :
      
        if node != self.theNullLevel :
            self.theExpression += indent + " "
            #print(indent, end=' ')
            if last :
                self.theExpression += "R---- "
                #print ("R----",end= ' ')
                indent += "     "
            else :
                self.theExpression += "L---- "
                #print("L----",end=' ')
                indent += "|    "

            s_color = "RED" if node.theColour == 1 else "BLACK"
            self.theExpression += str ( node.thePrice ) + "(" + s_color + ")"
            #print ( str ( node.val ) + "(" + s_color + ")" )
            self.__expressCall ( node.theLeftChildLevel , indent , False )
            self.__expressCall ( node.theRightChildLevel , indent , True )

    def express_tree (self, aSide) :
        self.theExpression = ""

        if(aSide):
            myRoot = self.theBidLevelTree
        else:
            myRoot = self.theAskLevelTree
        self.__expressCall ( myRoot , "" , True )
        return self.theExpression
