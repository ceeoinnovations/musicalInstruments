# By Samson Bienstock
# FET Lab Summer 2022
# Written for Atlantis in PyVIEW

# NEEDS ble_legomusic4.py TO RUN !! 

#BEGINNING OF PROGRAM

#PART 1: ---------- SETUP
#import button
#import TESTALLCHORDS
#done = lambda : button.button_isPressed(button.BUTTON_RIGHT)[0]
import ble_legomusic4, motor, force_sensor, color_sensor, struct, ble_CBR, bluetooth, time, port
play = 60
NoteOn = 0x90
NoteOff = 0x80
MaxVol = 127
MinVol = 0

#PART 2: ---------- PACKAGE MIDI MESSAGE
# (takes place in LEGOMUSIC4)

#PART 3: ---------- PLAY MIDI
def Piano():
    chords = LEGOMUSIC4.createChords()
    #print(chords)
    
    #PART 3a: ---------- ADVERTISING BLE
    ble = bluetooth.BLE()
    p = ble_CBR.BLESimplePeripheral(ble, 'MIDI', 'MySPIKE')
    def on_rx(v):
        print("RX", v)
        
    p.on_write(on_rx)
    
    
    #PART 3b: ---------- SETUP VARIABLES and DATASTREAMS
    was_connected = False
    
    stateM = False
    n = 0
    song = [11,4,6,8]
    root0 = chords[song[0]][0]
    third0 = chords[song[0]][1]
    fifth0 = chords[song[0]][2]
    if song[0]>23:
        seventh0 = chords[song[0]][3]
    root1 = chords[song[1]][0]
    third1 = chords[song[1]][1]
    fifth1 = chords[song[1]][2]
    if song[1]>23:
        seventh1 = chords[song[1]][3]
    root2 = chords[song[2]][0]
    third2 = chords[song[2]][1]
    fifth2 = chords[song[2]][2]
    if song[2]>23:
        seventh2 = chords[song[2]][3]
    root3 = chords[song[3]][0]
    third3 = chords[song[3]][1]
    fifth3 = chords[song[3]][2]
    if song[0]>23:
        seventh3 = chords[song[3]][3]
    stateB = False
    stateD = False
    stateF = False
    stateE = False
    stateT = False
    key = -1
   


    

    while True:
        
        #activate if BLE connected
        if p.is_connected():
            
            was_connected = True
            #play here
            
           
            
            #if melody button is pressed
            if stateM == False and force_sensor.get_touch(port.PORTC) :
                position = port.port_getSensor(0)[2]
                position = position + 180
                n = LEGOMUSIC4.determineNote(position, 0, key)
                print(n)
                p.send(LEGOMUSIC4.note(NoteOn,n,MaxVol))
                stateM = True
                stateT = True
                #legato while loop
                while stateT == True :
                    position = port.port_getSensor(0)[2]
                    position = position + 180
                    k = LEGOMUSIC4.determineNote(position, 0, key)
                    if k != n :
                        p.send(LEGOMUSIC4.note(NoteOff,n,MinVol))
                        p.send(LEGOMUSIC4.note(NoteOn,k,MaxVol))
                        n=k
                    if not force_sensor.get_touch(port.PORTC) :
                        stateT = False
                    
                    #button 1
                    if stateB == False and force_sensor.get_touch(port.PORTB) :
                        if song[0]<=23:
                            p.send(LEGOMUSIC4.note3(NoteOn,root0,MaxVol,third0,MaxVol,fifth0,MaxVol))
                        else :
                            p.send(LEGOMUSIC4.note4(NoteOn,root0,MaxVol,third0,MaxVol,fifth0,MaxVol,seventh0,MaxVol))
                        stateB = True 
                    if stateB == True and not force_sensor.get_touch(port.PORTB) :
                        if song[0]<=23:
                            p.send(LEGOMUSIC4.note3(NoteOff,root0,MinVol,third0,MinVol,fifth0,MinVol))
                        else :
                            p.send(LEGOMUSIC4.note4(NoteOff,root0,MinVol,third0,MinVol,fifth0,MinVol,seventh0,MinVol))
                        stateB = False
                    #end button 1
                    
                    #button 2
                    if stateD == False and force_sensor.get_touch(port.PORTD) :
                        if song[1]<=23:
                            p.send(LEGOMUSIC4.note3(NoteOn,root1,MaxVol,third1,MaxVol,fifth1,MaxVol))
                        else :
                            p.send(LEGOMUSIC4.note4(NoteOn,root1,MaxVol,third1,MaxVol,fifth1,MaxVol,sev1,MaxVol))
                        stateD = True 
                    if stateD == True and not force_sensor.get_touch(port.PORTD) :
                        if song[1]<=23:
                            p.send(LEGOMUSIC4.note3(NoteOff,root1,MinVol,third1,MinVol,fifth1,MinVol))
                        else :
                            p.send(LEGOMUSIC4.note4(NoteOff,root1,MinVol,third1,MinVol,fifth1,MinVol,seventh1,MinVol))
                        stateD = False
                    #end button 2
                        
                    #button 3
                    if stateF == False and force_sensor.get_touch(port.PORTF) :
                        if song[2]<=23:
                            p.send(LEGOMUSIC4.note3(NoteOn,root2,MaxVol,third2,MaxVol,fifth2,MaxVol))
                        else :
                            p.send(LEGOMUSIC4.note4(NoteOn,root2,MaxVol,third2,MaxVol,fifth2,MaxVol,seventh2,MaxVol))
                        stateF = True  
                    if stateF == True and not force_sensor.get_touch(port.PORTF) :
                        if song[2]<=23:
                            p.send(LEGOMUSIC4.note3(NoteOff,root2,MinVol,third2,MinVol,fifth2,MinVol))
                        else :
                            p.send(LEGOMUSIC4.note4(NoteOff,root2,MinVol,third2,MinVol,fifth2,MinVol,seventh2,MinVol))
                        stateF = False
                    #end button 3
                        
                    #button 4
                    if stateE == False and force_sensor.get_touch(port.PORTE) :
                        if song[3]<=23:
                            p.send(LEGOMUSIC4.note3(NoteOn,root3,MaxVol,third3,MaxVol,fifth3,MaxVol))
                        else :
                            p.send(LEGOMUSIC4.note4(NoteOn,root3,MaxVol,third3,MaxVol,fifth3,MaxVol,seventh3,MaxVol))
                        stateE = True  
                    if stateE == True and not force_sensor.get_touch(port.PORTE) :
                        if song[3]<=23:
                            p.send(LEGOMUSIC4.note3(NoteOff,root3,MinVol,third3,MinVol,fifth3,MinVol))
                        else :
                            p.send(LEGOMUSIC4.note4(NoteOff,root3,MinVol,third3,MinVol,fifth3,MinVol,seventh3,MinVol))
                        stateE = False
                    #end button 4
                #end legato loop 
                   
            #if melody button unpressed
            if stateM == True and not force_sensor.get_touch(port.PORTC) :
                p.send(LEGOMUSIC4.note(NoteOff,n,MinVol))
                stateM = False
            #end melody button
        
        
        
            #button 1
            if stateB == False and force_sensor.get_touch(port.PORTB) :
                if song[0]<=23:
                    p.send(LEGOMUSIC4.note3(NoteOn,root0,MaxVol,third0,MaxVol,fifth0,MaxVol))
                else :
                    p.send(LEGOMUSIC4.note4(NoteOn,root0,MaxVol,third0,MaxVol,fifth0,MaxVol,seventh0,MaxVol))
                stateB = True 
            if stateB == True and not force_sensor.get_touch(port.PORTB) :
                if song[0]<=23:
                    p.send(LEGOMUSIC4.note3(NoteOff,root0,MinVol,third0,MinVol,fifth0,MinVol))
                else :
                    p.send(LEGOMUSIC4.note4(NoteOff,root0,MinVol,third0,MinVol,fifth0,MinVol,seventh0,MinVol))
                stateB = False
            #end button 1
            
            #button 2
            if stateD == False and force_sensor.get_touch(port.PORTD) :
                if song[1]<=23:
                    p.send(LEGOMUSIC4.note3(NoteOn,root1,MaxVol,third1,MaxVol,fifth1,MaxVol))
                else :
                    p.send(LEGOMUSIC4.note4(NoteOn,root1,MaxVol,third1,MaxVol,fifth1,MaxVol,sev1,MaxVol))
                stateD = True 
            if stateD == True and not force_sensor.get_touch(port.PORTD) :
                if song[1]<=23:
                    p.send(LEGOMUSIC4.note3(NoteOff,root1,MinVol,third1,MinVol,fifth1,MinVol))
                else :
                    p.send(LEGOMUSIC4.note4(NoteOff,root1,MinVol,third1,MinVol,fifth1,MinVol,seventh1,MinVol))
                stateD = False
            #end button 2
                
            #button 3
            if stateF == False and force_sensor.get_touch(port.PORTF) :
                if song[2]<=23:
                    p.send(LEGOMUSIC4.note3(NoteOn,root2,MaxVol,third2,MaxVol,fifth2,MaxVol))
                else :
                    p.send(LEGOMUSIC4.note4(NoteOn,root2,MaxVol,third2,MaxVol,fifth2,MaxVol,seventh2,MaxVol))
                stateF = True  
            if stateF == True and not force_sensor.get_touch(port.PORTF) :
                if song[2]<=23:
                    p.send(LEGOMUSIC4.note3(NoteOff,root2,MinVol,third2,MinVol,fifth2,MinVol))
                else :
                    p.send(LEGOMUSIC4.note4(NoteOff,root2,MinVol,third2,MinVol,fifth2,MinVol,seventh2,MinVol))
                stateF = False
            #end button 3
                
            #button 4
            if stateE == False and force_sensor.get_touch(port.PORTE) :
                if song[3]<=23:
                    p.send(LEGOMUSIC4.note3(NoteOn,root3,MaxVol,third3,MaxVol,fifth3,MaxVol))
                else :
                    p.send(LEGOMUSIC4.note4(NoteOn,root3,MaxVol,third3,MaxVol,fifth3,MaxVol,seventh3,MaxVol))
                stateE = True  
            if stateE == True and not force_sensor.get_touch(port.PORTE) :
                if song[3]<=23:
                    p.send(LEGOMUSIC4.note3(NoteOff,root3,MinVol,third3,MinVol,fifth3,MinVol))
                else :
                    p.send(LEGOMUSIC4.note4(NoteOff,root3,MinVol,third3,MinVol,fifth3,MinVol,seventh3,MinVol))
                stateE = False
            #end button 3
            
            
        else:
            if was_connected:
                break
     
