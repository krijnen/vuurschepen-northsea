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

    def loadQs(self):
        try:
            self.Q_vmg_up = np.load('Qs.npy')
        except:
            self.Q_vmg_up = np.zeros((360, 100, 16, 19))

    def saveQs(self):
        np.save('Qs.npy', self.Q_vmg_up)

    def get_action(self, twa, v, ws, vmg):
        self.update_Q(vmg)

        #Qs = full_Q()
        action = int(18 * (random.random() - 0.5))
        a = np.array([[int(twa + 179), int(v * 10),
                          int(ws), int(action+9)]])
        self.history = np.concatenate((a, self.history[0:-1, :]))
        return action

    def update_Q(self, vmg):
        self.Q_vmg_up[self.history] = self.Q_vmg_up[self.history] * (1-self.j) + vmg * self.j


    def full_Q(self):
        ind = np.nonzero(self.Q_vmg_up)
        Q = self.Q_vmg_up[ind]
        print(Q.shape)
        ind = np.transpose(ind)
        print(Q)
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
        Qs = self.full_Q()
        b = timer()
        print(b-a)
        xi, yi = np.meshgrid(x, y)
        o = np.ones(xi.shape)
        z = Qs(xi, o*5, o*10, yi)
        ax.plot_surface(xi, yi, z)
        plt.show()


if __name__ == '__main__':
    s = sailor()
    s.show_Q()


"""        try:
            self.Q_vmg_down = Qs['Q_vmg_down']
        except:
            self.Q_vmg_down = np.zeros((360, 100, 16, 19))
        try:
            self.Q_vmg_mark = Qs['Q_vmg_mark']
        except:
            self.Q_vmg_mark = np.zeros((360, 100, 360))
"""
