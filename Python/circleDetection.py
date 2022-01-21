from asyncio.subprocess import DEVNULL
from collections import defaultdict
import math
from math import pi
from matplotlib.pyplot import imshow
from gaussianBlur import GaussianBlur
from numpyEquivelant import countX
from cv2 import Sobel, accumulate
from textfileReader import readTextfile, writeTextfile
import numpy as np
from comparison import imgPlotter
from convolution import convolution2D, seperableConvolution
import time
from globalVars import DEBUGGING, firstPrinciplePlotting

def SobelEdgeDetection(I, prevX = None, prevY = None):
    """
    Sobel Operator using edge detection(approximation to the derivative to an image)

    Parameters
    ----------
    I : list[list[int]], required
        The image matrix
    Returns
    -------
    M : list[list[float]]
        The magnitude of the image after the Sobel edge detection
    gradient : list[list[float]]
        The gradient of the image after the Sobel edge detection
    width : int 
        The width of image in pixels
    height : int 
        The height of image in pixels
    maxPixelIntensity : 
        The maximum pixel intensity detected in an image
    
    Noteworthy to look at the Sobel Derivatives:
        https://docs.opencv.org/4.5.2/d2/d2c/tutorial_sobel_derivatives.html
    Note: if we have prevX and prevY we only have to worry about the the full size image in hough transform
    """

    """ 
    The following lines of code are an optimisation on the Hough Circles Algorithm

    How it works:
    -------------
    The Hough Circles Gradient algorithm is already an improvement on the standard
    method, however it is still slow and sequential.

    The Hough Circles method is still remarkably robust to noise, so it makes it 
    good in noisy environments. Changing methods may not be feasible so how it can be 
    sped up is by allowing performing the Algorithm on the entire image. Following that 
    the position of the ball can be found. We can then use that position as a reference
    for a window that would surround the ball. The window is much smaller than the
    entire image, but is still large enough to still track the ball. 
    """
    width = len(I[0])
    height = len(I)

    if (prevX is not None) and (prevY is not None):
        # Distance to scan around the last point
        distanceTravelled = 100
        
        xRange = [prevX - distanceTravelled, prevX + distanceTravelled]
        yRange = [prevY - distanceTravelled, prevY + distanceTravelled]
                    # x                 #y
        arrSize = [2*distanceTravelled, 2*distanceTravelled]

        # --- Catching for the edges of the screen
        # X - catches
        if prevX + distanceTravelled > width:
            xRange[1] = width
            arrSize[0] = width - prevX + distanceTravelled
        if prevX - distanceTravelled < 0:
            xRange[0] = 0
            arrSize[0] = 0 + prevX + distanceTravelled
        
        # Y - catches
        if prevY - distanceTravelled > height:
            yRange[1] = height
            arrSize[1] = height - prevY + distanceTravelled
        if prevY - distanceTravelled < 0:
            yRange[0] = 0
            arrSize[1] =0 + prevY + distanceTravelled
        
        img = [[0 for x in range(arrSize[0])] for y in range(arrSize[1])]
        for y in range(yRange[0], yRange[1]):
            for x in range(xRange[0], xRange[1]):
                # Must minus the values off to ensure that don't exceed allowable value
                try:
                    img[y-yRange[0]][x-xRange[0]] = I[y][x]
                except:
                    IndexError(f"{x}:{y}:{xRange[0]}:{yRange[0]}")
        imageWidth = arrSize[0]
        imageHeight = arrSize[1]
        
    else:
        imageWidth = width
        imageHeight = height
        img = I
        # These are just to keep the program happy
        xRange = [0, width]
        yRange = [0, height]
    
    """
    # Alternate method from OpenCV using the Scharr Adjustment
    
    # --------------------- #
    # X Kernel - Horizontal #
    # --------------------- #
    # Gh_h = [-1,-2,-1]
    # Scharr Adjustment
    Gh_h = [-3,-10,-3]
    Gh_v = [[1],[0],[-1]]
    G_x = seperableConvolution(I=img,
                            K_v=Gh_v,
                            K_h=Gh_h,
                            imgWidth=imageWidth,
                            imgHeight=imageHeight,
                            W=3)
    # --------------------- #
    #  Y Kernel - Vertical  #
    # --------------------- #
    Gv_h = [1,0,-1]
    # Scharr Adjustment
    # Gv_v = [[-1],[-2],[-1]]
    Gv_v = [[-3],[-10],[-3]]

    G_y = seperableConvolution(I=img,
                            K_v=Gv_v,
                            K_h=Gv_h,
                            imgWidth=imageWidth,
                            imgHeight=imageHeight,
                            W=3)    
    G_x1 = G_x
    G_y1 = G_y
    
    """
    
    maxPixelIntensity = 0
    # ---------------------------------------- #
    # This must be adaptive as well            #
    # ---------------------------------------- #
    # Magnitude 
    M = [[0 for i in range(imageWidth)] for j in range(imageHeight)]
    gradient = [[0 for i in range(imageWidth)] for j in range(imageHeight)]
    for y in range(0,imageHeight):
        for x in range(0,imageWidth): # This had to change to change the structure
            if (1 < x < imageWidth - 1) and (1 < y < imageHeight - 1):
                # The gradient
                G_x1 = img[y][x + 1] - img[y][x - 1]
                G_y1 = img[y + 1][x] - img[y - 1][x]

                calcMag = np.sqrt((G_x1)**2 + (G_y1)**2)
                M[y][x] = calcMag

                calcGradient = math.atan2(G_y1, G_x1)
                gradient[y][x] = calcGradient

                if calcMag > maxPixelIntensity:
                    maxPixelIntensity=calcMag
    

    # Plotting Things of Importance:
    if firstPrinciplePlotting:
        print("img:")
        imgPlotter(img)
        print("M:")
        imgPlotter(M)
        print("gradient:")
        imgPlotter(gradient)
    if DEBUGGING == 1:
        print("Image Width", imageWidth)
        print("Image Height", imageHeight)
        print("Maximum Pixel Intensity", maxPixelIntensity)
        # writeTextfile(M)
        # writeTextfile(gradient)
                                # Returning these values for final position in hough transform
    return M, gradient, imageWidth, imageHeight, maxPixelIntensity, xRange[0], yRange[0] 

