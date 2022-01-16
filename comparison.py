"""
This was a file containing functions that would compare the pixel values
and compare them to one another. It was particularly useful for the 
grayscaling operations and the Gaussian blur applications. 
"""

import cv2
import numpy as np
from gaussianBlur import GaussianBlur
import matplotlib.pyplot as plt
from colourConversion import cvtColour

def imgPlotter(img):
    """
    Matplot function wrapper that was just used to read in 
    non-OpenCV image data and then display it.

    Parameters
    ----------
    img : list[list[int]], required
        The 2D matrix that would be displayed
    """
    plt.imshow(img, cmap='gray')
    plt.show()

def imageComparator(img1, img2):
    """
    The image comparator function that counts the and displays inaccuracies of 
    of image data. Used to compare OpenCV functions to first principle implementations.

    Parameters
    ----------
    img1 : list[list[]], reqired
        The reference image
    img2 : list[list[]], reqired
        The second image
    """
    counter = 0
    for x in range(0,len(img1[0])):
        for y in range(0,len(img1)):
            plt.plot(x,y,'w')
            test = img1[y][x] == int(round(img2[y][x]))
            if test == False:
                plt.plot(x,y,'rx')
                counter+=1
                print(f"{x}, {y} = {img1[y][x]} , {int(round(img2[y][x]))} / {img2[y][x]}")
    
    print("Total Missed Cases:", counter)
    plt.show()

def grayScaleAndBlurring(frame):
    """
    Function that was used to test both first principles and OpenCV
    implementations.
    """

    gray1 = cv2.cvtColor(frame.copy(), cv2.COLOR_RGB2GRAY)
    imgPlotter(gray1)
    
    gray2 = cvtColour(frame.copy())
    imgPlotter(gray2)

    gb1 = cv2.GaussianBlur(gray1, (3,3), 1)
    # imgPlotter(gb1)

    gb2 = GaussianBlur(gray1, (3,3), 1)
    # imgPlotter(gb2)

    print(np.sum(gray1))
    print(np.sum(gray2))

    # Comparing the arrays
    grayscaleTest = np.array(gray1) == np.array(gray2)
    gaussianBlurTest = np.array(gb1) == np.array(gb2)

    print("Shape",np.array(gb1).shape)
    print("Shape",np.array(gb2).shape)

    print("GrayScaleTest",grayscaleTest.all())
    print("Gaussian Blur Test", gaussianBlurTest.all())

    # imageComparator(gray1, gray2)

    imageComparator(gb1, gb2)