from comparison import imgPlotter
from globalVars import firstPrinciplePlotting

def resize(I, decimation=3):
    """
    Resized image function that returns a downscaled image (Simplistic)

    Parameters
    ----------
    I : int, required
        The image that must be downscaled
    
    decimation : int, default = 3
        The amount of decimation that happens on an image

    Returns
    -------
    resizedImage : list[list[int]]
        The resized image
    """
    resizedImage = []
    width = len(I[0])
    height = len(I)
    for y in range(0,height,decimation):
        rowVec = []
        for x in range(0,width,decimation):
            rowVec.append(I[y][x])
        resizedImage.append(rowVec)
    
    if firstPrinciplePlotting:
        imgPlotter(resizedImage)

    return resizedImage