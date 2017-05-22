import numpy as np
from math import *
import random
from scipy import interpolate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from timeit import default_timer as timer
from scipy.ndimage.filters import convolve, gaussian_filter

class sailor(object):
    def __init__(self):
        self.loadQs()
        self.history = np.zeros((20, 4), dtype=int)
        self.j = np.array([0.8 ** i for i in range(len(self.history[:,1]))])
        self.e = 0.05                               #fraction of random actions

    def loadQs(self):
        try:
            self.Q_vmg_up = np.load('Qs.npy')
        except:
            self.Q_vmg_up = np.zeros((360, 100, 16, 19))

    def saveQs(self):
        np.save('Qs.npy', self.Q_vmg_up)

    def get_action(self, twa, v, ws, vmg):
        self.update_Q(vmg)

        Qs = local_Q(np.array([twa, v, ws]))
        best = np.argmax(np.array([Qs(twa, v, ws, i) for i in range(19)]))
        action = best if random.random()>(1-self.e) else int(18 * (random.random() - 0.5))
        a = np.array([[int(twa + 179), int(v * 10),
                          int(ws), int(action+9)]])
        self.history = np.concatenate((a, self.history[0:-1, :]))
        return best

    def update_Q(self, vmg):
        self.Q_vmg_up[self.history] = self.Q_vmg_up[self.history] * (1-self.j) + vmg * self.j

    def local_Q(self, loc):
        a = timer()
        k = 0.01
        dim = np.array([360, 100, 16, 19])     
        for j in range(100):
            slice1 = loc - j * k * dim[0:3] - 1
            slice1[slice1<0] = 0
            slice2 = loc + j * k * dim[0:3] + 1
            for i in range(3): 
                if slice2[i] > dim[i]: slice2[i] = dim[i]
            ind = np.nonzero(self.Q_vmg_up[int(slice1[0]):int(slice2[0]),int(slice1[1]):int(slice2[1]),int(slice1[2]):int(slice2[2]),0:18])
            ids = np.transpose(ind)
            if ids.size > 100:
                break
        for i in range(3): 
            for j in range(len(ind[i])):
                ind[i][j] += int(slice1[i])
        ids = np.transpose(ind)
        Qs = (interpolate.Rbf(ids[:,0], ids[:,1], ids[:,2], ids[:,3], self.Q_vmg_up[ind], kind='cubic'))
        b = timer()
        #print(b-a)
        return Qs, slice1, slice2

    def full_Q(self):
        ind = np.nonzero(self.Q_vmg_up)
        Q = self.Q_vmg_up[ind]
        ind = np.transpose(ind)
        Qs = (interpolate.Rbf(ind[:,0], ind[:,1], ind[:,2], ind[:,3], Q, kind='cubic'))
        return Qs

    def show_Q(self):
        fig = plt.figure()
        ax = Axes3D(fig)
        #v = np.arange(0, 100, 1)
        #for vb in v:
        x = np.arange(-9, 10, 1)
        y = np.arange(-180, 180, 1)
        a = timer()
        Qs, s1,s2 = self.local_Q([45,4,10])
        b = timer()
        #print(b-a)
        xi, yi = np.meshgrid(x, y)
        o = np.ones(xi.shape)
        z = Qs(xi, o*5, o*10, yi)
        ax.plot_surface(xi, yi, z)
        plt.show()


if __name__ == '__main__':
    s = sailor()
    Qs, s1, s2 = s.local_Q(np.array([45,4,10]))
    #Qs2 = s.full_Q()
    print(Qs(45,4,10,0))
    #print(Qs2(45,4,10,0))
    #s.show_Q()
    print(np.argmax(np.array([Qs(45, 4, 10,i) for i in range(19)])))




"""        try:
            self.Q_vmg_down = Qs['Q_vmg_down']
        except:
            self.Q_vmg_down = np.zeros((360, 100, 16, 19))
        try:
            self.Q_vmg_mark = Qs['Q_vmg_mark']
        except:
            self.Q_vmg_mark = np.zeros((360, 100, 360))
"""
