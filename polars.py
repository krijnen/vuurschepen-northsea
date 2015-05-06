import numpy as np
import matplotlib.pyplot as plt

def main():
	a, a0, w = polars()
	t1,t2,dt, wdir, wspd = [],[],[],[],[]
	routes = route()
	naam, r, ddt = ['vuurschepen', 'north sea'], 0,0
	for route1 in routes:
		xdt = 0
		for i in range (0,1000):
			x,y,z = run(a,a0,w, route1)
			t1.append(x)
			t2.append(y)
			dt.append(int(z))
			if z > 4:
				xdt +=1
		print naam[r], sum(dt) / float(len(dt)), xdt / float(len(dt))
		plt.hist(dt)
		plt.show()
		r+=1


def run(a, a0, w, route):	
	t1,t2=0,0
	for i in range (0, len(route)-1):
		dt1, dt2 = leg(a, a0, route[i,:], w)
		t1 += dt1
		t2 += dt2		
	dt = ((t1 - t2)) * 3600.0 / t1
	return t1,t2,dt

def leg(a, a0, route, w):
	x1 = route[1]
	x2 = route[1]
	v1, t1, v2, t2 = 0,0,0,0	
	while x1 > v1:
		wi = wind(w)
		v1 = velocity(wi, a,route[0])
		v2 = velocity(wi, a0,route[0])
		if x1 > v1:
			t1 += 1
			x1 -= v1
		if x2 > v2:
			t2 += 1
			x2 -= v2
	t1 += x1 / v1
	t2 += x2 / v2
	return t1, t2




def polars():
	a = np.loadtxt("polar.txt")
	a0 = np.loadtxt("polar0.txt")
	w = np.loadtxt("wind.txt")
	return a, a0, w

def wind(w):
	mu, sigma = 14, 8.55
	x = int(abs(np.random.normal(mu,sigma)))+1  #windspeed kts normal distribution
	#x = int(29*np.random.random()) 			#windspeed uniform distribution
	y = np.random.random()
	pw, wdf = w[0,1],w[0,1]
	wdf, i, wdir, dy = 0,0,0,y * 100
	while (y * 100 > wdf):
		i += 1
		if i == len(w):
			i = len(w)-1
		pw = (w[i,1] + w[i-1,1])/2
		dy = y * 100 - wdf
		wdir = w[i,0]
		wdf += w[i,1]
	wind = int(dy/pw * 22.5 + wdir)
	return x, wind			#windspeed, winddir

def route():
	routeNS = np.loadtxt("routeNS.txt")
	routeVS = np.loadtxt("routeVS.txt")
	return routeVS, routeNS

def velocity(wind, polar, leg):
	twa = abs(wind[1] - leg)
	if twa > 180:
		twa = abs(twa-360)
	tws = wind[0]
	wscale = [0,45,52,60,75,90,110,120,135,150,180]
	ws,wd = 0,0
	for i in range(0,len(wscale)):
		if twa > wscale[i]:			
			wd = i
	vscale = [0,6,8,10,12,14,16,20]
	for i in range(0,len(vscale)):
		if tws > vscale[i]:
			ws = i
			

	if 	wd == len(wscale)-1 and ws == len(vscale)-1:
		v = polar[wd,ws]
		

	elif wd == len(wscale)-1:
		v1 = polar[wd,ws]*(vscale[ws+1]-tws)
		v2 = polar[wd,ws+1]*(-vscale[ws]+tws)
		v = (v1+v2)/(vscale[ws+1]-vscale[ws])


	elif ws == len(vscale)-1:
		v1 = polar[wd+1,ws]*(wscale[wd+1]-twa)
		v2 = polar[wd,ws]*(-wscale[wd]+twa)
		v = (v1+v2)/(wscale[wd+1]-wscale[wd])

	else:
		m = 1./((wscale[wd+1]-wscale[wd])*(vscale[ws+1]-vscale[ws]))
		v1 = polar[wd,ws]*(wscale[wd+1]-twa)*(vscale[ws+1]-tws)
		v2 = polar[wd+1,ws]*(-wscale[wd]+twa)*(vscale[ws+1]-tws)
		v3 = polar[wd,ws+1]*(wscale[wd+1]-twa)*(-vscale[ws]+tws)
		v4 = polar[wd+1,ws+1]*(-wscale[wd]+twa)*(-vscale[ws]+tws)
		v = m*(v1+v2+v3+v4)	

	return v



	


if __name__ == "__main__":
	main()
