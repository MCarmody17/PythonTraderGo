import numpy as np
from queue import PriorityQueue


def rightRotate(aRoot, aLevel):
    y = aLevel.left                                       # Y = Left child of x
    aLevel.left = y.right                                 # Change left child of x to right child of y
    if y.right != None :
        y.right.parent = aLevel

    y.parent = aLevel.parent                              # Change parent of y as parent of x
    if aLevel.parent == None :                            # If x is root node
        aRoot = y                                # Set y as root
    elif aLevel == aLevel.parent.right :
        aLevel.parent.right = y
    else:
        aLevel.parent.left = y
    y.right = aLevel
    aLevel.parent = y

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

    def doTimestamp(self, aTimestamp):
        self.theCount += 1
        myLastTimestamp = self.theTimestamps[self.theLastTimestamp]
        self.theLastTimestamp = (self.theLastTimestamp + 1) % self.theSize
        self.theTimestamps[self.theLastTimestamp] = aTimestamp
        return aTimestamp - myLastTimestamp

class Trader:

    def __init__(self, aName):
        self.theName = aName
        self.thePosition = 0

    def getPosition(self):
        return self.thePosition

    def updatePosition(self, aChange):
        self.thePosition += aChange

class Level:

    def __init__(self, aPrice):
        self.thePrice = aPrice
        self.theTotalVolume = 0
        self.theMyVolume = 0
        self.theSize = 0
        self.theColour = 1 # 1 = red, 0 = black
        self.theFirstOrder = None
        self.theLastOrder = None
        self.theParentLevel = None
        self.theLeftChildLevel = None
        self.theRightChildLevel = None

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
        self.theBidLevelTree = None
        self.theAskLevelTree = None
        self.theLowestAsk = None
        self.theHighestBid = None

    def addOrder(self, aOrder):
        self.theOrders[aOrder.getId()] = aOrder

        myOrderPrice = aOrder.getPrice()
        if(not myOrderPrice in self.theLevels):
            myLevel = self.addNewLevel(aOrder.thePrice, aOrder.theSide)
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
            if(self.theBidLevelTree == None):
                # initialize tree
                self.theBidLevelTree = aLevel
                self.theHighestBid = aLevel
            else:
                # add to tree
                self.insertLevel(aLevel, aSide)  
                self.updateHighestBidAfterAdd(aLevel)              
        else:
            if(self.theAskLevelTree == None):
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
        # it will be the highest bid if
        # either if the following are true:
        # 1. aLevel is the right child of the current largest bid
        # 2. the current largest bid is the left child of aLevel
        if(self.theHighestBid.theRightChildLevel == aLevel):
            self.theHighestBid = aLevel
        elif(aLevel.theLeftChildLevel == self.theHighestBid):
            self.theHighestBid = aLevel
        
    def updateLowestAskAfterAdd(self, aLevel):
        # we have added 'aLevel to the tree
        # we want to check if it is the lowest ask
        # it will be the lowest ask if 
        # either of the following are true:
        # 1. aLevel is the left child of the current lowest ask
        # 2. the current lowest ask is the right child of aLevel
        if(self.theLowestAsk.theLeftChild == aLevel):
            self.theHighestBid = aLevel
        elif(aLevel.theRightChild == self.theLowestAsk):
            self.theLowestAsk = aLevel

    def updateHighestBidBeforeRemove(self, aLevel):

        # we have removed 'aLevel' from the tree
        # if aLevel was the highest bid, we must
        # find the new highest bid
        # there are two possibilities:
        # 1. The max bid is a right child
        #    --> take the parent as the new max
        # 2. The max bid is the root
        #    --> take the left child as the new max
        if(aLevel != self.theHighestBid):
            return
        elif(aLevel.theParentLevel is not None):
            self.theHighestBid = aLevel.theParentLevel
        else:
            self.theHighestBid = aLevel.theLeftChildLevel

    def updateLowestAskBeforeRemove(self, aLevel):
        # we have removed 'aLevel' from the tree
        # if aLevel was the lose, we must
        # find the new lowest ask
        # there are two possibilities:
        # 1. The min ask is a left child
        #    --> take the parent as the new min
        # 2. The min ask is the root
        #    --> take the left child as the new min
        if(aLevel != self.theLowestAsk):
            return
        elif(aLevel.theParentLevel is not None):
            self.theLowestAsk = aLevel.theParentLevel
        else:
            self.theLowestBid = aLevel.rightChildLevel

    def addNewLevel(self, aPrice, aSide):
        myNewLevel = Level(aPrice)
        self.theLevels[aPrice] = myNewLevel
        self.addExistingLevel(myNewLevel, aSide)
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
        y = aLevel.theRightChildLevel                                   
        aLevel.theRightChildLevel = y.theLeftChildLevel                                
        if(y.theLeftChildLevel != None):
            y.theLeftChildLevel.theParentLevel = aLevel

        y.theParentLevel = aLevel.theParentLevel                             
        if(aLevel.theParentLevel == None):  
            if(aSide):                          
                self.theBidLevelTree = y 
            else:
                self.theAskLevelTree = y                                               
        elif(aLevel == aLevel.theParentLevel.theParentLevel):
            aLevel.theParentLevel.theLeftChildLevel = y
        else:
            aLevel.theParentLevel.theRightChildLevel = y
        y.theLeftChildLevel = aLevel
        aLevel.theParentLevel = y

    def rightRotate(self, aLevel, aSide):
        myOldLeftChild = aLevel.theLeftChildLevel                         
        aLevel.theLeftChildLevel = myOldLeftChild.theRightChildLevel       
        if(myOldLeftChild.theRightChildLevel != None):
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

        while(x != None):                        
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

        if(aSide):
            myRootLevel = self.theBidLevelTree
        else:
            myRootLevel = self.theAskLevelTree

        while(aLevel.theParentLevel.theColour == 1):                      
            if(aLevel.theParentLevel == aLevel.theParentLevel.theParentLevel.theRightChildLevel): 
                u = aLevel.theParentLevel.theParentLevel.theLeftChildLevel            
                if(u != None and u.theColour == 1):                       
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
            if(aLevel == myRootLevel):                           
                break
        myRootLevel.theColour = 0                             

    def removeLevel(self, aLevel, aSide) :
        y = aLevel
        y_original_color = y.theColour                         
        if(aLevel.theLeftChildLevel == None):                           
            x = aLevel.theRightChildLevel                               
            self.__rb_transplant(aLevel , aLevel.theRightChildlevel)          
        elif (aLevel.theRightChildLevel == None) :                      
            x = aLevel.theLeftChildLevel                                    
            self.__rb_transplant (aLevel , aLevel.theLeftChildLevel)           
        else:                                              
            y = self.minimum(aLevel.theRightChildLevel)                   
            y_original_color = y.theColour                
            x = y.theRightChildLevel
            if(y.theParentLevel == aLevel):                           
                x.theParentLevel = y                            
            else:
                self.__rb_transplant(y , y.theRightChildLevel)
                y.theRightChildLevel = aLevel.theRightChildLevel
                y.theRightChildLevel.theParentLevel = y

            self.__rb_transplant(aLevel , y )
            y.theLeftChildLevel = aLevel.theLeftChildLevel
            y.theLeftChildLevel.theParentLevel = y
            y.theColour = aLevel.theColour
        if(y_original_color == 0):                       
            self.fixDelete(x, aSide)

    def fixDelete(self , aLevel, aSide) :
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
        while(aLevel.theLeftChildLevel != None):
            aLevel = aLevel.theLeftChildLevel
        return aLevel

    def __printCall(self, aLevel, indent, last) :
        if(aLevel != None):
            print(indent, end=' ')
            if last :
                print ("R----",end= ' ')
                indent += "     "
            else :
                print("L----",end=' ')
                indent += "|    "

            s_color = "RED" if aLevel.theColour == 1 else "BLACK"
            print ( str ( aLevel.thePrice ) + "(" + s_color + ")" )
            self.__printCall ( aLevel.theLeftChildLevel, indent , False )
            self.__printCall ( aLevel.theRightChildLevel , indent , True )

    def print_tree (self, aSide) :
        if(aSide):
            myRoot = self.theBidLevelTree
        else:
            myRoot = self.theAskLevelTree
        self.__printCall ( myRoot , "" , True )
