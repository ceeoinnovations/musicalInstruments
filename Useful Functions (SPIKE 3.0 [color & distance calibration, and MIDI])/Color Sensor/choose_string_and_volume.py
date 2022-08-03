# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Gets current LEGO color (e.g. violin string), finds volume based on distance from the color sensor

# 'Distance' from color sensor is found from the percentage a current RGBI reading is between the calibrated min and max RGBI values
# The color sensor reads HIGHER RGBI values when an object is closer to the sensor, and LOWER RGBI values when an object is further from the sensor,
# So HIGH RGBI values correspond to a close distance, which for a violin represents greater string pressure and therefore higher volume,
# and LOW RGBI values correspond to a far distance, which for a violin represents lesser string pressure and therefore lower volume.

# Inputs: 
  # None
# Returns:
  # string_color (int): LEGO color detected by color sensor
  # volume_from_color_distance (int): volume to play sound at from a percentage of min and max volume (based on the percentage the current measured RGBI color is between calibrated min and max RGBI colors)

# Others functions used here:
  # calculate_rgbi_min_max(current_min_max_and_new_rgbi)

# ----- GLOBAL STUFF -----
import color_sensor as cs
import port

MaxVol = 127
MinVol = 0

string_color_sensor = port.PORTB

# Create list of possible colors
lego_color_list = [LEGO_MAGENTA, LEGO_BLUE, LEGO_YELLOW, LEGO_RED]

# Initialize buffer of error: no color over sensor
no_color_max = 5

# New 2D list to track min and max rgbi values for each color brick on the bow
# Each inner list: [color_name, color_min_rgbi, color_max_rgbi]
all_colors_min_max_rgbi = []
# ------------------------

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
            
        # Average percentage of min/max â‰ˆ distance from color sensor
        # Higher =  closer
        # Lower = farther
        avg_percentage = sum_percentages / len(current_color_rgbi_percentage_btwn_min_max)
        
        vol_range = MaxVol - MinVol
        
        volume_from_color_distance = int(avg_percentage * vol_range) # Cast to int because volume can't be a decimal float
    
    return string_color, volume_from_color_distance