# By Julia Zelevinsky and Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

import struct
import ble_CBR
import bluetooth
import button, port
import color_sensor as cs
import force_sensor as fs
import time
import display

NoteOn = 0x90
NoteOff = 0x80
MaxVol = 127
MinVol = 0

#initializing sensors
g_color_sensor = port.PORTA
force_sensor = port.PORTB

LEGO_MAGENTA = 1
LEGO_BLUE = 3
LEGO_GREEN = 6
LEGO_RED = 9

# Dictionary mapping number displays
numbers = {
    1: b"\x00\x00d\x00\x00\x00\x00d\x00\x00\x00\x00d\x00\x00\x00\x00d\x00\x00\x00\x00d\x00\x00",
    2: b"\x00ddd\x00\x00\x00\x00d\x00\x00ddd\x00\x00d\x00\x00\x00\x00ddd\x00",
    3: b"\x00ddd\x00\x00\x00\x00d\x00\x00ddd\x00\x00\x00\x00d\x00\x00ddd\x00",
    4: b"\x00d\x00d\x00\x00d\x00d\x00\x00ddd\x00\x00\x00\x00d\x00\x00\x00\x00d\x00",
    5: b"\x00ddd\x00\x00d\x00\x00\x00\x00ddd\x00\x00\x00\x00d\x00\x00ddd\x00",
    6: b"\x00ddd\x00\x00d\x00\x00\x00\x00ddd\x00\x00d\x00d\x00\x00ddd\x00",
}

color_list = [LEGO_MAGENTA, LEGO_BLUE, LEGO_GREEN, LEGO_RED]

done = lambda : button.button_isPressed(button.BUTTON_CENTER)[0]

package = [0x00,0x00,0x00,0x00,0x00]

def note(cmd,value,volume):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    return struct.pack("bbbbb", package[0], package[1], package[2], package[3], package[4])
    
def display_number(string):
    display.display_clear()
    if string == 1:
        display.display_show_image(numbers[1])
    if string == 2:
        display.display_show_image(numbers[2])
    if string == 3:
        display.display_show_image(numbers[3])
    if string == 4:
        display.display_show_image(numbers[4])
    if string == 5:
        display.display_show_image(numbers[5])
    if string == 6:
        display.display_show_image(numbers[6])   
    
def Bass_Guitar():
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySPIKE')

    def on_rx(v):
        print("RX", v)
    
    p.on_write(on_rx)
        
    was_connected = False
    string = 1
    display_number(1)
    
    while True:
        if p.is_connected():
            guitar = 0
            was_released = False
            #OUR CODE ------------------------------------
            color = cs.get_color(g_color_sensor)
            if color == 10: # WHITE
                fret = 4
            elif color == 9:
                fret = 3
            elif color == 4:
                fret = 2
            elif color == 5:
                fret = 1
            else:
                fret = 0
            if button.button_isPressed(button.BUTTON_RIGHT)[0] == 1:
                time.sleep(0.05)
                if string == 6:
                    string = 1
                else:
                    string = string + 1
                 display_number(string)
            if button.button_isPressed(button.BUTTON_LEFT)[0] == 1:
                time.sleep(0.05)
                if string == 1:
                    string = 6
                else:
                    string = string - 1
                display_number(string)
            if string == 1:
                guitar = 40 + fret
            if string == 2:
                guitar = 45 + fret
            if string == 3:
                guitar = 50 + fret
            if string == 4:
                guitar = 55 + fret
            if string == 5:
                guitar = 60 + fret
            if string == 6:
                guitar = 64 + fret                
            if fs.get_touch(force_sensor) == 0:
                guitar = 0         
                was_released = True
            else:
                was_released = False      
            if guitar != 0 and not was_released: 
                p.send(note(NoteOn,guitar,MaxVol))
                time.sleep(0.1)
                p.send(note(NoteOff,guitar,MinVol))
                time.sleep(0.1)
                drum = 0
          
            #was_connected = True
            time.sleep(0.1)
        else:
            if was_connected:
                break
    
Bass_Guitar()
