import time
from Adafruit_I2C import Adafruit_I2C as bus
i2c = bus(0x70)

bus.write8(i2c, 2, 255)
bus.write8(i2c, 1, 0)
locations = {
0: '0-0.35m    (0-352mm)', 
1: '0.35-0.7m  (353-705mm)', 
2: '0.7-1m     (706-1057mm)', 
3: '1-1.4m     (1058-1410mm)', 
4: '1.41-1.76m (1411-1763mm)',
5: '1.76-2.11m (1764-2116mm)', 
6: '2.11-2.36m (2117-2369mm)', 
7: '2.37-2.62m (2370-2622mm)', 
8: '2.62-2.87m (2623-2875mm)', 
9: '2.87-3.22m (2876-3228mm)', 
10: '3.22-3.58m (3229-3581mm)', 
11: '3.58-3.93m (3582-3934mm)', 
12: '3.93-4.28m (3934-4287mm)'   }

while True :
	bus.write8(i2c, 0, 84)
	time.sleep(0.09)
	a = []
	i = 4
	while i < 30 :
		a.append(bus.readU8(i2c, i)) 
		i +=1
	print a
	for index, element in enumerate(a) :		
     		if element == 255:
			print index
			print locations[index]
			break		
	 
