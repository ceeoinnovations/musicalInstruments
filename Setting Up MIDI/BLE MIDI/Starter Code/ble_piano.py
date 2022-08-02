import struct
import ble_CBR
import bluetooth
import time

NoteOn = 0x90
NoteOff = 0x80
MaxVol = 127
MinVol = 0
package = [0x00,0x00,0x00,0x00,0x00]

notes = [60, 62, 64]

#done = lambda : button.button_isPressed(button.BUTTON_RIGHT)[0]

def note(cmd,value,volume):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    return struct.pack("bbbbb", package[0], package[1], package[2], package[3], package[4])

def Piano():
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySPIKE')

    def on_rx(v):
        print("RX", v)
    
    p.on_write(on_rx)
        
    was_connected = False
    
    while True:  
        if p.is_connected(): # WRITE YOUR CODE IN HERE
            for x in notes:
                p.send(note(NoteOn,x,MaxVol))
                time.sleep(0.5)
                p.send(note(NoteOff,x,MinVol))
                time.sleep(0.5)
        else:
            if was_connected:
                break
        time.sleep_ms(1000)
    
Piano()
