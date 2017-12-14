

for cube in cubes:
  print(cube.attributes)
  print((cube.interpolate(location, iris.analysis.Nearest())))


indx = pygrib.index('gribs/harmonie_zy_ijmg_wind.grb', 'typeOfLevel', 'level', 'parameterName')
msg = indx.select(level=10, typeOfLevel='heightAboveGround', parameterName="U U-component of wind m s**-1")
u10 = np.array(msg[0].values)





#print(u10)

grb = grbs.read(100)[0]
print(grb)

goal:
policy pi 

episodic environments: start value J1(th) = Vpi0(s1)
from mpl_toolkits.basemap import Basemap
bm = Basemap()
#bm.is_land()
compatible function approximation
