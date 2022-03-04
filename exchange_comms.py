from utils import Order

class Sender:

    __slots__ = 'theConnectionInfo'

    def __init__(self, aConnectionInfo):
        self.theConnectionInfo = aConnectionInfo

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
