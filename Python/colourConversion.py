# https://docs.opencv.org/3.4/de/d25/imgproc_color_conversions.html

"""
OpenCV from first principles is using the existing OpenCV library documentation and 
The Textbook series Principles of Digital Image Processing
"""
import numpy as np
import matplotlib.pyplot as plt


def cvtColour( I, slightlyInaccurateMethod = True ):
    """
    Equivalent to COLOR_RGB2GRAY, which converts a RGB image to a grayscale image
    
    Parameters
    ----------
    I : list[list[int]], required
        Triple Channel channel image containing R,G,B channels;

    slightlyInaccurateMethod : bool, optional
        Selection between methods of computation

    TODO: typeConv - The type of conversion that is required to take to place
    
    Returns
    -------
    Y : list[list], required
        Containing gray image as output 
        
    """
    if slightlyInaccurateMethod == True:
        # Number of columns 
        M = len(I)   
        # Number of rows 
        N = len(I[0])
        # Number of Channels
        depth = len(I[0][0])
        
        # Initialization Gray scale array
        Y = []
        for y in range(M):
            Y.append([0 for x in range(N)]) 

        # TODO: Check this link to parallelise the calculation
        # https://www.geeksforgeeks.org/image-processing-without-opencv-python/
        # Cols
        for y in range(M):
            # Rows 
            for x in range(N):
                # Multiplication
                # Red Channel
                Y[y][x] = 0.299 * I[y][x][0]
                # Green Channel
                Y[y][x] += 0.578 * I[y][x][1]
                # Blue Channel
                Y[y][x] += 0.114 * I[y][x][2]

        # Cols
        for y in range(M):
            # Rows 
            for x in range(N):
                Y[y][x] = round(Y[y][x]) 
    else:
        # Closest thing to OpenCV -> They both have problems with the rounding
        # Is over 2 seconds faster in processing
        r, g, b = I[:,:,0], I[:,:,1], I[:,:,2]
        Y = 0.299 * r + 0.5870 * g + 0.1140 * b
    
    return np.array(Y).astype(np.uint8)

    
    """
    Non-Parallel Calculation
    # Depth
    for z in range(depth):
        # Cols
        for y in range(M):
            # Rows 
            for x in range(N):
                multiplicant = 0.0
                
                # --- Read in BGR format
                # Red Channel
                if z == 0:
                    multiplicant = 0.299
                # Green Channel
                elif z == 1:
                    multiplicant = 0.5870
                # Blue Channel
                elif z == 2:
                    multiplicant = 0.1140
                else: 
                    return IndexError("There can only be three channels, please check dimensions")
                
                # Multiplication
                # print(I[z][y][x])
                Y[y][x] += (multiplicant * I[y][x][z])
                # if Y[y][x] > (2**8-1): #255
                #     Y[y][x] = 255
    """