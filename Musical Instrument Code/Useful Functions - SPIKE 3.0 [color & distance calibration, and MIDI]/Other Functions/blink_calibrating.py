# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Blinks middle row of pixels one at a time on hub light matrix

# Input:
  # start_or_stop (str): 'start' or 'stop' to indicate start/stop of calibration state (respectively)
# Return:
  # None

# This function is used by:
  # calibrate_color(block_color, string_index)
  # calibrate_color_w_ratios(block_color, string_index)

# ----- GLOBAL STUFF -----
import display
import time
# ------------------------

def blink_calibrating(start_or_stop):
        
    pixel_on = 100
    pixel_off = 0
    pixel_state = 0
    
    # At start, clear screen and turn pixels on in order
    if start_or_stop.lower() == 'start':
        display.display_clear() 
        pixel_state = pixel_on
    # At end, turn pixels off in order
    else:
        pixel_state = pixel_off
    
    # Blink pixels in row 2 individually across screen
    # On or off depending on start or finish calibrating
    row = 2
    for i in range(5):
        display.display_set_pixel(i, row, pixel_state)
        time.sleep_ms(100)