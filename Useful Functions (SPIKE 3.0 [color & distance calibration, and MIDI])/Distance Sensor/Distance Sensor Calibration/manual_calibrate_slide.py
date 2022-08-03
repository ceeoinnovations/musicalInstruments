# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# This code is untested and may be buggy!

# Calibrates slide positions so they are evenly spaced physically, rather than the automatic slide position settings (which are not evenly spaced because the ultrasonic sensor doesn't measure linearlly)

# Input: 
    # num_positions (int): number of slide positions that you want
# Return:
    # slide_position_distances (list of ints): min distances associated with each slide position

# ----- GLOBAL STUFF -----
import force_sensor as fs
import port

import time

slide_distance_sensor = port.PORTC
air_force_sensor = port.PORTE
# ------------------------

def manual_calibrate_slide(num_positions):

    print("------------------------------------------------")
    print("Starting manual calibration for slide positions.")

    is_force_pressed = False
    slide_position_distances = []

    print("Mark out", num_positions, "physically even spaces on your slide.")
    print("Press the force sensor and release when you are ready to calibrate the distances.")

    # keep testing if force sensor is pressed until it's pressed
    while not is_force_pressed: 
        is_force_pressed = fs.get_touch(air_force_sensor) == 1
        time.sleep(0.01)

    # wait until force sensor is released to move on with program
    while is_force_pressed:
        is_force_pressed = fs.get_touch(air_force_sensor) == 1
        time.sleep(0.01)

    print("Ready to calibrate slide positions.")

    for i in range(num_positions):

        print("Move slide to the start of position number:")
        print(i + 1)
        print("and press force sensor to record the distance here. Release the force sensor to move on to measuring the next distance.")
        
        # keep measuring distances until the force sensor is pressed
        while not is_force_pressed: 
            current_distance = slide_distance_sensor.get_distance_cm()
            time.sleep(0.05)
            is_force_pressed = fs.get_touch(air_force_sensor) == 1

        # record indicated distance in array
        slide_position_distances.append(current_distance)
        
        # wait until force sensor is released
        while is_force_pressed: 
            is_force_pressed = fs.get_touch(air_force_sensor) == 1
            time.sleep(0.01)
    
        # go to next iteration of for loop to measure next slide distance

    print("You're all set calibrating your slide position distances. Let's get playing!")

        # since populated array from highest (i.e. 1st) position to lowest position (i.e. 7th) which feels more natural for human calibrating an instrument,
        # but need for mirroring purposes to have lowest (i.e. 7th) positon at index 0 and highest (i.e. 1st) position at the last index (to mirror low notes at index 0 to high notes at last index)
    slide_position_distances.reverse()

        # return list of min distance associated with each slide position
    return slide_position_distances