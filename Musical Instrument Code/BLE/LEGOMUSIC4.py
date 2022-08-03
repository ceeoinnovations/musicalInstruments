#setup

import time
import ustruct, struct, ble_CBR, bluetooth, time, port

index = 0
chords = []#make this a global variable ???????
#CHOOSE YOUR CHORDS
songA = [['G', 'd' ,'Em', 'c']]
songB = []
package = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]


def note(cmd,value,volume):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    return struct.pack("bbbbb", package[0], package[1], package[2], package[3], package[4])

def note2(cmd,value,volume,value2, volume2):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    package[5] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[6] =  0x80 | (timestamp_ms & 0b1111111)
    package[7] =  0x80 | cmd
    package[8] = value2
    package[9] = volume2
    
    return struct.pack("bbbbbbbbbb", package[0], package[1], package[2], package[3], package[4], package[5], package[6], package[7], package[8], package[9])

def note3(cmd,value,volume,value2,volume2,value3,volume3):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    package[5] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[6] =  0x80 | cmd
    package[7] = value2
    package[8] = volume2
    package[9] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[10] =  0x80 | cmd
    package[11] = value3
    package[12] = volume3
    return struct.pack("bbbbbbbbbbbbb", package[0], package[1], package[2], package[3], package[4], package[5], package[6], package[7], package[8], package[9], package[10], package[11], package[12])

def note4(cmd,value,volume,value2,volume2,value3,volume3,value4,volume4):
    timestamp_ms = time.ticks_ms()
    package[0] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[1] =  0x80 | (timestamp_ms & 0b1111111)
    package[2] =  0x80 | cmd
    package[3] = value
    package[4] = volume
    package[5] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[6] =  0x80 | cmd
    package[7] = value2
    package[8] = volume2
    package[9] = (timestamp_ms >> 7 & 0b111111) | 0x80
    package[10] =  0x80 | cmd
    package[11] = value3
    package[12] = volume3
    package[13] =(timestamp_ms >> 7 & 0b111111) | 0x80
    package[14] = 0x80 | cmd
    package[15] = value4
    package[16] = volume4
    return struct.pack("bbbbbbbbbbbbbbbbb", package[0], package[1], package[2], package[3], package[4], package[5], package[6], package[7], package[8], package[9], package[10], package[11], package[12], package[13], package[14], package[15], package[16])

    
    
def createChords():
    #adds 12 major chords following 1 3 5 structure
    # 0 through 11
    chords = []
    for i in range (12) :
        chords.append([60+i, 64+i, 55+i])

    
    #minor chords
    # 12 through 23
    for i in range (12) :
        chords.append ([60+i, 63+i, 55+i])
        
    #major 7
    #24-35
    for i in range (12) :
        chords.append([60+i, 64+i, 55+i, 59+i])
        
    #dom 7
    #36-47
    for i in range (12) :
        chords.append([60+i, 64+i, 55+i, 58+i])
        
    #min 7
    #48-59
    for i in range (12) :
        chords.append([60+i, 63+i, 55+i, 58+i])
        
        
    return chords
    

    
    
def determineNote(position, mode, k):
    
    maj = [65,67,69,71,72,74,76,77,79,81,83,84,86,88]
    blues = [60,63,65,66,67,70,72,75,77,78,79,82,84,87]
    if mode == 0 :
        if position <= 296 and position >= 271 :
            return maj[0]+k
        elif position <= 321 and position >= 297 :
            return maj[1]+k
        elif position <= 348 and position >= 322 :
            return maj[2]+k
        elif position <= 14 or position >= 349 :
            return maj[3]+k
        elif position <= 39 and position >= 15 :
            return maj[4]+k
        elif position <= 65 and position >= 40 :
            return maj[5]+k
        elif position <= 90 and position >= 66 :
            return maj[6]+k
        elif position <= 115 and position >= 91 :
            return maj[7]+k
        elif position <= 141 and position >= 116 :
            return maj[8]+k
        elif position <= 167 and position >= 142 :
            return maj[9]+k
        elif position <= 192 and position >= 168 :
            return maj[10]+k
        elif position <= 219 and position >= 193 :
            return maj[11]+k
        elif position <= 245 and position >= 220 :
            return maj[12]+k
        else : return maj[13]+k
    if mode == 1 :
        if position <= 296 and position >= 271 :
            return blues[0]+k
        elif position <= 321 and position >= 297 :
            return blues[1]+k
        elif position <= 348 and position >= 322 :
            return blues[2]+k
        elif position <= 14 or position >= 349 :
            return blues[3]+k
        elif position <= 39 and position >= 15 :
            return blues[4]+k
        elif position <= 65 and position >= 40 :
            return blues[5]+k
        elif position <= 90 and position >= 66 :
            return blues[6]+k
        elif position <= 115 and position >= 91 :
            return blues[7]+k
        elif position <= 141 and position >= 116 :
            return blues[8]+k
        elif position <= 167 and position >= 142 :
            return blues[9]+k
        elif position <= 192 and position >= 168 :
            return blues[10]+k
        elif position <= 219 and position >= 193 :
            return blues[11]+k
        elif position <= 245 and position >= 220 :
            return blues[12]+k
        else : return blues[13]+k    
    else :
        return 90
    
    
    
   
    
    
