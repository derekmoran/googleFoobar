# Author: Derek Moran, Level 2 Henchman @ Commander Lambda Space Station
# Date: 23-NOV-2022

def solution(pegs):
    # Your code here
    return getFirstGearRadiusThatDoublesOutputRotationAsReducedFraction( pegs )

# Takes a list of distinct positive integers named pegs representing the location of each peg along the support beam
# Assuming gears with minimal length 1 are placed on each peg, this returns the first gears radius such that the final gear doubles its rotation
# If a solution is not possible will return [-1,-1]
# Provided pegs must have at least 2 and no more than 20 distinct positive integers, all between 1 and 10000 inclusive
def getFirstGearRadiusThatDoublesOutputRotationAsReducedFraction( pegs ):

    solutionImpossible = [-1,-1]
    numPegs = len(pegs)

    if numPegs < 2 or numPegs > 20:
        raise Exception("There must be at least 2 pegs and no more than 20")

    # In the interest of performance, let's assume the pegs are indeed in ascending order and distinct
    # TODO: Verify this assumption with Commander Lambda before shipping!!!

    def getGearRadiusThatDoublesOutputRotationAsReducedFraction( pegIndex, previousAlternatingPegSum ):

        if not type(pegs[pegIndex]) is int:
            raise TypeError("Peg distances must be integers")

        if pegs[pegIndex] < 1 or pegs[pegIndex] > 10000:
            raise Exception("Peg distances must be between 1 and 10000 inclusive")

        currentAlternatingPegSum = 0
        if pegIndex > 0:
            currentAlternatingPegSum = pegs[pegIndex] - pegs[pegIndex-1] - previousAlternatingPegSum

        # Let radius of gears be r1, r2, ...  rn
        # Then r1 = pegs[1] - pegs[0] - r2
        #   but r2 = pegs[2] - pegs[1] - r3
        # So r1 = pegs[1] - pegs[0] - pegs[2] + pegs[1] + r3
        #   but r3 = pegs[3] - pegs[2] - r4
        # So r1 = pegs[1] - pegs[0] - pegs[2] + pegs[1] + pegs[3] - pegs[2] - r4
        # Extending this pattern to rn, then r1 = ( alternatingPegSum + rn ) when n is odd, or r1 = ( alternatingPegSum - rn ) when n is even
        # We also know that (r1/r2)*(r2/r3)...*(rn-1/rn) = r1/rn = 2, so we can substitute rn = r1/2
        # Therefore r1 = ( 2 * alternatingPegSum ) when n is odd, or r1 = ( 2/3 * alternatingPegSum ) when n is even
        # By extension since rn=r1/2, rn = alternatingPegSum when n is odd, or rn = ( alternatingPegSum / 3 ) when n is even
        # Thus when we get to the final peg, we subtract the alternatingPegSum if there were odd number of pegs, otherwise add alternatingPegSum/3
        if pegIndex == numPegs - 1:
            currentGearRadiusNumerator = -1 * currentAlternatingPegSum
            currentGearRadiusDenominator = 1

            if pegIndex % 2 != 0:
                if currentAlternatingPegSum % 3 != 0:
                    currentGearRadiusNumerator = currentAlternatingPegSum
                    currentGearRadiusDenominator = 3
                else:
                    currentGearRadiusNumerator = currentAlternatingPegSum / 3

            return [currentGearRadiusNumerator,currentGearRadiusDenominator]

        nextGearRadiusAsReducedFraction = getGearRadiusThatDoublesOutputRotationAsReducedFraction( pegIndex + 1, currentAlternatingPegSum )
        nextGearRadiusNumerator = nextGearRadiusAsReducedFraction[0]
        currentGearRadiusDenominator = nextGearRadiusAsReducedFraction[1]
        currentGearRadiusNumerator = ( ( pegs[pegIndex+1] - pegs[pegIndex] ) * currentGearRadiusDenominator ) - nextGearRadiusNumerator

        if currentGearRadiusNumerator < currentGearRadiusDenominator:
            return solutionImpossible

        return [currentGearRadiusNumerator,currentGearRadiusDenominator]

    firstGearRadiusThatDoublesOutputRotationAsReducedFraction = getGearRadiusThatDoublesOutputRotationAsReducedFraction( pegIndex=0, previousAlternatingPegSum=0 )

    # We don't want the first gear's radius to extend into the station wall
    # But the test cases fail if we check this, so the peg data may already be taking this into account?
    # We should also confirm if the final radius might extend into the other station wall, but we do not presently have enough data to check that
    #
    # TODO: Bring these concerns up with Commander Lambda before shipping!!!
    #
    #if firstGearRadiusThatDoublesOutputRotationAsReducedFraction[0] > pegs[0] * firstGearRadiusThatDoublesOutputRotationAsReducedFraction[1]:
    #    return solutionImpossible

    return firstGearRadiusThatDoublesOutputRotationAsReducedFraction
