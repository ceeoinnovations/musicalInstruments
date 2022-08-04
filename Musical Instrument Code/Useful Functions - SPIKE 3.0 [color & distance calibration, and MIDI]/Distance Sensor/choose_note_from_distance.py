# By Rose Kitz and Fletcher Boyd
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Choose pitch of note based on distance measured from distance sensor (written for a trombone slide)

# MODIFY IT!
# --- How can you activate other events (besides playing a single note) based on measured distance? 

# NOTE: Make sure to change the min/max and lists of distances below for the code to work with your build(s)! You can choose to 'calibrate' your distance sensor in a few different ways:
# 1. Manual + hardcode: get & print distance values at your desired physical positions and assign to variables (like we did below with min_dist and max_dist)
# 2. 'Manual' via algorithm: check out the (still buggy) calibrate_slide_max_min_distance.py to automatically find & store min/max distance
# --- You can also automate (rather than hardcoding) finding the distances for each note (or e.g. slide position on a trombone). Check out manual_calibrate_slide.py to choose your own physical positions then easily report those to the program, or check out automatic_calibrate_slide.py to 

# --------------------------------------- FOR LOOP ------------------------------------------------
# Input:
  # None
# Return:
  # note (int): MIDI note number to be played

# ----- GLOBAL STUFF -----
import distance_sensor as ds
import port

distance_sensor = port.PORTC

# ----- Choose note with "for" loop" -----
min_dist = 30
max_dist = 230

for_loop_positions_min_distances = [min_dist, 50, 70, 100, 135, 170, 198, max_dist]

# List of notes associated with each distance range (e.g. by position for a trombone slide)
# This list is in terms of MIDI numbers, feel free to write your note lists as you are most comfortable (e.g. as letters), as long as in the end your 'notes' that you send over BLE are represented as MIDI numbers. If you'd prefer to stick with note letters, check out the note_letter_to_midi_number.py file for a function that takes in a note letter and automatically converts it to and returns a MIDI number
notes_list = [60, 61, 62, 63, 64, 65, 66, 67]
# -------------------------

def choose_note_in_for_loop():
  # Initialize note number
  note = 0
  positionNumber = 0
  
  distance = ds.get_distance(distance_sensor)

  # Define end bounds (in case sensor detects values outside of min/max while playing to avoid errors)
  if distance < min_dist:
    distance = min_dist
  if distance > max_dist:
    distance = max_dist

  # Find which position we're in 
  for i in range(len(for_loop_positions_min_distances) - 1):
      if distance >= for_loop_positions_min_distances[i]:
        positionNumber = i

  # Based on the found current positionNumber, get the note associated with that position
  note = notes_list[positionNumber]
  return note
    

# --------------------------------------- "IF" STATEMENTS ------------------------------------------------
  
# Input:
  # None
# Return:
  # note (int): MIDI note number to be played
  
# ----- GLOBAL STUFF -----
# ----- Choose note with multiple "if/elif" statements -----
if_statements_positions_min_distances = [6, 10, 14, 18, 22]
# ------------------------

def choose_note_with_if_statements():
  # Initialize note number
  note = 0

  distance = ds.get_distance(distance_sensor)

  # Define end bounds (in case sensor detects values outside of min/max while playing to avoid errors)
  if distance < min_dist:
    distance = min_dist
  if distance > max_dist:
    distance = max_dist
  
  # Different distances trigger different notes 
  if distance < if_statements_positions_min_distances[0]: note = 71
  elif distance < if_statements_positions_min_distances[1]: note = 69
  elif distance < if_statements_positions_min_distances[2]: note = 67
  elif distance < if_statements_positions_min_distances[3]: note = 65
  elif distance < if_statements_positions_min_distances[4]: note = 64
  else: note = 31
    
  return note


    