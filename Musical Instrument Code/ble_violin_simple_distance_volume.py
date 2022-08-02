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

# Initialize common inputs for note package
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

# Create list of possible colors
lego_color_list = [LEGO_MAGENTA, LEGO_BLUE, LEGO_YELLOW, LEGO_RED]
lego_color_list_as_str = ['LEGO_MAGENTA', 'LEGO_BLUE', 'LEGO_YELLOW', 'LEGO_RED']

# --- LEGO color to violin string key ---
# Violin open string notes = [G3, D4, A4, E5]
# Leftmost color is the brick at END of bow = leftmost string if looking from hub to end of violin = G3 open string
# Second color is D4 open string
# Third color is A4 open string
# Rightmost color is brick nearest hand on bow = rightmost string looking from hub to end of violin = E5 open string

# Initialize buffer of error: no color over sensor
no_color_max = 5

# New 2D list to track min and max rgbi values for each color brick on the bow
# each inner list: [color_name, color_min_rgbi, color_max_rgbi]
all_colors_min_max_rgbi = []

# List to collect sets of rgbi values for initial calibration, to then calculate min/max values
all_colors_all_rgbi = []

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


# Calculates the current min and max rgbi values of the inputted rgbi list for current block
def calculate_rgbi_min_max(current_list_all_rgbi):

    # Initialize min and max value of each r, g, b, i as the first recorded values for each color
    # Assign min & max as first values to start
    min_rgbi = [current_list_all_rgbi[0][0], current_list_all_rgbi[0][1], current_list_all_rgbi[0][2], current_list_all_rgbi[0][3]]
    max_rgbi = [current_list_all_rgbi[0][0], current_list_all_rgbi[0][1], current_list_all_rgbi[0][2], current_list_all_rgbi[0][3]]
    current_num_training_colors = len(current_list_all_rgbi)
    
    # Loop through each test rgbi value set
    for i in range (current_num_training_colors):
        # Loop through each r, g, b, i of each set
        for j in range(4):
            
            current_value = current_list_all_rgbi[i][j]
            current_min = min_rgbi[j] 
            current_max = max_rgbi[j]
            
            # Finds actual rgbi min / max
            if current_value < current_min:
                min_rgbi[j] = current_value
            if current_value > current_m:
                max_rgbi[j] = current_value
    
    return min_rgbi, max_rgbi


# Blinks middle row of pixels on hub light matrix
def blink_calibrating(start_or_stop):
        
    pixel_on = 100
    pixel_off = 0
    pixel_state = 0
    
    # At start, clear screen and turn pixels on in order
    if start_or_stop.lower() == 'start':
        display.display_clear() 
        pixel_state = pixel_on
    # At end, turn pixels off in order
    else:
        pixel_state = pixel_off
    
    # Blink pixels in row 2 individually across screen
    # On or off depending on start or finish calibrating
    row = 2
    for i in range(5):
        display.display_set_pixel(i, row, pixel_state)
        time.sleep_ms(100)
        

