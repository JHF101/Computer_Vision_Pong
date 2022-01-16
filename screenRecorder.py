import numpy as np
from PIL import ImageGrab

def screenRecord(w, h):
    """
    Screen recording function that returns the same outputs as
    the cap.read() OpenCV function.

    Parameters
    ----------
    w: int, required
        Width of the screen
    h: int, required
        Height of the screen

    Returns
    -------
    True, and the recorded image of the screen
    """
    img = ImageGrab.grab(bbox=(0, 0, w, h)) #x, y, w, h
    img_np = np.array(img)
    return True, img_np