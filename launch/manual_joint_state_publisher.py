import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math

class ManualJointStatePublisher(Node):
    def __init__(self, joint_names):
        super().__init__('dynamic_joint_state_publisher')

        # List of joint names
        self.joint_names = joint_names

        # Initialize angles for all joints (start at 0.0 for each joint)
        self.joint_angles = [0.0 for _ in self.joint_names]

        # Publisher for joint states
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)

        # Timer to publish joint states every 0.1 seconds
        self.timer = self.create_timer(0.1, self.publish_joint_state)

    def publish_joint_state(self):
        # Create a new JointState message
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = self.joint_names

        # Update each joint's angle to simulate continuous rotation
        for i in range(len(self.joint_angles)):
            # Increment angle for each joint to simulate smooth motion
            self.joint_angles[i] += 0.1  # Increment by 0.1 rad per update

            # Keep angles within a reasonable range (e.g., 0 to 2π)
            if self.joint_angles[i] > 2 * math.pi:
                self.joint_angles[i] -= 2 * math.pi

        # Set the joint positions
        joint_state.position = self.joint_angles

        # Publish the joint state
        self.publisher_.publish(joint_state)

        # Log the joint angles for debugging
        self.get_logger().info(f'Publishing joint states: {self.joint_angles}')

def main(args=None):
    rclpy.init(args=args)
    
    # Define your joint names here (you can add/remove names as needed)
    joint_names = ["left_wheel_joint", "right_wheel_joint"]

    # Create and run the dynamic joint state publisher
    node = ManualJointStatePublisher(joint_names)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
