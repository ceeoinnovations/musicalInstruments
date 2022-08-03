# By Samson Bienstock
# FET Lab Summer 2022
# Written for Spike 2 in the Spike Web App

#Play function

def NoteSequencer() :
    #start program 
    print("starting in 3....2.....1.....")
    time.sleep(1)
    #start spinning
    motor.motor_move_at_power(port.PORTA, 2200)
    #initialize chords array, run, song, index
    chords = []
    for i in range (12) :
        chords.append([261.63*(1.0593**(i)), 329.63*(1.0593**(i)), 392*(1.0593**(i)), 523.25*(1.0593**(i))])
    for i in range (12) :
        chords.append([261.63*(1.0593**(i)), 311.13*(1.0593**(i)), 392*(1.0593**(i)), 523.25*(1.0593**(i))])
    run = True
    #pick the chords to your song!
    #0-11 C-B major, 12-23 is C-B minor,
    song = [0,7,21,5]
    #i keeps track of song index
    index = 0
   
    #while loop for main functionality
    while run :
        #get color constantly
        x = color_sensor.get_color(port.PORTC)
        if x == 9 :
            sound.beepPlay(int(chords[song[i]][0]),300)
            time.sleep(0.3)
        if x == 7 :
            sound.beepPlay(int(chords[song[i]][1]),300)
            time.sleep(0.3)
        if x == 3 :
            sound.beepPlay(int(chords[song[i]][2]),300)
            time.sleep(0.1)
        if x == 0 :
            i = i + 1
            if i == len(song) :
                i = 0
            print(i)
            time.sleep(0.3)
        if x == 1 :
            run = False
            
    motor.motor_stop()



NoteSequencer()

            
          
