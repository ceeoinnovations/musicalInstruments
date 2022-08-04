# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Calculates the current min and max RGBI values of the inputted RGBI list

# (could do many others ways, e.g. by making lists of each R, G, B, I from input 2D list and finding min() from each new list)

# Input:
  # current_list_all_rgbi (2D list of ints): with inner rgbi value lists ([R, G, B, I])
# Returns:
  # min_rgbi (list of ints): minimum rgbi values ([min_r, min_g, min_b, min_i])
  # max_rgbi (list of ints): maximum rgbi values ([max_r, max_g, max_b, max_i])

# This function is used by:
  # calibrate_color(block_color, string_index)
  # choose_string_and_volume()

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
            if current_value > current_max:
                max_rgbi[j] = current_value
    
    return min_rgbi, max_rgbi