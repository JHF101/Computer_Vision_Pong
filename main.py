from turtle import circle
from textfileReader import writeTextfile
from circleDetection import HoughCircles
from gaussianBlur import GaussianBlur
from colourConversion import cvtColour
import cv2
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import time
from gameplayController import paddleMovement
from screenRecorder import screenRecord
from histogram import Histogrammer
# from colourConversion import cvtColor
import matplotlib.pyplot as pyplot
from resizer import resize
from globalVars import DEBUGGING, openCVImp, firstPrincipleImp, TIME_DEBUGGING

# Testing Functions
import comparison

"""
Just a note about arrays
The news value is inserted first
e.g.
    x[0]=new
    x[1]=older
    x[2]=oldest

"""

# Previous ball positions
ballX = [0,0,0]
ballY = [0,0,0]

# Previous Paddle Positions
paddlePosX = [0,0,0]
paddlePosY = [0,0,0]

# Previous Control Actions
u_in = [0,0,0]

memoryControl = 3

time_arr = []

# Keeping track of the circle
prevX = None
prevY = None

"""
    Use the following combinations for different input sources:
    chooseStream =
        1) Webcam Stream
        2) Video Stream
        3) Image Read
        4) Screen Record
"""

chooseStream = 1

if chooseStream == 0:
    cap = cv2.VideoCapture(0)
    streamVar = cap.isOpened()
elif chooseStream == 1:
    cap = cv2.VideoCapture('PONGTest1.mp4')
    streamVar = cap.isOpened()
elif chooseStream == 2:
    frame = cv2.imread('test.jpg')
    streamVar = True
elif chooseStream == 3:
    print("Screen Recording")
    streamVar = True

while streamVar:

# while True:
    if  TIME_DEBUGGING == 1:
        start_time = time.time()
    
    if (chooseStream == 0) or (chooseStream == 1):
        ret, frame = cap.read()
    if chooseStream == 2:
        ret = True 
    if chooseStream == 3:
        ret, frame = screenRecord(1920, 1080)


    if ret == True:
        if openCVImp:
            # --- INTER_LINEAR is faster version of interpolation
            frame = cv2.resize(frame, (640,360), fx=0, fy=0, interpolation = cv2.INTER_LINEAR) # Fastest
            # frame = cv2.resize(frame, (640,360), fx=0, fy=0, interpolation = cv2.THRESH_BINARY) # 2nd Fastest
            # frame = cv2.resize(frame, (640,360), fx=0, fy=0, interpolation = cv2.INTER_AREA) # Slowest

            if DEBUGGING == 1:
                print("")
                print(frame)

        if firstPrincipleImp:
            frame = resize(frame,3)

    if ret is False:
        break
    # ============================================================== #
    #            Applying filtering and Thresholding                 #
    # ============================================================== #
    if openCVImp:
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (3,3), 0)
        
    if firstPrincipleImp:
        # Exact results as OpenCV
        gray = cvtColour(frame)
        gray = GaussianBlur(gray, (3,3), -1)
        

        
    
    """ 
    # Adaptive Thresholding is way too slow
        This method is not good for our application
    grayScaleInput = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(grayScaleInput, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    """

    # Histogram function here
    # Histogrammer(gray)

    # ============================================================== #
    #            Detecting Circles in an image                       #
    # ============================================================== #
    if openCVImp:
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
        if DEBUGGING == 1:
            print("Circles OpenCV")
            print(circles)

    if firstPrincipleImp:
        # Hough circle calculation help - https://www.codingame.com/playgrounds/38470/how-to-detect-circles-in-images 
        # TODO: Try this
        # https://stackoverflow.com/questions/27245352/what-is-the-best-way-to-parallelize-hough-transform-algorithm?rq=1 

        circles = HoughCircles(gray, radius = 20, prevX = prevX, prevY = prevY)
        if DEBUGGING == 1:
            print("Circles First Principles")
            print(circles)

    
    # Check Condition to ensure correct processing
    if firstPrincipleImp:
        if circles[0][0] is not None:
            circleCheck = True
        else:
            circleCheck = False
    if openCVImp:
        if circles is not None:
            circleCheck = True
        else:
            circleCheck = False
    
    if circleCheck:
        boolNumOfCircles = False
        # Ensure at least some circles were found
        if openCVImp:
            circles = np.uint16(np.around(circles))
            if len(circles[0]) == 1:
                # Only care about one circle
                boolNumOfCircles = True
                circularOutput = circles[0,:]

        if firstPrincipleImp:
            prevX = circles[0][0]
            prevY = circles[0][1]
            print("Length of circles", len(circles))
            if len(circles)==1: # Means that only one circle was detected
                boolNumOfCircles = True
                circularOutput = circles
                # print(circularOutput)

        if boolNumOfCircles == True:
            for i in circularOutput:
                print("Coordinates of the centre of the ball:", i)
                # draw the outer circle
                # cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                # cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)

                # These are the coordinates from the circle, the processing should be based off of this
                ballX.insert(0, i[0])
                ballY.insert(0, i[1])
                print("Ball X",ballX)
                print("Ball Y",ballY)
                paddlePosX, paddlePosY, u_in = paddleMovement( xCoords = ballX,
                                                               yCoords = ballY,
                                                               xPaddle = paddlePosX,
                                                               yPaddle = paddlePosY,
                                                               frame = gray, 
                                                               u = u_in,
                                                               method = 1)

                if len(ballX)>memoryControl or len(ballY)>memoryControl:
                    ballX.pop(len(ballX)-1)
                    ballY.pop(len(ballX)-1)
    else:
        print("This is the catch condition, no circles are detected so do something about it!(call openCV function)")
        # circles = HoughCircles(gray, radius = 20, prevX = None, prevY = None)

    # Write a sample image to textfile
    # fil = open('file.txt', 'w')
    # pixel = gray
    # row, column = len(gray[0]), len(gray)
    # for y in range(column):
    #     pix = []
    #     for x in range(row):
    #         pix.append(pixel[y][x])
    #     fil.write(str(pix))
    #     fil.write('\n')
    # fil.close()

    # Uncomment to display what is being seen 
    # cv2.imshow('frame',frame)
    
    # Measuring the time of an execution loop
    if TIME_DEBUGGING == 1:
        print("--- %s seconds for entire execution ---" % (time.time() - start_time))
        time_arr.append((time.time() - start_time))
    
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
    
cv2.destroyAllWindows()
