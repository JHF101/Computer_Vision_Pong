from moments import moments
import cv2

"""
This script was a test to see if we could use connected component labelling as 
an alternative to detect the ball and the paddles alike.

It would be possible to do this with an implementation like YACCLAB:
https://github.com/prittt/YACCLAB

It would possibly be one of the fastest ways to detect and handle all of the 
components.
"""

def connected_component_label(I):
    """
    The connected component labelling function done in OpenCV

    Parameters
    ----------
    I : list[list[]], required
        The 2D matrix (Image)
    
    Returns
    -------
    listOfDataPoints : list[list[]]
        The datapoints of the different connect componets in the image
    """
    # Getting the input image
    img = I
    img = cv2.resize(img, (640,360), fx=0, fy=0, interpolation = cv2.INTER_LINEAR)
    # Applying cv2.connectedComponents() 
    num_labels, labels = cv2.connectedComponents(img)

    pointInformation = (cv2.connectedComponents(img)[1])
    # We know in this case that there will only be three elements in the frame
    listOfDataPoints = [
        [],
        [],
        [],
    ]
    # Sweep to find information about the points
    for y in range(len(pointInformation)):
        for x in range(len(pointInformation[0])):
            if pointInformation[y][x]!=0:
                if pointInformation[y][x] == 1:
                    listOfDataPoints[0].append([x,y])
                if pointInformation[y][x] == 2:
                    listOfDataPoints[1].append([x,y])
                if pointInformation[y][x] == 3:
                    listOfDataPoints[2].append([x,y])

    return listOfDataPoints

# Unit Testing
if __name__=="__main__":
    from approxPolyDP import rdp
    from globalVars import openCVImp, firstPrincipleImp
    cap = cv2.VideoCapture('PONGTest1.mp4')

    while cap.isOpened():

        ret, frame = cap.read()

        if ret == True:
            frame = cv2.resize(frame, (640,360), fx=0, fy=0, interpolation = cv2.INTER_LINEAR) 

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        conComp = connected_component_label(gray)

        # Accessing the
        connected0 = conComp[0]
        connected1 = conComp[1]
        connected2 = conComp[2]

        # Displays the right side paddle coordinates
        m00, m01, m10 = moments(connected0)
        
        cX = int(m10 / m00)
        cY = int(m01 / m00)

        print("Right Paddle: \n",cX, cY)
        
        # Displays the left side paddle coordinates
        m00, m01, m10 = moments(connected1)
        
        cX = int(m10 / m00)
        cY = int(m01 / m00)

        print("Left Paddle: \n ",cX, cY)

        # Displays the ball coordinates
        m00, m01, m10 = moments(connected2)
        
        cX = int(m10 / m00)
        cY = int(m01 / m00)

        print("Ball Coordinates: \n",cX, cY)

        cv2.imshow("frame",gray)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
        
    cv2.destroyAllWindows()


