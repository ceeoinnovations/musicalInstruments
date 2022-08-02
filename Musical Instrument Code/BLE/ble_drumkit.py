import struct
import ble_CBR
import bluetooth
import time
import port
import distance_sensor as ds
import force_sensor as fs
import color_sensor as cs
import imu

NoteOn = 0x90
NoteOff = 0x80
MaxVol = 127
MinVol = 0

#initializing instruments
ride = port.PORTF
crash = port.PORTB
highhat = port.PORTD
snare = port.PORTA
lowtom = port.PORTC
hightom = port.PORTE

package = [0x00,0x00,0x00,0x00,0x00]

def note(cmd,value,volume):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    return struct.pack("bbbbb", package[0], package[1], package[2], package[3], package[4])

def Drumkit():
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySPIKE')

    def on_rx(v):
        print("RX", v)
    
    p.on_write(on_rx)
        
    was_connected = False
    
    while True:
        if p.is_connected():
            #OUR CODE ------------------------------------
            drum = 0
            print("top of loop") 
            if ds.get_distance(crash) < 100: 
                print("crash!")
                drum = 49
            if ds.get_distance(ride) < 100: 
                print("ride!")
                drum = 51
            if fs.get_touch(highhat) == 1:
                time.sleep(0.03)
                if fs.get_force(highhat) < 50:
                    print("high hat! 1")
                    drum = 51
                else: 
                    print("high hat! 2")
                    drum = 42
            if fs.get_touch(snare) == 1:
                print("snare!")
                drum = 38
            if imu.getGesture()[1] == 0:
                print("kick!")
                drum = 36
            if fs.get_touch(hightom) == 1:
                print("high tom!")
                drum = 50
            if cs.get_reflection(lowtom) != 0:
                print("low tom!")
                drum = 43

            if drum != 0:
                p.send(note(NoteOn,drum,MaxVol))
                time.sleep(0.1)
                p.send(note(NoteOff,drum,MinVol))
                time.sleep(0.1)
                drum = 0
         
            time.sleep(0.1)
        else:
            if was_connected:
                break
    
Drumkit()
