# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# This code is untested and may be buggy!

# On a trombone, this code finds a slide position while playing by checking if a real-time distance sensor measurement is within a range of start and end distances for each position (using a list of minimum distances for each position, which can be either physically or automatically calibrated)

# Inputs:
  # in_slide_distance (int): real-time slide distance measured by distance sensor
  # in_min_distance_each_slide_position (list of ints): minimum distances at each slide position
# Returns:
  # get_slide_position (int): current slide position based on inputted distance

# ----- GLOBAL STUFF -----
# Initialize number of positions for slide instrument to have
num_positions = 7
# Initialize min and max slide distances (can hardcode or use calibration function)
min_slide_distance, max_slide_distance = calibrate_slide_max_min_distances()
# ------------------------

def get_slide_position_from_distance(in_slide_distance, in_min_distance_each_slide_position):
  
    get_slide_position = 0
    
    # WRITE LOOPING IF STATEMENTS TO GO THROUGH LIST OF MIN DISTANCES AND CHECK IF in_slide_distance IS WITHIN EACH INTERVAL, ONCE IT'S IN AN INTERVAL, THAT'S THE CURRENT SLIDE POSITION, and break out of loop
    for i in range(num_positions):
        test_slide_position = num_positions - i
        
        min_this_position = 0
        max_this_position = 0

        # at lowest slide position @ index 0 of min_distance_each_slide_position
        # need to set max of this range as max_slide_distance (b/c for all other positions, there is a min_range_distance and can use next position's min as current position's max)
        if i == 0:
            # set min distance of range for this position as the value of in_min_distance_each_slide_position at this index
            min_this_position = in_min_distance_each_slide_position[i]
            # for lowest position need to set max distance separately since can't use next index (since there isn't a next further index) for max distance in this position range
            max_this_position = max_slide_distance
        # for all slide positions except for lowest
        else:
            # set min distance of range for this position as the value of in_min_distance_each_slide_position at this index
            min_this_position = in_min_distance_each_slide_position[i]
            # set max distance of range for this position as the value of in_min_distance_each_slide_position at the previous index
            # (min distance of next further position is the max distance of the current position)
            max_this_position = in_min_distance_each_slide_position[i - 1]

        # if current measured slide distance is within range of current position testing
        # (minimum of range is inclusive, maximum of range is exclusive since it is start of next position)
        if (in_slide_distance >= min_this_position) and (in_slide_distance < max_this_position): 
            get_slide_position = test_slide_position
            break # break out of for loop of testing for current position, once I've found the current position based on distance
    
        #make sure right order. for now just get slide position number (later in main code I flip slide position to index to get notes)

    # in case current measured distance is not within any ranges so no value of get_slide_position was assigned previously (besides initialized 0)
    # currently, force a position if measured distance is out of range (code right after this if-statement commented out could force recalibration before continuing to play, but for now don't want to interrupt playing, b/c assume anything out of range is minor since unlikely to significantly change physical possible distance of slide in the middle of running the program, if signficantly change distance, would likely restart program)
    if get_slide_position == 0:
        # if current slide distance is less than minimum possible for last calibrated
        if in_slide_distance < min_slide_distance:
            # set slide position to first position (any instrument will have at least one position)
            get_slide_position = 1
        # if current slide distance is more than maximum possible for last calibrated
        elif in_slide_distance > max_slide_distance:
            # set slide position to lowest note position (i.e. 7th)
            get_slide_position = num_positions

    return get_slide_position
