# By Rachel Hsin
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

import struct
import ble_CBR
import bluetooth
import button
import time
import distance_sensor
import port
import color_sensor
import force_sensor
import hub
import imu

colors = {
    -1:'ERR',
    0:"LEGO_BLACK",
    1:"LEGO_MAGENTA",
    2:"LEGO_PURPLE",
    3:"LEGO_BLUE",
    4:"LEGO_AZURE",
    5:"LEGO_TURQUOISE",
    6:"LEGO_GREEN",
    7:"LEGO_YELLOW",
    8:"LEGO_ORANGE",
    9:"LEGO_RED",
    10:"LEGO_WHITE",
    11:"LEGO_DIM_WHITE",
}

notes = [60,61,62,63,64,63,62,61]

NoteOn = 0x90
NoteOff = 0x80
MaxVol = 127
MinVol = 0

done = lambda : button.button_isPressed(button.BUTTON_RIGHT)[0]

package = [0x00,0x00,0x00,0x00,0x00]

def note(cmd,value,volume):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    return struct.pack("bbbbb", package[0], package[1], package[2], package[3], package[4])

def Drum():
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySPIKE')

    def on_rx(v):
        print("RX", v)
    
    p.on_write(on_rx)
    
    taps=0
    count=0
        
    was_connected = False
    while not done():
        
        if p.is_connected():
        
            if count%4==1:
                dist=distance_sensor.get_distance(port.PORTF)
                print(dist)
                if dist>55:
                    p.send(note(NoteOn,51,MaxVol))
            
            col=colors[color_sensor.get_color(port.PORTD)]
            #print(col)
            if col=="LEGO_TURQUOISE" or col=="LEGO_BLUE" or col=="LEGO_GREEN":
                if count%3==1:
                    time.sleep_ms(100)          
                    p.send(note(NoteOn,42,MaxVol))
                
            forceB=force_sensor.get_touch(port.PORTE)
            if forceB==1:
                time.sleep_ms(100)
                p.send(note(NoteOn,38,MaxVol))
                
            if force_sensor.get_touch(port.PORTA)<1:
                time.sleep_ms(100)
                p.send(note(NoteOn,51,MaxVol))
                
            if imu.getGesture()[2]>taps:
                p.send(note(NoteOn,36,MaxVol))
                taps=imu.getGesture()[2]
                
            count=count+1
        else:
            if was_connected:
                break
        time.sleep_ms(300)
    
Drum()
