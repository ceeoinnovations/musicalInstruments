import struct
import ble_CBR
import bluetooth
import button
import time
import display
import math

import color_sensor as cs
import distance_sensor as ds
import port

time_between_note_loops = 10 # ms (see at end of Violin() loop)

# Initialize common inputs for note package to send over BLE MIDI
NoteOn = 0x90
NoteOff = 0x80
MaxVol = 127
MinVol = 0

# Left button ends program
done = lambda : button.button_isPressed(button.BUTTON_LEFT)[0]

# Initialize package to send BLE MIDI information
package = [0x00,0x00,0x00,0x00,0x00]

# Initialize sensors
string_color_sensor = port.PORTB
slide_distance_sensor = port.PORTD

# Create list of possible colors (for each string)
lego_color_list = [LEGO_MAGENTA, LEGO_BLUE, LEGO_YELLOW, LEGO_RED]

# --- LEGO color to violin string key ---
# Violin open string notes = [G3, D4, A4, E5]
# Leftmost color is the brick at END of bow = leftmost string if looking from hub to end of violin = G3 open string
# Second color is D4 open string
# Third color is A4 open string
# Rightmost color is brick nearest hand on bow = rightmost string looking from hub to end of violin = E5 open string

# Minimum and maximum distances of violin finger board from the distance sensor
min_distance = 42 # mm
max_distance = 96 # mm

# Function to package up MIDI information to send over BLE
def note(cmd,value,volume):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    return struct.pack("bbbbb", package[0], package[1], package[2], package[3], package[4])
 
# Gets the current LEGO color (a.k.a. violin string)   
def choose_string():
    
    string_color = cs.get_color(string_color_sensor)
    
    return string_color
 
# Gets the current distance of the finger board from the sensor   
def choose_distance():
    slide_distance = ds.get_distance(slide_distance_sensor)
    
    return slide_distance
    
# Gets frequency from distance and string, assuming values are not 0 or negative
def get_frequency_from_distance_and_string(string, distance):
    
    # Fundamental frequency equation: f1 = (1/2L)(T/M)^(1/2)
        # f1 = fundamental frequency
        # L = length of vibrating part of string = DISTANCE SENSED = distance
        # T = tension of string (depends on string chosen)
        # M = mass per unit length of string (depends on string chosen)
    
    frequency = 0 # [Hz]
        
    # LENGTH
    # Make proportional to real-world violin string
    standard_violin_string_length = 0.328 # [m]
    percentage_of_lego_distance = (distance - min_distance) / (max_distance - min_distance)
    
    real_life_string_distance = percentage_of_lego_distance * standard_violin_string_length # [m] length of vibrating string
        
    # TENSION and MASS PER UNIT LENGTH
    # Find T (tension) and M (mass per unit length) from string chosen
    # Source for typical T and M of violin strings: http://knutsacoustics.com/files/Typical-string-properties.pdf
    tension_and_mass_per_length_by_string_color = [[35.0, 0.00212], [34.3, 0.00092], [48.3, 0.00058], [71.4, 0.00038]]
    tension = 0
    mass_per_length = 0
    
    # Find which string we want to play
    for color_index in range(len(lego_color_list)):
        if string == lego_color_list[color_index]:
            # Based on color, get list of this string/color's tension and mass per unit length
            current_t_and_m_list = tension_and_mass_per_length_by_string_color[color_index]
            tension = current_t_and_m_list[0]
            mass_per_length = current_t_and_m_list[1]
                
    # Find current fundamental frequency
    frequency = (1 / (2 * real_life_string_distance)) * ((tension / mass_per_length)**.5)
    
    return frequency
    
# Gets MIDI number from a frequency (iff freq is NOT zero)
def get_midi_num_from_frequency(freq):
    # Equation: m  =  12*log2(f/440 Hz) + 69
    # m = midi number, f = frequency (Hz)
    # math.log(a,Base) gets the log of number a with Base
    
    num_to_log = freq / 440
    midi_num = (12 * (math.log(num_to_log, 2))) + 69
    
    return int(midi_num) # Cast in case number is a decimal because note() can't take a float

# ----- MAIN FUNCTION -----
def Violin():
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySPIKE')

    def on_rx(v):
        print("RX", v)
    
    p.on_write(on_rx)
        
    was_connected = False
    
    while not done():
        if p.is_connected():
            
            current_string = choose_string()
            current_distance = choose_distance()
            
            # Play note iff color in the color list is detected AND distance is NOT zero or negative
            if (current_string in lego_color_list) and ((current_distance - min_distance) > 0.0):
                
                current_frequency = get_frequency_from_distance_and_string(current_string, current_distance)
                current_midi_note = get_midi_num_from_frequency(current_frequency)
                
                
                p.send(note(NoteOn,current_midi_note,MaxVol))
                time.sleep_ms(10)
                p.send(note(NoteOff,current_midi_note,MinVol))
                time.sleep_ms(10)
            
        else:
            if was_connected:
                break
        
        time.sleep_ms(time_between_note_loops)
   
Violin()
