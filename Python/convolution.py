import imghdr
from matplotlib import pyplot as plt
from textfileReader import readTextfile
import time
from numpyEquivelant import pad
import numpy as np
from numpy.fft import fft

def seperableConvolution(I, K_v, K_h, imgWidth, imgHeight, W):
    """
    Returns a convolved 2D array.

    Parameters
    ----------
    I : list[list[int]], required
        The array of image data 
    
    K_v : list[list[float]], required
        Column Vector of seperable kernel

    K_h : list[float], required
        Row Vector of seperable kernel
    
    imgWidth : int, required
        Width of the image in pixels

    imgHeight : int, required
        Height of the image in pixels
    
    W : int, required
        Kernel size, must be an odd number

    Returns:
    --------
    H : product after 2D convolution 

    Raises
    ------
    If one of the paramenters are not completed a not implemented error is returned

    """
    if not(I is None or  \
       K_v is None or \
       K_h is None or \
       imgWidth is None or \
       imgHeight is None or \
       W is None):
        
        start_time = time.time()            
        
        """
        mean = int(W/2) # Kernel radius

        # ------ Padding the array ------ #
        # Padded width and height
        newDimimgHeight = imgHeight + 2*(W - mean)
        newDimimgWidth = imgWidth + 2*(W - mean)

        # --- Equivelant piece of code --- #
        # np.pad(I,W-mean,mode='constant')
        # Padded image array
        I_padded = pad(I, W-mean)

        # New array filled with zeros
        H = [[0 for i in range(imgWidth)] for j in range(imgHeight)]

        for y in range(0,imgHeight):
            for x in range(0,imgWidth):
                # Process of convolution
                for j in range(0,W):
                    for i in range(0,W):
                        if (y < imgHeight and y+j < newDimimgHeight) and (x < imgWidth and x+i < newDimimgWidth):
                            H[y][x] += K_v[j][0] * I_padded[y+j][x+i] * K_h[i]
        
        print("--- %s seconds for Convolution ---" % (time.time() - start_time))

        return H
        """

        # For some reason this is slower implementation Implementation, altough it has fewer
        # operations performed on it
        H = [[0 for i in range(imgWidth)] for j in range(imgHeight)]
        
        for y in range(0, imgHeight):
            for x in range(0, imgWidth):
                for j in range(0, W):
                    for i in range(0, W):
                        if ( x-i >= 0 and x-i < imgWidth) and ( y-j>=0 and y-j < imgHeight ):
                            H[y][x] += K_v[j][0] * I[y-j][x-i] * K_h[i]

            
        return H
        
    else:
        raise NotImplementedError("Please make sure all of the paramters are entered correctly")

def convolution2D(I, K, imgWidth, imgHeight, W):
    """
    Convolution of a kernel and an image

    Parameters
    ----------
    I : list[list[int]], required
        The array of image data 
    
    K : list[list[float]], required
        Kernel matrix

    imgWidth : int, required
        Width of the image in pixels

    imgHeight : int, required
        Height of the image in pixels
    
    W : int, required
        Kernel size, must be an odd number
    
    Returns:
    --------
    H : product after 2D convolution 

    Raises
    ------
    If one of the paramenters are not completed a not implemented error is returned

    Based on https://math.stackexchange.com/questions/241041/what-does-it-mean-to-convolve-a-matrix-with-a-kernel
    """
    if not(I is None or  \
       K is None or \
       imgWidth is None or \
       imgHeight is None or \
       W is None):

        # Implementation note: If you know the kernel size already, you can just remove the loops over the kernel
        H = [[0 for i in range(imgWidth)] for j in range(imgHeight)]
        for y in range(0, imgHeight):
            for x in range(0, imgWidth):
                for i in range(0, W):
                    for j in range(0, W):
                        if (x-i>=0 and x-i < imgWidth) and (y-j>=0 and y-j<imgHeight):
                            H[y][x] += I[y-j][x-i] * K[j][i]
        return H

    else:
        raise NotImplementedError("Please make sure all of the paramters are entered correctly")


# TODO Fix this       
def convolution2DFFT(I, K):
    """
    Convolution using by doing 2D fft and then doing 2D ifft

    Parameters
    ----------
    I : list[list[int]], required
        The array of image data
    K : int, required
        Lowpass value

    Note: This approach was briefly explored, it was however not pursued further
    """
    I = np.asarray(I)
    origImg = np.fft.fft2(I)
    centerOfImg = np.fft.fftshift(origImg)
    
    # Low passing 
    base = np.zeros(I.shape[:2])
    
    rows,cols = I.shape[:2]
    center = (rows/2, cols/2)
    for x in range(cols):
        for y in range(rows):
            base[y,x] = np.exp((
                (
                -np.sqrt((y-center[0])**2 + (x-center[1])**2)
                )
                )/
                (2*(K**2)
                )
            )

    lowPassCenter = centerOfImg* base
    lowPass = np.fft.ifftshift(lowPassCenter)
    inverseLowpass = np.fft.ifft2(lowPass)
    plt.imshow(
        np.abs(inverseLowpass), cmap="gray"
    )    

# Unit Testing
if __name__=="__main__":

    I = np.asarray(readTextfile('file.txt'))

    start_time = time.time()
    print("Convolution using 2D FFT and IFFT method")
    # Low pass filter constant
    K = 50
    print("Image Dims",len(I[0]),len(I))    
    convolution2DFFT(I, K)
    
    print("--- %s seconds ---" % (time.time() - start_time))   
    
    start_time = time.time()

    # Kernel 
    K = [
        [0.0625, 0.125, 0.0625],
        [0.125,  0.25,  0.125],
        [0.0625, 0.125, 0.0625],
    ]
    print("2D Convolution")
    plt.imshow(
        convolution2D(I,K,imgHeight=360, imgWidth=640, W=3), cmap='gray'
    )
    plt.show()
    print("--- %s seconds ---" % (time.time() - start_time))   

    start_time = time.time()
    print("Separable Convolution")
    # Separeble kernels
    K_v = [[0.25],
            [0.5 ],
            [0.25]]
    K_h = [0.25,0.5,0.25]
    plt.imshow(
        seperableConvolution(I,K_v,K_h,imgHeight=360, imgWidth=640, W=3), cmap='gray'
    )
    plt.show()
    print("--- %s seconds ---" % (time.time() - start_time))   
