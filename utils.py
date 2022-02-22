from asyncio.windows_events import NULL
import numpy as np
from queue import PriorityQueue

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
        self.theColour = False # False = black, True = red
        self.theFirstOrder = NULL
        self.theLastOrder = NULL
        self.theParentLevel = NULL
        self.theLeftChildLevel = NULL
        self.theRightChildLevel = NULL

    def addOrder(self, aOrder):
        if(self.theFirstOrder == NULL):
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
        if(aOrder.getPreviousOrder() != NULL):
            aOrder.getPreviousOrder().setNextOrder(aOrder.getNextOrder())            
        if(aOrder.getNextOrder() != NULL):
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
        self.theNextOrder = NULL
        self.thePreviousOrder = NULL
        self.theIsMine = aIsMine
        self.theLevel = NULL
        
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
        self.theBidLevelTree = NULL
        self.theAskLevelTree = NULL
        self.theLowestAsk = NULL
        self.theHighestBid = NULL

    def addOrder(self, aOrder):
        self.theOrders[aOrder.getId()] = aOrder

        myOrderPrice = aOrder.getPrice()
        if(not myOrderPrice in self.theLevels):
            myLevel = self.addLevel(aOrder.getPrice)
        else:
            myLevel = self.theLevels[myOrderPrice]

        aOrder.setLevel(myLevel)
        myLevel.addOrder(aOrder)       

    def addLevel(self, aPrice, aSide):
        myNewLevel = Level(aPrice)
        self.theLevels[aPrice] = myNewLevel

        # we have to add the level to the tree 
        return myNewLevel

    def removeOrder(self, aId):
        myOrder = self.theOrders[aId]
        self.theLevels[myOrder.getPrice()].removeOrder(myOrder)

    def changeOrderVolume(self, aId, aVolumeChange):
        myOrder = self.theOrders[aId]
        self.theLevels[myOrder.getPrice()].changeOrderVolume(myOrder, aVolumeChange)

    def getHighestBidLevel(self):
        return self.theHighestBidLevel

    def getLowestAskLevel(self):
        return self.theHighestAskLevel


