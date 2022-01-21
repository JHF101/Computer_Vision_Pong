"""
Numpy equivelant functions. 
Specifically:
    1) Transposing a matrix function 
    2) Padding a matrix function
    3)
"""

# Transpose Matrix:
def transpose(matrix):
    """
    Transposing a matrix function

    Paramaters
    ----------
    matrix: list[list[]], required
        The matrix to be transposed

    Returns
    -------
    Transposed matrix
    """
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def pad(matrix, num_of_zeros):
    """
    Pads a 2D matrix by a specified amount around the edges

    Parameters
    ----------
    matrix: list[list[]], required
        The 2D matrix that should be padded
    num_of_zeros: int, required
        The number of zeros that will be padded to the matrix

    Returns
    -------
    paddedArrFin: list[list[]]
        The padded 2D array 
    """
    paddedArrFin = []
    width = len(matrix[0])
    height = len(matrix)
    newDimWidth = width + 2*num_of_zeros
    newDimHeight = height + 2*num_of_zeros
    for i in range(newDimHeight):
        paddedArr = []
        # Padding the top and bottom of the matrix
        if (i < num_of_zeros) or (i >= height + num_of_zeros):
            for j in range(newDimWidth):
                paddedArr.append(0)
        # Padding the rows of the matrix
        else:
            for j in range(newDimWidth):
                if (j < num_of_zeros) or (j >= width + num_of_zeros):
                    paddedArr.append(0)
                else:
                    paddedArr.append(matrix[i - num_of_zeros][j- num_of_zeros])

        paddedArrFin.append(paddedArr)    
    return paddedArrFin

def countX(lst,X):
    """
    Function that counts the number of occurrences of a specific element in an array 

    Paramters
    ---------
    lst: list[], required
        List of values
    X: Any, required
        The value to be counted in the array

    Returns 
    -------
    count: int
        The number of times X occurred
    """
    count = 0
    for element in lst:
        if element == X:
            count += 1
    return count

# Unit Testing
if __name__=="__main__":
 print(pad(
     [[1,1,1,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1],
    [1,1,1,1,1]],
    2 # Number of zeros which should pad the matrix with
 ))
