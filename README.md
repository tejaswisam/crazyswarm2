# Crazyswarm2 with Multi-Ranger Deck Control

This repository is a modified version of the [Crazyswarm2](https://github.com/IMRCLab/crazyswarm2) package, with added support for the Crazyflie Multi-Ranger deck. This enhancement enables control and sensor data integration from the Multi-Ranger deck, making it ideal for autonomous navigation and obstacle avoidance tasks in 3D space.

## Features

- Full integration of Multi-Ranger deck sensor data.
- Enhanced capabilities for autonomous navigation and obstacle avoidance.
- Maintains original Crazyswarm2 functionalities, allowing multi-agent coordination.
- Compatible with Crazyflie drones equipped with the Multi-Ranger deck.

## Requirements

| Software             | Version            |
|----------------------|--------------------|
| Ubuntu               | 22.04              |
| ROS2                 | Humble             |
| Gazebo               | Garden             |

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/tejaswisam/crazyswarm2.git --recursive
   ```

3. **Build the ROS2 Workspace**
   ```bash
   cd ros2_ws
   colcon build --symlink-install
   ```

4. **Setup the Crazyflie Firmware with Multi-Ranger Support**
   - Flash your Crazyflie with the latest firmware compatible with the Multi-Ranger deck.
   - Ensure the Multi-Ranger deck is securely attached to the Crazyflie.

## Usage

### 1. Launching the Crazyswarm2 System with Multi-Ranger Control

- Start the Crazyswarm2 server with Multi-Ranger control enabled:
  ```bash
  ros2 launch crazyswarm2 multiranger_swarm.launch.py
  ```

- This will:
  - Initialize ROS2 nodes for each Crazyflie.
  - Launch the Multi-Ranger control node to receive data from the Multi-Ranger deck and handle obstacle detection and avoidance.

### 2. Running Autonomous Navigation Scripts

- Use pre-defined scripts to control the Crazyflies autonomously:
  ```bash
  ros2 run crazyswarm2 scripts/auto_navigation.py
  ```

- The Multi-Ranger data allows the Crazyflies to autonomously avoid obstacles, navigate towards waypoints, or explore an environment based on your configuration.

## Multi-Ranger Deck Integration Details

The Multi-Ranger deck provides distance readings in four directions: front, back, left, and right. This modified Crazyswarm2 package includes a ROS2 node that:

- Subscribes to Multi-Ranger sensor topics for real-time distance data.
- Publishes obstacle detection messages to the Crazyswarm2 swarm controller.
- Controls the Crazyflie's navigation to avoid obstacles using the Multi-Ranger readings.

## Customization

The `multiranger_swarm.launch.py` file can be customized to adjust parameters such as:

- Obstacle avoidance sensitivity.
- Minimum safe distance.
- Autonomous navigation modes.

## Troubleshooting

- Ensure firmware compatibility: Use Crazyflie firmware version 2023.02 or newer.
- Verify Multi-Ranger deck connection: Ensure the Multi-Ranger deck is securely connected to the Crazyflie and detected on startup.
- Check ROS2 and Crazyswarm2 logs for error messages if control issues arise.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

This work builds upon the [Crazyswarm2](https://github.com/USC-ACTLab/crazyswarm2) project by the USC ACTLab.
```