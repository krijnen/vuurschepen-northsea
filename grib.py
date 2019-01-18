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
from scipy.interpolate import RegularGridInterpolator 


class Grib:
  def __init__(self, file = 'gribs/20171128_151424_.grb'):
    self.file = file
    self.gribfile = pygrib.open(file)
    
  def plot(self, idx = 0, show = False):
    grb = self.gribfile.select()[idx]
    grbU = self.gribfile.select(name='10 metre U wind component')[idx]
    grbV = self.gribfile.select(name='10 metre V wind component')[idx]
    lons = np.linspace(float(grb['longitudeOfFirstGridPointInDegrees']), \
              float(grb['longitudeOfLastGridPointInDegrees']), int(grb['Ni']) )
    lats = np.linspace(float(grb['latitudeOfFirstGridPointInDegrees']), \
                float(grb['latitudeOfLastGridPointInDegrees']), int(grb['Nj']) )
    data = np.sqrt(np.square(grbU.values)+np.square(grbV.values))
    grid_lon, grid_lat = np.meshgrid(lons, lats) #regularly spaced 2D grid
    self.map = Basemap(projection='cyl', llcrnrlon=lons.min(), \
        urcrnrlon=lons.max(),llcrnrlat=lats.min(),urcrnrlat=lats.max(), \
        resolution='c')
     
    x, y = self.map(grid_lon, grid_lat)
     
    cs =self.map.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.rainbow)
    
    self.map.drawcoastlines()
    self.map.drawmapboundary()
    self.map.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
    self.map.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])
     
    plt.colorbar(cs,orientation='vertical', shrink=0.5)
    plt.title('Predicted wind strength') 
    plt.savefig('grib.png')
    if show:
        plt.show()
    plt.close()


  def interpolator(self):
    grb = self.gribfile.select()[0]
    grb1 = self.gribfile.select()[1]
    grb_l = self.gribfile.select()[-1]
    lons = np.linspace(float(grb['longitudeOfFirstGridPointInDegrees']), \
              float(grb['longitudeOfLastGridPointInDegrees']), int(grb['Ni']) )
    lats = np.linspace(float(grb['latitudeOfFirstGridPointInDegrees']), \
                float(grb['latitudeOfLastGridPointInDegrees']), int(grb['Nj']) )
    grbU = self.gribfile.select(name='10 metre U wind component')
    grbV = self.gribfile.select(name='10 metre V wind component')
    times = np.array([i for i,g in enumerate(grbU) if g.values.shape == grb.values.shape])
    U = np.dstack([g.values for g in grbU if g.values.shape == grb.values.shape])
    V = np.dstack([g.values for g in grbV if g.values.shape == grb.values.shape])
    print(lats.shape, lons.shape, times.shape, U.shape)
    if lats[0] > lats[-1]:
        lats = np.flip(lats,0)
        U = np.flip(U, 0)
        V = np.flip(V,0)
    self.interpolatorU = RegularGridInterpolator((lats, lons, times), U)
    self.interpolatorV = RegularGridInterpolator((lats, lons, times), V)

  def getwind(self, p, time):
    U = self.interpolatorU((p.lat, p.lon, time))
    V = self.interpolatorV((p.lat, p.lon, time))
    wind = sqrt(U**2 + V**2)
    winddir = atan2(U,V)*180/pi
    return wind, winddir
  
  def is_land(self,p):
    return self.map.is_land(p.lat, p.lon)


class Position:
    def __init__(p, lat = 0, lon = 0):
      p.lat = lat
      p.lon = lon
      radius = 3440 # earths radius in nm
    def update(p, distance, direction):
      x = distance * sin(direction/180*pi)
      y = distance * cos(direction/180*pi)
      dlat = x / (p.radius * pi * 2) * 360
      dlon = y / (p.radius * pi * 2) * 360
      p.lat += dlat
      p.lon += dlon

if __name__ == '__main__':  
  g = Grib()
  g.plot(show =1)