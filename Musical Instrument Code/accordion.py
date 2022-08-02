# By Anna Quiros
# FET Lab Summer 2022
# Written in the SPIKE Web App

from spike import PrimeHub, Speaker, Motor

hub = PrimeHub()
angle = 0
motor = Motor('A')

while True:
    angle = motor.get_position()
    note = floor(120 - angle/5)
    print(note)
    hub.speaker.beep(note , 0.1)
