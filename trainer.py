import sailor as s
import boat as b
import random
from timeit import default_timer as timer

def episode(boat, sailor):
    for i in range(100):
        rudder = sailor.get_action(
            boat.twa, boat.v, boat.windspeed, boat.vmg())
        boat.control(rudder, 1)
        boat.update()
    sailor.saveQs()

for i in range(100):
    sailor = s.sailor()
    boat = b.boat(theta=int((random.random() - 0.5) * 180))
    episode(boat, sailor)

