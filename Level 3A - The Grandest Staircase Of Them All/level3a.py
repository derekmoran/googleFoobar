# Author: Derek Moran, Level 3, Commander Lambda's Personal Assistant @ Commander Lambda Space Station
# Date: 25-NOV-2022

def solution(n):
    # Your code here
    return getNumberOfStaircasePermutations(n)

# Returns the number of permutations of staircases that can be built with the input number of bricks. Staircases follow these rules:
#  - Each type of staircase should consist of 2 or more steps.
#  - No two steps are allowed to be at the same height - each step must be lower than the previous one.
#  - All steps must contain at least one brick.
#
# The provided number of bricks must be an integer between 3 and 200 inclusive
#
# TODO: Since the possible input set is small, if the Commander is likely to run this frequently, it would probably make sense
# to run this for all inputs 3-to-200 and store the results in a lookup table, thus allowing for O(1) lookups from that result table.
def getNumberOfStaircasePermutations( numTotalBricks ):

    if not type(numTotalBricks) is int:
        raise TypeError("Number of bricks must be an integer")

    if numTotalBricks < 3 or numTotalBricks > 200:
        raise Exception("Number of bricks must be between 3 and 200 inclusive")

    # Start with ( numBricksUsed, minNumBricksForNextStep ) = (0, 1)
    # We can use 1 brick for the first step, and the remaining staircase permutations then must start at height 2
    # Or we could use 2 bricks for the first step, and the remaining staircase permutations then must start at height 3
    # Or we could use 3 bricks for the first step, and the remaining staircase permutations then must start at height 4
    # And so on for as long as we have available bricks
    #
    # ie Starting from (0,1) we can add (1,2)+(2,3)+(3,4)+ ...
    # (1,2) can then have added to it (3,3)+(4,4)+(5,5)+ ...
    # (2,3) could then have added to it (5,4)+(6,5)+(7,6)+ ...
    #
    # This tree of calls can carry on until:
    #   - numBricksUsed reaches numTotalBricks, then that leaf ends the call chain and adds as a suitable permutation
    #   - numBricksUsed exceeds numTotalBricks, then that leaf ends the call chain and dismisses the permutation
    #
    # This may result in multiple calls with the same input ( numBricksUsed, minNumBricksForNextStep ),
    # so we'll cache on this key so we can re-use that work in such cases

    cache = {}

    def numStaircasePermutationsFromNumTotalBricks( numBricksUsed, minNumBricksForNextStep ):

        cacheKey = ( numBricksUsed, minNumBricksForNextStep )
        if cacheKey in cache: return cache[cacheKey]

        totalStaircasePermutations = 0

        for numBricksToTryForNextStep in range( minNumBricksForNextStep, numTotalBricks ):
            next_numBricksUsed = numBricksUsed + numBricksToTryForNextStep

            if next_numBricksUsed == numTotalBricks:
                totalStaircasePermutations += 1
                break

            if next_numBricksUsed > numTotalBricks:
                break

            next_minNumBricksForNextStep = numBricksToTryForNextStep + 1
            numAdditionalStaircasePermutations = numStaircasePermutationsFromNumTotalBricks( next_numBricksUsed, next_minNumBricksForNextStep )
            cache[ ( next_numBricksUsed, next_minNumBricksForNextStep ) ] = numAdditionalStaircasePermutations

            totalStaircasePermutations += numAdditionalStaircasePermutations

        cache[cacheKey] = totalStaircasePermutations
        return totalStaircasePermutations

    return numStaircasePermutationsFromNumTotalBricks( numBricksUsed = 0, minNumBricksForNextStep = 1 )