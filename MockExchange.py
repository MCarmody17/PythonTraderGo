from utils import *
from time import time

class Trade:

    def __init__(self, aBuyer, aSeller, aTime, aVolume, aPrice):
        self.theBuyer = aBuyer
        self.theSeller = aSeller
        self.theTime = aTime
        self.theVolume = aVolume
        self.thePrice = aPrice        

class ExchangeProduct:

    def __init__(self, aName):
        self.theName = aName
        self.theOrderBook = OrderBook()
        self.theTrades = {}
        self.theCurrentId = 0

    def addOrder(self, aTraderName, aPrice, aVolume, aSide):
        myTimestamp = time()
    
        myNewOrder = Order(aPrice, myTimestamp, aVolume, aTraderName, aSide, self.theCurrentId)
        self.theCurrentId += 1



class MockExchange:

    def __init__(self):
        self.theOrders = {}
        self.theProducts = {}
        self.theTraders = {}

    def addProduct(self, aName):
        self.theProducts[aName] = ExchangeProduct(aName)

    def addNewTrader(self, aName):
        self.theTraders[aName] = Trader(aName)

    def getTraderPosition(self, aName):
        return self.theTraders[aName].getPosition()

    def changeTraderPosition(self, aName, aChange):
        self.theTraders[aName].updatePosition(aChange)

    def traderExists(self, aName):
        return aName in self.theTraders.keys()