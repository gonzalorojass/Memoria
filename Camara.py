from foscam import FoscamCamera
from time import sleep

mycam = FoscamCamera('192.168.0.16', 88, 'admin1', 'admin1')
mycam.ptz_move_up()
sleep(1)
mycam.ptz_stop_run()