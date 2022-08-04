# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Calculates the current min, avg, and max rgbi values of the inputted rgbi list.

# (Could do many others ways, e.g. by making lists of each R, G, B, I from input 2D list and finding min() from each new list)

# Input:
  # current_list_all_rgbi (2D list of ints): with inner rgbi value lists ([R, G, B, I])
# Returns:
  # min_rgbi (list of ints): minimum rgbi values ([min_r, min_g, min_b, min_i])
  # avg_rgbi (list of ints): average rgbi values ([avg_r, avg_g, avg_b, avg_i])
  # max_rgbi (list of ints): maximum rgbi values ([max_r, max_g, max_b, max_i])

# This function is used by:
  # calibrate_color_w_ratios(block_color, string_index)

def calculate_rgbi_min_avg_max(current_list_all_rgbi):

    sum_rgbi = [0, 0, 0, 0]
  
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

            # For each individual value, add the value to the sum of that r, g, b, or i
            sum_rgbi[j] += current_value
            
            # Finds actual rgbi min / max
            if current_value < current_min:
                min_rgbi[j] = current_value
            if current_value > current_max:
                max_rgbi[j] = current_value

    avg_r = round(sum_rgbi[0] / current_num_training_colors)
    avg_g = round(sum_rgbi[1] / current_num_training_colors)
    avg_b = round(sum_rgbi[2] / current_num_training_colors)
    avg_i = round(sum_rgbi[3] / current_num_training_colors)
    
    avg_rgbi = [avg_r, avg_g, avg_b, avg_i]
    
    return min_rgbi, avg_rgbi, max_rgbi