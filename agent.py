# CSCI 561 USC Fall 2013
# Homework 1 Part 2 Problem 1
# Skeleton Code Written by Toy Leksut 08/30/13
# Assignment Done by [yxu336]

import Myro
from Myro import *
from Graphics import *
from math import *

width, height = 510, 300
sim = Simulation("Parking Structure", width, height, Color("lightgrey"))

# Add walls
wallLength = 100
for i in xrange(10, 510, 120):
    sim.addWall((i, 10), (i+10, 10+wallLength), Color("black"))
    sim.addWall((i, 200), (i+10, 200+wallLength), Color("black"))

# Add boundaries
sim.addWall((0, 0), (width, 10), Color("blue"))
sim.addWall((0, 0), (10, height), Color("blue"))
sim.addWall((width - 10, 0), (width, height), Color("blue"))
sim.addWall((0, height - 10), (width, height), Color("blue"))

# Add Goal
sim.addWall((30, 30), (120, 40), Color("red"))

# Set up simulation
sim.setup()
robot = makeRobot("SimScribbler", sim)


# +++++++++++++++++++++++++++++++++++++++++
# ----------      AGENTS       ------------
# +++++++++++++++++++++++++++++++++++++++++

class Agent(object):
    def useJoystick(self):
        return False
    def act(self, pic):
        return False

class UserControlAgent(Agent):
    def useJoystick(self):
        return True
    def act(self, pic):
        pix = getRed(getPixel(pic, getWidth(pic)/2, getHeight(pic)/2))
        if pix > 0:
            robot.translate(1)

class SimpleReflexAgent(Agent):
    def act(self, pic):
        # Only cares about red pixel in the center of the image
        pix = getRed(getPixel(pic, getWidth(pic)/2, getHeight(pic)/2))
        if pix > 0:
            robot.translate(1)
        else:
            robot.backward(1, randomNumber())
            robot.turnLeft(2, 1+randomNumber())
            robot.forward(1, 2+randomNumber())
        return False


# To do:
# Implement all the agents (Model-based, Utility-based, Goal-based)

# Agent 1: Model-based
class ModelBasedAgent(Agent):
    def __init__(self):
        self.previous_location = getLocation()

    def blocked(self):
    #check if is blocked by a wall
        present_location = getLocation()
        dist = (pow(self.previous_location[0] - present_location[0], 2) +
             pow(self.previous_location[1] - present_location[1], 2))
        self.previous_location = present_location
        if dist < 15.0:
            return True
        else:
            return False

    def act(self, pic):
        pix = getRed(getPixel(pic, getWidth(pic) / 2, getHeight(pic) / 2))
        if pix > 0:
            robot.translate(1)
        else:
            if self.blocked():
                print('Blocked')
                robot.backward(1, randomNumber())
                robot.turnLeft(2, 1 + randomNumber())
                robot.forward(1, 2 + randomNumber())
            else:
                robot.forward(1, 2 + randomNumber())
        return False;


# Agent 2: Utility-based method 1
class UtilityBasedAgent1(Agent):
    def __init__(self):
        self.previous_location = getLocation()
        self.goal_location = [75, 40]

    def blocked(self):
        present_location = getLocation()
        dist = (pow(self.previous_location[0] - present_location[0], 2) +
                pow(self.previous_location[1] - present_location[1], 2))
        self.previous_location = present_location
        if dist < 15.0:
            print('Blocked')
            return True
        else:
            return False

    def calx(self, p1, p2):
        return p1[0]-p2[0]

    def caly(self, p1, p2):
        return p1[1]-p2[1]

    def getxOrien(self, ydist):
        theta = getAngle()%360
        robot.forward(1,1)
        if self.blocked():
            robot.backward(1,0.5)
            if ydist > 0:
                robot.turnTo((theta+90)%360,"deg")
                robot.forward(1,0.8)
                if self.blocked():
                   robot.backward(1,0.5)
                   robot.turnTo((theta+180)%360, "deg")
                   robot.forward(1,0.8)
                   if self.blocked():
                       robot.backward(1,0.5)
                       robot.turnTo((theta-90)%360, "deg")
                       robot.forward(1,0.8)
            else:
                robot.turnTo((theta-90)%360,"deg")
                robot.forward(1,0.8)
                if self.blocked():
                    robot.backward(1,0.5)
                    robot.turnTo((theta+180)%360, "deg")
                    robot.forward(1,0.8)
                    if self.blocked():
                        robot.backward(1,0.5)
                        robot.turnTo((theta+90)%360, "deg")
                        robot.forward(1,0.8)

    def getyOrien(self, xdist):
        theta = getAngle()%360
        robot.forward(1,1)
        if self.blocked():
            robot.backward(1,0.5)
            if ydist < 0:
                robot.turnTo((theta+90)%360,"deg")
                robot.forward(1,0.5)
                if self.blocked():
                   robot.backward(1,0.5)
                   robot.turnTo((theta+180)%360, "deg")
                   robot.forward(1,0.8)
                   if self.blocked():
                       robot.backward(1,0.5)
                       robot.turnTo((theta-90)%360, "deg")
                       robot.forward(1,0.8)
            else:
                robot.turnTo((theta-90)%360,"deg")
                robot.forward(1,0.8)
                if self.blocked():
                    robot.backward(1,0.5)
                    robot.turnTo((theta+180)%360, "deg")
                    robot.forward(1,0.8)
                    if self.blocked():
                        robot.backward(1,0.5)
                        robot.turnTo((theta+90)%360, "deg")
                        robot.forward(1,0.8)

    def act(self, pic):
        pix = getRed(getPixel(pic, getWidth(pic)/2, getHeight(pic)/2))
        present_location = getLocation()
        if pix > 0:
            robot.translate(1)
            if self.blocked():
            #goal test: if is hitting the red wall
                print('Goal reached')
        else:
            x = self.calx(present_location, self.goal_location)
            y = self.caly(present_location, self.goal_location)
            if x > 45:
                robot.turnTo(180, "deg")
                self.getxOrien(y)
            elif x < -45:
                self.getxOrien(y)
            else:
                if y >= 0:
                    robot.turnTo(270,"deg")
                    self.getyOrien(x)
                else:
                    robot.turnTo(90, "deg")
                    self.getyOrien(x)
        return False;

