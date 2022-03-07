
# Hedging rules:
#    1. No more than 10 unhedged lots may be held in
#       any instrument for more than 1 minute
class Hedger:
    
    __slots__ = 'theExecutor', 'theExchangeInfo'

    def __init__(self, aExecutor, aExchangeInfo):
        self.theExecutor = aExecutor
        self.theExchangeInfo = aExchangeInfo

    def handlePositionChange(self, aProduct, aPositionChange):
        print("NOT IMLEMENTED")

class Executor: 

    __slots__ = 'theExchangeInfo', 'theHedger', 'theSender', 'theEncoder'
    def __init__(self, aExchangeInfo, aHedger, aSender, aEncoder):
        self.theExchangeInfo = aExchangeInfo
        self.theHedger = aHedger
        self.theSender = aSender
        self.theEncoder = aEncoder

    def doAddOrder(self, aProduct, aPrice, aVolume, aSide):
        myMessageData = self.theEncoder.encoderAddOrder(aProduct, aPrice, aVolume, aSide)
        self.theSender.sendMessage(myMessageData)

    def doCancelOrder(self, aId):
        myMessageData = self.theEncoder.encodeCancelOrder(aId)
        self.theSender.sendMessage(myMessageData)

    def doAmendOrder(self, aId, aNewPrice, aNewVolume):
        myMessageData = self.theEncode.encodeAmendOrder(aId, aNewPrice, aNewVolume)
        self.theSender.sendMessage(myMessageData)
    