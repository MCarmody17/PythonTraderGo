import time
from utils import *
from rb import *


def runTrials(aMethod, aIterations):

    myDurations = []
    for i in range(0, aIterations):

        myStartTime = time.time()
        aMethod()
        myEndTime = time.time()

        myDurations.append(myEndTime - myStartTime)

    return myDurations

def getAverage(aDurations):
    return sum(aDurations)/len(aDurations)

#
#   Unit tests for Stopwatch class
#
def testStopwatchSize(aSize):

    myStopwatch = Stopwatch(aSize)
    assert(myStopwatch.getSize() == aSize)
    
def testStopwatchCount(aSize, aTrialNumber):

    myStopwatch = Stopwatch(aSize)
    for i in range(aTrialNumber):
        assert(myStopwatch.getCount() == i)
        myStopwatch.doTimestamp(1)

def testStopwatchTimestampPointer(aSize, aTrialNumber):

    myStopwatch = Stopwatch(aSize)
    for i in range(aTrialNumber):
        assert(myStopwatch.theLastTimestamp == (i % aSize))
        myStopwatch.doTimestamp(1)

def testStopwatchTimestamp(aSize, aTrialNumber, aDelta):

    myStopwatch = Stopwatch(aSize)
    myTimestamp = 0
    for i in range(aTrialNumber):
        myTimestamp += aDelta
        if(i > 0):
            assert(myStopwatch.doTimestamp(myTimestamp) == aDelta)
        else:
            myStopwatch.doTimestamp(myTimestamp)
        
def testOrderBook():

    myOrderBook = OrderBook()
    testOrderBookAdd(myOrderBook)
    testOrderBookRemove(myOrderBook)

def testOrderBookAdd(aOrderBook):

    #__init__(self, aPrice, aTimestamp, aVolume, aTraderName, aSide, aId, aIsMine):
    myOrderA = Order(10, 0, 100, "Bob", 1, 0, False)
    myOrderB = Order(11, 0, 100, "Bob", 1, 1, False)
    myOrderC = Order(12, 0, 100, "Bob", 1, 2, False)
    myOrderD = Order(13, 0, 100, "Bob", 1, 3, False)
    myOrderE = Order(14, 0, 100, "Bob", 1, 4, False)

    aOrderBook.addOrder(myOrderA)
    aOrderBook.addOrder(myOrderB)
    aOrderBook.addOrder(myOrderC)
    aOrderBook.addOrder(myOrderD)
    aOrderBook.addOrder(myOrderE)

def testOrderBookRemove(aOrderBook):

    print("====")
    aOrderBook.removeOrder(0)
    print("====")
    aOrderBook.removeOrder(1)
    print("====")
    aOrderBook.removeOrder(2)
    print("====")
    aOrderBook.removeOrder(3)
    print("====")
    aOrderBook.removeOrder(4)
    
class OrderBookTester:

    def __init__(self):

        self.theOrderBook = OrderBook()
        self.theRbTree = RBTree()
        self.theTime = 0

    def checkEquals(self, aSide):
  
        return self.theOrderBook.express_tree(aSide) \
            == self.theRbTree.express_tree()

    def addNode(self, aVal, aSide):

        myNewOrder = Order(aVal, self.theTime, 1, "Bob", aSide, aSide, False)
        self.theOrderBook.addOrder(myNewOrder)        
        self.theRbTree.insertNode(aVal)
        self.theTime += 1

    def removeNode(self, aId):

        myVal = self.theOrderBook.theOrders[aId].thePrice
        self.theOrderBook.removeOrder(aId)
        self.theRbTree.delete_node(myVal)

myTester = OrderBookTester()
myTester.addNode(10, True)
print(myTester.checkEquals(True))
print(myTester.theOrderBook.theExpression)
print(myTester.theRbTree.theExpression)