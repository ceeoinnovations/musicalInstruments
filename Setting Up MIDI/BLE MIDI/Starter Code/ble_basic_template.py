# Written for Atlantis
# Code by Chris Rogers
# Comments by Anna Quiros and Rose Kitz

import struct
import ble_CBR
import bluetooth
import button
import time

# Initialize common values as variables
NoteOn = 0x90
NoteOff = 0x80
MaxVol = 127
MinVol = 0

# Initialize button that ends program
# Can change to any desired button, e.g. BUTTON_CENTER, BUTTON_LEFT
done = lambda : button.button_isPressed(button.BUTTON_RIGHT)[0]
    
# Initialize package for MIDI note
package = [0x00,0x00,0x00,0x00,0x00]

# Packages up the MIDI command   
def note(cmd,value,volume):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    return struct.pack("bbbbb", package[0], package[1], package[2], package[3], package[4])

def Instrument():
    # Don't change this stuff, it's related to the ble_CBR and ble_advertising files
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySPIKE')
    def on_rx(v):
        print("RX", v)
    p.on_write(on_rx)
    was_connected = False

    # Loop to play notes until right button is pressed to end the program
    while not done():
        # Check that hub is still connected to MIDI software to play notes
        if p.is_connected():
            
            # THIS IS WHERE YOU SHOULD PUT YOUR MAIN CODE *******************************************

              # How to play a note (plays middle C, MIDI Number: 60)
              p.send(note(NoteOn,60,MaxVol))
              time.sleep(0.5)
              p.send(note(NoteOff,60,MinVol))
              time.sleep(0.5)                
        
          # If hub is not connected...                    
        else:
            if was_connected:
                break
        
        # Edit this to make your loop run faster / slower, in milliseconds
        time.sleep_ms(1000)
    
Instrument()