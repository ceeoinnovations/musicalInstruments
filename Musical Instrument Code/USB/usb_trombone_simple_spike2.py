# By Chris Rogers, Samson Bienstock, and Rose Kitz
# FET Lab Summer 2022
# Written for SPIKE 2.0 in PyVIEW

# Using MIDI USB Pico Breadboard set-up and MIDIBerry as a DAW (on a Windows PC, to play real instrument sounds through)
# See README.md for tutorial on how to set up MIDI over USB

# Program to play MIDI sounds on a slide instrument
# Uses USB to enable MIDI sounds through a Windows PC (MIDI BLE on Windows currently in progress)
# Program currently plays a C major scale, with one note associated with one of the 7 slide positions (no partials)

import hub, utime
import machine
import time
import ustruct

# Initialize devices
midi_port = hub.port.E # acts simply as a port, not a device like the SPIKE sensors
slide_distance_sensor = hub.port.C.device
air_force_sensor = hub.port.A.device

# Initialize common MIDI variables
NoteOn = 0x90
NoteOff = 0x80
MaxVol = 127
MinVol = 0

# Start MIDI connection
midi_port.mode(hub.port.MODE_FULL_DUPLEX)
midi_port.baud(31250)
# hub.speaker.set_volume(100)
# hub.speaker.beep(80, 0.5)

# Plays a C (to test connection)
midi_port.write(ustruct.pack("bbb",NoteOn,60,MaxVol))
midi_port.write(ustruct.pack("bbb",NoteOff,60,MinVol))

# Initialize variable to track if a note is currently off (0) or on (1)
note_state = 0

# Initialize variable to store MIDI note value
note = None

# Loop to play a note
# Press force sensor to start playing a new note
# Move trombone slide to change the note
while not hub.button.center.is_pressed():

    time.sleep(0.05)
    
    # Get whether force sensor is pressed (1) or not (0)
    air_force = air_force_sensor.get()[1]
    
    # If force sensor is pressed and note is currently off, get slide distance and play a note
    if air_force and note_state == 0 :
        
        # Get current slide distance [cm]
        slide_distance = slide_distance_sensor.get()[0]
        # print("slide_distance:", slide_distance)
        
        # If no slide distance detected, set to 0 to avoid type error
        if slide_distance == None:
            slide_distance = 0
            
        # Set note based on slide distance (C major scale)
        # Greater slide distance = further from distance sensor = longer 'tubing' = lower note
        # Smaller slide distance = closer to distance sensor = shorter 'tubing' = higher note
        
        # Simple hardcode measured distances for each slide position (get with print statements)
        if slide_distance < 4 : note = 72
        elif slide_distance < 5: note = 71
        elif slide_distance < 6: note = 69
        elif slide_distance < 7 : note = 67
        elif slide_distance < 8 : note = 65
        elif slide_distance < 9 : note = 64
        elif slide_distance < 10 : note = 62
        else :  note = 60
            
        # Turn note on
        midi_port.write(ustruct.pack("bbb",NoteOn,note,MaxVol))
        # Report that note is currently on
        note_state = 1
        
    # If force sensor isn't pressed and note is currently on, turn note off
    if (not air_force) and note_state == 1 :
        # Turn note off
        midi_port.write(ustruct.pack("bbb",NoteOff, note, MinVol))
        # Report that note is currently off
        note_state = 0
        
