
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

    __slots__ = 'theHedger'
    def __init__(self, aHedger):
        self.theHedger = aHedger
