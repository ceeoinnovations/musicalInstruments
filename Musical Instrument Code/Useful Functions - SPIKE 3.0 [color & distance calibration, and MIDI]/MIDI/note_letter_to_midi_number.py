# By Rose Kitz
# Comments with Anna Quiros
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# Converts the name of a note (letter & octave) to its MIDI number
# (UPPERCASE for natural, lowercase for sharped notes (flats act as sharps); and num to indicate octave level)

# Resource: https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies

# Input:
    # note_letter (str): note as a string as the english letter (uppercase for natural, lowercase for sharp) + number (of octave) combination
# Return: 
    # midi_num (int): MIDI note number to play

def note_letter_to_midi_number(note_letter):
    
    # ['note_letter', midi_num]
    notes_letters_and_midi = [['A0', 21], ['a0', 22], ['B0', 23], ['C1', 24], ['c1', 25], ['D1', 26], ['d1', 27], ['E1', 28], ['F1', 29], ['f1', 30], ['G1', 31], ['g1', 32], ['A1', 33], ['a1', 34], ['B1', 35], ['C2', 36], ['c2', 37], ['D2', 38], ['d2', 39], ['E2', 40], ['F2', 41], ['f2', 42], ['G2', 43], ['g2', 44], ['A2', 45], ['a2', 46], ['B2', 47], ['C3', 48], ['c3', 49], ['D3', 50], ['d3', 51], ['E3', 52], ['F3', 53], ['f3', 54], ['G3', 55], ['g3', 56], ['A3', 57], ['a3', 58], ['B3', 59], ['C4', 60], ['c4', 61], ['D4', 62], ['d4', 63], ['E4', 64], ['F4', 65], ['f4', 66], ['G4', 67], ['g4', 68], ['A4', 69], ['a4', 70], ['B4', 71], ['C5', 72], ['c5', 73], ['D5', 74], ['d5', 75], ['E5', 76], ['F5', 77], ['f5', 78], ['G5', 79], ['g5', 80], ['A5', 81], ['a5', 82], ['B5', 83], ['C6', 84], ['c6', 85], ['D6', 86], ['d6', 87], ['E6', 88], ['F6', 89], ['f6', 90], ['G6', 91], ['g6', 92], ['A6', 93], ['a6', 94], ['B6', 95], ['C7', 96], ['c7', 97], ['D7', 98], ['d7', 99], ['E7', 100], ['F7', 101], ['f7', 102], ['G7', 103], ['g7', 104], ['A7', 105], ['a7', 106], ['B7', 107], ['C8', 108], ['c8', 109], ['D8, 110'], ['d8', 111], ['E8', 112], ['F8', 113], ['f8', 114], ['G8', 115], ['g8', 116], ['A8', 117], ['a8', 118], ['B8', 119], ['C9', 120], ['c9', 121], ['D9', 122], ['d9', 123], ['E9', 124], ['F9', 125], ['f9', 126], ['G9', 127]]
   
    midi_num = 0
    
    # loops through 2D list 
    # checks the first element (index 0) of each pair for a matching note_letter string 
    for note in notes_letters_and_midi:
        if note_letter in note[0]:
            midi_num = note[1]
            
    return midi_num
