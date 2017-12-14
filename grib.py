import os
#import pygrib
import numpy as np
import datetime
import iris_grib
import iris
from math import *
import numpy.random as npr
from timeit import default_timer as timer


#grbs = pygrib.open('gribs/harmonie_zy_ijmg_wind.grb')
#for g in grbs:
#  print(g.time)
  #print(g.latlons())


class Grib:
  def __init__(self, file = 'gribs/20171128_151424_.grb'):
    self.file = file
    self.cubes = self._cubes()
    self.dict = {}
    
    
  def _cubes(self):
    cubes = list(iris_grib.load_cubes(self.file))
    cubes = iris.cube.CubeList(cubes)
    cubes = cubes.merge()
    cubes = cubes.merge()
    return cubes

  def get_wind(self, time, location):
    if not time in self.dict:
      point = [('time', time)]
      x = grb.cubes[2].interpolate(point, iris.analysis.Nearest())
      y = grb.cubes[4].interpolate(point, iris.analysis.Nearest())
      self.dict[time] = [x,y]
    point = [('longitude', location.lon), ('latitude', location.lat)]
    x = self.dict[time][0].interpolate(point, iris.analysis.Linear()).data
    y = self.dict[time][1].interpolate(point, iris.analysis.Linear()).data
    return (x,y)


class Location:
  def __init__(self, lon, lat):
    # init lon and lat in degrees
    self.lon = lon
    self.lat = lat

  def angle_to(self, loc1):
    # in degr from north
    dx = loc1.lon - self.lon
    dy = loc1.lat - self.lat
    return atan2(dx,dy)*180/pi % 360

  def angle_from(self, loc1):
    # in degr
    dx = loc1.lon - self.lon
    dy = loc1.lat - self.lat
    return atan2(-dx,-dy)*180/pi % 360

  def dist_to(self, loc1):
    # in nm
    dx = loc1.lon - self.lon
    dy = loc1.lat - self.lat
    return sqrt(dx**2 + dy**2) * 60

  def move(self, hdg, speed, t=1):
    #speed in nm, hdg in degrees
    dx = speed / 60. * t * sin(hdg/180*pi)
    dy = speed / 60. * t * cos(hdg/180*pi)
    self.lon = self.lon + dx
    self.lat = self.lat + dy


def route(start, end):
  length = start.dist_to(end)
  print(start.angle_from(end))
  n_nodes = 10
  bearings = np.multiply(npr.randn(n_nodes,2), np.array([90, length/n_nodes/4]) * np.ones((n_nodes, 2))) + (np.array([start.angle_to(end), length/n_nodes])) * np.ones((n_nodes, 2))
  #print (nodes)
  #nodes= list(n_nodes)
  for hdg, dist in bearings:
    print(hdg, dist)



start = Location(lon = -9, lat = 38) #Lisboa
end = Location(lon=18.43, lat = -33.97) #CapeTown

route(start, end)




time1 = timer()
grb = Grib()
print('start')
time2 = timer()
print(time2-time1)

time3 = timer()
print(grb.get_wind(0, end))
time4 = timer()
print(grb.get_wind(0, start))
time5 = timer()
print(time4 - time3, time5-time4)

"""

location = [('time', 0), ('longitude', 0), ('latitude', 0)]
print(grb.cubes[0].interpolate(location, iris.analysis.Nearest()).data)
print(grb.cubes[1].interpolate(location, iris.analysis.Nearest()).data)
print(grb.cubes[2].interpolate(location, iris.analysis.Nearest()).data)
print(grb.cubes[3].interpolate(location, iris.analysis.Nearest()).data)
print(grb.cubes[4].interpolate(location, iris.analysis.Nearest()).data)
print(grb.cubes[5].interpolate(location, iris.analysis.Nearest()).data)
print(grb.cubes[2].interpolate(location, iris.analysis.Nearest()).data)
#print(grb.cubes[4].interpolate(location, iris.analysis.Nearest()).summary(shorten=True) """