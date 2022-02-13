from foscam import *         
import numpy as np
from time import sleep
import math

HORIZONTAL_CAMERA_SPEED = 40/math.pi
VERTICAL_CAMERA_SPEED = 10.8/math.pi

class Camera:
    def __init__(self, camera_position):
        self.mycam = FoscamCamera('192.168.1.100', 88, 'admin1', 'admin1')
        self.current_direction = np.array([0,0,math.pi/2])
        self.camera_position = camera_position
        self.reset_camera()

    def reset_camera(self):
        self.mycam.ptz_reset()
        sleep(22)
        self.mycam.ptz_move_down()
        sleep(1.5)
        self.mycam.ptz_stop_run()

    def point_at_location(self, position):
        position_diff = position - self.camera_position

        xy = position_diff[0]**2 + position_diff[1]**2
        r = np.sqrt(xy + position_diff[2]**2)
        theta = np.arctan(np.array([position_diff[2]/np.sqrt(xy)])) 
        azimuth = np.arctan(np.array([position_diff[1]/position_diff[0]])) + (0 if (position_diff[0] > 0) else math.pi)
        
        theta_diff = theta[0] - self.current_direction[1] 
        if(theta_diff < 0):
            self.mycam.ptz_move_down()
            sleep(abs(theta_diff)*VERTICAL_CAMERA_SPEED)
            self.mycam.ptz_stop_run()
        else:
            self.mycam.ptz_move_up()
            sleep(theta_diff*VERTICAL_CAMERA_SPEED)
            self.mycam.ptz_stop_run()

        azimuth_diff = self.current_direction[2] - azimuth[0]
        if(azimuth_diff < 0):
            self.mycam.ptz_move_left()
            sleep(abs(azimuth_diff)*HORIZONTAL_CAMERA_SPEED)
            self.mycam.ptz_stop_run()
        else:
            self.mycam.ptz_move_right()
            sleep(azimuth_diff*HORIZONTAL_CAMERA_SPEED)
            self.mycam.ptz_stop_run()
            
        self.current_direction = np.array([r,theta[0],azimuth[0]])