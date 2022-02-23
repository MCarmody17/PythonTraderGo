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
            myLevel = self.addNewLevel(aOrder.getPrice)
        else:
            myLevel = self.theLevels[myOrderPrice]
            # if level has size zero, it is not in the tree
            # and must be added again
            self.addExistingLevel(myLevel)

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
                self.updateHigestBidAfterAdd(aLevel)              
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
        elif(aLevel.theLeftChild == self.theHighestBid):
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
        if y.theLeftChildLevel != None :
            y.theLeftChildLevel.theParentLevel = aLevel

        y.theParentLevel = aLevel.theParentLevel                             
        if aLevel.theParentLevel == None :  
            if(aSide):                          
                self.theBidLevelTree = y 
            else:
                self.theAskLevelTree = y                                               
        elif aLevel == aLevel.parent.theParentLevel :
            aLevel.theParentLevel.theLeftChildLevel = y
        else :
            aLevel.theParentLevel.theRightChildLevel = y
        y.theLeftChildLevel = aLevel
        aLevel.theParentLevel = y

    def rightRotate(self, aLevel, aSide):
        myOldLeftChild = aLevel.theLeftChildLevel                         
        aLevel.theLeftChildLevel = myOldLeftChild.theRightChildLevel       
        if myOldLeftChild.theRightChildLevel != None :
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

        while(x != None):                           # Find position for new node
            y = x
            if(aNewLevel.getPrice() < x.getPrice()):
                x = x.theLeftChildLevel
            else:
                x = x.theRightChildLevel

        aNewLevel.theParentLevel = y                                  # Set parent of Node as y
        if(y == None):                                   # If parent i.e, is none then it is root node
            if(aSide):
                self.theBidLevelTree = aNewLevel
            else:
                self.theAskLevelTree = aNewLevel
        elif(aNewLevel.getPrice() < y.getPrice()):
            y.theLeftChildLevel = aNewLevel
        else:
            y.theRightChildLevel = aNewLevel

        if(aNewLevel.theParentLevel == None):                   
            aNewLevel.colour = 0
            return

        if(aNewLevel.theParentLevel.theParentLevel == None):                  
            return

        self.fixInsert(aNewLevel, aSide)                         

    def fixInsert(self, aLevel, aSide):

        if(aSide):
            myRootLevel = self.theBidLevelTree
        else:
            myRootLevel = self.theAskLevelTree

        while aLevel.theParentLevel.colour == 1:                        # While parent is red
            if aLevel.theParentLevel == aLevel.theParentLevel.theParentLevel.theRightChildLevel:         # if parent is right child of its parent
                u = aLevel.theParentLevel.theParentLevel.theLeftChildLevel                  # Left child of grandparent
                if u.theColour == 1:                          # if color of left child of grandparent i.e, uncle node is red
                    u.theColour = 0                           # Set both children of grandparent node as black
                    aLevel.theParentLevel.theColour = 0
                    aLevel.theParentLevel.theParentLevel.theColour = 1             # Set grandparent node as Red
                    aLevel = aLevel.theParentLevel.theParentLevel                   # Repeat the algo with Parent node to check conflicts
                else:
                    if aLevel == aLevel.theParentLevel.theLeftChildLevel:                # If k is left child of it's parent
                        aLevel = aLevel.theParentLevel
                        self.rightRotate(aLevel, aSide)                        # Call for right rotation
                    aLevel.theParentLevel.theColour = 0
                    aLevel.theParentLevel.theParentLevel.theColour = 1
                    self.leftRotate(aLevel.theParentLevel.theParentLevel, aSide)
            else:                                         # if parent is left child of its parent
                u = aLevel.theParentLevel.theParentLevel.theRightChildLevel                 # Right child of grandparent
                if u.theColour == 1:                          # if color of right child of grandparent i.e, uncle node is red
                    u.theColour = 0                           # Set color of childs as black
                    aLevel.theParentLevel.theColour = 0
                    aLevel.theParentLevel.theParentLevel.theParentLevel = 1             # set color of grandparent as Red
                    aLevel = aLevel.theParentLevel.theParentLevel                   # Repeat algo on grandparent to remove conflicts
                else:
                    if aLevel == aLevel.theParentLevel.theRightChildLevel:               # if k is right child of its parent
                        aLevel = aLevel.theParentLevel
                        self.leftRotate(aLevel, aSide)                        # Call left rotate on parent of k
                    aLevel.theParentLevel.theColour = 0
                    aLevel.theParentLevel.theParentLevel.theColour = 1
                    self.rightRotate(aLevel.theParentLevel.theParentLevel, aSide)              # Call right rotate on grandparent
            if aLevel == myRootLevel:                            # If k reaches root then break
                break
        myRootLevel.theColour = 0                               # Set color of root as black

    

    def removeLevel(self, aLevel, aSide) :
        y = aLevel
        y_original_color = y.theColour                          # Store the color of z- node
        if aLevel.theLeftChildLevel == None :                            # If left child of z is NULL
            x = aLevel.theRightChildLevel                                     # Assign right child of z to x
            self.__rb_transplant(aLevel , aLevel.theRightChildlevel)            # Transplant Node to be deleted with x
        elif (aLevel.theRightChildLevel == None) :                       # If right child of z is NULL
            x = aLevel.theLeftChildLevel                                      # Assign left child of z to x
            self.__rb_transplant (aLevel , aLevel.theLeftChildLevel)             # Transplant Node to be deleted with x
        else :                                              # If z has both the child nodes
            y = self.minimum (aLevel.theRightChildLevel)                    # Find minimum of the right sub tree
            y_original_color = y.theColour                      # Store color of y
            x = y.theRightChildLevel
            if(y.theParentLevel == aLevel):                              # If y is child of z
                x.theParentLevel = y                                # Set parent of x as y
            else:
                self.__rb_transplant(y , y.theRightChildLevel)
                y.theRightChildLevel = aLevel.theRightChildLevel
                y.theRightChildLevel.theParentLevel = y

            self.__rb_transplant(aLevel , y )
            y.theLeftChildLevel = aLevel.theLeftChildLevel
            y.theLeftChildLevel.theParentLevel = y
            y.theColour = aLevel.theColour
        if y_original_color == 0 :                          # If color is black then fixing is needed
            self.fixDelete(x, aSide)

    # Function to fix issues after deletion
    def fixDelete(self , aLevel, aSide) :
        if(aSide):
            myRoot = self.theBidLevelTree
        else:
            myRoot = self.theAskLevelTree

        while(aLevel != myRoot and aLevel.theColour == 0):           # Repeat until x reaches nodes and color of x is black
            if(aLevel == aLevel.theParentLevel.theLeftChildLevel):                       # If x is left child of its parent
                s = aLevel.theParentLevel.theRightChildLevel        # Sibling of x
                if(s.theColour == 1):                         # if sibling is red
                    s.theColour = 0                           # Set its color to black
                    aLevel.theParentLevel.theColour = 1                    # Make its parent red
                    self.leftRotate(aLevel.theParentLevel, aSide)                  # Call for left rotate on parent of x
                    s = aLevel.theParentLevel.theRightChildLevel
                # If both the child are black
                if(s.theLeftChildLevel.theColour == 0 and s.theRightChildLevel.theColour == 0):
                    s.theColour = 1                           # Set color of s as red
                    aLevel = aLevel.theParentLevel
                else:
                    if(s.theRightChildLevel.theColour == 0):               # If right child of s is black
                        s.theLeftChildLevel.theColour = 0                  # set left child of s as black
                        s.theColour = 1                       # set color of s as red
                        self.rightRotate(s, aSide)                     # call right rotation on x
                        s = aLevel.theParentLevel.theRightChildLevel

                    s.theColour = aLevel.theParentLevel.theColour
                    aLevel.theParentLevel.theColour = 0                    # Set parent of x as black
                    s.theRightChildLevel.theColour = 0
                    self.leftRotate(aLevel.theParentLevel, aSide)                  # call left rotation on parent of x
                    aLevel = myRoot
            else:                                        # If x is right child of its parent
                s = aLevel.theParentLevel.theLeftChildLevel                         # Sibling of x
                if s.theColour == 1 :                         # if sibling is red
                    s.theColour = 0                           # Set its color to black
                    aLevel.theParentLevel.theColour = 1                    # Make its parent red
                    self.rightRotate(aLevel.theParentLevel, aSide)                  # Call for right rotate on parent of x
                    s = aLevel.theParentLevel.theLeftChildLevel

                if(s.theRightChildLevel.theColour == 0 and s.theRightChildLevel.theColour == 0):
                    s.theColour = 1
                    aLevel = aLevel.theParentLevel
                else:
                    if(s.theLeftChildLevel.theColour == 0):                # If left child of s is black
                        s.theRightChildLevel.theColour = 0                 # set right child of s as black
                        s.theColour = 1
                        self.leftRotate(s, aSide)                     # call left rotation on x
                        s = aLevel.theParentLevel.theLeftChildLevel

                    s.theColour = aLevel.theParentLevel.theColour
                    aLevel.theParentLevel.theColour = 0
                    s.theLeftChildLevel.theColour = 0
                    self.rightRotate(aLevel.theParentLevel, aSide)
                    aLevel = myRoot
        aLevel.theColour = 0

        
    # Function to transplant nodes
    def __rb_transplant(self, u, v, aSide):
        
        if u.theParentLevel == None :
            if(aSide):
                self.theBidLevelTree = v
            else:
                self.theAskLevelTree = v
        elif(u == u.theParentLevel.theLeftChildLevel):
            u.theParentLevel.theLeftChildLevel = v
        else:
            u.theParentLevel.theRightChildLevel = v
        v.theParentLevel = u.theParentLevel


    # Function to print
    def __printCall (self , aLevel, indent , last) :
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

    # Function to call print
    def print_tree (self, aSide) :
        if(aSide):
            myRoot = self.theBidLevelTree
        else:
            myRoot = self.theAskLevelTree
        self.__printCall ( myRoot , "" , True )
'''
self.thePrice = aPrice
        self.theTotalVolume = 0
        self.theMyVolume = 0
        self.theSize = 0
        self.theColour = 1 # 1 = red, 0 = black
        self.theFirstOrder = NULL
        self.theLastOrder = NULL
        self.theParentLevel = NULL
        self.theLeftChildLevel = NULL
        self.theRightChildLevel = NULL
'''