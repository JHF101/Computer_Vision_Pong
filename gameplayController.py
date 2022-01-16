from circleDetection import paddleDetectors
from moments import moments
import cv2
import imutils
from globalVars import DEBUGGING, openCVImp, firstPrincipleImp, firstPrinciplePlotting
from motorController import keyBoardController
from objectDetector import ShapeDetector
import numpy as np

"""
The difficulty is a scalar multiplier that will cause the paddle to approach it's target
destination more aggressively

Paramters of interest:
y-coordinate, this will determine the height of the paddle
posArr - the array that can be used for advanced
"""

def paddleMovement(xCoords, yCoords, 
                   xPaddle, yPaddle, 
                   frame, 
                   u,                       # Control Action
                   memControl=3,
                   method = 2):
    """
    1. Need to get the position the paddle is currently
    2. Control
        * Method 1: Simple Control 
            Using simple control to to check the required y position and continue to move to that direction
            until it reaches that destination
             - https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
        * Method 2: Control System Method
            After that we need to be able to approach that system using a control systems equation 

        * Method 3: Prediction Method with Control System
            Using vectors to predict the position of the ball based off of reflections in the environment
    3. Difficulty to how fast it can move
    """
   
    if (method==1):
        print("Gameplay Controller")
        # Catch condition for return variables
        btest = True

        image = frame
        # find contours in the thresholded image and initialize the shape detector
        # CV_RETR_EXTERNAL gives "outer" contours, so if you have (say) one contour enclosing another (like concentric circles), only the outermost is given.
        if DEBUGGING == 1:
            print(image)

        # cv2.imshow(np.array(image))
        cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if DEBUGGING == 1:
            print("Finding contours in image (cnts)")
            print(cnts)

        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        sd = ShapeDetector() 
        for c in cnts:
            if openCVImp:
                # compute the center of the contour
                M = cv2.moments(c)
                # This is calculating the coordinates of the centroid
                if M["m00"] != 0:
                    cX = int((M["m10"] / M["m00"]))
                    cY = int((M["m01"] / M["m00"]))
                else:
                    # Catch Condition to prevent zero division error
                    cX = 0
                    cY = 0
                print("CV2 moments x",cX)
                print("CV2 moments y",cY)
             
            if firstPrincipleImp:
                # --- The paddle detecting algorithm is not very good
                # c = paddleDetectors(frame)
                cArr = []
                for i in range(len(c)):
                    cArr.append(c[i][0])
                
                # Using the find contours method from OpenCV because it just works
                m00, m01, m10 = moments(cArr) #TODO: Change to frame

                if m00 != 0:
                    cX = int(m10 / m00)
                    # Technically we are just interested in cY because it tells us the position 
                    # of the paddle, cX is only used to determine if the region of operation is 
                    # correct
                    cY = int(m01 / m00)    
                else:
                    # Catch Condition to prevent zero division error
                    cX = 0
                    cY = 0
                if firstPrinciplePlotting:
                    print("Paddle coordinates according to adapted hough transform method",c)
                    print("Fist Principle Paddle coordinates", cX, cY)
                
            # Checking if the paddle lies on the left hand or right side
            if (cX < 60 and xCoords[1] > xCoords[0]) or (cX > 580 and xCoords[1] < xCoords[0]): # can extend it to be for paddle on the other side too
                shape = sd.detect(c)
                # Checking that the detected shape is a rectangle
                if shape == "rectangle":
                    # then draw the contours and the name of the shape on the image
                    c = c.astype("int")

                    xPaddle.insert(0, cX)
                    yPaddle.insert(0, cY)

                    kb = keyBoardController(xBall = xCoords,
                                            yBall = yCoords,
                                            xPaddlePos = xPaddle,
                                            yPaddlePos = yPaddle) 
                    
                    # --- Used to manage which controller is used
                    u_out,(keyPushedLeft, keyPushedRight) = kb.relativeSimplistic()
                    # u_out,(keyPushedLeft, keyPushedRight) = kb.positionPID(u)

                    # if type(u_out) is None:
                    #     raise Exception("Control is empty")
                    # else:
                    #     pass

                    if len(yPaddle)>memControl or len(xPaddle)>memControl:
                        yPaddle.pop(len(yPaddle)-1)
                        xPaddle.pop(len(xPaddle)-1)
                    
                    kb.scoreCheck()

                    """
                    Debugging Functions that allow you to see the position of the ball and paddle
                    """
                    # Ball Position
                    cv2.putText(image,                    # image on which the writing can be placed
                                "y:"+str(yCoords[0]),     # text
                                (xCoords[0], yCoords[0]), # position of writing
                                cv2.FONT_HERSHEY_SIMPLEX, # font family
                                0.5,                      # font size
                                (100, 80, 0, 255),        # font color
                                2)                        # font stroke
                    
                    # Current Paddle Position
                    cv2.putText(image,                    # image on which the writing can be placed
                                "Paddle:"+str(cY),        # text
                                (330, 25),                # position of writing
                                cv2.FONT_HERSHEY_SIMPLEX, # font family
                                0.5,                      # font size
                                (209, 10, 0, 255),        # font color
                                2)                        # font stroke

                    # Displaying Keypresses
                    cv2.putText(image,                    # image on which the writing can be placed
                                keyPushedLeft,            # text
                                (25, 25),                 # position of writing
                                cv2.FONT_HERSHEY_SIMPLEX, # font family
                                0.5,                      # font size
                                (209, 10, 0, 255),        # font color
                                2)                        # font stroke

                    cv2.putText(image,                    # image on which the writing can be placed
                                keyPushedRight,           # text
                                (580, 25),                # position of writing
                                cv2.FONT_HERSHEY_SIMPLEX, # font family
                                0.5,                      # font size
                                (209, 10, 0, 255),        # font color
                                2)                        # font stroke

                    # Displaying Control Action
                    cv2.putText(image,                    # image on which the writing can be placed
                                "Control:"+str(u_out[0]), # text
                                (80, 25),                 # position of writing
                                cv2.FONT_HERSHEY_SIMPLEX, # font family
                                0.5,                      # font size
                                (209, 10, 0, 255),        # font color
                                2)                        # font stroke            
                    # ==================================================================================== #  

                    # show the output image
                    cv2.imshow("Image", image)

                    return xPaddle, yPaddle, u_out
            else:
                # This is a catch condition to ensure that something is always being returned
                btest = False

        if btest == False:
            return xPaddle, yPaddle, u
    
    # --------------------------------------------------------------------------------------------------- #
    #           Using first principles Only to determine the position of the paddle
    # --------------------------------------------------------------------------------------------------- #
    if (method==2):
        print("Gameplay Controller Method 2")
        # Catch condition for return variables
        btest = True

        image = frame
 
        # Calculate the moment of the left hand side of the screen as a test
        c = paddleDetectors(frame) # This is technically just going to look at the LHS

        cArr = []
        for i in range(len(c)):
            cArr.append(c[i][0])
        m00, m01, m10 = moments(cArr) #TODO: Change to frame

        if m00 != 0:
            cX = int(m10 / m00)
            # Technically we are just interested in cY because it tells us the position 
            # of the paddle, cX is only used to determine if the region of operation is 
            # correct
            cY = int(m01 / m00)    
        else:
            # Catch Condition to prevent zero division error
            cX = 0
            cY = 0
            
        if DEBUGGING == 1:
            print("Paddle coordinates according to adapted hough transform method",c)
            print("Fist Principle Paddle coordinates", cX, cY)
            print("xCooords",xCoords)
            print("xCooords",yCoords)

        # Checking if the paddle lies on the left hand side
        if (cX < 60 and xCoords[1] > xCoords[0]):
            # Checking that the detected shape is a rectangle
            if len(c) == 4: # then it is infact a rectangle
                xPaddle.insert(0, cX)
                yPaddle.insert(0, cY)

                kb = keyBoardController(xBall = xCoords,
                                        yBall = yCoords,
                                        xPaddlePos = xPaddle,
                                        yPaddlePos = yPaddle) 
                            
                u_out,(keyPushedLeft, keyPushedRight) = kb.relativeSimplistic()
                # u_out,(keyPushedLeft, keyPushedRight) = kb.positionPID(u)

                # if type(u_out) is None:
                #     raise Exception("Control is empty")
                # else:
                #     pass

                if len(yPaddle)>memControl or len(xPaddle)>memControl:
                    yPaddle.pop(len(yPaddle)-1)
                    xPaddle.pop(len(xPaddle)-1)
                
                kb.scoreCheck()

                return xPaddle, yPaddle, u_out
        else:
            # This is a catch condition to ensure that something is always being returned
            btest = False
            return xCoords[0], yCoords[0], 0

    # Catch condition to prevent program crash
    if btest == False:
        return xPaddle, yPaddle, u

