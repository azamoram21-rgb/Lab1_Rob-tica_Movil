#!/usr/bin/env python3
import rclpy
import pygame # voy a manejar la interfaz de teclado con pygame
import threading
from rclpy.node import Node
from geometry_msgs.msg import Twist



class WASD(Node):
    def __init__(self):
        super().__init__("wasd")
        self.goal_list_pub = self.create_publisher(Twist, "cmd_vel", 10)
        self.running = True
        self.thread = threading.Thread(target=self.crear_goal_list, daemon=True) # lo pongo daemon para que no hayua deadlock
        self.thread.start()

    def crear_goal_list(self):
        pygame.init()
        screen = pygame.display.set_mode((200, 200))
        pygame.display.set_caption("DA LO MISMO ESTA PANTALLA")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            msg = Twist()
            keys = pygame.key.get_pressed() # Esto me revisa si hay teclas presionadas
            if keys[pygame.K_i]:
                msg.linear.x = 0.2
            elif keys[pygame.K_j]:
                msg.linear.x = -0.2
            elif keys[pygame.K_a]:
                msg.angular.z = 1.0
            elif keys[pygame.K_s]:
                msg.angular.z = -1.0
            elif keys[pygame.K_q]:
                msg.linear.x = 0.2
                msg.angular.z = 1.0
            elif keys[pygame.K_w]:
                msg.linear.x = 0.2
                msg.angular.z = -1.0
            else:
                msg.linear.x = 0.0
                msg.angular.z = 0.0

            self.goal_list_pub.publish(msg)
        pygame.quit()

        
def main(args=None):
    rclpy.init(args=args)
    node = WASD()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()