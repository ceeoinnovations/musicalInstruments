import imu
import time
import sound
import random
import button

faces = {
    0:'HUB_FACE_TOP',
    1:'HUB_FACE_FRONT',
    2:'HUB_FACE_RIGHT',
    3:'HUB_FACE_BOTTOM',
    4:'HUB_FACE_BACK',
    5:'HUB_FACE_LEFT',
}

note_nums = {
    1: "C",
    2: "C#",
    3: "D",
    4: "D#",
    5: "E",
    6: "F",
    7: "F#",
    8: "G",
    9: "G#",
    10: "A",
    11: "A#",
    12: "B",
    13: "C2",
    14: "C2#",
    15: "D2",
}

note_freq = {
    "C": 524,
    "C#": 554,
    "D": 587,
    "D#": 622,
    "E": 659,
    "F": 698,
    "F#": 740,
    "G": 784,
    "G#": 831,
    "A": 880,
    "A#": 932,
    "B": 988,
    "C2": 1047,
    "C2#": 1109,
    "D2": 1175,
}

def playNote():
    random_num = random.randint(1, 15)
    #print(random_num)
    note = note_freq[note_nums[random_num]]
    print("Playing ", note)
    sound.beepPlay(note, 400)

while not button.button_isPressed(button.BUTTON_RIGHT)[0]:
    #sound.beepPlay(524, 600)
    if faces[imu.getUpFace()] != 'HUB_FACE_BACK':
        playNote()
        #print("WOULD PLAY HERE")
        
    #print(faces[imu.getUpFace()])
    time.sleep(0.3)