def CannyEdgeDetection(I, lowThreshold = 0.4, highThreshold = 0.6, prevX = None, prevY = None):
    """ 
    0.4 and 0.8 for normal use
    Canny Edge Detection using a Sobel operator
    to get rid of the edges we are not interested in 

    Parameters
    ----------
    I : list[list[int]], required
        The image matrix

    lowThreshold : float, optional
        The lower threshold of the image used in the second pass
        of thresholding 
    
    highThreshold : float, optional
        The upper threshold of the image used in the second pass
        of thresholding 

    prevX : int, optional 
        The X value that is used for the optimisation window method

    prevY : int, optional 
        The Y value that is used for the optimisation window method

    Returns
    -------
    result : list[list[int]]
        The resulting windowed image
    width : int
        The window width
    
    height : int
        The window height

    xStart : int 
        The starting x position of the window

    yStart : int
        The starting y position of the window
    """   
    M, gradient, width, height, maxPixelIntensity, xStart, yStart = SobelEdgeDetection(I, prevX = prevX, prevY = prevY)

    # ============================ #
    # Non-maximum value suppresion #   
    # ============================ #
    for y in range(1, width - 1):
        for x in range(1, height - 1):
            angle = gradient[x][y] if gradient[x][y] >= 0 else gradient[x][y] + pi
            rangle = round(angle / (pi / 4))
            mag = M[x][y]
            if ((rangle == 0 or rangle == 4) and ( M[x - 1][y] > mag or  M[x + 1][y] > mag)
                    or (rangle == 1 and ( M[x - 1][y - 1] > mag or  M[x + 1][y + 1] > mag))
                    or (rangle == 2 and ( M[x][y - 1] > mag or  M[x][y + 1] > mag))
                    or (rangle == 3 and ( M[x + 1][y - 1] > mag or  M[x - 1][y + 1] > mag))):
                M[x][y] = 0

    # ============================ #
    # Secondary Thresholding       #   
    # ============================ #
    posArr = []
    
    highThreshold *= maxPixelIntensity
    lowThreshold *= maxPixelIntensity

    # High Threshold
    for y in range(height):
        for x in range(width):
            if M[y][x] > highThreshold:
                # Holds the position of the high values
                posArr.append((x,y))

    # Low Threshold
    traverse = [-1,0,1]
    for y in range(height):
        for x in range(width):
            # Checking array around
            for b in traverse:
                for a in traverse:
                    if (y+b>=0) and (x+a>=0) and (y+b<height) and (x+a<width): 
                        if M[y+b][x+a] > lowThreshold and not ((x+a,y+b) in posArr):
                            posArr.append((x+a, y+b))
    
    # Creating the final image
    result = []
    for y in range(height):
        rowArr = []
        for x in range(width):
            if (x,y) in posArr:
                rowArr.append(255)
            else:
                rowArr.append(0)
        result.append(rowArr)
    
    # Plotting Things of Importance:
    if firstPrinciplePlotting:
        imgPlotter(result)
    if DEBUGGING == 1:
        print("Max pixel intensity", maxPixelIntensity)
        print("High Threshold", highThreshold)
        print("Low threshold", lowThreshold)
        

    return result, width, height, xStart, yStart

