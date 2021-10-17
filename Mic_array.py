import pyaudio
import queue
import threading
import numpy as np
import math
import Grid

NUMBER_OF_MICROPHONES = 6

class MicArray:
    def __init__(
        self,
        grid: Grid,
        center = np.array([0,0,0]),
        distance_to_center = 5,
        rate = 34000,
        chunk_size = None
    ):
        channels = 6
        self.pyaudio_instance = pyaudio.PyAudio()
        self.queue = queue.Queue()
        self.quit_event = threading.Event()
        self.sample_rate = rate
        self.chunk_size = chunk_size if chunk_size else rate / 100

        
        mic_position = np.zeros((NUMBER_OF_MICROPHONES,3))

        for  i in range(0, NUMBER_OF_MICROPHONES):
            x = math.sin((i*math.pi)/3)*distance_to_center + center[0]
            y = math.cos((i*math.pi)/3)*distance_to_center + center[1]
            mic_position[i, :] = [x, y , center[2]]

        mic_position[abs(mic_position) < 1e-14] = 0

        grid.place_mic_array(center, mic_position)

        device_index = None
        for i in range(self.pyaudio_instance.get_device_count()):
            dev = self.pyaudio_instance.get_device_info_by_index(i)
            name = dev['name'].encode('utf-8')
            print(i, name, dev['maxInputChannels'], dev['maxOutputChannels'])
            if dev['maxInputChannels'] == channels:
                print('Use {}'.format(name))
                device_index = i
                break
        if device_index is None:
            raise Exception('can not find input device with {} channel(s)'.format(channels))

        self.stream = self.pyaudio_instance.open(
            input=True,
            start=False,
            format=pyaudio.paInt16,
            channels= channels,
            rate=int(self.sample_rate),
            frames_per_buffer=int(self.chunk_size),
            stream_callback=self._callback,
            input_device_index=device_index,
        )


    def _callback(self, in_data, frame_count, time_info, status):
        self.queue.put(in_data)
        return None, pyaudio.paContinue

    def start(self):
        self.queue.queue.clear()
        self.stream.start_stream()


    def read_chunks(self):
        self.quit_event.clear()
        while not self.quit_event.is_set():
            frames = self.queue.get()
            if not frames:
                break

            frames = np.fromstring(frames, dtype='int16')
            yield frames

    def stop(self):
        self.quit_event.set()
        self.stream.stop_stream()
        self.queue.put('')

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        if value:
            return False
        self.stop()