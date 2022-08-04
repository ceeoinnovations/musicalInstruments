
Trying to connect trombone to PC via USB MIDI cable
Didn’t work at first when running program, no blue light to indicate MIDI data sent
Unplugged and replugged in MIDI ports
Ran program and got blue light for C! Now to connect to Cakewalk
LET’S GO IT’S WORKING
Tried with FL Studio, which got the USB MIDI device to show up (see if it shows up without doing this in the future)
Tried with Cakewalk, didn’t work, but after trying in FL Studio, the USB MIDI input showed up
Opened loopMIDI, tried to use loopMIDI ports with MIDIberry, didn’t work
Hearing trombone sounds by running PyView code through MIDIberry, which can change instruments and has cool input monitor!

# Setting up SPIKE Prime as a MIDI instrument over **USB** (on PC running Windows)

*Note: the template code used in this tutorial uses SPIKE 2.0 commands*

#### STEP ONE: CONNECT SPIKE HUB WITH Pico Breadboard MIDI Setup

1. From the Pico breadboard setup:
	1. Take the clear SPIKE connector end of the black 6-wire cord and plug it into a SPIKE hub port.
	2. Take the USB-C connector end of the MIDI cable and plug it into your PC.
	3. Make sure that your wire connections on the breadboard match the image below before moving on.
[](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/BLE%20MIDI/assets/MIDI%20USB%20SetUp.jpg)
<hr>

#### STEP TWO: SET UP FILE
1. On your PC, access this [repository](https://github.com/ceeoinnovations/musicalInstruments/tree/main/Setting%20Up%20MIDI/USB%20MIDI) to download code onto your SPIKE hub.
2. Download [usb_basic_template.py](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/USB%20MIDI/usb_basic_template.py) and modify the file as you wish to program your instrument (e.g. adding sensors - see [usb_trombone_simple_spike2.py](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Musical%20Instrument%20Code/USB/usb_trombone_simple_spike2.py) for examples)  
3. Move this file into the LabVIEW folder on your computer (so it is visible in the file tree once LabVIEW opens).  
    a. This is a folder that is automatically created when you download LabVIEW and stores all of your LabVIEW projects and files.
<hr>

#### STEP THREE: SET UP DAW (Digital Audio Workspace)
1. Download [MIDIberry](https://apps.microsoft.com/store/detail/midiberry/9N39720H2M05?hl=en-us&gl=US) (you can also try other [GarageBand alternatives for Windows](https://www.musicianwave.com/free-garageband-alternatives-for-windows/), we've only tested MIDIberry so far and will refer to it throughout the tutorial for Windows).
2. Open MIDIberry:
	1. Click the three horizontal lines in the upper-left corner of the screen to open the instrument chooser.
	2. Click on the dropdown that says "Program Change (GM)," and select the instrument you'd like to play.
	3. Make sure your volume is on (so you can hear the program play later on). You can test that sound is working through MIDIberry by pressing the black and white 'piano' keys right under the instrument drop down.
	4. Under "INPUT," select "USB Midi".
	5. Under "OUTPUT," select something like "Microsoft GS Wavetable Synth".
[](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/BLE%20MIDI/assets/MIDIBerry%20Set-Up.png)
<hr>

#### STEP FOUR: CONNECT SPIKE HUB WITH PYVIEW AND START RUNNING CODE

1. Turn on SPIKE Prime. 
2. Connect SPIKE Prime to your computer via USB cord (to later download programs onto the hub). 
3. Open PyView on your code-running computer, your instrument code (e.g. usb_basic_template.py) in your file tree on the left of your screen.  
    a. If the files don’t show up, go to the toolbar, select “Tools” > “Reload File Tree.” 
4. Run your instrument code.

<hr>

#### FINAL STEPS

1. You should hear your sounds playing (through your PC)!
2. . You will also see various messages (one for each midi_port.write() statement) both in the MIDIberry "INPUT MONITOR" (something like "0 : NoteOn, Ch: 1, Note: 60, Velocity: 127") and in the PyView console (something like "3," which refers to the number of bytes you are sending when writing the MIDI package).  

## Modifying the template

There is a folder of useful functions that you can use in the [Musical Instrument Code](https://github.com/ceeoinnovations/musicalInstruments/tree/main/Musical%20Instrument%20Code/Useful%20Functions%20-%20SPIKE%203.0%20%5Bcolor%20%26%20distance%20calibration%2C%20and%20MIDI%5D) folder. 

<br>

## Tips & Tricks
* Every time a piece of MIDI information is sent from the hub to your PC (for every midi_port.write() statement), you should see the light on the MIDI cable turn from red to blue (e.g. when a note is turned on or off)
* If information is not sending as expected, try disconnecting and reconnecting the MIDI cable and hub port and re-run your code.