def HoughCircles(I, radius, prevX = None, prevY = None):
    """
    Detecting circles using the Hough Gradient Method

    Parameters
    ----------
    I : list[list[int]], required
        The image matrix
    radius: int, required
        The radius of the circle in pixels

    Returns
    ------- 
    The centre position of a singular circle.

    TODO: Later add the ability to detect multiple circles in the image

    Working Principle
    -----------------
    The tangent algorithm works by taking a 3x3 grid centred around a detected point in the image
    the grid then scans for the positions external to it and reacts accordingly.
    """

    # Determine the length of the normals
    startRadius = int(5*radius/12)
    endRadius = int(3*radius/4)

    # if prevX is None and prevY is None:
    cannyResult, width, height, xStart, yStart = CannyEdgeDetection(I, prevX = prevX, prevY = prevY)
    # ---- 5x5 ---- #
    # |---------------------------------------------|
    # | [-2,-2]  [-1,-2]  [ 0,-2]  [ 1,-2]  [ 2,-2] |
    # | [-2,-1]  [-1,-1]  [ 0,-1]  [ 1,-1]  [ 2,-1] |
    # | [-2, 0]  [-1, 0]  [ 0, 0]  [ 1, 0]  [ 2, 0] |
    # | [-2, 1]  [-1, 1]  [ 0, 1]  [ 1, 1]  [ 2, 1] |
    # | [-2, 2]  [-1, 2]  [ 0, 2]  [ 1, 2]  [ 2, 2] |
    # |---------------------------------------------|

    accumulatator = [[0 for i in range(width)] for j in range(height)]
    traverse = [-4,-3,-2,-1,0,1,2,3,4]
    for y in range(height):
        for x in range(width):
            # Checking array around
            indexArr = []
            if cannyResult[y][x] == 255:
                # Taking the grid over it to determine the tangent
                for b in traverse:
                    for a in traverse:
                        if (y+b>=0) and (x+a>=0) and (y+b<height) and (x+a<width): 
                            if cannyResult[y+b][x+a] == 255:
                                indexArr.append([a,b])
    
            # Checking if the value is 255 and if thats the case mark the index

            # ==================== #
            #       CASE 45        #
            # ==================== #
            # |--------------------|
            # | 0   0   0   0   1  |
            # | 0   0   0   1   0  |
            # | 0   0   1   0   0  |
            # | 0   1   0   0   0  |
            # | 1   0   0   0   0  |
            # |--------------------|
            """case45 = ([-1,1] in indexArr) and ([1,-1] in indexArr) and ([-2,2] in indexArr) and ([2,-2] in indexArr) and ([-3,3] in indexArr) and ([3,-3] in indexArr) and ([-4,4] in indexArr) and ([4,-4] in indexArr) \
                    or ([-1,1] in indexArr) and ([1,-1] in indexArr) and ([-2,2] in indexArr) and ([2,-2] in indexArr) and ([-3,3] in indexArr) and ([3,-3] in indexArr) \
                    or ([-1,1] in indexArr) and ([1,-1] in indexArr) and ([-2,2] in indexArr) and ([2,-2] in indexArr) """
            case45 = ([-1,1] in indexArr) and ([1,-1] in indexArr) and ([-2,2] in indexArr) and ([2,-2] in indexArr) 


            # ==================== #
            #       CASE 135       #
            # ==================== #
            # |--------------------|
            # | 1   0   0   0   0  |
            # | 0   1   0   0   0  |
            # | 0   0   1   0   0  |
            # | 0   0   0   1   0  |
            # | 0   0   0   0   1  |
            # |--------------------|
            """case135 = ([-1,-1] in indexArr) and ([1,1] in indexArr) and ([-2,-2] in indexArr) and ([2,2] in indexArr) and ([-3,-3] in indexArr) and ([3,3] in indexArr) and ([-4,-4 in indexArr]) and ([4,4] in indexArr) \
                    or ([-1,-1] in indexArr) and ([1,1] in indexArr) and ([-2,-2] in indexArr) and ([2,2] in indexArr) and ([-3,-3] in indexArr) and ([3,3] in indexArr) \
                    or ([-1,-1] in indexArr) and ([1,1] in indexArr) and ([-2,-2] in indexArr) and ([2,2] in indexArr) """
            case135 = ([-1,-1] in indexArr) and ([1,1] in indexArr) and ([-2,-2] in indexArr) and ([2,2] in indexArr)

            caseNoAct = True if (len(indexArr)>=22) else False

            #-------------------------#
            #Checking if all surrounded#
            #-------------------------#
            if caseNoAct:
                # Skip this loop iteration and do nothing with it
                continue
            
            #-----------#    
            # 45 degree #
            #-----------#
            elif case45: # Remember these are just tangents and we are intersted in the normal
                for i in range(startRadius,endRadius):
                    # TODO: Only look after a specific distance regarding the radius because we don't want to detect really small circles
                    if (x-i>=0 and x+i < width) and (y-i>=0 and y+i < height):
                        if DEBUGGING == 1:
                            print(f"Case 45: {x} {x-i}, {x+i}; {y}, {y-i}, {y+i}")
                        accumulatator[y+i][x+i] += 1
                        accumulatator[y-i][x-i] += 1

            #-----------#
            # 135 degree#
            #-----------#
            elif case135: # Remember these are just tangents and we are intersted in the normal
                for i in range(startRadius, endRadius):
                    # TODO: Only look after a specific distance regarding the radius because we don't want to detect really small circles
                    if (x-i>=0 and x+i < width) and (y-i>=0 and y+i < height):
                        if DEBUGGING == 1: 
                            print(f"Case 135: {x} {x-i}, {x+i};{y}, {y-i}, {y+i}")
                        accumulatator[y-i][x+i] += 1
                        accumulatator[y+i][x-i] += 1
                    
    # -------------------------------------------------------------------------------- # 
    #              Algorithm to determine true centre of a single circle               #
    # -------------------------------------------------------------------------------- # 
    
    # Algorithm: The mode values and values close enough to it determine which values
    # Determine the center or the circle, if they are outliers then we can ignore them
    modeX = []
    modeY = []
    maxVal = 0
    position = []
    for y in range(height):
        for x in range(width):
            if accumulatator[y][x] > maxVal:
                position = []
                #------#
                modeX = []
                modeY = []
                #------#
                maxVal = accumulatator[y][x]
                position = [[x,y]]
                modeX = [(int)(x/10)]
                modeY =[(int)(y/10)]
            # Averaging if there a certain number of equal array values
            elif accumulatator[y][x] == maxVal:
                position.append([x,y])
                modeX.append((int)(x/10))
                modeY.append((int)(y/10))
    if DEBUGGING == 1:
        print("Maximum Value:", maxVal)

    # If the maximum value in the accumulator is 1(or very small) there is no proof that there is circle
    if maxVal > 1:
        # Range that we still count the value to be valid
        rangeToCheck = 2 # TODO: Determine a sufficient size of the array
        
        # Determining the most frequent pixel values detected, so that we can ignore outliers
        mostFreqX = 0
        valOfMostfreqX = 0
        valOfMostfreqY = 0
        
        for i in modeX:
            temp = countX(modeX, i)
            if mostFreqX < temp:
                mostFreqX = temp
                valOfMostfreqX = i
        mostFreqY = 0
        for i in modeY:
            temp = countX(modeY, i)
            if mostFreqY < temp:
                mostFreqY = temp
                valOfMostfreqY = i

        # Adding the values that fall into a specific range to the final arr
        finalArr = []
        for j in range(len(position)):
            # Checking the X and Y value to see if it falls into a specific range
            if ((valOfMostfreqX - rangeToCheck) < (int)(position[j][0]/10) < (valOfMostfreqX + rangeToCheck)) and \
                ((valOfMostfreqY - rangeToCheck) < (int)(position[j][1]/10) < valOfMostfreqY + rangeToCheck):
                finalArr.append(position[j])
                    
        # Summing the values together to get a midpoint
        sumX = 0
        sumY = 0
        lenFinArr = len(finalArr)
        for i in range(lenFinArr):
            sumX += position[i][0]
            sumY += position[i][1]
        center = [int(sumX/lenFinArr), int(sumY/lenFinArr)] # TODO: Catch for zero division error
        
        # Catch for the prev values
        if prevX is None and prevY is None:
            xStart = 0
            yStart = 0

        # Plotting Things of Importance:
        if firstPrinciplePlotting:
            imgPlotter(accumulatator)
            if DEBUGGING == 1:
                print("Maximum value of accumulator",maxVal)
                print("Position", position)
                print("ModeX", modeX)
                print("ModeY", modeY)
                print("most frequently occuring values", valOfMostfreqX, valOfMostfreqY)
                print("Center as determined by the algorithm", center)
                print("Center as determined by the algorithm", [xStart + center[0], yStart + center[1]])

        return [[xStart + center[0], yStart + center[1]]]
    else:
        # If there is no maximum then search whole image
        return [[None, None]]


