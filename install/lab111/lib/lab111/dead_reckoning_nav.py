#!/usr/bin/env python3
import math
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseArray
# Ocuparé el molde que nos dio el Nacho que grande


class DeadReckoningNav(Node):
    def __init__(self):
        super().__init__("dead_reckoning_nav")
        self.pos_actual = [0.0, 0.0, 0.0]
        self.lineal_vel = 0.2 
        self.rot_vel = 1.0
        self.cmd_vel_pub = self.create_publisher(Twist, "cmd_vel", 10)
        self.goal_list_sub = self.create_subscription(PoseArray, "goal_list", self.accion_mover, 10)

    def aplicar_velocidad(self, speed_command_list):
        for comand in speed_command_list:
            msg = Twist()
            msg.linear.x = comand[0]
            msg.angular.z = comand[1]
            time_exec = comand[2]
            inicio = time.monotonic()  # parte un contador en "cero"
            while time.monotonic() - inicio < time_exec: # compara con un contador nuevo
                self.cmd_vel_pub.publish(msg) 
            self.cmd_vel_pub.publish(Twist())

    def mover_robot_a_destino(self, goal_pose):
        xpos = goal_pose[0]
        ypos = goal_pose[1]
        apos = goal_pose[2]
        ang_final = apos - (math.pi/2)
        comand_list = []
        comand_list.append((self.lineal_vel, 0.0, xpos/self.lineal_vel)) # muevo en x
        comand_list.append((0.0, self.rot_vel, (math.pi/2)/self.rot_vel)) # roto en el eje hasta llegar a y
        comand_list.append((self.lineal_vel, 0.0, ypos/self.lineal_vel)) # me desplazo en y
        comand_list.append((0.0, self.rot_vel, abs(ang_final)/self.rot_vel)) # roto al angulo deseado
        self.aplicar_velocidad(comand_list)

    def accion_mover(self, msg):
        for pose in msg.poses: # aca la info viene en tipo pose array, viendo la documentacion
            # tiene x, y, z, yaw, pitch, roll, me voy a quedar con el x, y y el ángulo 
            pos_x = pose.position.x
            pos_y = pose.position.y
            # ya para el ángulo es medio engorroso, porque necesito el yaw nomas
            yaw = 2 * math.atan2(pose.orientation.z, pose.orientation.w) # acá el z equivale al yaw 
            # y se compara con el vector unitario w.
            self.mover_robot_a_destino((pos_x, pos_y, yaw))

        

def main(args=None):
    rclpy.init(args=args)
    node = DeadReckoningNav()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()