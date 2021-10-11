from Grid import *
from Mic_array import *
from GCC import *
import matplotlib.pyplot as plt
import pyaudio
import wave
import numpy as np

####    INICIALIZACIÓN DE GRILLA     ####

grid1 = Grid(x_room = 283, y_room = 310, z_room = 233)
mic_position = np.array([121,10,75])
posicion_estimada = np.zeros(3)
grid1.place_mic_array(mic_position)


####    ESCUCHA DEL MICROFONO        ####

RESPEAKER_RATE = 44100
RESPEAKER_CHANNELS = 8
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 2  # refer to input device id
CHUNK = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"
 
p = pyaudio.PyAudio()
 
stream = p.open(
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            rate=RESPEAKER_RATE,
            input=True,
            input_device_index=RESPEAKER_INDEX,)

data_np = np.zeros(6, CHUNK)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_title("Points in Space")
ax.set_xlim([0, grid1.dimensiones[0]])
ax.set_ylim([0, grid1.dimensiones[1]])
ax.set_zlim([0, grid1.dimensiones[2]])

x = np.arange(0, 2 * CHUNK, 2)

sc, = ax.scatter(0,0,0)
ax.scatter(mic_position[0], mic_position[1], mic_position[2])

fig.show(block=False)

try: 
    while(True):
        data = stream.read(CHUNK)
        # extract channel 0 data from 8 channels, if you want to extract channel 1, please change to [1::8]
        for i in range(6):
            data_np[i] = np.frombuffer(data,dtype=np.int16)[i::8]
        None, posicion_estimada = grid1.HSRP(data_np,"room", RESPEAKER_RATE)
        print(posicion_estimada)

        sc._offsets3d = (posicion_estimada[0], posicion_estimada[1], posicion_estimada[2])
        plt.draw()

except KeyboardInterrupt:
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()