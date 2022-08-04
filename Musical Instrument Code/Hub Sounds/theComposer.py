from spike import PrimeHub, Button, Speaker, ColorSensor, Motor

hub = PrimeHub()

motor = Motor('B')
color_sensor = ColorSensor('D')

power = 30

# initial beep
hub.speaker.beep(60, 0.25)
hub.speaker.set_volume(100)

while True:
    color = color_sensor.get_color()
    print(color)
    motor.start_at_power(power)
    if color == 'red':
        hub.speaker.beep(60, 0.25)
    if color == 'violet':
        hub.speaker.beep(62, 0.25)
    if color == 'yellow':
        hub.speaker.beep(64, 0.25)
    if color == 'blue':
        hub.speaker.beep(65, 0.25)
    if hub.left_button.was_pressed():
        if power == 100:
            power = 100
        else:
            power = power + 10
    if hub.right_button.was_pressed():
        if power == -100:
            power = -100
        else:
            power = power - 10


motor.stop()