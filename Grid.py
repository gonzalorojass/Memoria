import numpy as np
import wave
from treelib import Tree, Node
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

        self.room_partitions = Tree()
        self.room_partitions.create_node(identifier="room", data= self.n)

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

        invXi_Xj = np.zeros((sum(range(self.Mic_Array.mics_n)), recieved_signal[0].size))
        n = 0
        for i in range(0, self.Mic_Array.mics_n-1):
            for j in range (i+1, self.Mic_Array.mics_n):
                Xi_Xj = np.fft.rfft(recieved_signal[i], n = recieved_signal[i].size)*np.conj(np.fft.rfft(recieved_signal[j], n = recieved_signal[j].size))
                peso = 1/(abs(Xi_Xj))
                invXi_Xj[n] = np.fft.irfft(Xi_Xj*peso, n = recieved_signal[0].size)
                n += 1

        return invXi_Xj, fs

    def HSRP(
        self,
        inverted_signal,
        parent_id,
        fs,
        halfs
    ):
        halfs = np.array([(halfs[0]-1)/2, (halfs[1]-1)/2, (halfs[2]-1)/2])
        id_potencia_mayor = None
        potencia_alta = 0

        if self.room_partitions.depth() == 0:
            esquinas_nodo = self.corners(np.array([0,0,0]), halfs)
            self.room_partitions.create_node(identifier="1", parent="room",
            data={
                "halfs": halfs,
                "esquinas": self.corners(np.array([0,0,0]), halfs),
                "potencia": GCC(inverted_signal, esquinas_nodo, self.Mic_Array, fs),
            })

            for i in range(1,8):
                esquinas_nodo = self.corners(self.room_partitions.get_node("1").data["esquinas"][i], halfs)
                self.room_partitions.create_node(identifier=str(i+1), parent="room",
                data={
                    "halfs": halfs,
                    "esquinas": esquinas_nodo,
                    "potencia": GCC(inverted_signal, esquinas_nodo, self.Mic_Array, fs),
                })

        else:
            for i in range(0,8):
                esquinas_nodo = self.corners(self.room_partitions.get_node(parent_id).data["esquinas"][i], halfs)
                self.room_partitions.create_node(identifier=parent_id + str(i+1), parent=parent_id,
                data={
                    "halfs": halfs,
                    "esquinas": esquinas_nodo,
                    "potencia": GCC(inverted_signal, esquinas_nodo, self.Mic_Array, fs),
                })        

        for hoja in self.room_partitions.leaves():
            if potencia_alta < hoja.data["potencia"]:
                potencia_alta = hoja.data["potencia"]
                id_potencia_mayor = hoja.identifier

        
        # TODO: CAMBIAR CONDICION PARA QUE NO SE TERMINE SI EXISTE UNA HOJA A NIVEL MAYOR POR RECORRER        
        if np.prod(halfs) <= 1000:
            self.room_partitions.show()
            return id_potencia_mayor

        # TODO: DEVOLVER EL PUNTO CENTRAL DEL CUBO
        else:
            halfs = self.room_partitions.get_node(id_potencia_mayor).data["halfs"]
            print(halfs)
            id_posicion = self.HSRP(inverted_signal, id_potencia_mayor, fs, halfs)
            return id_posicion

    def corners(
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