import time
from Adafruit_I2C import Adafruit_I2C as bus
i2c = bus(0x70)

bus.write8(i2c, 0x02, 0xFF)
bus.write8(i2c, 0x01, 0x00)
while True :
	bus.write8(i2c, 0x00, 0x51)
	time.sleep(0.09)
	range1 = bus.readU8(i2c, 0x02) + bus.readU8(i2c, 0x03)
	range2 = bus.readU8(i2c, 0x04) + bus.readU8(i2c, 0x05)
	range3 = bus.readU8(i2c, 0x06) + bus.readU8(i2c, 0x07)
	range4 = bus.readU8(i2c, 0x08) + bus.readU8(i2c, 0x09)
	range5 = bus.readU8(i2c, 0x0a) + bus.readU8(i2c, 0x0b)
	range6 = bus.readU8(i2c, 0x0c) + bus.readU8(i2c, 0x0d)
	range7 = bus.readU8(i2c, 0x0e) + bus.readU8(i2c, 0x0f)
#	range8 = bus.readU8(i2c, 0x08) + bus.readU8(i2c, 0x09)
#	range9 = bus.readU8(i2c, 0x08) + bus.readU8(i2c, 0x09)
#	range10 = bus.readU8(i2c, 0x08) + bus.readU8(i2c, 0x09)
	print range1, range2, range3, range4, range5, range6, range7
	time.sleep(0.09)
	bus.write8(i2c, 0x00, 0x54)
	time.sleep(0.09)
	range1 = bus.readU8(i2c, 0x02) + bus.readU8(i2c, 0x03)
	range2 = bus.readU8(i2c, 0x04) + bus.readU8(i2c, 0x05)
	range3 = bus.readU8(i2c, 0x06) + bus.readU8(i2c, 0x07)
	range4 = bus.readU8(i2c, 0x08) + bus.readU8(i2c, 0x09)
	range5 = bus.readU8(i2c, 0x0a) + bus.readU8(i2c, 0x0b)
	range6 = bus.readU8(i2c, 0x0c) + bus.readU8(i2c, 0x0d)
	range7 = bus.readU8(i2c, 0x0e) + bus.readU8(i2c, 0x0f)
#	range8 = bus.readU8(i2c, 0x08) + bus.readU8(i2c, 0x09)
#	range9 = bus.readU8(i2c, 0x08) + bus.readU8(i2c, 0x09)
#	range10 = bus.readU8(i2c, 0x08) + bus.readU8(i2c, 0x09)
	print range1, range2, range3, range4, range5, range6, range7, 'ANN'
