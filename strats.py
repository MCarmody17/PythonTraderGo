class FirstStrategy:

    __slots__ = 'theExchangeInfo', 'theExecutor'

    def __init__(self, aExchangeInfo, aExecutor):
        self.theExchangeInfo = aExchangeInfo
        self.theExecutor = aExecutor

    def handleAddOrder(self, aProductName, aOrder):
        print("NOT IMPLEMENTED")