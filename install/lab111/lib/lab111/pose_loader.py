#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import PoseArray, Pose
# se asume formato de texto libre.


class PoseLoader(Node):
    def __init__(self):
        super().__init__("pose_loader")
        self.goal_list_pub = self.create_publisher(PoseArray, "goal_list", 10)

    def crear_goal_list(self, arch_txt):
        lista_vacia = []
        with open(arch_txt, "r", encoding="utf-8") as archivo: # leo el archivo 
            for linea in archivo: # y lo hago lista de lista
                lista_vacia.append(linea.strip().split(","))
        msg = PoseArray() # creo el objeto que voy a mandar al final 
        for linea in lista_vacia: # cargo data 
            pos_x = float(linea[0]) 
            pos_y = float(linea[1])
            ang = float(linea[2])
            pose = Pose()
            pose.position.x = pos_x
            pose.position.y = pos_y
            pose.position.z = 0.0
            pose.orientation.x = 0.0
            pose.orientation.y = 0.0
            pose.orientation.z = math.sin(ang / 2) # solo se mueve en yaw
            pose.orientation.w = math.cos(ang / 2) # el vector  base
            msg.poses.append(pose)
        self.goal_list_pub.publish(msg)

        
def main(args=None):
    rclpy.init(args=args)
    node = PoseLoader()
    node.crear_goal_list("/home/al2/ros2_ws/src/lab111/arch_txt/pose.txt") # el .txt va en arch_txt
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()