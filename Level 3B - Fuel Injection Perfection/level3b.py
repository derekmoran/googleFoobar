# Author: Derek Moran, Level 3, Commander Lambda's Personal Assistant @ Commander Lambda Space Station
# Date: 01-DEC-2022

def solution(n):
    # Your code here
    return getMinNumberOfFuelControlOperationsRequiredToReduceToOnePellet( n )

# Returns the minimum number of fuel control operations ( ie add pellet, remove pellet, divide pellets in half )
# required to transform the input number of pellets to one
#
# The provided numInitialFuelPelletsAsString must be a postive integer ( passed as string ) with length no more than 309
def getMinNumberOfFuelControlOperationsRequiredToReduceToOnePellet( numInitialFuelPelletsAsString ):

    validationError = "numInitialFuelPelletsAsString must be a postive integer ( passed as string ) with length no more than 309"
    if not type(numInitialFuelPelletsAsString) is str or len(numInitialFuelPelletsAsString) > 309 or not numInitialFuelPelletsAsString.isdigit():
        raise Exception( validationError )

    numInitialFuelPellets = int(numInitialFuelPelletsAsString)

    if numInitialFuelPellets < 0:
        raise Exception( validationError )

    # If we have 1 pellet then there are zero operations
    # If we have 2 pellets then we can finish in a single division
    # For larger numbers, we can compare adding and removing a pellet before dividing, which makes a recursive approach seem ideal
    # BUT, inputs can be up to 309 digits in length!!!
    # Even though Python's arbitrary-precision arithmetic can handle that, we would still overflow the call stack with straight recursion
    # So let's use our own custom ( in an effort to reduce memory and increase performance ) stacks to ensure that doesn't happen.
    # We'll also use a cache to minimize duplicate work, and bitwise operators in an additional effort to speed up the divisions
    callStack, numOperationsStack = Stack(), Stack()

    class CallHandlers:
        Controller = 0 # For the main logic - this handler will setup the stack for other handlers
        AddOrRemovePellet = 1
        DividePelletsByHalf = 2

    callStack.push( ( CallHandlers.Controller, numInitialFuelPellets ) )

    # Note cache is pre-populated with 1 pellet ( 0 operations since we are done ) and 2 pellets ( 1 division operation will complete the job )
    cache = { 1: 0, 2: 1 }

    while True:

        nextCall = callStack.pop()
        if nextCall == None: break

        nextCallType, nextNumFuelPellets = nextCall

        if nextCallType == CallHandlers.Controller:
            if nextNumFuelPellets in cache:
                numOperationsStack.push( cache[nextNumFuelPellets] )
            elif nextNumFuelPellets & 1 != 0: # Fuel cannot be safely divided, so setup a call stack for comparing the adding/removing of a pellet
                callStack.push( ( CallHandlers.AddOrRemovePellet, nextNumFuelPellets ) )
                callStack.push( ( CallHandlers.Controller, nextNumFuelPellets + 1 ) )
                callStack.push( ( CallHandlers.Controller, nextNumFuelPellets - 1 ) )
            else: # We can safely divide the pellets, so setup a call stack for the division
                callStack.push( ( CallHandlers.DividePelletsByHalf, nextNumFuelPellets ) )
                callStack.push( ( CallHandlers.Controller, nextNumFuelPellets >> 1 )  )
        elif nextCallType == CallHandlers.DividePelletsByHalf:
            numOperationsAfterDividingPellets = 1 + numOperationsStack.pop()
            numOperationsStack.push( numOperationsAfterDividingPellets )
            cache[nextNumFuelPellets] = numOperationsAfterDividingPellets
        elif nextCallType == CallHandlers.AddOrRemovePellet:
            numOperationsAfterRemovingPellet = numOperationsStack.pop()
            numOperationsAfterAddingPellet = numOperationsStack.pop()
            numOperationsAfterAddingOrRemovingPellets = 1 + min( numOperationsAfterRemovingPellet, numOperationsAfterAddingPellet )
            numOperationsStack.push( numOperationsAfterAddingOrRemovingPellets )
            cache[nextNumFuelPellets] = numOperationsAfterAddingOrRemovingPellets

    return numOperationsStack.pop()

class StackElement:
       def __init__( self, object ):
           self.object = object
           self.next = None

class Stack:
    def __init__( self ):
        self.top = None

    def push( self, object ):
        newStackElement = StackElement( object )
        newStackElement.next = self.top
        self.top = newStackElement

    def pop( self ):
        if self.top is None: return None
        poppedElement = self.top
        self.top = self.top.next
        return poppedElement.object