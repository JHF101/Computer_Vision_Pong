import matplotlib.pyplot as plt
import numpy as np
import re

def readTextfile(filename):
    """
    Function to read in image data that is saved into a textfile

    Parameters
    -----------
    filename : str, required
        The filename that should be read

    Returns
    -------
    arr : list[list[]]
        2D array (Image)
    """
    f =  open(filename)
    arr = []
    with f as current_file:
        # Reads each line of the file, and creates a 1d list of each point: e.g. [1,2].
        for line in current_file.readlines():
            #if line is empty, you are done with all lines in the file
            # cleanText = line.replace(", ","")
            
            # cleanText = line.replace(",","")
            # cleanText = line.replace(" ","")
            cleanText = line.replace("[","")
            cleanText = cleanText.replace("]","")
            cleanText = cleanText.replace(" ","")
            cleanText = cleanText.replace("\n","")
            # print(cleanText)
            
            test = re.split(",+",cleanText)
            # test = list(cleanText)
            temp = []
            for x in range(0,640):
                if test[x]==',':
                    pass
                else:
                    temp.append(int(test[x]))
            arr.append(temp)

    for y in range(0,len(arr)):
        for x in range(0, len(arr[0])):
            arr[y][x] = arr[y][x]
    #close file
    f.close()
    return arr

def writeTextfile(arr):
    """
    Function to write to a textfile

    Parameters:
    -----------
    arr: list[list[]], required
        The 2D array that is to be written to a textfile
    """
    with open('text.txt', 'w') as f:
        for y in range(0,len(arr)):
            f.write("[")
            for x in range(0, len(arr[0])):
                f.write(str(arr[y][x])+",")
            f.write("]\n")

        
if __name__ == "__main__":
    
    plt.imshow(readTextfile('file.txt'))
    plt.show()
    # print(readTextfile("file.txt")[120][100])