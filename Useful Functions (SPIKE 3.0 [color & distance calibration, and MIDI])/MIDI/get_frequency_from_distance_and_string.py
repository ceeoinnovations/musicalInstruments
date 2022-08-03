# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Takes in distance sensor and LEGO color (instrument string choice) and calculates the corresponding frequency, assuming values are not 0 or negative 

# Inputs:
  # string (int, as LEGO color): selected string on instrument to play (measured from color sensor)
    # (written for Violin, based on typical string lengths, tensions, and mass per unit length)
    # (see SPIKE 3 Docs for LEGO color options)
  # distance (int): measured from distance sensor

# Returns:
  # frequency (float): note frequency to play based on inputted selected instrument string and distance on 'finger board' of total instrument string length

# ----- GLOBAL STUFF -----
# Create list of possible colors
lego_color_list = [LEGO_MAGENTA, LEGO_BLUE, LEGO_YELLOW, LEGO_RED]

# Minimum and maximum distances of violin finger board from the distance sensor
min_distance = 42 # [mm]
max_distance = 96 # [mm]
# ------------------------

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