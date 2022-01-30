import keyboard
import time
from typing import List
from Python.globalVars import DEBUGGING 
from popUpMessage import popupmsg

# TODO: Can add a damping parameter onto the on off controller
# which will allow for less jitter in paddle movement

class keyBoardController:
    
    def __init__(self, xBall, yBall, xPaddlePos, yPaddlePos):
        # Ball position Array
        self.xBall = xBall
        self.yBall = yBall
        # Paddle Position Array
        self.xPaddlePos = xPaddlePos
        self.yPaddlePos = yPaddlePos
            
    def simplistic(self):
        """
        Just moves up and on based on the way direction the ball moves
        """
        if (self.xBall[1] > self.xBall[0]):
            if (self.yBall[1] > self.yBall[0]):
                keyboard.press_and_release("w")
                if DEBUGGING == 1:
                    print("w")
            if self.yBall[1] < self.yBall[0]:
                keyboard.press_and_release("s")
                if DEBUGGING == 1:
                    print("s")   
            if DEBUGGING == 1:
                print(self.yPaddlePos[0])
            
    def relativeSimplistic(self):    
        """
        Keeps track of the ball and keeps track of the position of the 
        paddle relative to the ball.
        Also if the ball is moving away from the paddle it stops moving
        This is essentially on-off control
        """
        keyPushedLeft = "empty"
        keyPushedRight = "empty"
        # if hasattr(self, "_difficulty"): so that it can be used with difficulty setting
        # Set speed that will adjust according to difficulty
        
        # ===================================================== #
        # Left hand Side
        # ===================================================== #
        if (self.xBall[1] > self.xBall[0]):
            if (self.yBall[0] < self.yPaddlePos[0]): # Add later when you move the paddle
                keyboard.press("w")
                time.sleep(0.015)
                keyPushedLeft = "w"
                keyboard.release('w')

            elif (self.yBall[0] > self.yPaddlePos[0]):
                keyboard.press("s")
                time.sleep(0.0015)
                keyPushedLeft = "s"
                keyboard.release('s')

            else:
                if DEBUGGING == 1:
                    print("Wait")
                keyPushedLeft = "x"
            if DEBUGGING == 1:
                print("LHS Paddle Position: ",self.yPaddlePos[0])
                print("LHS Ball Position: ",self.yBall[0])
        else:
            if DEBUGGING == 1:
                print("LHS Stationary")

        # ===================================================== #
        # Right hand Side
        # ===================================================== #
        if (self.xBall[1] < self.xBall[0]):
            if (self.yBall[0] < self.yPaddlePos[0]): # Add later when you move the paddle
                keyboard.press("t")
                time.sleep(0.0015)
                keyPushedRight = "t"
                keyboard.release('t')


            elif (self.yBall[0] > self.yPaddlePos[0]):
                keyboard.press("g")
                time.sleep(0.0015)
                keyPushedRight = "g"
                keyboard.release('g')

            else:
                if DEBUGGING == 1:
                    print("Wait")
                keyPushedRight = "x"

            if DEBUGGING == 1:
                print("RHS Paddle Position: ",self.yPaddlePos[0])
                print("RHS Ball Position: ",self.yBall[0])
        else:
            if DEBUGGING == 1:
                print("RHS Stationary")
                
        return [1,1,1],(keyPushedLeft, keyPushedRight)
    
    def positionPID(self, u:List[float]):
        """
        Variables:
            u: Previous Control Actions (length of 2)
            e: Previous errors (length of 3)
            y_p: the paddle position 
            y_sp: the ball position

        Description:
            PID control Implementation
            Ensure memoryControl is large enough so that the errors
            can be traced back
        """
        keyPushedLeft = "empty"
        keyPushedRight = "empty"

        # Sampling Time
        del_t = 0.1
        K_c = 1
        tau_D = 0.1
        tau_I = 1

        if (self.xBall[1] > self.xBall[0]):
            """
            Depending on the configuration and how the step motors move according to power input
            A velocity form might be better if power is required to move the motor faster or slower
            which I believe it is, the power will then stop when it reaches it's settling point.

            """
            # Error array
            e = []
            # Memory of integral
            k = 2

            # For k
            # Might need to keep track of control actions
            for i in range(3):
                e.append(self.yBall[i] - self.yPaddlePos[i])

            if DEBUGGING == 1:
                print("e",e)
                print("u",u)
            # insert u as the zero-eth control action
            
            # -------------------- Position form of PID -------------------- #
            # u.insert(0, 
            #             u[1] + K_c * (e[1] + (del_t/tau_I) * sum(e[1:k]) + tau_D/del_t * (e[1]-e[2]))
            #         )

            # ------------------- Velocity form of PID --------------------- #
            u.insert(0, 
                        u[1] + K_c * ((e[0] - e[1]) + (del_t/tau_I) * e[0] + tau_D/del_t * (e[0] - 2*e[1] + e[2]))
                    )

            if len(u)>2:
                u.pop(2)

            # Only playing with one player at the moment (PID is not activated here because it is only on off control)
                if u[0]<=0:
                    keyboard.release('s')
                    keyboard.press("w")
                    # time.sleep(0.01)
                    time.sleep(abs(u[0])*10**(-3))
                    keyPushedRight = "w"
                    # keyboard.release('w')
                elif u[0]>0:
                    keyboard.release('w')
                    keyboard.press("s")
                    time.sleep(abs(u[0])*10**(-3))
                    keyPushedRight = "s"
                    # keyboard.release('s')
            return u,(keyPushedLeft, keyPushedRight)
        else:
            return [0,0,0],(keyPushedLeft,keyPushedRight)

    def scoreCheck(self):
        """
        Displays a pop up message showing who scored
        
        """
        # Checking the condition if the ball passes the paddle
        if (self.xBall[1] > self.xBall[0]) and (self.xPaddlePos[0] > self.xBall[0]):
            # scoreRight += 1
            popupmsg("Right Scored")
            
        if (self.xBall[1] < self.xBall[0]) and (self.xPaddlePos[0] < self.xBall[0]):
            # scoreLeft += 1
            popupmsg("Left Scored")