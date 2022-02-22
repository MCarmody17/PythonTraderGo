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
        
