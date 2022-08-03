import struct
import ble_CBR
import bluetooth
import button
import time
import distance_sensor
import port
import color_sensor
import force_sensor


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

def Flute():
    prevnote=0
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'Flute')

    def on_rx(v):
        print("RX", v)
    
    p.on_write(on_rx)
        
    was_connected = False
    
    while not done():
        if p.is_connected():
            if distance_sensor.get_distance(port.PORTD)<60:
                light1=color_sensor.get_reflection(port.PORTA)
                light2=color_sensor.get_reflection(port.PORTF)
                light3=color_sensor.get_reflection(port.PORTC)
                light4=color_sensor.get_reflection(port.PORTE)
           
                playnote=int(65-2*light1/30-light2/30+light3/30+2*light4/30)
                if playnote!=prevnote:
                    prevnote=playnote
                    p.send(note(NoteOff,playnote,MaxVol))
                    p.send(note(NoteOn,playnote,MaxVol))
                    
                                
                
        
        else:
            if was_connected:
                break
        time.sleep_ms(300)

    
Flute()

