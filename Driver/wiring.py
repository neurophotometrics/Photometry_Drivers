import spidev
import RPi.GPIO as GPIO
import const
import time
import sys
import wiringpi

bus = 0
device = 0
spi = spidev.SpiDev()
spi.open(bus,device)
spi.max_speed_hz = const.potSpeed
spi.mode = 0

#wiringpi.wiringPiSPISetup(const.selectPin,const.potSpeed)
msg = [0x50]


while (True):
  for i in range(3):
    chan = [i]
    #wiringpi.wiringPiSPIDataRW (const.selectPin, chan) 
    read = spi.xfer2(chan)
    print('1',read)
    time.sleep(0.1)
    #wiringpi.wiringPiSPIDataRW (const.selectPin, msg) 
    read = spi.xfer2(msg)
    print('2',read)
    time.sleep(0.1)




