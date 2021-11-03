from Grid import *
from Mic_array import *
from GCC import *
from Camara import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time



camara = Camara(np.array([121,0,75]))

camara.point_at_location(np.array([41,188,132]))
camara.point_at_location(np.array([230,188,165]))

# NUMBER_OF_MICROPHONES = 6
# ####    INICIALIZACIÓN DE GRILLA     ####

# grid1 = Grid.Grid(x_room = 283, y_room = 310, z_room = 233)
# mic_position = np.array([121,10,75])
# posicion_estimada = np.zeros(3)

# ####    ESCUCHA DEL MICROFONO        ####

# RESPEAKER_RATE = 44100
# CHUNK = 44100
# RESPEAKER_CHANNELS = 8
# RESPEAKER_WIDTH = 2
# RESPEAKER_INDEX = 2


# fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = plt.subplots(8, figsize=(15, 7))

# # variable for plotting
# x = np.arange(0, 2 * CHUNK, 2)
# data_np = np.zeros((6, CHUNK))

# # create a line object with random data
# line1, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)
# line2, = ax2.plot(x, np.random.rand(CHUNK), '-', lw=2)
# line3, = ax3.plot(x, np.random.rand(CHUNK), '-', lw=2)
# line4, = ax4.plot(x, np.random.rand(CHUNK), '-', lw=2)
# line5, = ax5.plot(x, np.random.rand(CHUNK), '-', lw=2)
# line6, = ax6.plot(x, np.random.rand(CHUNK), '-', lw=2)
# line7, = ax7.plot(x, np.random.rand(CHUNK), '-', lw=2)
# line8, = ax8.plot(x, np.random.rand(CHUNK), '-', lw=2)

# ax1.set_ylim(-1000,1000)
# ax2.set_ylim(-1000,1000)
# ax3.set_ylim(-1000,1000)
# ax4.set_ylim(-1000,1000)
# ax5.set_ylim(-1000,1000)
# ax6.set_ylim(-1000,1000)
# ax7.set_ylim(-1000,1000)
# ax8.set_ylim(-1000,1000)
# plt.show(block=False)

# to_check = np.zeros((6))
# not_mic = np.array([0,1])

# with MicArray(grid=grid1, center=mic_position, rate = RESPEAKER_RATE, chunk_size = CHUNK) as mic:
#     for chunk in mic.read_chunks():
#         for i in range(RESPEAKER_CHANNELS):
#             to_check[i] = np.max(chunk[i::8])
#             print("canal "+str(i) +": " + str(np.max(chunk[i::8])))

#         if((not_mic != np.argpartition(to_check, 2)).all()):
#             print("\n \n REVISANDO LOS VALORES: \n \n")
#             not_mic = np.argpartition(to_check, 2)
#             print("channels to ignore:")
#             print(not_mic)
#             channel_0 = np.max(not_mic)+1
#             print("Mic channel 0:" + str(channel_0))
        
#         line1.set_ydata(chunk[(channel_0 if (channel_0 <= 7) else channel_0-8)::8])
#         line2.set_ydata(chunk[(1+channel_0 if (1+channel_0 <= 7) else channel_0-7)::8])
#         line3.set_ydata(chunk[(2+channel_0 if (2+channel_0 <= 7) else channel_0-6)::8])
#         line4.set_ydata(chunk[(3+channel_0 if (3+channel_0 <= 7) else channel_0-5)::8])
#         line5.set_ydata(chunk[(4+channel_0 if (4+channel_0 <= 7) else channel_0-4)::8])
#         line6.set_ydata(chunk[(5+channel_0 if (5+channel_0 <= 7) else channel_0-3)::8])

        
#         fig.canvas.draw()
#         fig.canvas.flush_events()
        
#         time.sleep(0.1)

