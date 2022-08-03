# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Calculates the corresponding MIDI number for a given frequency (iff freq is NOT zero)

# Inputs:
  # freq (float): note frequency
# Returns:
  # midi_num (int): MIDI note number associated with inputted frequency

# ----- GLOBAL STUFF -----
import math
# ------------------------

def get_midi_num_from_frequency(freq):
    # Equation: m  =  12*log2(f/440 Hz) + 69
    # m = midi number, f = frequency [Hz]
    # math.log(a,Base) gets the log of number a with Base
    
    num_to_log = freq / 440
    midi_num = (12 * (math.log(num_to_log, 2))) + 69
    
    return int(midi_num) # Cast in case number is a decimal because note() can't take a float