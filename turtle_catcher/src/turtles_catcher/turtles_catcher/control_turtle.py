#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
import math
from my_robot_interfaces.msg import GoalArg
from geometry_msgs.msg import Twist
from turtlesim.srv import Kill



class ControlTurtle(Node): 
    def __init__(self):
        super().__init__("control_turtle") 
        self.goal_dic = {}
        self.key = "none"
        self.tolerance = 0.5
        self.Start_flag = True
        self.robot_pos_subscriber = self.create_subscription(Pose,'/turtle1/pose',self.callback_robot_pos,5)
        self.goal_arg_subscriber = self.create_subscription(GoalArg,'goal_arg',self.callback_goal_arg,10)
        self.speed_publisher = self.create_publisher(Twist,'turtle1/cmd_vel',10)

                    

    def chase_goal(self):
        distance = math.sqrt(math.pow(self.x - self.goal_dic[self.key][0],2)+math.pow(self.y - self.goal_dic[self.key][1],2))
        if distance < self.tolerance:
            #self.chase_goal_timer.cancel()
            del self.goal_dic[self.key]
            self.kill_client = self.create_client(Kill,'/kill')
            kill_name = Kill.Request()
            kill_name.name = self.key
            self.kill_client.call_async(kill_name) 
            self.vel_com.angular.z = 0.0
            self.vel_com.linear.x = 0.0
            self.find_goals()
            
        else:    
            angle = math.atan2 (self.goal_dic[self.key][1] - self.y , self.goal_dic[self.key][0] - self.x) - self.theta
            if angle > math.pi:
                angle = angle - 2*math.pi
            elif angle < -math.pi:
                angle = angle + 2*math.pi
            self.vel_com = Twist()
            self.vel_com.angular.z = 6*angle
            self.vel_com.linear.x = 2*distance * math.cos(angle)

        self.speed_publisher.publish(self.vel_com)


    
    def callback_goal_arg(self,goal_arg):
        self.goal_dic[goal_arg.goal_name] = [goal_arg.goal_x,goal_arg.goal_y]
        
        if  self.Start_flag:
                self.find_goals()
                self.chase_goal_timer = self.create_timer(0.01,self.chase_goal)
                self.Start_flag = False
            
            

        
       

    def callback_robot_pos(self,pose):
        self.x = pose.x
        self.y = pose.y
        self.theta = pose.theta


    def find_goals(self):
        self.distance = 1000
        if bool(self.goal_dic):
            for key in self.goal_dic:
                distance = math.sqrt(math.pow(self.x - self.goal_dic[key][0],2)+math.pow(self.y - self.goal_dic[key][1],2))
                if distance < self.distance:
                    self.distance = distance
                    self.key = key
        else:
            self.Start_flag = True
            self.chase_goal_timer.cancel()

        
            
            

        



def main(args=None):
    rclpy.init(args=args)
    node = ControlTurtle() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
