"""Takeoff-hover-land for one CF. Useful to validate hardware config."""

from crazyflie_py import Crazyswarm


TAKEOFF_DURATION = 2.5
HOVER_DURATION = 5.0


def main():
    swarm = Crazyswarm()

    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]

    cf.takeoff(targetHeight=0.5, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + HOVER_DURATION)

    # cf.setParam('ring.solidRed', int(0.7 * 255))
    # cf.setParam('ring.solidGreen', int(0.0 * 255))
    # cf.setParam('ring.solidBlue', int(0.0 * 255))
    
    cf.goTo([0.0,0.0,0.0],6,6.0, relative=True)
    timeHelper.sleep(4)

    # cf.setParam('ring.solidRed', int(0.0 * 255))
    # cf.setParam('ring.solidGreen', int(0.7 * 255))
    # cf.setParam('ring.solidBlue', int(0.0 * 255))

    # cf.goTo([-0.7,0.0,0.0],1.57,5.0, relative=True)
    # timeHelper.sleep(4)

    # cf.setParam('ring.solidRed', int(0.0 * 255))
    # cf.setParam('ring.solidGreen', int(0.7 * 255))
    # cf.setParam('ring.solidBlue', int(0.7 * 255))

    # cf.goTo([0.0,-0.7,0.0],1.57,5.0, relative=True)
    # timeHelper.sleep(4)

    # cf.setParam('ring.solidRed', int(0.8 * 255))
    # cf.setParam('ring.solidGreen', int(0.3 * 255))
    # cf.setParam('ring.solidBlue', int(0.7 * 255))

    # cf.goTo([0.7,0.0,0.0],1.57,5.0, relative=True)
    # timeHelper.sleep(4)

    # cf.setParam('ring.solidRed', int(0.0 * 255))
    # cf.setParam('ring.solidGreen', int(0.0 * 255))
    # cf.setParam('ring.solidBlue', int(0.7 * 255))

    cf.land(targetHeight=0.02, duration=2.5)
    timeHelper.sleep(TAKEOFF_DURATION)

if __name__ == '__main__':
    main()
