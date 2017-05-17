import numpy as np
from math import *


class sailor(object):
    def __init__(self):
        self.loadQs()

    def loadQs(self):
        try:
            Qs = np.load('Qs.npz')
        except:
            pass
        try:
            self.Q_vmg_up = Qs['Q_vmg_up']
        except:
            self.Q_vmg_up = zeros(360, 100, 16)
        try:
            self.Q_vmg_down = Qs['Q_vmg_down']
        except:
            self.Q_vmg_down = zeros(360, 100, 16)
        try:
            self.Q_vmg_mark = Qs['Q_vmg_mark']
        except:
            self.Q_vmg_mark = zeros(360, 100, 360)

    def saveQs(self):
        np.savez('Qs.npz', Q_vmg_up=self.Q_vmg_up,
                 Q_vmg_down=self.Q_vmg_down, Q_vmg_mark=self.Q_vmg_mark)

