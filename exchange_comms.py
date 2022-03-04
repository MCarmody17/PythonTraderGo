from utils import Order
from enum import Enum

# all possible message types 
class MessageType(Enum):
    ADD = 0
    CANCEL = 1
    TRADE = 2

class MessageHandler:

    __slots__ = 'theExchangeInfo', 'theStrategy', 'theEncoder', 'theDecoder'
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

class Listener:

    __slots__ = 'theMessageHandler'

    def __init__(self, aMessageHandler):
        self.theMessageHandler = aMessageHandler

class Sender:

    __slots__ = 'theConnectionInfo'

    def __init__(self, aConnectionInfo):
        self.theConnectionInfo = aConnectionInfo

    def sendMessage(self, aMessageData):
        print("NOT IMPLEMENTED")

class Encoder:

    __slots__ = 'theExchangeInfo'
    
    def __init__(self, aExchangeInfo):
        self.theExchangeInfo = aExchangeInfo

    def encodeAddOrder(self, aProduct, aPrice, aVolume, aSide):
        print("NOT IMPLEMENTED")

    def encodeCancelOrder(self, aProduct, aPrice, aVolume, aSide):
        print("NOT IMPLEMENTED")