# Program waits until user presses and releases right button to continue program
def wait_until_button_is_pressed_and_released():
    
    is_right_pressed = False # NOT pressed
    
    # Wait until user presses R button to indicate ready to calibrate color
    while not is_right_pressed:
        time.sleep_ms(1)
        
        right_pressed_or_not = button.button_isPressed(button.BUTTON_RIGHT)[
        
        if right_pressed_or_not == 1:
            is_right_pressed = True
    
    # Wait until button is released
    while is_right_pressed:
        time.sleep_ms(1)
       
        right_pressed_or_not = button.button_isPressed(button.BUTTON_RIGHT)[0] 
        
        if right_pressed_or_not == 0:
            is_right_pressed = False
   
# Calibrates color sensor to find RGBI values associated with each LEGO color
def calibrate_color(block_color, string_index):
    
    # Initialize RGBI list for final color for this block
    rgbi_list = [0, 0, 0, 0]
    # Initialize list of rgbi lists for training
    all_rgbi = []
    
    # Set number of times to test RGBI value
    num_tests = 100

    print("Hold the", block_color, "block CLOSE over the color sensor to calibrate and take", num_tests, "readings.")

    print("Press the right hub button when you are ready to start calibrating the", block_color, "block.")
    
    # Require right button to be both pressed and RELEASED to continue code
    wait_until_button_is_pressed_and_released()
        
    print("Starting to record values for the", block_color, "block.")
    
    # Start blinking lights to indicate calibrating
    blink_calibrating('start')
    
    current_min_rgbi = 0
    current_avg_rgbi = 0
    current_max_rgbi = 0
    
    # Get color sensor values
    for test in range(num_tests):
        
        # If in second half of tests, wait until user has bow far from sensor & right button pressed
        if test == 51:
            print("Hold the", block_color, "block FAR over the color sensor (near top of vertical magenta bar) to calibrate to take the second half of the readings.")
            print("Press the right hub button when you are ready to start calibrating the", block_color, "block.")
            
            wait_until_button_is_pressed_and_released()
            
        # Get current RGBI and convert from tuple to list
        current_rgbi = list(cs.get_rgbi(string_color_sensor))
        
        
        test_r = current_rgbi[0]
        test_g = current_rgbi[1]
        test_b = current_rgbi[2]
        test_i = current_rgbi[3]
        
        # Only count this sensed color as part of calibration if it's > [5, 5, 5, 5] (black)
        if (test_r > no_color_max) and (test_g > no_color_max) and (test_b > no_color_max) and (test_i > no_color_max):
            # If any r/g/b/i value is above 255, reset to 255 to avoid skewing max
            for value in range(4):
                if current_rgbi[value] > 255:
                    current_rgbi[value] = 255
            
            all_rgbi.append(current_rgbi)
        
    current_min_rgbi, current_max_rgbi = calculate_rgbi_min_max(all_rgbi) 
    
    print("Press the right hub button to finish calibrating this color.")
        
    final_min_rgbi = 0
    final_max_rgbi = 0

    # Catch if no color data was collected / accepted
    if len(all_rgbi) == 0:
        print("No color data collected. Brick was likely held too far away from sensor.")
        print("Please re-calibrate this color brick.")
        
        final_min_rgbi, final_max_rgbi = calibrate_color(block_color, string_index)
    # Otherwise, continue code and return final values
    else:
        wait_until_button_is_pressed_and_released() 
    
        final_min_rgbi = current_min_rgbi
        final_max_rgbi = current_max_rgbi 
        
        global all_colors_all_rgbi
        # Append to all_colors_all_rgbi: first element = lego name/number of the color
        all_colors_all_rgbi.append([block_color])
        # Second element = list of calibrated rgbi values for this block so far
        all_colors_all_rgbi[string_index].append(all_rgbi)
        
    # Show lights for calibration ending
    blink_calibrating('stop')
        
    return final_min_rgbi, final_max_rgbi
 
# Guides user to calibrate multiple colors with the color sensor   
def calibrate_all_colors():
    
    print("The program will prompt you through calibrating the colors on your bow to the color sensor.")
    print("Please make sure to move each brick up and down further and closer to the color sensor while calibrating.")
    
    num_strings = len(lego_color_list)
    
    global all_colors_min_max_rgbi
    
    # Calibrate all the strings (by their color)
    for current_string_num in range(num_strings):

        current_color_name = lego_color_list_as_str[current_string_num]
        
        color_min_rgbi, color_max_rgbi = calibrate_color(current_color_name, current_string_num)
        current_color_name_rgbi = [current_color_name, color_min_rgbi, color_max_rgbi]
        all_colors_min_max_rgbi.append(current_color_name_rgbi)
        
        print("Done calibrating", current_color_name, "color block.")      
     
    print("Done calibrating all colors.")
  
  
# Gets current color (i.e. violin string), finds volume based on distance from the color sensor
def choose_string_and_volume():
    
    string_color = cs.get_color(string_color_sensor)
    
    # Initialize current_volume
    # If color not in list, returns min vol
    volume_from_color_distance = MinVol
    
    # Only train color min/max AND choose volume if color is in list
    if string_color in lego_color_list:
        # Get RGBI color
        string_color_rgbi = cs.get_rgbi(string_color_sensor)
        
        # Find index of current color in list
        string_color_index = lego_color_list.index(string_color)
        
        # Get [color_name, color_min_rgbi, color_max_rgbi] for current color brick
        current_color_and_min_max = all_colors_min_max_rgbi[string_color_index]
        
        # Combine new and old lists for color and re-find min / max
        current_min_max_and_new_rgbi = [current_color_and_min_max[1], current_color_and_min_max[2], string_color_rgbi]
        new_color_min_rgbi, new_color_max_rgbi = calculate_rgbi_min_max(current_min_max_and_new_rgbi)
        new_color_name_min_max = [string_color, new_color_min_rgbi, new_color_max_rgbi]
        all_colors_min_max_rgbi[string_color_index] = new_color_name_min_max
       
        # Find percentage the current color is between new min and max
        current_color_rgbi_percentage_btwn_min_max = []
        
        # Loop through R, G, B, I for this color brick to get percentage current RGBI is between min and max
        for i in range(len(new_color_min_rgbi)):
            
            # Only calculate percentage if range is not 0, or else will get divide by 0 error
            # If 0, leave value_percentage as 1 (play max volume) 
            current_color_rgbi_range = new_color_max_rgbi[i] - new_color_min_rgbi[i]
            
            current_color_rgbi_diff = string_color_rgbi[i] - new_color_min_rgbi[i]
            
            value_percentage = 1
            if current_color_rgbi_range != 0:
                value_percentage = current_color_rgbi_diff / current_color_rgbi_range

            current_color_rgbi_percentage_btwn_min_max.append(value_percentage)
            
        # Min RGBI values = farthest distance away the color is detected
        # Max RGBI values = the closest distance away the color is detected
        
        # Get sum and average of r/g/b/i percentages between min and max
        sum_percentages = 0
        for percent in current_color_rgbi_percentage_btwn_min_max:
            sum_percentages += percent
            
        # Average percentage of min/max ≈ distance from color sensor
        # Higher =  closer
        # Lower = farther
        avg_percentage = sum_percentages / len(current_color_rgbi_percentage_btwn_min_max)
        
        vol_range = MaxVol - MinVol
        
        volume_from_color_distance = int(avg_percentage * vol_range) # Cast to int because volume can't be a decimal float
    
    return string_color, volume_from_color_distance  
 
 
# Gets current distance of the finger board from sensor   
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
    
    return int(midi_num) # Cast in case number is a decimal b/c note() can't take a float


# ---- MAIN FUNCTION TO RUN ALL CODE-----
def Violin():
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySPIKE')

    def on_rx(v):
        print("RX", v)
    
    p.on_write(on_rx)
        
    was_connected = False
    
    is_start = True
    
    while not done():
        if p.is_connected():
            
            if is_start:
                # Calibrate colors to start, as you play it will improve min/max
                calibrate_all_colors()
                
                is_start = False
                
                print("Let's play!")

            current_string, current_volume = choose_string_and_volume()

            current_distance = choose_distance()
            
            # Play note iff color in the color list is detected AND distance is NOT zero or negative
            if (current_string in lego_color_list) and ((current_distance - min_distance) > 0.0):
                
                current_frequency = get_frequency_from_distance_and_string(current_string, current_distance)
                current_midi_note = get_midi_num_from_frequency(current_frequency)
                
                # Volume changes (current_volume) based on distance the color is from sensor
                p.send(note(NoteOn,current_midi_note,current_volume))
                time.sleep_ms(10)
                p.send(note(NoteOff,current_midi_note,MinVol))
                time.sleep_ms(10)
              

        else:
            if was_connected:
                break

        time.sleep_ms(time_between_note_loops)
   
Violin()
