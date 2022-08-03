# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Program waits until user presses and releases right button to continue program

# Input:
  # None
# Return:
  # None

# This function is used by:
  # calibrate_color(block_color, string_index)
  # calibrate_color_w_ratios(block_color, string_index)
  # test_colors_sensed()

# ----- GLOBAL STUFF -----
import button
import time
# ------------------------

def wait_until_button_is_pressed_and_released():
    
    is_right_pressed = False # NOT pressed
    
    # Wait until user presses R button to indicate ready to calibrate color
    while not is_right_pressed:
        time.sleep_ms(1)
        
        right_pressed_or_not = button.button_isPressed(button.BUTTON_RIGHT)[0]
        
        if right_pressed_or_not == 1:
            is_right_pressed = True
    
    # Wait until button is released
    while is_right_pressed:
        time.sleep_ms(1)
       
        right_pressed_or_not = button.button_isPressed(button.BUTTON_RIGHT)[0] 
        
        if right_pressed_or_not == 0:
            is_right_pressed = False