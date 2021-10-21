from Grid import *
from Mic_array import *
from GCC import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

NUMBER_OF_MICROPHONES = 6
####    INICIALIZACIÓN DE GRILLA     ####

grid1 = Grid.Grid(x_room = 283, y_room = 310, z_room = 233)
mic_position = np.array([121,10,75])
posicion_estimada = np.zeros(3)

####    ESCUCHA DEL MICROFONO        ####

RESPEAKER_RATE = 44100
CHUNK = 44100
RESPEAKER_CHANNELS = 8
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 2

p = pyaudio.PyAudio()
 
stream = p.open(
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            rate=RESPEAKER_RATE,
            input=True,
            input_device_index=RESPEAKER_INDEX,)

fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = plt.subplots(8, figsize=(15, 7))

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)

# create a line object with random data
line1, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)
line2, = ax2.plot(x, np.random.rand(CHUNK), '-', lw=2)
line3, = ax3.plot(x, np.random.rand(CHUNK), '-', lw=2)
line4, = ax4.plot(x, np.random.rand(CHUNK), '-', lw=2)
line5, = ax5.plot(x, np.random.rand(CHUNK), '-', lw=2)
line6, = ax6.plot(x, np.random.rand(CHUNK), '-', lw=2)
line7, = ax7.plot(x, np.random.rand(CHUNK), '-', lw=2)
line8, = ax8.plot(x, np.random.rand(CHUNK), '-', lw=2)

ax1.set_ylim(-1000,1000)
ax2.set_ylim(-1000,1000)
ax3.set_ylim(-1000,1000)
ax4.set_ylim(-1000,1000)
ax5.set_ylim(-1000,1000)
ax6.set_ylim(-1000,1000)
ax7.set_ylim(-1000,1000)
ax8.set_ylim(-1000,1000)
plt.show(block=False)

data_np = np.zeros(6, CHUNK)

try:
    while(True):
        data = stream.read(CHUNK)
        for i in range(6):
                data_np[i] = np.frombuffer(data,dtype=np.int16)[i::8]

        line1.set_ydata(data_np[0::8])
        line2.set_ydata(data_np[1::8])
        line3.set_ydata(data_np[2::8])
        line4.set_ydata(data_np[3::8])
        line5.set_ydata(data_np[4::8])
        line6.set_ydata(data_np[5::8])
        line7.set_ydata(data_np[6::8])
        line8.set_ydata(data_np[7::8])

        fig.canvas.draw()
        fig.canvas.flush_events()

        input("Press Enter to continue...")

except KeyboardInterrupt:
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()


# with MicArray(grid=grid1, center=mic_position, rate = RESPEAKER_RATE, chunk_size = CHUNK) as mic:
#     for chunk in mic.read_chunks():
#         line1.set_ydata(chunk[0::8])
#         line2.set_ydata(chunk[1::8])
#         line3.set_ydata(chunk[2::8])
#         line4.set_ydata(chunk[3::8])
#         line5.set_ydata(chunk[4::8])
#         line6.set_ydata(chunk[5::8])
#         line7.set_ydata(chunk[6::8])
#         line8.set_ydata(chunk[7::8])
#         input("Press Enter to continue...")

