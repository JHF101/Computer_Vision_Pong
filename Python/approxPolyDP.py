"""
Ramer-Douglas-Peuker Algorithm
The following sites were used as reference:
https://github.com/sebleier/RDP/blob/master/__init__.py
https://towardsdatascience.com/simplify-polylines-with-the-douglas-peucker-algorithm-ac8ed487a4a1
"""
from math import sqrt
from matplotlib import pyplot as plt
import numpy as np

def distance(x1, x2):
    """
    The distance formula.
    """
    return  sqrt((x1[0] - x2[0])**2 + (x1[1] - x2[1])**2)


def point_line_distance(point, start, end):
    """
    The distance from a pont to a line.
    """
    if (start == end):
        return distance(point, start)
    else:
        n = abs((end[0] - start[0])*(start[1] - point[1]) - (start[0] - point[0])*(end[1] - start[1]))
        d = sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        return n / d


def rdp(points, epsilon):
    """
    Reduces a series of points to a simplified version that loses detail, but
    maintains the general shape of the series.
    
    Paramaters
    ----------
    points : list[], required
        The list of points that requires reduction.
    epsilon : float, required
        The tolerance parameter of which values outside are included.

    Returns
    -------
    results : list[list[]], required
        The simplified array.
    """
    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d

    if dmax >= epsilon:
        results = rdp(points[:index+1], epsilon)[:-1] + rdp(points[index:], epsilon)
    else:
        results = [points[0], points[-1]]

    return results

# Unit testing
if __name__ == "__main__":
    import cv2

    # The value used to determine the tolerance for outliers
    eps = 0.04*142.82842707633972

    out = [[630, 216], [629, 217], [628, 217], [628, 276], [629, 277], [639, 277], [639, 216]]
    pres = rdp(out, eps)
    print(pres)


