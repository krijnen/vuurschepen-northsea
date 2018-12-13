import os
#import pygrib
import numpy as np
import datetime
import pygrib
from math import *
import numpy.random as npr
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import shiftgrid
from scipy.interpolate import LinearNDInterpolator

class Grib:
  def __init__(self, file = 'gribs/20171128_151424_.grb'):
    self.file = file
    self.gribfile = pygrib.open(file)
    self.interpolator()
    
  def plot(self):
    grb = self.gribfile.select()[0]
    lons = np.linspace(float(grb['longitudeOfFirstGridPointInDegrees']), \
              float(grb['longitudeOfLastGridPointInDegrees']), int(grb['Ni']) )
    lats = np.linspace(float(grb['latitudeOfFirstGridPointInDegrees']), \
                float(grb['latitudeOfLastGridPointInDegrees']), int(grb['Nj']) )
    data = grb.values
    grid_lon, grid_lat = np.meshgrid(lons, lats) #regularly spaced 2D grid
    m = Basemap(projection='cyl', llcrnrlon=lons.min(), \
        urcrnrlon=lons.max(),llcrnrlat=lats.min(),urcrnrlat=lats.max(), \
        resolution='c')
     
    x, y = m(grid_lon, grid_lat)
     
    cs = m.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.gist_stern_r)
     
    m.drawcoastlines()
    m.drawmapboundary()
    m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])
     
    plt.colorbar(cs,orientation='vertical', shrink=0.5)
    plt.title('CAMS AOD forecast') # Set the name of the variable to plot
    plt.savefig('picture.png') # Set the output file name

  def interpolator(self):
    grb = self.gribfile.select()[0]
    lons = np.linspace(float(grb['longitudeOfFirstGridPointInDegrees']), \
              float(grb['longitudeOfLastGridPointInDegrees']), int(grb['Ni']) )
    lats = np.linspace(float(grb['latitudeOfFirstGridPointInDegrees']), \
                float(grb['latitudeOfLastGridPointInDegrees']), int(grb['Nj']) )
    grbU = self.gribfile.select(name='10 metre U wind component')

    grbV = self.gribfile.select(name='10 metre V wind component')
    times = np.linspace(float(grb.P2), float((self.gribfile.select()[-1]).P2), 
            float((self.gribfile.select()[1]).P2 - grb.P2))
    U = np.array([grbU[i].values for i in range(times.size)])
    V = np.array([grbV[i].values for i in range(times.size)])
    print(U.shape)
    points = np.meshgrid(lons, lats, times)
    self.interpolatorU = LinearNDInterpolator(points, U)
    self.interpolatorV = LinearNDInterpolator(points, V)

  def getwind(self, position, time):
    U = self.interpolatorU(position(1), position(2), time)
    V = self.interpolatorV(position(1), position(2), time)
    wind = sqrt(U**2 + V**2)
    winddir = arctan(U/V)*180/pi
    return wind, winddir


if __name__ == '__main__':  
  g = Grib()
  g.plot()
