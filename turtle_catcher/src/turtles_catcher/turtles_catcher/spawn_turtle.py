#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
import random
import math
from my_robot_interfaces.msg import GoalArg
from functools import partial


class SpawnTurtle(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("spawn_turtle") 
        self.declare_parameter("spawn_frequency",2.0)
        self.frequency = self.get_parameter("spawn_frequency").value
        self.timer = self.create_timer(1/self.frequency, self.call_spawn_service)
        self.goal_arg_publisher = self.create_publisher(GoalArg,'goal_arg',10)

    def call_spawn_service(self):
        self.client = self.create_client(Spawn,'spawn')
        request = Spawn.Request()
        request.x = random.uniform(1,10)
        request.y = random.uniform(1,10)
        request.theta = random.uniform(0,2*math.pi)
        future = self.client.call_async(request=request)
        future.add_done_callback(partial(self.result_func,request = request))

    def result_func(self,future,request):
        result = future.result()
        self.get_logger().info(result.name)

        goal_arg = GoalArg()
        goal_arg.goal_x = request.x
        goal_arg.goal_y = request.y
        goal_arg.goal_name = result.name
        self.goal_arg_publisher.publish(goal_arg)





def main(args=None):
    rclpy.init(args=args)
    node = SpawnTurtle() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
