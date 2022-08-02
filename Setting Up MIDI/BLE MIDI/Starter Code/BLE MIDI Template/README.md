# Quick description and implementation of useful functions

*For more information about initializing sensors and specific SPIKE 3 functions, visit:
https://spike3-docs.web.app/*

## CODE EXAMPLES:

**ds_choose_note.py**

Allows the distance sensor to choose the pitch of a note. 

<br>

**note_letter_to_midi_number.py**

Converts the name of a note to its MIDI number.

<br> 

**playing_a_chord.py** 

Allows you to play a chord.

<br> 

**calibrate_slide_max_min_distances.py**

Lets you define a maximum and minimum distance for a range to be used by a distance sensor. 

<br> 

## UNTESTED CODE EXAMPLES:

**automatic_calibrate_slide.py**

  Includes a function to automatically choose slide position distances (not linearlly even) if user doesn't want to mark out themselves

  <br> 
  
**get_slide_position_from_distance.py**

  On a trombone, this code finds a slide position while playing by checking if a real-time distance sensor measurement is within a range of start and end distances for each position (using a list of minimum distances for each position, which can be either physically or automatically calibrated). 

<br> 

**manual_calibrate_slide.py**

  Includes a fnction to calibrate slide positions so they are evenly spaced physically, rather than the automatic slide position settings (which are not evenly spaced because the ultrasonic sensor doesn't measure linearlly).


