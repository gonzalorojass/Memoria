import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024*4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate= RATE,
    input = True,
    output = True,
    frames_per_buffer = CHUNK
)

fig, ax = plt.subplots(1, figsize=(15, 7))
x = np.arange(0, 2 * CHUNK, 2)

# create a line object with random data
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)

# basic formatting for the axes
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('volume')
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)

plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

# show the plot
plt.show(block=False)

while True:
    data = stream.read(CHUNK)  
       
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    data_np = np.array(data_int, dtype='b')[::2] +128
    
    line.set_ydata(data_np) 
    fig.canvas.draw()
    fig.canvas.flush_events()

