
from OmegaExpansion import onionI2C
from time import sleep


i2c = onionI2C.OnionI2C()

# Configure HTC1080 address : 100 0000
address = 0x40

# Configure 0x02 to both acquire temperature & humidity with 11-bit & 8-bit resolution
# 0001 0110 0000 0000
config = 0x1600

i2c.writeByte(address, 0x02, config)
sleep(0.1)
# Read from 0x00 & 0x01 (2-byte registers)
#To trigger the read, one must beforehand use an empty write on the 0x02 address, however i2c.writeByte won't work
#without a value argument. We may have to rework the onioni2c library to fix that
i2c.writeByte(address,0x02)
sleep(1)
temp=i2c.readBytes(address,0x00,2)
sleep(0.1)


humidbrut=i2c.readBytes(address,0x01,1)
sleep(0.1)


temperature = (float(temp[0]) / float(pow(2,8)))*165 - 40
humidity = (float(humidbrut) / float(pow(2,8)))*100
print (temp[0])
print (temp[1])
print (humidbrut)
print (temperature)
print (humidity)
