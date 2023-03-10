# Author: Derek Moran, Level 2 Henchman @ Commander Lambda Space Station
# Date: 21-NOV-2022

def solution(x, y):
    # Your code here
    return str( getWorkerId(x, y) )

# Take as its input a space station cell location at ( distanceFromWall, heightFromGround )
# Returns the workerId for the provided location
# Provided distanceFromWall and heightFromGround must be integer between 1 and 100,000 inclusive
def getWorkerId( distanceFromWall, heightFromGround ):

    if not type(distanceFromWall) is int:
        raise TypeError("Provided distanceFromWall must be an integer")

    if not type(heightFromGround) is int:
        raise TypeError("Provided heightFromGround must be an integer")
        
    if distanceFromWall < 1 or distanceFromWall > 100000:
        raise Exception("Provided distanceFromWall must be between 1 and 100000 inclusive")
        
    if heightFromGround < 1 or heightFromGround > 100000:
        raise Exception("Provided heightFromGround must be between 1 and 100000 inclusive")

    # Given the space station's particular layout, getWorkerId( distanceFromWall, 1 )
    # = 1+2+3+ ... + (distanceFromWall-1) + distanceFromWall
    # = (distanceFromWall*(distanceFromWall+1))/2
    #
    # So getWorkerId( distanceFromWall, heightFromGround )
    # = getWorkerId( distanceFromWall, 1 )
    #   + ( (distanceFromWall+heightFromGround-2)*(distanceFromWall+heightFromGround-1) )/2
    #   - ( (distanceFromWall - 1)*distanceFromWall )/2
    #
    # i.e getWorkerId( distanceFromWall, heightFromGround ) can be obtained by starting with the result
    # of getWorkerId( distanceFromWall, 1 ) and then adding the same subseries starting at
    # distanceFromWall-1 and ending at distanceFromWall+heightFromGround-1
    #
    # Simplifying that equation, we can obtain the result in O(1):
    workerId = ( distanceFromWall + heightFromGround ) ** 2
    workerId -= 3 * heightFromGround
    workerId -= distanceFromWall - 2
    workerId /= 2

    return workerId