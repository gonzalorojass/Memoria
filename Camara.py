from foscam import *         
import numpy as np
from time import sleep
import math

HORIZONTAL_CAMERA_SPEED = 4            ## A DEFINIR SEGUN CUANTO DEMORE EN RECORRER 90 GRADOS
VERTICAL_CAMERA_SPEED = 4            ## A DEFINIR SEGUN CUANTO DEMORE EN RECORRER 90 GRADOS

class Camara:
    def __init__(self):
        self.mycam = FoscamCamera('192.168.0.16', 88, 'admin1', 'admin1')
        self.mycam.get_ptz_speed()
        self.current_position = np.array([0,0,math.pi])
        self.reset_camera(self)

    def reset_camera(self):
        self.mycam.ptz_reset()
        sleep(15)
        self.mycam.ptz_move_down()
        sleep(1)
        self.mycam.ptz_stop_run()

    def point_at_location(self, position):
        xy = position[0]**2 + position[1]**2
        r = np.sqrt(xy + position[2]**2)            ## ignorado por ahora
        theta = np.arctan2(position[2], np.sqrt(xy))
        azimuth = np.arctan2(position[1], position[0])
        
        azimuth_diff = self.current_position[2] - azimuth
        if(azimuth_diff < 0):
            self.mycam.ptz_move_left()
            sleep(azimuth_diff*HORIZONTAL_CAMERA_SPEED)
        else:
            self.mycam.ptz_move_right()
            sleep(azimuth_diff*HORIZONTAL_CAMERA_SPEED)

        theta_diff = self.current_position[1] - theta
        if(theta_diff < 0):
            self.mycam.ptz_move_left()
            sleep(theta_diff*HORIZONTAL_CAMERA_SPEED)
        else:
            self.mycam.ptz_move_right()
            sleep(theta_diff*HORIZONTAL_CAMERA_SPEED)
            
        self.current_position = np.array([r,theta,azimuth])

