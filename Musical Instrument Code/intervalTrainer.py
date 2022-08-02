# By Anna Quiros
# FET Lab Summer 2022
# Written in the Spike Web App for Spike 2

from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, Speaker, Motor
from spike.control import wait_for_seconds
import random

hub = PrimeHub()

chosen_angle = 0
note1 = 0
note2 = 0

motor = Motor('B')
force = ForceSensor('D')

note1 = random.randint(72, 84)
up_down = random.randint(1, 2)
if up_down == 1:
    multiplier = 1
else:
    multiplier = -1
interval = random.randint(0,12)
note2 = multiplier * interval + note1
distance = fabs(note1 - note2)

hub.speaker.beep(note1, 0.5)
hub.speaker.beep(note2, 0.5)

while True:
    hub.status_light.on('white')
    if hub.right_button.was_pressed():
        note1 = random.randint(72, 84)
        up_down = random.randint(1, 2)
        if up_down == 1:
            multiplier = 1
        else:
            multiplier = -1
        interval = random.randint(0,12)
        note2 = multiplier * interval + note1
        distance = fabs(note1 - note2)

        hub.speaker.beep(note1, 0.5)
        hub.speaker.beep(note2, 0.5)
    
    if hub.left_button.was_pressed():
        print(distance)
        hub.speaker.beep(note1, 0.5)
        hub.speaker.beep(note2, 0.5)
    
    if force.is_pressed():
        if distance == chosen_angle:
            hub.status_light.on('green')
            hub.light_matrix.show_image('YES', 100)
            wait_for_seconds(0.5)
        else: 
            hub.status_light.on('red')
            hub.light_matrix.show_image('NO', 100)
            wait_for_seconds(0.5)


    read_angle = motor.get_position()
    if read_angle >= 0 and read_angle < 27:
        hub.light_matrix.write("P1")
        chosen_angle = 0
    elif read_angle >= 27 and read_angle < 27*2:
        hub.light_matrix.write("m2")
        chosen_angle = 1
    elif read_angle >= 27*2 and read_angle < 27*3:
        hub.light_matrix.write("M2")
        chosen_angle = 2
    elif read_angle >= 27*3 and read_angle < 27*4:
        hub.light_matrix.write("m3")
        chosen_angle = 3
    elif read_angle >= 27*4 and read_angle < 27*5:
        hub.light_matrix.write("M3")
        chosen_angle = 4
    elif read_angle >= 27*5 and read_angle < 27*6:
        hub.light_matrix.write("P4")
        chosen_angle = 5
    elif read_angle >= 27*6 and read_angle < 27*7:
        hub.light_matrix.write("tt")
        chosen_angle = 6
    elif read_angle >= 27*7 and read_angle < 27*8: 
        hub.light_matrix.write("P5")
        chosen_angle = 7
    elif read_angle >= 27*8 and read_angle < 27*9:
        hub.light_matrix.write("m6")
        chosen_angle = 8
    elif read_angle >= 27*9 and read_angle < 27*10:
        hub.light_matrix.write("M6")
        chosen_angle = 9
    elif read_angle >= 270 and read_angle < 27*11:
        hub.light_matrix.write("m7")
        chosen_angle = 10
    elif read_angle >= 27*11 and read_angle < 27*12:
        hub.light_matrix.write("M7")
        chosen_angle = 11
    elif read_angle >= 27*12 and read_angle <=360:
        hub.light_matrix.write("P8")
        chosen_angle = 12
    else:
        print("error")
    
