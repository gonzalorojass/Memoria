# from Grid import *
from Mic_array import *
from GCC import *
import matplotlib.pyplot as plt

X = np.array([30, 20, 10, 90, 70])
Y = np.array([10, 80, 30, 40, 25])
Z = np.array([40, 50, 30, 50, 70])

XD = np.array([[30,20,40],[50,60,70],[60,60,2]])
print(XD[:,0])

n = ['Pt. 1', 'Pt. 2', 'Pt. 3', 'Pt. 4', 'Pt. 5']

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_title("Points in Space")
ax.set_xlim([0, 100])
ax.set_ylim([0, 100])
ax.set_zlim([0, 100])
ax.scatter(X, Y, Z)

for i, txt in enumerate(n):
    ax.text(X[i],Y[i],Z[i],  '%s' % (txt))
plt.show()