def paddleDetectors(I, prevX = 0, prevY = 180):
    """
    Uses a similar idea to the algorithm above in that it tries to detect the corners of the paddles.

    Parameters
    ----------
    I : list[list[int]], required
        The image matrix
    
    Returns
    ------- 
    paddleCorners: list[list[int]]
        The detected paddle corners

    Working Principle
    -----------------
    This algorithm assumes that no other paddle will be present during the scan of a particular area

    Cons
    ----
    If the exact corners are not matched it returns no detected paddles which is an issue, something like
    connected component labelling would work better, with the RDP algorithm would work better.
    """
    # if prevX is None and prevY is None:
    cannyResult, width, height, xStart, yStart = CannyEdgeDetection(I, prevX = prevX, prevY = prevY) # In C++ take this directly from function

    # ---- 5x5 ---- #
    # |---------------------------------------------|
    # | [-2,-2]  [-1,-2]  [ 0,-2]  [ 1,-2]  [ 2,-2] |
    # | [-2,-1]  [-1,-1]  [ 0,-1]  [ 1,-1]  [ 2,-1] |
    # | [-2, 0]  [-1, 0]  [ 0, 0]  [ 1, 0]  [ 2, 0] |
    # | [-2, 1]  [-1, 1]  [ 0, 1]  [ 1, 1]  [ 2, 1] |
    # | [-2, 2]  [-1, 2]  [ 0, 2]  [ 1, 2]  [ 2, 2] |
    # |---------------------------------------------|
    paddleCorners = [
        [[0,0]],
        [[0,0]],
        [[0,0]],
        [[0,0]],]
    traverse = [-3,-2,-1,0,1,2,3]
    for y in range(height):
        for x in range(width):
            # Checking array around
            indexArr = []
            if cannyResult[y][x] == 255:
                # Taking the grid over it to determine the tangent
                for b in traverse:
                    for a in traverse:
                        if (y+b>=0) and (x+a>=0) and (y+b<height) and (x+a<width): 
                            if cannyResult[y+b][x+a] == 255:
                                indexArr.append([a,b])

            # ==================== #
            #       CASE L         #
            # ==================== #
            # |--------------------|
            # | 0   0   1   0   0  |
            # | 0   0   1   0   0  |
            # | 0   0   1   1   1  |
            # | 0   0   0   0   0  |
            # | 0   0   0   0   0  |
            # |--------------------|
            caseBigL = ([0,-2] in indexArr) and ([0,-1] in indexArr) and ([1,0] in indexArr) and ([2,0] in indexArr) #and ([3,0] in indexArr)
            # ==================== #
            #     CASE UPSIDE L    #
            # ==================== #
            # |--------------------|
            # | 0   0   0   0   0  |
            # | 0   0   0   0   0  |
            # | 0   0   1   1   1  |
            # | 0   0   1   0   0  |
            # | 0   0   1   0   0  |
            # |--------------------|
            caseUpdsideL = ([1,0] in indexArr) and ([2,0] in indexArr) and ([0,1] in indexArr) and ([0,2] in indexArr) #and ([0,3] in indexArr)
            # ==================== #
            #    CASE INVERSE L    #
            # ==================== #
            # |--------------------|
            # | 0   0   1   0   0  |
            # | 0   0   1   0   0  |
            # | 1   1   1   0   0  |
            # | 0   0   0   0   0  |
            # | 0   0   0   0   0  |
            # |--------------------|
            caseInverseL = ([-2,0] in indexArr) and ([-1,0] in indexArr) and ([0,-1] in indexArr) and ([0,-2] in indexArr) #and ([0,-3] in indexArr)
            # ==================== #
            # CASE INVERSE UPSIDE L#
            # ==================== #
            # |--------------------|
            # | 0   0   0   0   0  |
            # | 0   0   0   0   0  |
            # | 1   1   1   0   0  |
            # | 0   0   1   0   0  |
            # | 0   0   1   0   0  |
            # |--------------------|
            caseInverseUpsideL = ([-2,0] in indexArr) and ([-1,0] in indexArr) and ([0,1] in indexArr) and ([0,2] in indexArr) #and ([0,3] in indexArr) 
            # TODO: Add catch conditions for outliers and then they can be filled in
            # We now do detection regarding if there are a certain number of points
            # and what to do if we only detect 3 corners
            # if (prevX is not None) and (prevY is not None): 
            if caseBigL: # Bottom Left
                paddleCorners[0] = [[xStart+x, yStart+y]]
                if firstPrinciplePlotting:
                    print("x,y coordinate of Inverse Upside L",x,y) 

            
            if caseUpdsideL: # Top left
                paddleCorners[1] = [[xStart+x, yStart+y]]
                if firstPrinciplePlotting:
                    print("x,y coordinate of Inverse Upside L",x,y) 

            
            if caseInverseL: # Bottom right
                paddleCorners[2] = [[xStart+x, yStart+y]]
                if firstPrinciplePlotting:
                    print("x,y coordinate of Inverse Upside L",x,y) 

            
            if caseInverseUpsideL: # Top Right 
                paddleCorners[3] = [[xStart+x, yStart+y]]                
                if firstPrinciplePlotting:
                    print("x,y coordinate of Inverse Upside L",x,y) 

    if firstPrinciplePlotting:
        imgPlotter(cannyResult)

    return paddleCorners

