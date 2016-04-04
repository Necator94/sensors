import time
from Adafruit_I2C import Adafruit_I2C as bus
from collections import Counter

i2c = bus(0x70)

bus.write8(i2c, 2, 255)
bus.write8(i2c, 1, 0)

locations = {
0:  '0-0.35m    	(0-352mm)', 
1:  '0.35-0.7m  	(353-705mm)', 
2:  '0.7-1m     	(706-1057mm)', 
3:  '1-1.4m     	(1058-1410mm)', 
4:  '1.41-1.76m 	(1411-1763mm)',
5:  '1.76-2.11m 	(1764-2116mm)', 
6:  '2.11-2.36m 	(2117-2369mm)', 
7:  '2.37-2.62m 	(2370-2622mm)', 
8:  '2.62-2.87m 	(2623-2875mm)', 
9:  '2.87-3.22m 	(2876-3228mm)', 
10: '3.22-3.58m 	(3229-3581mm)', 
11: '3.58-3.93m 	(3582-3934mm)', 
12: '3.93-4.28m 	(3934-4287mm)',
13: '4.28-4.64m 	(4288-4640mm)',
14: '4.64-4.99m 	(4641-4993mm)',
15: '4.99-5.34m 	(4994-5346mm)',
16: '5.34-5.59m 	(5347-5599mm)',
17: '5.6-5.85m  	(5600-5852mm)',
18: '5.85-6.1m  	(5853-6105mm)',
19: '6.1-6.35m  	(6106-6358mm)',
20: '6.35-6.61m 	(6359-6611mm)',
21: '6.61-6.86m 	(6612-6864mm)',
22: '6.86-7.11m 	(6865-7117mm)',
23: '7.11-7.37m 	(7117-7370mm)',
24: '7.37-7.62m 	(7371-7623mm)',
25: '7.62-7.87m 	(7624-7876mm)',
26: '7.87-8.12m 	(7877-8129mm)',
27: '8.13-8.38m 	(8130-8382mm)',
28: '8.38-8.63m 	(8383-8635mm)',
29: '8.63-8.88m 	(8636-8888mm)',
30: '8.88-9.14m 	(8889-9141mm)',
31: '9.14-9.39m  	(9142-9394mm)',
}
k = 0
window = [None] * 15
while True :
	bus.write8(i2c, 0, 84)
	time.sleep(0.07)
	ranging_result = []
	i = 4
	while i < 36 :
		ranging_result.append(bus.readU8(i2c, i)) 
		i +=1
	for index, element in enumerate(ranging_result) :		
     		if element == 255:
			window.insert(0, index)
			del window[-1]
#			print locations[index], '         location index -  ', index
			break		

	print window	



























