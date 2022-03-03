import numpy as np


class Listener:

    __slots__ = 'theConnectionInfo', 'theExchangeInfo', 'theStrategy'

    def __init__(self, aConnectionInfo, aExchangeInfo, aStrategy):
        self.theConnectionInfo = aConnectionInfo
        self.theExchangeInfo = aExchangeInfo
        self.theStrategy = aStrategy

    def handleAddOrder(self, aProductName, aPrice, aTimestamp, aVolume, aTraderName, aSide, aId):
        myIsMine = (aTraderName == self.theExchangeInfo.theOurName)
        myNewOrder = Order(aPrice, aTimestamp, aVolume, aTraderName, aSide, aId, myIsMine)
        self.theExchangeInfo.addOrder(aProductName, myNewOrder)
        self.theStrategy.handleAddOrder(aProductName, myNewOrder)

    def handleCancelOrder(self):
        print("NOT IMPLEMENTD")

    def handleTrade(self):
        print("NOT IMPLEMENTED")

class Product:

    __slots__ = 'theName', 'theOrderBook'

    def __init__(self, aName):
        self.theName = aName
        self.theOrderBook = OrderBook()
 
# TODO: might have to add some quick way to answer
# the question "how many orders in the last second?"
# Currently this data structure just quickly tells us
# how long ago the (n - 50)th order was if we are on
# the nth order
class Stopwatch:

    __slots__ = 'theTimestamps', 'theSize', 'theCount', 'theLastTimestamp'

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

    # returns the total number of stored timestamps
    # which are within aPeriod of aTimestamp
    def recentTimestampCount(self, aTimestamp, aPeriod):
        myTimestampVector = np.full(self.theSize, aTimestamp)
        myDifferences = np.subtract(myTimestampVector, self.theTimestamps)
        myPeriodVector = np.full(self.theSize, aPeriod)
        myComparison = np.less_equal(myDifferences, myPeriodVector)
        return np.count_nonzero(myComparison)

class Trader:

    __slots__ = 'theName', 'thePositions', 'theStopwatch', 'theActiveOrders'

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

class Level:

    __slots__ = 'thePrice', \
        'theTotalVolume', \
        'theMyVolume', \
        'theSize', \
        'theColour', \
        'theFirstOrder', \
        'theLastOrder', \
        'theParentLevel', \
        'theLeftChildLevel', \
        'theRightChildLevel'

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

    __slots__ = 'thePrice', \
        'theTimestamp', \
        'theVolume', \
        'theTraderName', \
        'theSide', \
        'theId', \
        'theNextOrder', \
        'thePreviousOrder', \
        'theIsMine', \
        'theLevel'

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
