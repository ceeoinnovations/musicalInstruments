# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Calibrates color sensor to find RGBI min/max values associated with each LEGO color

# Inputs:
  # block_color (str): chosen color to calibrate (e.g. from list of colors to play)
  # string_index (int): index of current instrument string playing from list of colors
# Returns:
  # final_min_rgbi (list of ints): minimum rgbi values ([min_r, min_g, min_b, min_i])
  # final_max_rgbi (list of ints): maximum rgbi values ([max_r, max_g, max_b, max_i])

# Others functions used here:
  # wait_until_button_is_pressed_and_released()
  # blink_calibrating(start_or_stop)
  # calculate_rgbi_min_max(current_list_all_rgbi)

# This function is used by:
  # calibrate_all_colors()

# ----- GLOBAL STUFF -----
import color_sensor as cs
import port

string_color_sensor = port.PORTB

# Initialize buffer of error: no color over sensor
no_color_max = 5

# List to collect sets of rgbi values for initial calibration, to then calculate min/max values
all_colors_all_rgbi = []
# ------------------------

def calibrate_color(block_color, string_index):

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