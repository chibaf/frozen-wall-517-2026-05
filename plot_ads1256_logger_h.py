import ADS1256
from datetime import date
import time
import matplotlib.pyplot as plt
import serial
import os
import RPi.GPIO as GPIO

ssr_pin11 =11
ssr_pin12 =12
ssr_pin16 =16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ssr_pin11,GPIO.OUT)
GPIO.setup(ssr_pin12,GPIO.OUT)
GPIO.setup(ssr_pin16,GPIO.OUT)

from read_m5_class import m5logger
from ads1256_class import read_ads1256

today = date.today()
t=time.localtime()
current_time=time.strftime("_H%H_M%M_S%S",t)
fn="AL_"+str(today)+current_time+".csv"
f=open(fn,'w',encoding="utf-8")
start = time.time()

ldata0=[0]*10
ldata=[ldata0]*10
ser1 = serial.Serial("/dev/ttyACM0",19200)
#ser2 = serial.Serial("/dev/ttyACM1",19200)
#ser2 = serial.Serial("/dev/ttyUSB0",115200)
ads1256=read_ads1256()
sport=m5logger()

data0=[0]*8
data=[data0]*10
data02=[0]*10
data2=[data02]*10

path = './going.txt'

while True:
#  is_file = os.path.isfile(path)
#  if is_file:
#    continue
#  else:
#    print("stop this proram")
#    GPIO.output(ssr_pin11, False)
#    GPIO.output(ssr_pin12, False)
#    GPIO.output(ssr_pin16, False)
#    f.close()
#    ser1.close()
#    ser2.close()
#    exit()
  try:
    ttime=time.time()-start
    if ttime<0.001:
      ttime=0.0
    st=time.strftime("%Y %b %d %H:%M:%S", time.localtime())
    ss=str(time.time()-int(time.time()))
    rttime=round(ttime,2)
    array=ads1256.read(ser1)
#    array2=sport.read_logger(ser2)
    ss=st+ss[1:5]+","+str(rttime)+","
    for i in range(0,len(array)-1):
      ss=ss+str(array[i])+","
    ss=ss+str(array[len(array)-1])
#    for i in range(0,len(array2)-1):
#      ss=ss+str(array2[i])+","
#    ss=ss+str(array2[len(array2)-1])+"\n"
#    f.write(ss)
    print(ss)
    data.pop(-1)
#    data2.pop(-1)
    data.insert(0,array)
#    data2.insert(0,array2)
    rez = [[data[j][i] for j in range(len(data))] for i in range(len(data[0]))]
#    rez2 = [[data2[j][i] for j in range(len(data2))] for i in range(len(data2[0]))]
    x=range(0, 10, 1)
    plt.figure(100)
    plt.clf()
    plt.ylim(-1.0,5.0)
    lin=[0]*8
    h1=[]
    for i in range(0,8):
     lin[i],=plt.plot(x,rez[i],label="A"+str(i))
    for i in range(0,8):
      h1.append(lin[i])
    plt.legend(handles=h1)
    plt.pause(0.1)
#    plt.figure(200)
#    plt.clf()
#    plt.ylim(-25,30)
#    tl=[0]*10
#    h2=[]
#    for i in range(0,10):
#     tl[i],=plt.plot(x,rez2[i],label="T"+str(i))
#    for i in range(0,10):
#      h2.append(tl[i])
#    plt.legend(handles=h2)
#    plt.pause(0.1)
  except KeyboardInterrupt:
    f.close()
    ser1.close()
    ser2.close()
    exit()
