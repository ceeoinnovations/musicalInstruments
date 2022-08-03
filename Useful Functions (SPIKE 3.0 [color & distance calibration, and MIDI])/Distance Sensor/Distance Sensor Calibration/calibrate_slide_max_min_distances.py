# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Lets you define a maximum and minimum distance for a range to be used by a distance sensor.

# This function guides you (with print statements) to find the min/max distances of an object from the distance sensor (e.g. for a trombone slide), which you can then store in variables to use in later caluclations (e.g. to find slide distance to automatically calculate trombone slide positions).

# It may be useful to 'calibrate' min/max distances like this rather than hardcoding if you are iterating and changing your build, if the min/max distances can change over time, and more.

# Inputs: 
    # None
# Returns:
    # min_local (int): minimum slide distance found by distance sensor
    # max_local (int): maximum slide distance found by distance sensor

# ----- GLOBAL STUFF -----
import distance_sensor as ds
import force_sensor as fs
import port

import time

slide_distance_sensor = port.PORTC
air_force_sensor = port.PORTE
# ------------------------

def calibrate_slide_max_min_distances():
    print("------------------------------------------------")
    print("Starting calibration for minimum and maximum slide distances.")

    is_force_pressed = False

    min_local = 0
    max_local = 0

    print("Move slide to shortest position to find the minimum slide distance. Press force sensor ONLY when you are ready to measure.")
    # if get bugs, change to manual boolean set to False so loop will always run the first time, and later set boolean to True if force sensor is pressed

    # start collecting min slide distances, lock in by hitting force sensor
    while not is_force_pressed:
        min_local = ds.get_distance(slide_distance_sensor)
        time.sleep(0.5)
        is_force_pressed = (fs.get_touch(air_force_sensor) == 1) 

    print("Min slide distance:", min_local)
    print("Please release the force sensor to prepare for the next measurement.")

    time.sleep(0.5)
    
    while not is_force_pressed:
        time.sleep(0.01)
        is_force_pressed = (fs.get_touch(air_force_sensor) == 1)

    print("Move slide to furthest position to find the maximum slide distance. Press force sensor ONLY when you are ready to measure.")
    # if get bugs, change to manual boolean set to False so loop will always run the first time, and later set boolean to True if force sensor is pressed

    # get max slide distance, lock in by hitting force sensor
    while not is_force_pressed: 
        max_local = ds.get_distance(slide_distance_sensor)
        time.sleep(0.5)
        is_force_pressed = (fs.get_touch(air_force_sensor) == 1)

    # is_force_pressed = True after loop (force sensor still held as last tested, so need to keep testing)
      
    print("max slide distance:", max_local)

    print("Please release the force sensor to finish calibration.")

    # wait until the force sensor isn't pressed
    while is_force_pressed: 
        time.sleep(0.1)
        is_force_pressed = (fs.get_touch(air_force_sensor) == 1)
    
    print("You're all set! Let's get playing.")

    return min_local, max_local


# ----- Get min/max distances in your main program -----
# Store as separate variables
min_dist, max_dist = calibrate_slide_max_min_distances()
# Store as a tuple (Python default for multiple returns if only one variable name given)
min_and_max_dists = calibrate_slide_max_min_distances()
# Store as a list (convert default tuple return to list)
min_and_max_dists = list(calibrate_slide_max_min_distances())