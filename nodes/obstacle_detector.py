#!/usr/bin/env python3
import rclpy
import numpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import Image
from cv_bridge import CvBridge # Para usar el kinect usare opencv
# como recomendo el nacho


DISTANCIA_MIN_OBSTACULO = 0.5 # Esto lo dice el enunciado


class ObstacleDetector(Node):
    def __init__(self):
        super().__init__("obstacle_detector")
        self.occupancy_state_pub = self.create_publisher(Vector3, "occupancy_state", 10)
        self.camera_sub = self.create_subscription(Image, "/camera/depth/image_raw", self.callback_camera, 10)
        self.bridge = CvBridge() 

    def callback_camera(self, msg):

        depth_array = self.bridge.imgmsg_to_cv2(msg)
        alto, ancho = depth_array.shape

        region_izq = depth_array[:, 0:(ancho // 3)]
        region_mid = depth_array[:, (ancho // 3):2*(ancho // 3)]
        region_der = depth_array[:, 2*(ancho // 3):ancho]

        # la funcion nanmin agarra un array y busca el valor mas chico que encuentre
        # al final del dia lo que importa para ver la distancia es lo que esta mas cerca
        dist_izq = numpy.nanmin(region_izq)
        dist_mid = numpy.nanmin(region_mid)
        dist_der = numpy.nanmin(region_der)

        # filtro binario
        if dist_izq <= DISTANCIA_MIN_OBSTACULO:
            e_izq = 1
        else:
            e_izq = 0
        if dist_mid <= DISTANCIA_MIN_OBSTACULO:
            e_mid = 1
        else:
            e_mid = 0
        if dist_der <= DISTANCIA_MIN_OBSTACULO:
            e_der = 1
        else:
            e_der = 0
        # creo el vector con la data en binario
        data_msg = Vector3()
        data_msg.x = float(e_izq)
        data_msg.y = float(e_mid)
        data_msg.z = float(e_der)
        self.occupancy_state_pub.publish(data_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleDetector()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()