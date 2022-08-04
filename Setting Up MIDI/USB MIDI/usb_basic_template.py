# By Chris Rogers, Samson Bienstock, and Rose Kitz
# Comments by Rose Kitz
# FET Lab Summer 2022
# Written for SPIKE 2.0 in PyVIEW

# Using MIDI USB Pico Breadboard set-up and MIDIBerry as a DAW (on a Windows PC, to play real instrument sounds through)
# See README.md for tutorial on how to set up MIDI over USB

import hub, utime
import machine
import time
import ustruct

# Initialize ports (MIDI port and SPIKE sensors as devices)
midi_port = hub.port.E # acts simply as a port, not a device like the SPIKE sensors

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

# Loop to play notes until center button is pressed to end the program
while not hub.button.center.is_pressed():
    
    # ----- THIS IS WHERE YOU SHOULD PUT YOUR MAIN CODE -----
    
    # How to play a note (plays middle C, MIDI Number: 60)
    # Turn note on
    midi_port.write(ustruct.pack("bbb",NoteOn,60,MaxVol))
    time.sleep(0.5)
    
    # Turn note off
    midi_port.write(ustruct.pack("bbb",NoteOff,60,MinVol))
    time.sleep(0.5)
    
    # -------------------------------------------------------
