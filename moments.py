import numpy as np
from textfileReader import readTextfile
import time 

def moments(dataPoints):
    """
    Takes in a contour returned by suzuki85 algorithm in order calculate the moment of shape

    Parameters
    ----------
    dataPoints: list[list[int]]
        Data points multiple x and y values 

    Returns
    -------
    m00: int
        Area for grasclae image
    m01: int
        Centroid x * area
    m10: int
        Centroid y * area
    """
    xVals = []
    yVals = []
    for i in range(len(dataPoints)):
        xVals.append(dataPoints[i][0])
        yVals.append(dataPoints[i][1])

    m00 = 0
    m01 = 0
    m10 = 0
    for y in yVals:
        for x in xVals:
            # m00 - sum of I
            m00 += 1 #I[y][x] -> Taking the value as equal to 1 because no image is needed

            # sum(sum(y*I(x,y)))
            m01 += y #*I[y][x]

            # sum(sum(y*I(x,y)))
            m10 += x #*I[y][x]

    
    return m00, m01, m10

# Unit testing
if __name__ == "__main__":
    start_time = time.time()
    
    I = np.asarray(readTextfile('file.txt'))

    m00, m01, m10 = moments(I)
    
    cX = int(m10 / m00)
    cY = int(m01 / m00)

    print(cX, cY)
    print(len(I[0]),len(I))

    print("--- %s seconds ---" % (time.time() - start_time))    
