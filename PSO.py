import random
import math
import matplotlib.pyplot as pyplot
import numpy as np



def Sphere(X):
    return sum([(x ** 2) for x in X])


def Rastrigin(X):
    A = 10
    return A + sum([(x ** 2 - A * np.cos(2 * math.pi * x)) for x in X])


def StyblinskiTang(X):
    return sum([(x ** 4 - 16 * x ** 2 + 5 * x) for x in X]) / 2


def Rosenbrock(X):
    return sum([(100*(x+1 - x**2)**2) for x in X])


def randVarSize():  # get a vector of size==nVar
    tmpList = []
    for tmp in range(Dimensions):
        tmpList.append(random.random())
    return tmpList


class Best:
    def __init__(self):
        self.Position = []
        self.Cost = math.inf


class Particle:
    def __init__(self):
        self.Position = []
        self.Velocity = []
        self.Cost = math.inf
        self.LocalBest = Best()

        for i in range(Dimensions):  #
            self.Position.append(random.uniform(lowerBound, upperBound))
            self.Velocity.append(random.uniform(-1, 1))
            self.LocalBest.Position.append(self.Position[i])
        self.Cost = Function(self.Position)

    # End __init__

    def update(self):
        global GlobalBest
        # Update Velocity
        for i in range(Dimensions):
            r1 = random.random()
            r2 = random.random()
            Inertia = w * self.Velocity[i]
            cognitiveComponent = c1 * r1 * (self.LocalBest.Position[i] - self.Position[i])
            socialComponent = c2 * r2 * (GlobalBest.Position[i] - self.Position[i])
            self.Velocity[i] = Inertia + cognitiveComponent + socialComponent


        # Apply Velocity limits
        for i in range(Dimensions):
            self.Velocity[i] = max(self.Velocity[i], MinVelocity)
            self.Velocity[i] = min(self.Velocity[i], MaxVelocity)
        # Update Position
        for i in range(Dimensions):
            self.Position[i] = self.Position[i] + self.Velocity[i]
        # Apply Bound Limits
        for i in range(Dimensions):
            self.Position[i] = max(self.Position[i], lowerBound)
            self.Position[i] = min(self.Position[i], upperBound)
        # Evaluation
        self.Cost = Function(self.Position)
        # Update Personal Best
        if self.Cost < self.LocalBest.Cost:
            self.LocalBest.Cost = self.Cost
            self.LocalBest.Position = self.Position.copy()

        # Update Global Best
        if self.LocalBest.Cost < GlobalBest.Cost:
            GlobalBest.Cost = self.Cost

    # End update

# End Particle

#
# pick one of these functions
# Sphere Rastrigin StyblinskiTang Rosenbrock
Function = Sphere
Dimensions = 2
lowerBound = -5  # lower bound
upperBound = 5  # upper bound
allowPrint = False

# Clerc & Kennedy Constriction Coefficients
# Chi = 2 * kappa / abs( 2 -phi - sqrt(phi^2 - 4phi)
# 0 <= kappa <= 1
# phi = phi1 + phi2 >= 4
############################################
# w = chi
# c1 = chi * phi1
# c2 = chi * phi2
# wdamp = 1
kappa = 1
phi1 = 2.05
phi2 = 2.05
phi = phi1 + phi2
chi = 2 * kappa / abs(2 - phi - math.sqrt(phi ** 2 - 4 * phi))

population = 50
iterations = 50
w = chi  # inertia coefficient
wdamp = 1  # Damping Ratio of Inertia coefficient
c1 = chi * phi1  # cognitive coefficient
c2 = chi * phi2  # social coefficient

MaxVelocity = 0.4 * (upperBound - lowerBound)
MinVelocity = MaxVelocity * -1

GlobalBest = Best()
BestCosts = []
# Create particle pop
swarm = []
for i in range(population):
    swarm.append(Particle())
    if swarm[i].LocalBest.Cost < GlobalBest.Cost or GlobalBest.Cost == math.inf:
        GlobalBest.Cost = swarm[i].LocalBest.Cost
        GlobalBest.Position = swarm[i].LocalBest.Position.copy()

# Main Loop
out = ""
for i in range(iterations):
    out = out + ("iteration: {}\n".format(i))
    for j in range(population):
        out = out + ("particle: {} ".format(j))
        swarm[j].update()
        for pos in swarm[j].Position:
            out = out + str(pos)
            out = out + " "
        out = out + "Cost = "
        out = out + str(swarm[j].Cost)
        out = out + "\n"
        
    BestCosts.append(GlobalBest.Cost)
    if allowPrint:
        print("""Iteration {}: Best Cost = {}""".format(i, BestCosts[i]))
    w = w * wdamp
out = out + "\n\nBest Cost: {}\nAt position: {}".format(GlobalBest.Cost, GlobalBest.Position)
f = open("output.txt","w")
f.write(out)
f.close()
# Result
print("Final Best Cost is: {}\nAt position: {}".format(GlobalBest.Cost, GlobalBest.Position))
pyplot.plot(BestCosts)
pyplot.xlabel('iteration')
pyplot.ylabel('cost')
pyplot.show()

