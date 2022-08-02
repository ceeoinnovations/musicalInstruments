from time import sleep as sl
from hub import sound as s
from hub import button as b
from hub import display as d
from spike import ForceSensor
import uasyncio as ua

d.clear()
d.pixel(0,0,10)
d.pixel(1,0,10)
d.pixel(2,0,10)
d.pixel(3,0,10)
d.pixel(4,0,10)
sl(.5)
d.clear()
sl(.5)

red = ForceSensor('A') # C
yellow = ForceSensor('B') # E
green = ForceSensor('C') # F
blue = ForceSensor('D') # A
purple = ForceSensor('E') # B

C_val = 523 # red
D_val = 587
E_val = 659 # yellow
F_val = 698 # green 
G_val = 783
A_val = 880 # blue
B_val = 987 # purple

# def ramp(freq,vol):
#    print('ramping')

# for i in range(90):
#    s.beep(800+i,100,0)
#    sl(.008)

async def thingy(note):
    for i in range(10):
        vol = 10 - i
        s.volume(vol)
        s.beep(note,350,0)
        await ua.sleep(.025)


async def main():
    while True:
        if red.is_pressed():
            print('C')
            ua.create_task(thingy(C_val))
        if yellow.is_pressed():
            print('E')
            ua.create_task(thingy(E_val))
        if green.is_pressed():
            print('F')
            ua.create_task(thingy(F_val))
        if blue.is_pressed():
            print('A')
            ua.create_task(thingy(A_val))
        if purple.is_pressed():
            print('B')
            ua.create_task(thingy(B_val))
        await ua.sleep(.03)

ua.run(main())
