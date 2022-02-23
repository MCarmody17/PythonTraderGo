import time
from utils import *

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

def testOrderBookAdd(aOrderBook):

    #__init__(self, aPrice, aTimestamp, aVolume, aTraderName, aSide, aId, aIsMine):
    myOrderA = Order(10, 0, 100, "Bob", 1, 0, False)
    myOrderB = Order(10, 0, 100, "Bob", 1, 1, False)
    myOrderC = Order(11, 0, 100, "Bob", 1, 2, False)
    myOrderD = Order(12, 0, 100, "Bob", 1, 3, False)
    myOrderE = Order(13, 0, 100, "Bob", 1, 4, False)

    aOrderBook.addOrder(myOrderA)
    aOrderBook.addOrder(myOrderB)
    aOrderBook.addOrder(myOrderC)
    aOrderBook.addOrder(myOrderD)
    aOrderBook.addOrder(myOrderE)

testOrderBook()