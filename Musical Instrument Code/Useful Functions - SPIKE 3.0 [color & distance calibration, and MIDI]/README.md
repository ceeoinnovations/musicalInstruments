# Quick description and implementation of useful functions

*For more information about initializing sensors and specific SPIKE 3 functions, visit:
https://spike3-docs.web.app/*

## Color Sensor

**choose_string_and_volume.py**

Gets current LEGO color (e.g. violin string), finds volume based on distance from the color sensor
<br>

### Calibration

**calculate_rgbi_min_max.py**

Calculates the current min and max RGBI values of the inputted RGBI list.
<br>

**calibrate_all_colors.py**

Guides user to calibrate multiple colors with the color sensor.
<br>

**calibrate_color.py**

Calibrates color sensor to find RGBI min/max values associated with each LEGO color.
<br>

### RGBI Testing

**calculate_rgbi_min_avg_max.py**

Calculates the current min, avg, and max rgbi values of the inputted RGBI list.
<br>

**calibrate_rgbi_ratios_to_r.py**

Calculates the ratios of G/B/I values to R for a color brick for a variety of test values.
<br>

**calibrate_all_colors_w_ratios.py**

Guides user to calibrate multiple colors with the color sensor.
<br>

**calibrate_color_w_ratios.py**

Calibrates color sensor to find RGBI min/avg/max values (and ratios of G/B/I to R) associated with each LEGO color
<br>

**calibrate_multiple_times_to_compare_heights_for_ratios.py**

Runs calibrate_color_w_ratios for multiple heights from color sensor for multiple colors
<br>

**choose_string_rgbi.py**

Get the color brick (e.g. violin string) held over the color sensor based on RGBI calibration (NOT LEGO colors)
<br>

**test_colors_sensed.py**

Test color sensor's ability to detect colors when different-colored bricks are held over sensor
<br>

## Distance Sensor

**choose_note_from_distance.py**

Choose pitch of note based on distance measured from distance sensor (written for a trombone slide). 
<br>

### Calibration

**automatic_calibrate_slide.py (UNTESTED)**

Automatically chooses slide position distances (not linearly even) if user doesn't want to mark out themselves
<br>

**calibrate_slide_max_min_distances.py**

Lets you define a maximum and minimum distance for a range to be used by a distance sensor.
<br>

**get_slide_position_from_distance.py (UNTESTED)**

On a trombone, this code finds a slide position while playing by checking if a real-time distance sensor measurement is within a range of start and end distances for each position (using a list of minimum distances for each position, which can be either physically or automatically calibrated). 
<br>

**manual_calibrate_slide.py (UNTESTED)**

Calibrates slide positions so they are evenly spaced physically, rather than the automatic slide position settings (which are not evenly spaced because the ultrasonic sensor doesn't measure linearlly).

## MIDI

**get_frequency_from_distance_and_string.py**

Takes in distance sensor and LEGO color (instrument string choice) and calculates the corresponding frequency.
<br>

**get_midi_num_from_frequency.py**

Calculates the corresponding MIDI number for a given frequency (iff freq is NOT zero).
<br>

**note_letter_to_midi_number.py**

Converts the name of a note (letter & octave) to its MIDI number.
<br> 

## Other Functions

**blink_calibrating.py**

Blinks middle row of pixels one at a time on hub light matrix.
<br>

**wait_until_button_is_pressed_or_released.py**

Waits until user presses and releases the right button on the hub to continue program. 

<br>

