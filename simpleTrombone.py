import struct
import ble_CBR
import bluetooth
import button, port
import distance_sensor as ds
import force_sensor as fs
import time, math

NoteOn = 0x90
NoteOff = 0x80
MaxVol = 127
MinVol = 0
done = lambda : button.button_isPressed(button.BUTTON_CENTER)[0]

#initializing sensors
slide_distance_sensor = port.PORTD
air_force_sensor = port.PORTF

#defining variables
min_dist = 50 # what's the closest == CHANGE THESE
max_dist = 120 # what's the farthest == CHANGE THESE
positions_min_distances = [min_dist, 60, 70, 82, 95, max_dist] # --> Start/ranges of each position
note_list = [71, 69, 67, 65, 64] # corresponding MIDI notes
partialNumber = 0

package = [0x00,0x00,0x00,0x00,0x00]

def note(cmd,value,volume):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    return struct.pack("bbbbb", package[0], package[1], package[2], package[3], package[4])

# gets a slide distance and then goes through and compares if the current distance is more than the min 
#for each to get correct note
def choose_note():
    print("\n ----------- START OF NEW NOTE ------------")
    # Trombone notes by positions (lowest notes 5th position to highest notes 1st position)
    # uppercase is natural notes, lowercase is sharped notes
    notes_by_position_letters = [['A2', 'E3', 'A3', 'c4', 'E4'], ['g2', 'd3', 'g3', 'C4'], ['G2', 'D3', 'G3', 'B3'], ['f2', 'c3', 'f3'], ['F2', 'C3'],]


    # initialize note int variable (MIDI number)
    our_note = 0

    # get distance
    slide_distance = ds.get_distance(slide_distance_sensor)

    # define end bounds
    if slide_distance < min_dist:
      slide_distance = min_dist
    if slide_distance > max_dist:
      slide_distance = max_dist
      
   # print("Slide distance: ", slide_distance)
    
    positionNumber = 0
    i = 0
    
    # find which position we're in 
    for i in range(len(positions_min_distances) - 1):
        if slide_distance >= positions_min_distances[i]:
          positionNumber = i

    # initialize array of partials and determine the amount of partials per position
    partialList = notes_by_position_letters[positionNumber]
    numPartials = len(partialList)

    # get force from force sensor  (0 -100)
    force = fs.get_force(air_force_sensor)

    if force == 100:
      force = 99

    # determine how much force is needed for each partial
    intervalAmount = math.floor(100 / numPartials)

    # identifies which partial we are at
    partial = math.floor(force / intervalAmount) 
    print("Partial: ", partial)

    # finds correct partial from set of partials for that position
    our_note = partialList[partial]
    print("Our note: ", our_note)

    #print("Chosen note: ", our_note)
    # converts note to MIDI number
    our_note = note_letter_to_midi_number(our_note)

    return our_note
    
def note_letter_to_midi_number(note_letter):
    notes_letters_and_midi = [['A0', 21], ['a0', 22], ['B0', 23], ['C1', 24], ['c1', 25], ['D1', 26], ['d1', 27], ['E1', 28], ['F1', 29], ['f1', 30], ['G1', 31], ['g1', 32], ['A1', 33], ['a1', 34], ['B1', 35], ['C2', 36], ['c2', 37], ['D2', 38], ['d2', 39], ['E2', 40], ['F2', 41], ['f2', 42], ['G2', 43], ['g2', 43], ['A2', 45], ['a2', 46], ['B2', 47], ['C3', 48], ['c3', 49], ['D3', 50], ['d3', 51], ['E3', 52], ['F3', 53], ['f3', 54], ['G3', 55], ['g3', 56], ['A3', 57], ['a3', 58], ['B3', 59], ['C4', 60], ['c4', 61], ['D4', 62], ['d4', 63], ['E4', 64], ['F4', 65], ['f4', 66], ['G4', 67], ['g4', 68], ['A4', 69], ['a4', 70], ['B4', 71], ['C5', 72], ['c5', 73], ['D5', 74], ['d5', 75], ['E5', 76], ['F5', 77], ['f5', 78], ['G5', 79], ['g5', 80], ['A5', 81], ['a5', 82], ['B5', 83], ['C6', 84], ['c6', 85], ['D6', 86], ['d6', 87], ['E6', 88], ['F6', 89], ['f6', 90], ['G6', 91], ['g6', 92], ['A6', 93], ['a6', 94], ['B6', 95], ['C7', 96], ['c7', 97], ['D7', 98], ['d7', 99], ['E7', 100], ['F7', 101], ['f7', 102], ['G7', 103], ['g7', 104], ['A7', 105], ['a7', 106], ['B7', 107], ['C8', 108], ['c8', 109], ['D8, 110'], ['d8', 111], ['E8', 112], ['F8', 113], ['f8', 114], ['G8', 115], ['g8', 116], ['A8', 117], ['a8', 118], ['B8', 119], ['C9', 120], ['c9', 121], ['D9', 122], ['d9', 123], ['E9', 124], ['F9', 125], ['f9', 126], ['G9', 127]]
    midi_num = 0 
    for note in notes_letters_and_midi:
      if note_letter in note[0]: 
        midi_num = note[1]
    return midi_num


def Trombone():
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySPIKE')

    def on_rx(v):
        print("RX", v)
    
    p.on_write(on_rx)
        
    was_connected = False
    
    while True:
        if p.is_connected():
            air_force = fs.get_touch(air_force_sensor) # 0 off, 1 pressed / use get_force for 0-10N
            print("Force sensor: ", air_force)
            if air_force == 1:
                current_note = choose_note()
                print(current_note)
                p.send(note(NoteOn,current_note,MaxVol))
                time.sleep(0.25)
                p.send(note(NoteOff,current_note,MinVol))
                print("//////////////////////////////////")
                time.sleep(0.25)
            #was_connected = True
        else:
            if was_connected:
                break
        time.sleep_ms(100)

Trombone()
