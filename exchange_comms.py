from utils import Order

class MessageHandler:

    __slots__ = 'theExchangeInfo', 'theStrategy', 'theEncoeder', 'theDecoder'
    def __init__(self, aExchangeInfo, aStrategy, aEncoder, aDecoder):
        self.theExchangeInfo = aExchangeInfo
        self.theStrategy = aStrategy
        self.theEncoder = aEncoder
        self.theDecoder = aDecoder

    def handleAddOrder(self, aProductName, aPrice, aTimestamp, aVolume, aTraderName, aSide, aId):
        myIsMine = (aTraderName == self.theExchangeInfo.theOurName)
        myNewOrder = Order(aPrice, aTimestamp, aVolume, aTraderName, aSide, aId, myIsMine)
        self.theExchangeInfo.addOrder(aProductName, myNewOrder)
        self.theStrategy.handleAddOrder(aProductName, myNewOrder)

    def handleCancelOrder(self):
        print("NOT IMPLEMENTD")

    def handleTrade(self):
        print("NOT IMPLEMENTED")


class Sender:

    __slots__ = 'theConnectionInfo'

    def __init__(self, aConnectionInfo):
        self.theConnectionInfo = aConnectionInfo

    def sendMessage(self, aMessageData):
        print("NOT IMPLEMENTED")

class Listener:

    __slots__ = 'theMessageHandler'

    def __init__(self, aMessageHandler):
        self.theMessageHandler = aMessageHandler

    
