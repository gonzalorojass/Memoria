from Grid import *
from Mic_array import *
from GCC import *
import matplotlib.pyplot as plt
import pyaudio
import wave
import numpy as np

####    INICIALIZACIÓN DE GRILLA     ####

grid1 = Grid(x_room = 200, y_room = 300, z_room = 200)
mic_position = np.array([100,70,0])
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

## TODO O: DELETE EVERYTHING IN BETWEEN TODOs
fig, (ax, ax2) = plt.subplots(2, figsize=(15, 7))
x = np.arange(0, 2 * CHUNK, 2)
x_fft = np.linspace(0, RESPEAKER_RATE, CHUNK)
# create a line object with random data
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)
line_fft, = ax2.semilogx(x_fft, np.random.rand(CHUNK), '-', lw=2)

# basic formatting for the axes
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('volume')
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

ax2.set_xlim(0, RESPEAKER_RATE/2)

plt.show(block=False)
## TODO C: DELETE EVERYTHING IN BETWEEN TODOs

try: 
    while(True):
        data = stream.read(CHUNK)
        # extract channel 0 data from 8 channels, if you want to extract channel 1, please change to [1::8]
        data_np = np.fromstring(data,dtype=np.int16)[0::8]

        line.set_ydata(data_np)
        y_fft = np.fft.fft(data_np)
        line_fft.set_ydata(np.abs(y_fft[0:CHUNK]) * 2 / (256 * CHUNK))

        fig.canvas.draw()
        fig.canvas.flush_events()

except KeyboardInterrupt:
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()

####    GRAFICOS DE POSICIÓN        ####
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.set_title("Points in Space")
# ax.set_xlim([0, grid1.dimensiones[0]])
# ax.set_ylim([0, grid1.dimensiones[1]])
# ax.set_zlim([0, grid1.dimensiones[2]])

# ax.scatter(mic_position[0], mic_position[1], mic_position[2])
# ax.scatter(posicion_estimada[:,0], posicion_estimada[:,1], posicion_estimada[:,2])

# label_original = '1'

# for i, txt in enumerate(label_original):
#     ax.text(posicion_estimada[0],posicion_estimada[1],posicion_estimada[2],  '%s' % label_original)

# plt.show()