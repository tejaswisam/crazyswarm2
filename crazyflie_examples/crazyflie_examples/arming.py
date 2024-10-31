import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from tf2_ros import Buffer, TransformListener
from tf2_ros.transform_listener import TransformException
from geometry_msgs.msg import TransformStamped

class ScanTransformer(Node):
    def __init__(self):
        super().__init__('scan_transformer')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.subscription  # prevent unused variable warning

    def scan_callback(self, msg: LaserScan):
        try:
            transform: TransformStamped = self.tf_buffer.lookup_transform('map', 'crazyflie_0/base_link/gpu_lidar', rclpy.time.Time())
            # Transform the scan data here
            # For example, use a transformation library or custom code to convert scan data to the 'map' frame
        except TransformException as e:
            self.get_logger().info(f'Could not transform scan data: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = ScanTransformer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
