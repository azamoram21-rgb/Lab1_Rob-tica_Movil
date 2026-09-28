#!/usr/bin/env python3
import math
import time

import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose


class TrajectoryLogger(Node):
    def __init__(self):
        super().__init__("trajectory_logger")
        self.sub_odom = self.create_subscription(Odometry, "/odom", self.odom_cb, 10)
        self.sub_real = self.create_subscription(Pose, "/real_pose", self.real_cb, 10)
        self.odom_x, self.odom_y = [], []
        self.real_x, self.real_y = [], []

    def odom_cb(self, msg):
        self.odom_x.append(msg.pose.pose.position.x)
        self.odom_y.append(msg.pose.pose.position.y)

    def real_cb(self, msg):
        # Pose ya es la pose directamente (sin .pose.pose)
        self.real_x.append(msg.position.x)
        self.real_y.append(msg.position.y)

    def plot_and_calculate_error(self):
        if not self.real_x or not self.odom_x:
            print("\n[Logger] No se recibieron datos. Verifica que el robot se haya movido.")
            return

        # Odom parte en (0, 0) y real_pose parte en la pose inicial del robot:
        # se desplaza la odometría para compararlas en el mismo marco
        off_x, off_y = self.real_x[0], self.real_y[0]
        odom_x = [x + off_x for x in self.odom_x]
        odom_y = [y + off_y for y in self.odom_y]

        # Error entre punto de partida y llegada
        x_ini, y_ini = self.real_x[0], self.real_y[0]
        x_fin, y_fin = self.real_x[-1], self.real_y[-1]
        error_real = math.hypot(x_fin - x_ini, y_fin - y_ini)
        error_odom = math.hypot(odom_x[-1] - odom_x[0], odom_y[-1] - odom_y[0])

        print("\n--- Resultados ---")
        print(f"Error de cierre (real_pose): {error_real:.4f} m")
        print(f"Error de cierre (odom):      {error_odom:.4f} m")

        # Gráfico
        plt.figure(figsize=(8, 8))
        plt.plot(odom_x, odom_y, label="Odometría (/odom)", linestyle="--")
        plt.plot(self.real_x, self.real_y, label="Pose real (/real_pose)", linewidth=2)
        plt.scatter([x_ini], [y_ini], color="green", zorder=5, label="Inicio")
        plt.scatter([x_fin], [y_fin], color="red", zorder=5, label="Fin")
        plt.title("Trayectoria del TurtleBot - Cuadrado 3 vueltas")
        plt.xlabel("X [m]")
        plt.ylabel("Y [m]")
        plt.legend()
        plt.grid(True)
        plt.axis("equal")

        # Nombre con timestamp para no sobreescribir entre los 5 experimentos
        ruta = f"/home/al2/ros2_ws/trayectoria_{time.strftime('%H%M%S')}.png"
        plt.savefig(ruta)
        print(f"Gráfico guardado en: {ruta}")


def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryLogger()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        # Se ejecuta tanto si spin termina por excepción como si retorna normal
        node.plot_and_calculate_error()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()