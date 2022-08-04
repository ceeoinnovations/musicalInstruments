# By Rose Kitz
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Guides user to calibrate multiple colors with the color sensor  

# Input:
  # None
# Return:
  # None (only modifying global list all_colors_min_max_rgbi)

# Other functions used here:
  # calibrate_color_w_ratios(block_color, string_index)

# ----- GLOBAL STUFF -----
# Create list of possible colors
lego_color_list = [LEGO_MAGENTA, LEGO_BLUE, LEGO_YELLOW, LEGO_RED]
lego_color_list_as_str = ['LEGO_MAGENTA', 'LEGO_BLUE', 'LEGO_YELLOW', 'LEGO_RED']

# New 2D list to track min and max rgbi values for each color brick on the bow
# each inner list: [color_name, color_min_rgbi, color_max_rgbi]
all_colors_min_max_rgbi = []
# ------------------------

def calibrate_all_colors_w_ratios():
    
    print("The program will prompt you through calibrating the colors on your bow to the color sensor.")
    print("Please make sure to move each brick up and down further and closer to the color sensor while calibrating.")
    
    num_strings = len(lego_color_list)
    
    global all_colors_min_max_rgbi
    
    # Calibrate all the strings (by their color)
    for current_string_num in range(num_strings):

        current_color_name = lego_color_list_as_str[current_string_num]
        
        color_min_rgbi, color_avg_rgbi, color_max_rgbi, color_ratios_to_r, color_min_ratios_to_r, color_avg_ratios_to_r, color_max_ratios_to_r = calibrate_color_w_ratios(current_color_name, current_string_num)
        current_color_name_rgbi = [current_color_name, color_min_rgbi, color_max_rgbi]
        all_colors_min_max_rgbi.append(current_color_name_rgbi)
        
        print("Done calibrating", current_color_name, "color block.")      
     
    print("Done calibrating all colors.")