# Unit Testing 
if __name__=="__main__":
    import cv2
    start_time = time.time()
    
    # Reading in the values from the textfiles
    I = np.array(readTextfile('file.txt')).astype(np.uint8)
    print("Maximum value in array", I.ravel()[np.argmax(I)])

    # Using OpenCV as the bench mark
    gray = cv2.GaussianBlur(I, (3,3), 0)

    H = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    print("Hough Circle of OpenCV", H)

    I = (readTextfile('file.txt'))

    print("Sobel Result FP: ")
    H, gradient, imageWidth, imageHeight, maxPixelIntensity, xtemp, ytemp = SobelEdgeDetection(I)
    imgPlotter(H)

    print("Canny Result FP: ")
    result, width, height, xStart, yStart  = CannyEdgeDetection(I)
    imgPlotter(result)
    
    print("Paddle Detector Test: ")
    paddleDetectors(I, prevX = 0, prevY = 180)

    print("Hough Circle FP 1")
    [[houghPrevX, houghPrevY]] = HoughCircles(I=I, radius=20, prevX = None, prevY=None)
    print("Calculated Hough Circle First Principles",[[houghPrevX, houghPrevY]])
    
    print("Hough Circle FP 2")
    [[houghPrevX, houghPrevY]] = HoughCircles(I=I, radius=20, prevX = houghPrevX, prevY=houghPrevY)
    print("Calculated Hough Circle First Principles",[[houghPrevX, houghPrevY]])

    print("Hough Circle FP 3")
    [[houghPrevX, houghPrevY]] = HoughCircles(I=I, radius=20, prevX = houghPrevX, prevY=houghPrevY)
    print("Calculated Hough Circle First Principles",[[houghPrevX, houghPrevY]])

    print("--- %s seconds ---" % (time.time() - start_time))    