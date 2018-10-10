import serial
import io
import re
import time


port = '/dev/ttyACM0'

ser = serial.Serial(port,9600,timeout=1000.0)
print(ser.name)
p = re.compile("\\\\r\\\\n")
i = 0
while (1):
  start= time.time()
  string = 'n'
  string = string + 'C'
  string = string + '20.00'
  string = string + '07.00'
  string = string + '40.00'
  string = string + '73.12'
  string = string + '0'
  string = string.encode('utf-8')  
   
  ser.write(string)
  print("Write time: ",time.time() - start)
  val = ser.readline()
  print(val)
  #time.sleep(1000)









