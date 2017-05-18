import numpy as np
from math import *
from scipy import interpolate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class boat(object):
    def __init__(self, theta = 90, v = 1):
        self.theta = theta
        self.dtheta = 0
        self.v = v
        self.trim = 1.
        self.polar = self.load_polar()
        self.windspeed = 10
        self.winddir = 0
        self.update_twa()

    def control(self, rudder, trim):
        self.set_trim(trim)
        self.rudder(rudder)

    def update(self):
        new_state = np.dot(self.Phi(), self.state())
        self.theta = new_state[0]
        self.theta = self.theta % 360
        if (self.theta > 180):
            self.theta -= 360
        self.v = new_state[2]
        self.update_twa()
        return new_state

    def newwind(self, windspeed, winddir):
        self.windspeed = windspeed
        self.winddir = winddir
        self.update_twa()

    def update_twa(self):
        self.twa = self.theta - self.winddir

    def vmg(self):
        return cos(self.twa / 180 * pi) * self.v

    # INPUTS
    def rudder(self, amount):
        if abs(amount) <= 9:
            self.dtheta = amount

    def set_trim(self, amount):
        # Amount 0 < > 1
        if 0 <= amount <= 1:
            self.trim = amount

    # STATES
    def state(self):
        return np.array([self.theta, self.dtheta, self.v, self.dv()])

    def Phi(self):
        return np.array([[1, 1, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 1],
                         [0, 0, 0, 1]])

    def dv(self):
        ref = self.trim * self.maxv()
        k = 0.3
        d = self.dtheta * sin(self.dtheta / 180 * pi) * self.v**2 / 4
        return ((ref - self.v) - d) * k

    def maxv(self):
        return(self.polar(self.windspeed, abs(self.twa)))

    def load_polar(self):
        polar = np.loadtxt("polar.txt")
        wscale = np.array([[0, 44.5, 52, 60, 75, 90, 110, 120, 135, 150, 180],
                           [0, 42.9, 52, 60, 75, 90, 110, 120, 135, 150, 180],
                           [0, 43, 52, 60, 75, 90, 110, 120, 135, 150, 180],
                           [0, 42.1, 52, 60, 75, 90, 110, 120, 135, 150, 180],
                           [0, 40.4, 52, 60, 75, 90, 110, 120, 135, 150, 180],
                           [0, 39.2, 52, 60, 75, 90, 110, 120, 135, 150, 180],
                           [0, 39.5, 52, 60, 75, 90, 110, 120, 135, 150, 180]])

        vscale = np.array([[6, 8, 10, 12, 14, 16, 20]]) * np.ones((11, 1))
        return (interpolate.Rbf(vscale.T, wscale, polar, kind='thin-plate', smooth=.2))

    def plot_polar(self):
        x = np.arange(6, 22.1, 0.1)
        y = np.arange(0, 181, 1)
        xi, yi = np.meshgrid(x, y)
        z = self.polar(xi, yi)
        newx = z * np.cos(yi / 180 * pi)
        newy = z * np.sin(yi / 180 * pi)
        newz = xi

        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_surface(xi, yi, z)
        plt.show()

        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_surface(newx, newy, newz)
        newx = z * np.cos(-yi / 180 * pi)
        newy = z * np.sin(-yi / 180 * pi)
        ax.plot_surface(newx, newy, newz)
        plt.show()

if __name__ == '__main__':
    b = boat()
    b.plot_polar()