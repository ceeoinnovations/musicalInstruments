# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Get the color brick (e.g. violin string) held over the color sensor based on RGBI calibration (NOT LEGO colors)

# Goal was to test accuracy of predicting the color of a LEGO brick based on similarity of ratios of G/B/I to R values (getting RGBI values rather than LEGO colors from the color sensor)

# DISCLAIMER: I realized after much testing that comparing ratios of G/B/I to R to predict a LEGO brick color wasn't as accurate as I originally thought

# This function uses a simple note list to represent each violin string to test RGBI accuracy (rather than simply selecting a violin string to play to then send to a function to get the frequency from position on finger board)

# Input:
  # None
# Returns:
  # note (int): a MIDI number from note_list representing the violin string played

# ----- GLOBAL STUFF -----
lego_color_list = [LEGO_MAGENTA, LEGO_BLUE, LEGO_YELLOW, LEGO_RED]
# Create list of possible colors
lego_color_list_as_str = ['LEGO_MAGENTA', 'LEGO_BLUE', 'LEGO_YELLOW', 'LEGO_RED']

note_list = [60,62,64,66]

import color_sensor as cs
import port

string_color_sensor = port.PORTB

# Initialize buffer of error: no color over sensor
no_color_max = 5
# ------------------------

def choose_string_rgbi():
    # initialize note int variable (MIDI number)
    #print('running choose string')
    note = 0
    
    #string_color = cs.get_color(string_color_sensor)
    string_color_rgbi = cs.get_rgbi(string_color_sensor)
    #print(string_color)
    print("string color rgbi:", string_color_rgbi)
    
    # only calculate ratios if all rgbi values are above 5 ('a color is detected')
    # otherwise, note is still 0
    if (string_color_rgbi[0] > no_color_max) and (string_color_rgbi[1] > no_color_max) and (string_color_rgbi[2] > no_color_max) and (string_color_rgbi[3] > no_color_max):
        # get ratios of g/b/i to r  
        ratios_to_r = []
        # list to coolect boolean if ratios are withint r (will have length 3)
        are_within_ratios_to_r = [False, False, False]
        
        for i in range(3): # run through g/b/i to compare to r
            r_value = string_color_rgbi[0]
            # get either 1/2/3 indices for g/b/i (string_color has length 4)
            comparison_value = string_color_rgbi[i + 1]
                
            current_ratio = comparison_value / r_value
            # append this ratio to list
            ratios_to_r.append(current_ratio)
    
        # compare g/b/i ratios to r to calibrated numbers
        global color_brick_ratios_to_r_min_max
        # loop through each brick_color
        brick_number = 0
        for brick_color in color_brick_ratios_to_r_min_max: # there are 4 brick colors
            # loop through g-r, b-r, i-r ratios for this brick_color
            for num_ratio in range(len(brick_color)): # there are 3 ratios
                ratio_min = brick_color[num_ratio][0]
                ratio_max = brick_color[num_ratio][1]
                # if measured ratio is within range, change to True
                if (ratios_to_r[num_ratio] > ratio_min) and (ratios_to_r[num_ratio] < ratio_max):
                    are_within_ratios_to_r[num_ratio] = True
            
            # check if all ratios for this brick color are True
            if all(are_within_ratios_to_r): # all(iterable) returns True if all values are True
                note = note_list[brick_number]
                print("note:", note)
                print("approximate LEGO color from RGBI:", lego_color_list_as_str[brick_number])
                break # need to break from loop or else are_within_ratios_to_r will still be True and keep running to say multiple notes from one reading
            # iterate brick number for next loop , to save if note is True
            brick_number += 1
    
    return note