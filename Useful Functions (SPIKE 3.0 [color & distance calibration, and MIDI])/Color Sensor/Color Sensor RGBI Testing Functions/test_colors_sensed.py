# By Rose Kitz
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Test color sensor's ability to detect colors when different-colored bricks are held over sensor

# Goal was to test the 'speed' of the color sensor to see how quickly it can detect a new color held over the sensor (by seeing, out of 1000 tests, how many are unique)

# Input:
  # None
# Return:
  # None (only print statements)

# Other functions used here:
  # wait_until_button_is_pressed_and_released()

# ----- GLOBAL STUFF -----
import color_sensor as cs
import port

string_color_sensor = port.PORTB

# Initialize buffer of error: no color over sensor
no_color_max = 5
# ------------------------

def test_colors_sensed():
    print("Press right button to start color speed test")
    wait_until_button_is_pressed_and_released()
    
    colors_sensed_count = 0
    
    no_color_max = 5 # buffer of error to say that there's no color in particular over the sensor
    
    # initialize variable to store previous rgbi value to compare if color sensed is unique from last (in that case if unique, save in total list)
    last_rgbi = (0, 0, 0, 0)
    unique_rgbi_list = []
    
    for i in range(1000):
        # need color sensor get OUTSIDE of if statement, so whether or not the last reading was a color, we test again
        rgbi = cs.get_rgbi(string_color_sensor)
        
        # need each value multiple times so stored in intuitive variable names
        this_r = rgbi[0]
        this_g = rgbi[1]
        this_b = rgbi[2]
        this_i = rgbi[3]
        
        # if there's a color other than nothing over the sensor, print that color
        if (this_r > no_color_max) and (this_g > no_color_max) and (this_b > no_color_max) and (this_i > no_color_max):
            print(rgbi)
            
            # iterate by 1 to count number of colors of 1000 sensed
            colors_sensed_count += 1
            
            # if the current color (any r/g/b/i value) is different than the last color
            # save this unique color
            if (this_r != last_rgbi[0]) or (this_g != last_rgbi[1]) or (this_b != last_rgbi[2]) or (this_i != last_rgbi[3]):
                unique_rgbi_list.append(rgbi)
        
        # before next sensor test, set last_rgbi as the most recently found rgbi
        last_rgbi = rgbi
            
            
            
    print("Num colors sensed:", colors_sensed_count, "/ 1000 tests")
    print("Unique_rgbi_list has", len(unique_rgbi_list), "elements:", unique_rgbi_list)
      
        #time.sleep_ms(1)