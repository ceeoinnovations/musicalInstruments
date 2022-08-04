# By Rose Kitz
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Runs calibrate_color_w_ratios for multiple heights from color sensor for multiple colors  

# Goal was to see if, for the same color brick, there are common ratios of G/B/I to R values
# (to recognize the same color brick at different distances from the sensor, since higher values are returned closer and lower values are returned further from the sensor,
# [so when getting RGBI values of a sensed color you can't directly compare them])

# Input:
  # None
# Return:
  # None (only print statements)

# Other functions used here:
  # calibrate_color_w_ratios(block_color, string_index)

# ----- GLOBAL STUFF -----
# Create list of possible colors
lego_color_list_as_str = ['LEGO_MAGENTA', 'LEGO_BLUE', 'LEGO_YELLOW', 'LEGO_RED']
# ------------------------

def calibrate_multiple_heights_ratios():

    num_strings = len(lego_color_list_as_str)
    
    # Test 3-10 pegs away from the hub
    start_peg_height = 3 #from hub
    last_peg_height = 10 #from hub
    heights_to_test = list(range(start_peg_height, last_peg_height + 1)) # End is exclusive so add 1
    
    # Initialize list to collect avg ratios to r for each color over heights
    each_color_avg_ratios_to_r_over_heights = [] # Will populate with list of average over each height for each color
    
    # Initialize list to populate with sum of average ratios (to later find total avg) of g/b/i to r for each color over multiple heights
    each_color_sum_avg_ratios_to_r = []
    
    # Initialize list for total avg g/b/i ratios to r for each color brick
    each_color_total_avg_ratios_to_r = []
    
    # Initialize each_color, so inner element list has length of number of color names
    for i in range(num_strings):
        each_color_avg_ratios_to_r_over_heights.append([])
        # Fill sum for each color brick as [0,0,0] to initialize (don't hardcorde if number of colors/strings changes) for each g/b/i to r
        each_color_sum_avg_ratios_to_r.append([0,0,0])
        # Initialize each avg as 0 for each string
        each_color_total_avg_ratios_to_r.append([0,0,0])
    
    # For each color, calibrate at multiple heights
    for i in range(num_strings): # i is the index of the current string
        
        current_color_name = lego_color_list_as_str[i]
        
        # Loop through each height for a particular color
        for j in range(len(heights_to_test)):
            print("Hold the", current_color_name, heights_to_test[j], "pegs above the hub.")
            # Need to store all returned values to reuse calibrate_color function, but only need color_avg_ratios_to_r
            color_min_rgbi, color_avg_rgbi, color_max_rgbi, color_ratios_to_r, color_avg_ratios_to_r = calibrate_color_w_ratios(current_color_name, i)
            color_avg_g_to_r = color_avg_ratios_to_r[0]
            color_avg_b_to_r = color_avg_ratios_to_r[1]
            color_avg_i_to_r = color_avg_ratios_to_r[2]
            
            # Add g/b/i ratio to r for this string at this height to the sums
            each_color_sum_avg_ratios_to_r[i][0] += color_avg_g_to_r
            each_color_sum_avg_ratios_to_r[i][1] += color_avg_b_to_r
            each_color_sum_avg_ratios_to_r[i][2] += color_avg_i_to_r
            
        # Calculate for each string/color block the total avg g/b/i ratios to r
        each_color_total_avg_ratios_to_r[i][0] = each_color_sum_avg_ratios_to_r[i][0] / len(heights_to_test)
        each_color_total_avg_ratios_to_r[i][1] = each_color_sum_avg_ratios_to_r[i][1] / len(heights_to_test)
        each_color_total_avg_ratios_to_r[i][2] = each_color_sum_avg_ratios_to_r[i][2] / len(heights_to_test)
        
    print("Colors:", lego_color_list_as_str)
    print("Avg g/b/i ratios to r by color:", each_color_total_avg_ratios_to_r)