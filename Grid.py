import numpy as np
from copy import deepcopy
from treelib import Tree

NUMBER_OF_MICROPHONES = 6
SOUND_SPEED = 34300

class Grid:
    def __init__(
        self,
        x_room = 280,
        y_room = 560,
        z_room = 240,
    ):
        self.dimensiones = np.array([x_room, y_room, z_room])
        self.margin_dimensions = np.array([x_room, y_room, z_room])

    def HSRP(
        self,
        inverted_signal,
        parent_id,
        fs,
        to_divide = None
    ):
        if to_divide is None:
            to_divide = self.margin_dimensions
        to_divide = np.array([(to_divide[0])/2, (to_divide[1])/2, (to_divide[2])/2])
        id_potencia_mayor = None
        potencia_alta = 0

        if self.temporal_partitions.depth() == 0:
            esquinas_nodo = self.corners(self.temporal_partitions.get_node("room").data["esquinas"][0], to_divide)
            self.temporal_partitions.create_node(identifier="1", parent="room",
            data={
                "to_divide": to_divide,
                "esquinas": esquinas_nodo,
                "potencia": self.power(inverted_signal, esquinas_nodo, self.mic_position, fs),
            })

            for i in range(1,8):
                esquinas_nodo = self.corners(self.temporal_partitions.get_node("1").data["esquinas"][i], to_divide)
                self.temporal_partitions.create_node(identifier=str(i+1), parent="room",
                data={
                    "to_divide": to_divide,
                    "esquinas": esquinas_nodo,
                    "potencia": self.power(inverted_signal, esquinas_nodo, self.mic_position, fs),
                })
        else:
            esquinas_nodo_padre = self.corners(self.temporal_partitions.get_node(parent_id).data["esquinas"][0], to_divide)
            for i in range(0,8):
                esquinas_nodo = self.corners(esquinas_nodo_padre[i], to_divide)
                self.temporal_partitions.create_node(identifier=parent_id + str(i+1), parent=parent_id,
                data={
                    "to_divide": to_divide,
                    "esquinas": esquinas_nodo,
                    "potencia": self.power(inverted_signal, esquinas_nodo, self.mic_position, fs),
                })

        for hoja in self.temporal_partitions.leaves():
            if potencia_alta < hoja.data["potencia"]:
                potencia_alta = hoja.data["potencia"]
                id_potencia_mayor = hoja.identifier
  
        if np.prod(self.temporal_partitions.get_node(id_potencia_mayor).data["to_divide"]) <= 1000:
            centro = self.temporal_partitions.get_node(id_potencia_mayor).data["esquinas"][0] + self.temporal_partitions.get_node(id_potencia_mayor).data["to_divide"]/2
            return id_potencia_mayor, centro

        else:
            new_to_divide = self.temporal_partitions.get_node(id_potencia_mayor).data["to_divide"]
            id_posicion, centro = self.HSRP(inverted_signal, id_potencia_mayor, fs, new_to_divide)
            return id_posicion, centro

    def place_mic_array(
    self, 
    position,
    mic_position
    ):
        self.mic_position = mic_position
        mic_margin = position + np.array([0,100,0])
        self.margin_dimensions[1] = self.dimensiones[1] - mic_margin[1]
        self.margin_dimensions[2] = self.dimensiones[2] - mic_margin[2]

        self.room_partitions = Tree()
        esquinas_raiz = self.corners(np.array([0,mic_margin[1],mic_margin[2]]), self.margin_dimensions)
        self.room_partitions.create_node(identifier="room", data={
                    "to_divide": self.margin_dimensions,
                    "esquinas": esquinas_raiz,
                })
        self.temporal_partitions = deepcopy(self.room_partitions)

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

    def reset_tree(self, count):
        self.temporal_partitions.save2file("tree"+str(count)+".txt")
        self.temporal_partitions = deepcopy(self.room_partitions)

    def power(
        correlated,
        corners_to_check,
        mic_position,
        fs = 44100,
    ):
        potencia = 0
        if isinstance(correlated, np.ndarray):
            n=0
            for i in range(0, NUMBER_OF_MICROPHONES-1):
                for j in range (i+1, NUMBER_OF_MICROPHONES):
                    for corner in corners_to_check:
                        tau = -round(fs*(np.linalg.norm(corner-mic_position[i]) -
                        np.linalg.norm(corner-mic_position[j]))/SOUND_SPEED)

                        if((corner == corners_to_check[0]).all()):
                            tau_min = tau_max = tau

                        if tau < -(correlated[n].size):
                            tau = tau + correlated[n].size
                        if tau < 0:
                            tau = tau-1

                        if tau < tau_min:
                            tau_min = tau
                        if tau > tau_max:
                            tau_max = tau

                    for k in range(int(tau_min), int(tau_max)+1):
                        potencia += np.real(correlated[n][k])

                    n = n + 1

            return potencia

        else:
            print("Correlated debe ser del tipo numpy.ndarray")
            return None

    def GCC(
    mic_data,
    mic_n,
    ):
        invXi_Xj = np.zeros((sum(range(mic_n)), mic_data[0].size))
        n = 0
        for i in range(0, mic_n-1):
            for j in range (i+1, mic_n):
                
                Xi_Xj = np.fft.rfft(mic_data[i], n = mic_data[i].size)*np.conj(np.fft.rfft(mic_data[j], n = mic_data[j].size))
                peso = 1/(abs(Xi_Xj))
                invXi_Xj[n] = np.fft.irfft(Xi_Xj*peso, n = mic_data[0].size)
                n += 1