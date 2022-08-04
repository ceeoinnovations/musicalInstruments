# By Rose Kitz
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Calculates the ratios of G/B/I values to R for a color brick for a variety of test values

# Goal was to see if, for the same color brick, there are common ratios of G/B/I to R values
# (to recognize the same color brick at different distances from the sensor, since higher values are returned closer and lower values are returned further from the sensor,
# [so when getting RGBI values of a sensed color you can't directly compare them])

# Input:
  # current_list_all_rgbi (2D list of ints): with inner rgbi value lists ([R, G, B, I])
# Returns:
  # rgbi_ratios_to_r (2D list of floats): list of ratios of G/B/I to R for each measured RGBI set (inner list: [ratio_g_to_r, ratio_b_to_r, ratio_i_to_r])
  # min_ratios_to_r (list of floats): list of minimum ratios of G/B/I to R from all measured RGBI sets
  # avg_ratios_to_r (list of floats): list of average ratios of G/B/I to R from all measured RGBI sets
  # max_ratios_to_r (list of floats): list of maximum ratios of G/B/I to R from all measured RGBI sets

# This function is used by:
  # calibrate_color_w_ratios(block_color, string_index)

def calculate_rgbi_ratios_to_r(current_list_all_rgbi):
    # Initialize a list to collect ratios of g/b/i to r for each color brick from each test value
    rgbi_ratios_to_r = []
    # Initialize list to collect sum of each ratios to r value for each g/b/i to find average later
    sum_ratios_to_r = [0, 0, 0]
    
    # Since ratios can be more than 1 and are greater than 0, just find first ratios and start those as comparisons
    first_r = current_list_all_rgbi[0][0]
    first_g = current_list_all_rgbi[0][1]
    first_b = current_list_all_rgbi[0][2]
    first_i = current_list_all_rgbi[0][3]

    first_g_r_ratio = first_g / first_r
    first_b_r_ratio = first_b / first_r
    first_i_r_ratio = first_i / first_r
    
    # Initialize min ratios to r lists as first ratio values
    min_ratios_to_r = [first_g_r_ratio, first_b_r_ratio, first_i_r_ratio]
    # Initialize max ratios to r lists as first ratio values
    max_ratios_to_r = [first_g_r_ratio, first_b_r_ratio, first_i_r_ratio]
    
    current_num_training_colors = len(current_list_all_rgbi)
    
    # Loop through all collected rgbi values so far
    for i in range(current_num_training_colors):
        # Initialize new inner list in larger list for this test rgbi value
        rgbi_ratios_to_r.append([])
        
        for j in range(3): # Run through g/b/i to compare to r
            current_r = current_list_all_rgbi[i][0]
            # Get either 1/2/3 indices for g/b/i
            current_comparison = current_list_all_rgbi[i][j + 1]
            
            current_ratio = current_comparison / current_r
            
            # Add current ratio (g-r, b-r, or i-r) to current inner list for this test value
            rgbi_ratios_to_r[i].append(current_ratio)
            # Add current ratio to the index holding the sum of ratios for this relationship
            sum_ratios_to_r[j] += current_ratio
            
            # Test if this value is new min or max
            current_min_ratio = min_ratios_to_r[j] # So far min of g/b/i to r
            current_max_ratio = max_ratios_to_r[j] # So far max of g/b/i to r
            
            if current_ratio < current_min_ratio:
                min_ratios_to_r[j] = current_ratio
            
            if current_ratio > current_max_ratio:
                max_ratios_to_r[j] = current_ratio
                
    #print("current_num_training_colors:", current_num_training_colors)
    # Calculate average ratios of each g/b/i to r for this color brick tested
    avg_g_to_r = sum_ratios_to_r[0] / current_num_training_colors
    avg_b_to_r = sum_ratios_to_r[1] / current_num_training_colors
    avg_i_to_r = sum_ratios_to_r[2] / current_num_training_colors
    
    avg_ratios_to_r = [avg_g_to_r, avg_b_to_r, avg_i_to_r]
    
    # Return (for this brick tested) the ratios from each test point of g/b/i to r  
    # Also return the average ratios for this brick
    return rgbi_ratios_to_r, min_ratios_to_r, avg_ratios_to_r, max_ratios_to_r