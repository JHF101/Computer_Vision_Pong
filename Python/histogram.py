import cv2
import numpy as np
import matplotlib.pyplot as plt

def Histogrammer(frame):
    """
    Function that displays a histogram of an images pixel intensity
    for a grayscaled image
    
    Parameters
    ----------
    frame : list[list[int]], required
        The image itself
    """
    K = 256 # The number of intensity values
    B =  256 # Number of Bins - The size of the histogram 
    H = [0 for i in range(B)]

    h = len(frame) # Height 
    w = len(frame[0]) # Width 
    # Rows
    for v in range(h):
        # Cols 
        for u in frame[v]:
            i = int(np.floor((u*B)/K))
            H[i] += 1
    plt.plot(H)
    plt.title("Histogram of image")
    plt.xlabel("Image Intensity Values")
    plt.ylabel("Count")
    plt.show()

    # --- Easy Python Way of doing it
    # flat = list(np.concatenate(frame).flat)
    # # Assuming grey scale 2^8
    # H = [0 for i in range(256)]
    # for i in flat:
    #     H[i] += 1
    # plt.plot(H)
    # plt.show()
