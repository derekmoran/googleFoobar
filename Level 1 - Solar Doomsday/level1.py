# Author: Derek Moran, Level 1 Minion @ Commander Lambda Space Station
# Date: 11-NOV-2022

import math

def solution(area):
    # Your code here
    return getLargestSquareAreasListDescending(area)

# Takes as its input a single unit of measure representing the total area
# Provided area must be between 1 and 1000000 inclusive
# Returns a list of the areas of the largest squares you could make out of those panels, starting with the largest squares first
# ex: getLargestSquareAreasListDescending(12) would return [9, 1, 1, 1]
def getLargestSquareAreasListDescending(area):
    if not type(area) is int:
        raise TypeError("Provided area must be an integer")

    if area < 0 or area > 1000000:
        raise TypeError("Provided area must be between 1 and 1000000 inclusive")

    areaList = []
    remainingArea = area

    while remainingArea > 0:
        maxUnitArea = int(math.floor(math.sqrt(remainingArea)) ** 2)
        remainingArea -= maxUnitArea
        areaList.append(maxUnitArea)

    return areaList