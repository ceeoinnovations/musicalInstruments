import struct
import ble_CBR
import bluetooth
import button
import time
import distance_sensor as ds
import force_sensor as fs
import port

NoteOn = 0x90
NoteOff = 0x80
MaxVol = 127
MinVol = 0
done = lambda : button.button_isPressed(button.BUTTON_RIGHT)[0]
package = [0x00,0x00,0x00,0x00,0x00]
# initialize sensors
slide_distance_sensor = port.PORTC
air_force_sensor = port.PORTE
min_dist = 30
max_dist = 230
positions_min_distances = [min_dist, 50, 70, 100, 135, 170, 198, max_dist]
# B scale from C#3: C#, D#, E, F#, G#, A#, B
# list in opposite order so first position is higher note
note_list = [59, 58, 56, 54, 52, 51, 49]

def choose_note():
    # initialize note int variable (MIDI number)
    note = 0
    
    slide_distance = ds.get_distance(slide_distance_sensor)
    print(slide_distance)
    for i in range(len(positions_min_distances) - 1):
        if slide_distance >= positions_min_distances[i]:
            note = note_list[i] # note list written high notes to low notes
            print(note)
            
    # i.e. once get slide position, choose note by partial based on % of how hard force sensor is pressed
    # could apply at any position? (or should I make trombone easier to play so stays on same note for distances
    ##within a 'position range,' isn't super gradual change in pitch)
         
    #if slide_distance < 6:
        #note = 71
    #elif slide_distance < 10: note = 69
    #elif slide_distance < 14: note = 67
    #elif slide_distance < 18: note = 65
    #elif slide_distance < 22: note = 64
    #else: note = 31
    
    return note
    
def note(cmd,value,volume):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    return struct.pack("bbbbb", package[0], package[1], package[2], package[3], package[4])
    
def Trombone():
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySPIKE')
    
    def on_rx(v):
        print("RX", v)
    
    p.on_write(on_rx)
        
    was_connected = False
    
    note_state = False
    temp_note_state = False
    
    eighth_note = 0.234375 # [s]
    quarter_note = 0.46875 # [s]
    rest_btwn_notes = 0.02 # [s]
    
    while not done():
        if p.is_connected():
            # print("1 - top of if")
            air_force = fs.get_touch(air_force_sensor) # 0 off, 1 pressed / use get_force for 0-10N
            # print(air_force)
            # CHANGE NOTE IF DISTANCE CHANGES
            if air_force and not note_state: # if air_force is 1
                print("2- pressed and not note state (first if)")
                current_note = choose_note()
                #print(current_note)
                p.send(note(NoteOn,current_note,MaxVol))
                note_state = True
                temp_note_state = True
                
                while temp_note_state:
                    print("3- of of while temp_note_state")
                    # check if force still pressed but slide position changes to change note
                    temp_note = choose_note()
                    air_force = fs.get_touch(air_force_sensor)
                    # if slide position changes but force still pressed, turn current note off
                    # loop will go back to outer while not done()
                    if (temp_note != current_note) and (air_force):
                        print("4 - switching notes")
                        p.send(note(NoteOff,current_note,MinVol)) 
                        p.send(note(NoteOn,temp_note,MaxVol))
                        current_note = temp_note
                    if not air_force:
                        print("NOT BEING PRESSED ****** should leave while")
                        temp_note_state = False
                    time.sleep(0.01)

                time.sleep(0.01)
                
            if not air_force and note_state: # air_force is 0
                print("turning off note that was there")
                p.send(note(NoteOff,current_note,MinVol))
                note_state = False
                time.sleep(0.01)
            #was_connected = True
        else:
            if was_connected:
                break
        # rest between if air still played AND if doesn't catch air force
        # ask Samson how it plays new note only when pressed
        time.sleep(0.01)
    
Trombone()