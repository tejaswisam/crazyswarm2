#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import math
from geometry_msgs.msg import Twist, PoseArray, Pose
from nav_msgs.msg import Odometry
import time

class FollowerDrone(Node):
    def __init__(self):
        super().__init__('follower_drone')

        # Parameters for movement and tolerance
        self.move_speed = 0.1  # m/s
        self.tolerance = 0.1  # Distance tolerance for reaching a point
        self.safety_distance = 0.3  # Minimum distance to trajectory point to avoid obstacles
        self.current_point_idx = 0  # Track the index of the current point
        self.trajectory = []  # Store trajectory points from the mapper drone
        self.initial_position = [0.0, 0.0]  # Store the initial position of the follower drone
        self.offset = [0.0, 0.0]  # Offset between mapper and follower drones
        self.start_time = None  # Track when the follower drone should start moving

        # Subscriber for the trajectory from the mapper drone
        self.trajectory_sub = self.create_subscription(
            PoseArray, '/trajectory', self.trajectory_callback, 10)

        # Subscriber for odometry to track the follower drone's position
        self.odom_sub = self.create_subscription(
            Odometry, '/cf5/odom', self.odom_callback, 10)

        # Publisher for velocity commands to move the follower drone
        self.cmd_vel_pub = self.create_publisher(Twist, '/cf5/cmd_vel_follower', 10)

        # Timer for regular trajectory following
        self.create_timer(0.1, self.follow_trajectory)  # 10 Hz

    def odom_callback(self, msg):
        # Update the current position of the follower drone
        self.position = [msg.pose.pose.position.x, msg.pose.pose.position.y]

        # Set the initial position on the first callback
        if self.current_point_idx == 0:
            self.initial_position = self.position.copy()
            self.get_logger().info(f'Initial position set: {self.initial_position}')

    def trajectory_callback(self, msg):
        # Update the trajectory points from the mapper drone
        self.trajectory = [(pose.position.x, pose.position.y, pose.header.stamp.sec) for pose in msg.poses]
        self.get_logger().info(f'Trajectory received with {len(self.trajectory)} points.')

        # Calculate the offset between the initial positions of the mapper and follower drones
        if self.initial_position:
            mapper_initial_position = (self.trajectory[0][0], self.trajectory[0][1])  # First point in trajectory
            self.offset = [mapper_initial_position[0] - self.initial_position[0],
                           mapper_initial_position[1] - self.initial_position[1]]
            self.get_logger().info(f'Calculated offset: {self.offset}')

            # Adjust trajectory points based on the calculated offset
            self.adjust_trajectory()

    def adjust_trajectory(self):
        # Adjust each trajectory point based on the offset
        self.trajectory = [(x + self.offset[0], y + self.offset[1], t) for x, y, t in self.trajectory]
        self.get_logger().info('Trajectory adjusted for offset.')

    def follow_trajectory(self):
        current_time = time.time()  # Get the current time
        # If trajectory is available and the follower drone has not reached the last point
        if self.trajectory and self.current_point_idx < len(self.trajectory):
            target_point = self.trajectory[self.current_point_idx]
            distance = math.sqrt((target_point[0] - self.position[0]) ** 2 +
                                 (target_point[1] - self.position[1]) ** 2)

            # Check if enough time has passed to move to the next trajectory point
            if current_time >= target_point[2] + self.start_time and distance > self.tolerance:
                # Move towards the current target point
                self.move_to_point(target_point[:2])  # Only take x and y coordinates
            elif distance <= self.tolerance:
                # If within tolerance, move to the next point
                self.current_point_idx += 1
                self.get_logger().info(f'Reached point {self.current_point_idx}, moving to next.')
            else:
                # If not enough time has passed, stop the drone
                self.stop_drone()

        elif self.current_point_idx >= len(self.trajectory):
            self.get_logger().info('All trajectory points reached.')
            self.stop_drone()

    def move_to_point(self, point):
        # Calculate the direction to the target point
        direction_x = point[0] - self.position[0]
        direction_y = point[1] - self.position[1]
        angle = math.atan2(direction_y, direction_x)  # Calculate angle to target

        # Create a Twist message to move the drone
        twist_msg = Twist()
        twist_msg.linear.x = self.move_speed * math.cos(angle)
        twist_msg.linear.y = self.move_speed * math.sin(angle)

        # Publish the velocity command to move the drone
        self.cmd_vel_pub.publish(twist_msg)

    def stop_drone(self):
        # Publish zero velocity to stop the drone
        twist_msg = Twist()
        self.cmd_vel_pub.publish(twist_msg)
        self.get_logger().info('Drone stopped.')

def main(args=None):
    rclpy.init(args=args)
    node = FollowerDrone()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
