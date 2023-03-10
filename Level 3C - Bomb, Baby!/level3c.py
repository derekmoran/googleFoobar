# Author: Derek Moran, Level 3 Bunny Planet Saboteur
# Date: 04-DEC-2022

def solution(x, y):
    # Your code here
    return getNumReplicationCyclesToGenerateRequiredBombsAsString( x, y )

# Returns the number of replication cycles ( as a string ) it will take to generate the input number of Mach and Facula bombs
# This assumes we start with one of each bomb type. If the input targets are not possible, then 'impossible' will be returned.
#
# numRequiredMachBombsAsString and numRequiredFaculaBombsAsString must be postive integers ( passed as string ) with size no larger than 10^50
def getNumReplicationCyclesToGenerateRequiredBombsAsString( numRequiredMachBombsAsString, numRequiredFaculaBombsAsString ):

    validationError = "numRequiredMachBombsAsString and numRequiredFaculaBombsAsString must be postive integers ( passed as string ) with size no larger than 10^50"
    if not type(numRequiredMachBombsAsString) is str or not numRequiredMachBombsAsString.isdigit():
        raise Exception( validationError )

    if not type(numRequiredFaculaBombsAsString) is str or not numRequiredFaculaBombsAsString.isdigit():
        raise Exception( validationError )

    numRequiredMachBombs = int(numRequiredMachBombsAsString)
    numRequiredFaculaBombs = int(numRequiredFaculaBombsAsString)

    maxNumberOfInputBombs = 10 ** 50
    if numRequiredMachBombs < 1 or \
        numRequiredMachBombs > maxNumberOfInputBombs or \
        numRequiredFaculaBombs < 1 or \
        numRequiredFaculaBombs > maxNumberOfInputBombs:
        raise Exception( validationError )

    # Envision our starting point as having one of each bomb type: (1,1)
    # (1,1) can then replicate into one of (2,1) or (1,2)
    # (2,1) can then replicate into one of (3,1) or (2,3), and (1,2) into (3,2) or (1,3)
    # This tree structure could continue until each leaf exceeds or reaches the required number of bombs
    # If we reach the requirements, then the answer is the tree depth
    #
    # HOWEVER, starting from (1,1) would require traversing the entire tree
    # Instead, let's start with the target ( numRequiredMachBombsAsString, numRequiredFaculaBombsAsString )
    # Because we know that the parent node must be one of:
    #  ( numRequiredMachBombsAsString-numRequiredFaculaBombsAsString, numRequiredFaculaBombsAsString )
    #  ( numRequiredMachBombsAsString, numRequiredFaculaBombsAsString-numRequiredMachBombsAsString )
    # The number of bombs might be equal ( or one of them is zero ); if so we can tell immediately that this solution is impossible
    # Otherwise they are not equal, so one of these prior nodes would require a negative number of bombs, and thus can be safely discarded
    # Therefore a bottom up approach can give us a most direct path through our tree and avoid a full traversal
    #
    # Additionally note that if one bomb type has a count that is larger than multiples of the other type, that we would then be
    # taking that same branch multiple times. So in those cases we can jump up the tree by that multiple, thereby reducing
    # our traversal length even further
    numRequiredMachBombsRemaining = numRequiredMachBombs
    numRequiredFaculaBombsRemaining = numRequiredFaculaBombs
    numTotalReplicationCycles = 0

    while True:
        if numRequiredMachBombsRemaining == numRequiredFaculaBombsRemaining == 1:
            break

        if numRequiredMachBombsRemaining == numRequiredFaculaBombsRemaining or \
            numRequiredMachBombsRemaining == 0 or \
            numRequiredFaculaBombsRemaining == 0:
            return "impossible"

        numReplicationCycles = 1
        if numRequiredMachBombsRemaining > numRequiredFaculaBombsRemaining:
            if numRequiredFaculaBombsRemaining > 1:
                numReplicationCycles = int(numRequiredMachBombsRemaining / numRequiredFaculaBombsRemaining)
                numRequiredMachBombsRemaining -= numRequiredFaculaBombsRemaining * numReplicationCycles
            else:
                numReplicationCycles = numRequiredMachBombsRemaining - 1
                numRequiredMachBombsRemaining = 1
        else:
            if numRequiredMachBombsRemaining > 1:
                numReplicationCycles = int(numRequiredFaculaBombsRemaining / numRequiredMachBombsRemaining)
                numRequiredFaculaBombsRemaining -= numRequiredMachBombsRemaining * numReplicationCycles
            else:
                numReplicationCycles = numRequiredFaculaBombsRemaining - 1
                numRequiredFaculaBombsRemaining = 1

        numTotalReplicationCycles += numReplicationCycles

    return str(numTotalReplicationCycles)
