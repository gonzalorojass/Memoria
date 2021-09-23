import numpy as np
import wave
from Mic_array import *
from GCC import *

class Grid:
    ####        X,Y,Z se tienen que trabajar en centimetros         ####
    def __init__(
        self,
        x_room = 280,
        y_room = 560,
        z_room = 240,
    ):
        self.x_room = x_room + 1
        self.y_room = y_room + 1
        self.z_room = z_room + 1

        self.n = self.x_room*self.y_room*self.z_room        # CUBO MAS PEQUEÑO 10x10x10 cm POR DEFINIR
        self.points = np.zeros((self.n,3))
        self.place_mic_array(np.array([20,20,10]))
        self.potencia = np.zeros((self.n))


    def place_mic_array(
        self, 
        position, 
    ):
        self.Mic_Array = MicArray(position)


    def place_sound_source(
        self,
        filename,
        position,
        # CHUNK,                   # SE USARA ACTUALMENTE 1 SEGUNDO (CHUNK = fs)
    ):
        if position[0] > self.x_room or position[1] > self.y_room or position[2] > self.z_room:
            print("Posición esta fuera del espacio")
            return
        
        try:
            wf = wave.open(filename, 'r')
            
        except:
            print("Insertar el nombre de un archivo valido")
            return

        c = 34300
        fs = wf.getframerate()
        recieved_signal = np.zeros((self.Mic_Array.mics_n, fs))

        signal = wf.readframes(-1)
        signal = np.frombuffer(signal, dtype=np.int16)   
        left = signal[0::2]             # USO DE UN SOLO CANAL

        for i in range(0, self.Mic_Array.mics_n):

            tau = round(fs*(np.linalg.norm(position-self.Mic_Array.mic_position[i]))/c)
            recieved_signal[i] = left[tau: tau+fs]

        return recieved_signal, fs

    
    def SRP(
        self,
        signal,
        mic_array,
        fs
    ):
        # AGREGAR RUTINA DE DIVICIÓN DEL ESPACIO
        invXi_Xj = np.zeros((sum(range(mic_array.mics_n)), signal[0].size))
        n = 0
        for i in range(0, mic_array.mics_n-1):
            for j in range (i+1, mic_array.mics_n):
                Xi_Xj = np.fft.rfft(signal[i], n = signal[i].size)*np.conj(np.fft.rfft(signal[j], n = signal[j].size))
                peso = 1/(abs(Xi_Xj))
                invXi_Xj[n] = np.fft.irfft(Xi_Xj*peso, n = signal[0].size)
                n += 1

        l = 0
        while l < self.n:
            for k in range(0, self.z_room):
                for j in range(0, self.y_room):
                    for i in range(0, self.x_room):
                        self.points[l] = [i,j,k] 
                        self.potencia[l] = GCC(invXi_Xj, self.points[l], self.Mic_Array, fs)
                        l+=1
        return self.points[np.argmax(abs(self.potencia))] 


    def HSRP(
        self,
        signal,
        mic_array,
        fs
    ):
        halfs = np.array([self.x_room/2, self.y_room/2, self.z_room/2])
        TREE = self.cornerizator(np.array([0,0,0]), halfs)
        if np.prod(halfs) <= 1000:
            print("do it one last time only if big enough")
        invXi_Xj = np.zeros((sum(range(mic_array.mics_n)), signal[0].size))
        n = 0
        for i in range(0, mic_array.mics_n-1):
            for j in range (i+1, mic_array.mics_n):
                Xi_Xj = np.fft.rfft(signal[i], n = signal[i].size)*np.conj(np.fft.rfft(signal[j], n = signal[j].size))
                peso = 1/(abs(Xi_Xj))
                invXi_Xj[n] = np.fft.irfft(Xi_Xj*peso, n = signal[0].size)
                n += 1

        # PRIMERA ITERACIÓN
        halfs = np.array([self.x_room/2, self.y_room/2, self.z_room/2])

        TREE = self.cornerizator(np.array([0,0,0]), halfs)


        self.potencia[i] = GCC(invXi_Xj, self.points[i], self.Mic_Array, fs)    # USAR DATO DEL NODO

        return self.points[np.argmax(abs(self.potencia))] 

    def cornerizator(
        self,
        v0,
        v1
    ):
        esquinas = np.zeros((8,3))
        for i in range(0,8):
            l = format(i, '03b')
            l = np.array([int(l[0]),int(l[1]), int(l[2])])
            esquinas[i] = v0 + l*v1
        
        return esquinas