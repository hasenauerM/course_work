import numpy as np
import modern_robotics as mr

#max hasenauer
#code can be run from any terminal with python installed

#imported parameters describing the UR5
M01 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0.089159], [0, 0, 0, 1]]
M12 = [[0, 0, 1, 0.28], [0, 1, 0, 0.13585], [-1, 0, 0, 0], [0, 0, 0, 1]]
M23 = [[1, 0, 0, 0], [0, 1, 0, -0.1197], [0, 0, 1, 0.395], [0, 0, 0, 1]]
M34 = [[0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0.14225], [0, 0, 0, 1]]
M45 = [[1, 0, 0, 0], [0, 1, 0, 0.093], [0, 0, 1, 0], [0, 0, 0, 1]]
M56 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0.09465], [0, 0, 0, 1]]
M67 = [[1, 0, 0, 0], [0, 0, 1, 0.0823], [0, -1, 0, 0], [0, 0, 0, 1]]
G1 = np.diag([0.010267495893, 0.010267495893,  0.00666, 3.7, 3.7, 3.7])
G2 = np.diag([0.22689067591, 0.22689067591, 0.0151074, 8.393, 8.393, 8.393])
G3 = np.diag([0.049443313556, 0.049443313556, 0.004095, 2.275, 2.275, 2.275])
G4 = np.diag([0.111172755531, 0.111172755531, 0.21942, 1.219, 1.219, 1.219])
G5 = np.diag([0.111172755531, 0.111172755531, 0.21942, 1.219, 1.219, 1.219])
G6 = np.diag([0.0171364731454, 0.0171364731454, 0.033822, 0.1879, 0.1879, 0.1879])
Glist = [G1, G2, G3, G4, G5, G6]
Mlist = [M01, M12, M23, M34, M45, M56, M67] 
Slist = [[0,         0,         0,         0,        0,        0],
         [0,         1,         1,         1,        0,        1],
         [1,         0,         0,         0,       -1,        0],
         [0, -0.089159, -0.089159, -0.089159, -0.10915, 0.005491],
         [0,         0,         0,         0,  0.81725,        0],
         [0,         0,     0.425,   0.81725,        0,  0.81725]]

#additional parameters for the simulations, starting thetas ftip, tau, g, dt, intRes         
theta1 = [0, 0, 0, 0, 0, 0]
theta2 = [0, -1, 0, 0, 0, 0]
dtheta = [0, 0, 0, 0, 0, 0]
ddtheta = [0, 0, 0, 0, 0 ,0]
taumat1 = np.zeros((30,6))
taumat2 = np.zeros((50,6))
Ftip1 = np.zeros((300,6))
Ftip2 = np.zeros((500,6))
g = [0, 0, -9.81]
dt = 0.1
intRes = 100

#Forward dynamics trajectories

#sim 1 falling from zero position for 3 seconds
thetamat1, dthetamat1 = mr.ForwardDynamicsTrajectory(theta1, dtheta, taumat1, g, Ftip1, Mlist, Glist, Slist, dt, intRes)

#sim 2 robot falling from configuration where all joints are at their zero position, except for joint 2, which is at -1 radian for 5 seconds
thetamat2, dthetamat2 = mr.ForwardDynamicsTrajectory(theta2, dtheta, taumat2, g, Ftip2, Mlist, Glist, Slist, dt, intRes)

#print(thetamat1)
#print(thetamat2)

#makes to csv files one for each sim
np.savetxt("simulation1.csv", thetamat1, delimiter=",")
np.savetxt("simulation2.csv", thetamat2, delimiter=",")