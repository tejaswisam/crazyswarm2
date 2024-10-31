#!/usr/bin/env python

from crazyflie_py import Crazyswarm


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    # disable LED (one by one)
    for cf in allcfs.crazyflies:
        cf.setParam('ring.solidRed', int(0.7 * 255))
        cf.setParam('ring.solidGreen', int(0.0 * 255))
        cf.setParam('ring.solidBlue', int(0.0 * 255))
        timeHelper.sleep(1.0)

    timeHelper.sleep(2.0)

    # enable LED (broadcast)
    allcfs.setParam('ring.solidRed', int(0.0 * 255))
    allcfs.setParam('ring.solidBlue', int(0.9 * 255))
    timeHelper.sleep(5.0)


if __name__ == '__main__':
    main()
