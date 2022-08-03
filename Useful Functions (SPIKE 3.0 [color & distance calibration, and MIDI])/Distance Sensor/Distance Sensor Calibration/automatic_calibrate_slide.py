# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# This code is untested and may be buggy!

# Automatically chooses slide position distances (not linearly even) if user doesn't want to mark out themselves

# Inputs: 
  # num_positions (int): number of slide positions that you want
   # in_total_slide_distance (int): slide distance range determined by the distance sensor (using the function calibrate_slide_min_max_distances())
# Returns:
  # slide_position_distances (list of ints): min distances associated with each slide position

# ----- GLOBAL STUFF -----
import distance_sensor as ds
import force_sensor as fs
import port

import hub
import time

slide_distance_sensor = port.PORTC
air_force_sensor = port.PORTE

min_slide_distance, max_slide_distance = calibrate_slide_max_min_distances()
slide_dist = max_slide_distance - min_slide_distance
# ------------------------

def automatic_calibrate_slide(num_positions, in_total_slide_distance):

    print("------------------------------------------------")
    print("Starting automatic calibration for slide positions.")
  
    slide_position_distances = []

    distance_between_each_position = in_total_slide_distance / num_positions

    for i in range(num_positions):
        current_min_distance = min_slide_distance + (i * distance_between_each_position)
        slide_position_distances.append(current_min_distance)

        print("Move slide to the position where the center button light turns green.")
        print("Put a piece of tape down to indicate this minimum distance for this position number:")
        print(i + 1)
        at_correct_distance = False

        while not at_correct_distance:

            current_distance = ds.get_distance(slide_distance_sensor)
            
            # allow some error in physical positioning so not too difficult to meet (just want generally close tape marking for each position)
            allowed_error_from_exact_distance = 5 
            if (current_distance > current_min_distance - allowed_error_from_exact_distance) and (current_distance < current_min_distance + allowed_error_from_exact_distance):
                # set hub status light to green to show user that they are at the correct distance
                hub.status_light.on('green')
                at_correct_distance = True
                print("Program will wait until you are ready to move on to next position. Press the force sensor when you are done taping this position.")
                
                while fs.get_touch(air_force_sensor) == 0:
                    time.sleep(0.05)
      
        # reset hub status light to white to prepare to find next position
        hub.status_light.on('white')

    # since populated array from highest (i.e. 1st) position to lowest position (i.e. 7th) which feels more natural for human calibrating an instrument,
    # but need for mirroring purposes to have lowest (i.e. 7th) positon at index 0 and highest (i.e. 1st) position at the last index (to mirror low notes at index 0 to high notes at last index)
    slide_position_distances.reverse()

    # return list of min distance associated with each slide position
    return slide_position_distances