# Agent 2: Utility-based method 2
class UtilityBasedAgent2(Agent):
    def __init__(self):
        self.previous_location = getLocation()
        self.goal_location = [60, 120]

    def blocked(self):
    #check if is blocked by a wall
        present_location = getLocation()
        dist = (pow(self.previous_location[0] - present_location[0], 2) +
                pow(self.previous_location[1] - present_location[1], 2))
        self.previous_location = present_location
        if dist < 15.0:
            return True
        else:
            return False

    def calDist(self, p1, p2):
    #calculate the distance between two location
        x = p1[0] - p2[0]
        y = p1[1] - p2[1]
        return sqrt(x * x + y * y)

    def astarTurn(self, alist):
    #using A* algorithm to get the non-blocking optimal direction
        min_dist = 10000000
        opt_theta = 0
        radius = 20
        PI = acos(-1.0)
        present_location = getLocation()
        for theta in range(0, 359, 90):
            if not (theta in alist):
                future_location = [present_location[0] + radius * cos(theta / 180.0 * PI),
                         present_location[1] + radius * sin(theta / 180.0 * PI)]
                dist = self.calDist(self.goal_location, future_location)
                if dist < min_dist:
                    min_dist = dist
                    opt_theta = theta
        return opt_theta

    def act(self, pic):
        present_location = getLocation()
        alist = []
        pix = getRed(getPixel(pic, getWidth(pic) / 2, getHeight(pic) / 2))
        print("red pix: ",pix)
        if pix > 0:
        #goal test: if is hitting the red wall
            robot.translate(1)
            if self.blocked():
                print("Goal reached")
        else:
            opt_theta = self.astarTurn(alist)
            #get the current optimal direction
            print("optimal direction: ", opt_theta)
            robot.turnTo(opt_theta, "deg")
            robot.forward(1,1)
            if getObstacle('center')>180:
            #if the robot is blocked
                theta = opt_theta
                print('Blocked')
                alist.append(theta)
                #insert the blocked direction into the blocking list
                robot.backward(1, 0.5)
                for i in range(0, 3, 1):
                    robot.turnBy(90, "deg")
                    #turn to other 3 directions
                    theta = (theta+90)%360
                    if getObstacle('center')>4000:
                    #if these directions have walla ahead, add to the blocking list
                        alist.append(theta)
                opt_theta = self.astarTurn(alist)
                print('optimal direction: ', opt_theta)
                robot.turnTo(opt_theta, "deg")
                robot.forward(1,0.8)
        return False;

# Agent 3: Goal-based
class GoalBasedAgent(Agent):
    def __init__(self):
        self.previous_location = getLocation()
        self.goal_location = [75, 35]

    def blocked(self):
    #check if is blocked by a wall
        present_location = getLocation()
        dist = (pow(self.previous_location[0] - present_location[0], 2) +
                pow(self.previous_location[1] - present_location[1], 2))
        self.previous_location = present_location
        if dist < 15.0:
          return True
        else:
          return False

    def calx(self, p1, p2):
    #calculate the differece of x-coordinate between two position
        return p1[0]-p2[0]

    def caly(self, p1, p2):
    #calculate the difference of y-coordinate between two position
        return p1[1]-p2[1]

    def getOrien(self):
    #robot turn right if is blocked
        robot.forward(1,1)
        if self.blocked():
            print('Blocked')
            robot.backward(1,0.5)
            robot.turnBy(90, "deg")
            robot.forward(1, 0.8)

    def act(self, pic):
        pix = getRed(getPixel(pic, getWidth(pic)/2, getHeight(pic)/2))
        present_location = getLocation()
        if self.blocked() and pix > 0:
        #goal test: if it is hitting the red wall
            print('Goal reached')
            robot.translate(1)
        else:
            x = self.calx(present_location, self.goal_location)
            y = self.caly(present_location, self.goal_location)
            if x > 30:
            #getting close from x-coordinate
                robot.turnTo(180, "deg")
                self.getOrien()
            elif x < -30:
            #getting close from x-coordinate
                robot.turnTo(0,"deg")
                self.getOrien()
            else:
            #x-coordinate reach the goal range
                if y >= 0:
                #geting close from y-coordinate
                    robot.turnTo(270,"deg")
                    self.getOrien()
                else:
                #getting close from y-coordinate
                    robot.turnTo(90, "deg")
                    self.getOrien()
        return False;


# +++++++++++++++++++++++++++++++++++++++++

#agent = UserControlAgent()
#agent = SimpleReflexAgent()
#agent = ModelBasedAgent()
#agent = UtilityBasedAgent1()
agent = UtilityBasedAgent2()
#agent = GoalBasedAgent()

if agent.useJoystick(): joystick()

while True:
    # Feed video stream to the agent
    pic = takePicture()
    show(pic)
    agent.act(pic)
