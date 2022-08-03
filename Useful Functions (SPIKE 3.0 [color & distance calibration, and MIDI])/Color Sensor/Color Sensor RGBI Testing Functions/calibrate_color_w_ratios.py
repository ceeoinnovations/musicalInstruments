# By Rose Kitz
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Calibrates color sensor to find RGBI min/avg/max values (and ratios of G/B/I to R) associated with each LEGO color

# Inputs:
  # block_color (str): chosen color to calibrate (e.g. from list of colors to play)
  # string_index (int): index of current instrument string playing from list of colors
# Returns:  
    # final_min_rgbi (list of ints): minimum rgbi values ([min_r, min_g, min_b, min_i])
    # final_avg_rgbi (list of ints): average rgbi values ([avg_r, avg_g, avg_b, avg_i])
    # final_max_rgbi (list of ints): maximum rgbi values ([max_r, max_g, max_b, max_i])
    # final_ratios_to_r: (2D list of floats): list of ratios of G/B/I to R for each measured RGBI set (inner list: [ratio_g_to_r, ratio_b_to_r, ratio_i_to_r])
    # final_min_ratios_to_r (list of floats): minimum ratios of G/B/I to R from all measured RGBI sets
    # final_avg_ratios_to_r (list of floats): average ratios of G/B/I to R from all measured RGBI sets
    # final_max_ratios_to_r (list of floats): maximum ratios of G/B/I to R from all measured RGBI sets

# Other functions used here:
  # wait_until_button_is_pressed_and_released()
  # blink_calibrating(start_or_stop)
  # calculate_rgbi_min_avg_max(current_list_all_rgbi)
  # calculate_rgbi_ratios_to_r(current_list_all_rgbi)  

# This function is used by:
  # calibrate_all_colors_w_ratios()
  # calibrate_multiple_times_to_compare_heights_for_ratios()

# ----- GLOBAL STUFF -----
import color_sensor as cs
import port

string_color_sensor = port.PORTB

# Initialize buffer of error: no color over sensor
no_color_max = 5

# List to collect sets of rgbi values for initial calibration, to then calculate min/max values
all_colors_all_rgbi = []
# ------------------------

def calibrate_color_w_ratios(block_color, string_index):

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
        
    current_min_rgbi, current_avg_rgbi, current_max_rgbi = calculate_rgbi_min_avg_max(all_rgbi) 
    
    print("Press the right hub button to finish calibrating this color.")
        
    final_min_rgbi = 0
    final_avg_rgbi = 0
    final_max_rgbi = 0
    final_ratios_to_r = []
    final_min_ratios_to_r = []
    final_avg_ratios_to_r = []
    final_max_ratios_to_r = []

    # Catch if no color data was collected / accepted
    if len(all_rgbi) == 0:
        print("No color data collected. Brick was likely held too far away from sensor.")
        print("Please re-calibrate this color brick.")
        
        final_min_rgbi, final_avg_rgbi, final_max_rgbi, final_ratios_to_r, final_min_ratios_to_r, final_avg_ratios_to_r, final_max_ratios_to_r = calibrate_color_w_ratios(block_color, string_index)
    # Otherwise, continue code and return final values
    else:
        wait_until_button_is_pressed_and_released() 
    
        final_min_rgbi = current_min_rgbi
        final_avg_rgbi = current_avg_rgbi
        final_max_rgbi = current_max_rgbi

        final_ratios_to_r, final_min_ratios_to_r, final_avg_ratios_to_r, final_max_ratios_to_r = calculate_rgbi_ratios_to_r(all_rgbi)

        # Initialize new inner list to collect ratios to r min/max data for this color brick
        global color_brick_ratios_to_r_min_max
        color_brick_ratios_to_r_min_max.append([])
        # Append [min, max] for each g/b/i to r for this color brick
        # Inside else so it only runs once when we get data
        min_g_r = final_min_ratios_to_r[0]
        max_g_r = final_max_ratios_to_r[0]
        color_brick_ratios_to_r_min_max[string_index].append([min_g_r, max_g_r])
        min_b_r = final_min_ratios_to_r[1]
        max_b_r = final_max_ratios_to_r[1]
        color_brick_ratios_to_r_min_max[string_index].append([min_b_r, max_b_r])
        min_i_r = final_min_ratios_to_r[2]
        max_i_r = final_max_ratios_to_r[2]
        color_brick_ratios_to_r_min_max[string_index].append([min_i_r, max_i_r])
        
    # Show lights for calibration ending
    blink_calibrating('stop')
        
    return final_min_rgbi, final_avg_rgbi, final_max_rgbi, final_ratios_to_r, final_min_ratios_to_r, final_avg_ratios_to_r, final_max_ratios_to_r