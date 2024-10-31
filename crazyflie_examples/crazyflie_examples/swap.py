#!/usr/bin/env python

from crazyflie_py import Crazyswarm
import numpy as np


def main():
    # Id2 = 231
    # Id1 = 5
    Pos1 = np.array([0.0, -0.2, 0.0])
    Pos2 = np.array([0.0, 0.2, 0.0])
    Height1 = 1.0
    Height2 = 1.0
    swapTime = 3

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.crazyfliesByName["cf5"].enableCollisionAvoidance(["cf5","cf231"],[0.5,0.5,0.5])

    allcfs.crazyfliesByName["cf5"].takeoff(targetHeight=Height1, duration=3.0)
    allcfs.crazyfliesByName["cf231"].takeoff(targetHeight=Height1, duration=3.0)
    timeHelper.sleep(3)

    # go to initial positions
    allcfs.crazyfliesByName["cf5"].goTo(Pos1 + np.array([0, 0, Height1]), 0, 3.0)
    allcfs.crazyfliesByName["cf231"].goTo(Pos2 + np.array([0, 0, Height2]), 0, 3.0)
    timeHelper.sleep(3.5)

    # # swap 1
    # allcfs.crazyfliesByName["cf5"].goTo(Pos2 + np.array([0, 0, Height1]), 0, swapTime)
    # allcfs.crazyfliesByName["cf231"].goTo(Pos1 + np.array([0, 0, Height2]), 0, swapTime)
    # timeHelper.sleep(swapTime + 1.5)

    # # swap 2
    # allcfs.crazyfliesByName["cf5"].goTo(Pos1 + np.array([0, 0, Height1]), 0, swapTime)
    # allcfs.crazyfliesByName["cf231"].goTo(Pos2 + np.array([0, 0, Height2]), 0, swapTime)
    # timeHelper.sleep(swapTime + 1.5)

    allcfs.land(targetHeight=0.02, duration=3.0)
    timeHelper.sleep(3.5)


if __name__ == '__main__':
    main()
