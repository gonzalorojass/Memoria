# from Grid import *
from Mic_array import *
from GCC import *
import matplotlib.pyplot as plt

POSICIOOOON = np.array([0.1, 0.2, 0.7])

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_title("Points in Space")
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
ax.set_zlim([0, 1])
ax.scatter(0.1, 0.2, 0.5)
ax.scatter(0.6, 0.6, 0.7)
plt.show()