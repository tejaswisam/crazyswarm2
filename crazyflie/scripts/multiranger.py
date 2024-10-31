#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import math
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Pose, PoseArray
import time

class MazeSolver(Node):
    def __init__(self):
        super().__init__('mapper_drone')
        self.trajectory = []  # To store mapper drone's trajectory
        # Timer for publishing trajectory points
        self.create_timer(0.1, self.publish_trajectory)

        # Parameters for the goal
        self.declare_parameter('robot_prefix', '/cf1')
        self.declare_parameter('goal_x', 2)
        self.declare_parameter('goal_y', 0.5)

        robot_prefix = self.get_parameter('robot_prefix').value
        self.goal_x = self.get_parameter('goal_x').value
        self.goal_y = self.get_parameter('goal_y').value

        # Subscribers
        self.odom_subscriber = self.create_subscription(
            Odometry, robot_prefix + '/odom', self.odom_callback, 10)
        self.lidar_subscriber = self.create_subscription(
            LaserScan, robot_prefix + '/scan', self.scan_callback, 10)

        # Publisher for velocity commands
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Publisher for trajectory points
        self.trajectory_pub = self.create_publisher(PoseArray, '/trajectory', 10)

        self.trajectory = PoseArray()
        self.start_time = None

        # Lidar ranges: [back, right, front, left]
        self.lidar_ranges = [3.5] * 4
        self.obstacle_distance_threshold = 0.3  # meters

        # Movement control
        self.move_speed = 0.07  # m/s
        self.turn_speed = 0.2  # rad/s
        self.position = [0.0, 0.0]  # Current position [x, y]

        # State of the drone
        self.state = 'move_to_goal'
        self.goal_reached = False  # Initialize goal_reached flag

        # Timer for regular position, goal checking, and trajectory publishing
        self.create_timer(0.1, self.check_goal)  # 10 Hz

    def odom_callback(self, msg):
        if self.start_time is None:
            self.start_time = time.time()  # Record the start time

        current_time = time.time() - self.start_time  # Calculate elapsed time
        # Update the drone's current position
        self.position[0] = msg.pose.pose.position.x
        self.position[1] = msg.pose.pose.position.y

        # Create a Pose and set position and time
        pose = Pose()
        pose.position.x = msg.pose.pose.position.x
        pose.position.y = msg.pose.pose.position.y

        # Append timestamp to the pose
        self.trajectory.poses.append(pose)
        self.trajectory.header.stamp.sec = int(current_time)
        self.trajectory.header.stamp.nanosec = int((current_time - int(current_time)) * 1e9)

        # Publish the current position as part of the trajectory
        self.publish_trajectory()

    def scan_callback(self, msg):
        # Update Lidar readings: [back, right, front, left]
        self.lidar_ranges[0] = msg.ranges[0]  # Back
        self.lidar_ranges[1] = msg.ranges[1]  # Right
        self.lidar_ranges[2] = msg.ranges[2]  # Front
        self.lidar_ranges[3] = msg.ranges[3]  # Left

        if not self.goal_reached:
            self.solve_maze()

    def check_goal(self):
        if not self.goal_reached:
            distance_to_goal = math.sqrt((self.goal_x - self.position[0])**2 + 
                                         (self.goal_y - self.position[1])**2)
            if distance_to_goal < 0.1:
                self.stop_drone()
                self.goal_reached = True
                self.get_logger().info('Goal reached!')

    def stop_drone(self):
        # Publish zero velocity to stop the drone
        twist_msg = Twist()
        self.cmd_vel_pub.publish(twist_msg)
        self.get_logger().info('Drone stopped.')

    def move_in_direction(self, direction):
        # Move the drone in the specified direction
        twist_msg = Twist()
        if direction == 0:  # Move back
            twist_msg.linear.x = -self.move_speed
        elif direction == 1:  # Move right
            twist_msg.linear.y = -self.move_speed
        elif direction == 2:  # Move forward
            twist_msg.linear.x = self.move_speed
        elif direction == 3:  # Move left
            twist_msg.linear.y = self.move_speed
        self.cmd_vel_pub.publish(twist_msg)

    def solve_maze(self):
        # Improved maze solving logic to reduce oscillation
        clearance = 0.15  # Additional clearance to avoid collisions

        if self.lidar_ranges[2] > self.obstacle_distance_threshold:
            # No obstacle in front, move forward
            self.move_in_direction(2)
        else:
            # Check right and left distances with clearance
            right_distance = self.lidar_ranges[1] - clearance
            left_distance = self.lidar_ranges[3] - clearance

            if right_distance > self.obstacle_distance_threshold and left_distance > self.obstacle_distance_threshold:
                # Both sides are clear, prefer the direction with more space
                if right_distance > left_distance:
                    self.move_in_direction(1)
                else:
                    self.move_in_direction(3)
            elif right_distance > self.obstacle_distance_threshold:
                # Only right is clear
                self.move_in_direction(1)
            elif left_distance > self.obstacle_distance_threshold:
                # Only left is clear
                self.move_in_direction(3)
            else:
                # Obstacles in front, right, and left, move back
                self.move_in_direction(0)

    def publish_trajectory(self):
        if self.trajectory.poses:
            self.trajectory.header.stamp = self.get_clock().now().to_msg()  # Update header timestamp
            self.trajectory_pub.publish(self.trajectory)
            self.get_logger().info(f'Published trajectory with {len(self.trajectory.poses)} points.')


def main(args=None):
    rclpy.init(args=args)
    node = MazeSolver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
