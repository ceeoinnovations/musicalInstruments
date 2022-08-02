# Set-Up Tutorials


## Setting up a SPIKE Prime instrument with **BLE **MIDI on various devices


### Device list: make a diagram out of this to be clearer



* Required:
    * SPIKE Prime hub
* Choose one to run code:
    * Mac (running MacOS)
    * PC (running Windows)
* Choose a music-outputting device:
    * Mac (with GarageBand)
    * iPad (with GarageBand)
    * [(still in the works…) PC (with Cakewalk by Bandlab)]

_BLE Example:_ If you have a Mac computer, you only need the hub and your computer, since you can run the code AND GarageBand on your Mac

_BLE Example:_ If you have a Windows computer, for the time being, you will need the hub, your PC, and an iPad (to run GarageBand)


### CONNECTING SPIKE AS A MIDI DEVICE


#### SET UP FILES



1. On the device you are using to download code onto your SPIKE hub, go to the [Github repository](https://github.com/ceeoinnovations/musicalInstruments). 
2. Download the following programs onto your computer:
    1. ble_CBR.py
    2. ble_advertising.py
    3. Your instrument code to run (e.g. ble_piano.py, or a modified version of ble_atlantis_template.py)
3. Move all of these downloaded files into the LabVIEW folder on your computer (so that they are visible in the file tree once LabVIEW opens).
    4. This is a folder that is automatically created when you download LabVIEW and stores all of your LabVIEW projects and files.
4. Connect to GarageBand.


#### SET UP GARAGEBAND

FOR MAC:



1. Open GarageBand on Mac:
    1. If you haven’t already started a new project, create a new project.
    2. Choose “Software Instrument” for track type.
    3. Choose your instrument sound from the sound library.
    4. Make sure your volume is on (so you can hear the program play later on).

FOR IPHONE / IPAD:

_(you can follow the same instructions for both iPhone and iPad!)_



1. Open GarageBand on iPhone/iPad:
    1. If you haven’t already started a new project, add a new project:
        1. Select which instrument ‘category’ you’d like for your instrument. If you don’t see one close to your desired instrument, select “Keyboard,” and there will be many non-keyboard instrument options that you simply play with the keyboard keys.
    2. To change the instrument you wish to play through your program:
        2. **iPhone:** Select the down arrow in the upper left of the screen.
        3. **iPad:** Select the instrument image in the middle of the screen.
        4. Click on the current instrument to see other options.
    3. Ensure your volume is on (so you can hear the program play later on).


#### CONNECT SPIKE HUB WITH PYVIEW AND START RUNNING CODE



1. Turn on SPIKE Prime. 
2. Connect SPIKE Prime to your computer via USB cord (to later download programs onto the hub). 
3. Open PyView on your code-running computer, and find ble_advertising.py, ble_CBR.py, and ble_piano.py in your file tree on the left of your screen.
    1. If the files don’t show up, go to the toolbar, select “Tools” > “Reload File Tree.”
4. Click on ‘SPIKE Browser’ in the upper left corner. 
    2. If ble_advertising.py and ble_CBR.py are not already downloaded onto the hub, go back to the main PyView screen, select and download each program onto the hub.
5. Run ble_piano.py (or the instrument code that you want to run). The console should say “Starting advertising,” (the SPIKE is now advertising itself to the world as a Bluetooth peripheral device).


#### CONNECT SPIKE TO YOUR MIDI DEVICE

For MAC:



1. If Bluetooth is not already on, turn it on in settings. 
2. Find and open the Audio MIDI App (it’s built in on Mac laptops). 
3. In the Audio MIDI App. 
    1. In the toolbar, select “Window” > “Show MIDI Studio.”
    2. Hit the Bluetooth button on the top bar of the window. 
    3. A “Bluetooth Configuration” window should appear. 
    4. Connect to your SPIKE Prime. 
4. Back in PyView, you should see in the console something like “New connection 1025” (and you may see a few strange hex codes, which are just reporting the kind of MIDI device connected). 
5. You should see a pop-up in the upper-right corner of your screen saying “Changed number of MIDI inputs, 1 input is available” (this means that GarageBand is now connected to the SPIKE). 

**For iPhone/iPad:**



1. If Bluetooth is not already on, turn it on in settings. 
2. Go to GarageBand:
    1. Click the settings icon in the upper right corner. 
    2. Go to Advanced (It may be under “Song Settings”)
    3. Click “Bluetooth MIDI Devices”. 
    4. If there is a pop-up saying ‘“GarageBand” Would Like to Use Bluetooth,’ select “OK”. 
    5. The hub should show up as an option as something like “MySPIKE”. If multiple options are available and you have connected to a hub previously on GarageBand, any hub you have previously connected to should have its sub-text of “Input/Output” show up as white (rather than gray-colored).
    6. Click on the name “MySPIKE” to connect the hub to the iPhone/iPad. 
3. Back in PyView, the console should say something like “New connection 1025” (and you may see a few strange hex codes, which are just reporting the kind of MIDI device connected). 


#### FINAL STEPS



5. Your program should play! (You should hear audio through GarageBand). 
6. Click on “Abort” in PyView to end the program. 
    5. To run the program again, make sure you DISCONNECT from the SPIKE in the MIDI app first. 
    6. After hitting “Disconnect”, hit “Abort” in PyView again. 
    7. You should now be able to run the program in the REPL again. 
7. FOR MAC: If your hub disconnects from GarageBand at any point (or you turn it off on purpose), you’ll see a pop-up in the upper-right corner of your screen saying “Change number of MIDI inputs, 0 inputs are available.”


## Modifying the template

[https://replit.com/@aquiros/BLE-MIDI-Templates#Useful%20Functions/get_slide_position_from_distance.py](https://replit.com/@aquiros/BLE-MIDI-Templates#Useful%20Functions/get_slide_position_from_distance.py) 


## Tips & Tricks

* We recommend using Atlantis (SPIKE 3.0) for BLE MIDI, because one of the required files (ble_CBR.py) is quite large and usually too large for SPIKE 2.0 to handle (SPIKE 2.0 doesn’t have a lot of memory, and even when it gets a little fragmented, there’s not enough space for the ble_CBR.py file
* Make sure both the ble_CBR.py and ble_advertising.py files that you download don’t have any errors when they do download!
    * THE ONE OKAY ERROR: `ENOENT`
        * The download button erases a file and then writes a new one. If there isn’t a file that exists with that name already, it can’t delete that file, and therefore will throw this error.
    * Any other error is not good! Especially memory allocation and fatal errors :(
* If you run the ble_advertising.py file you will get one error (It’s okay! Your programs will still work) 
* If sound isn’t coming out of GarageBand when you think it should:
    * Turn the hub off, then turn it back on
    * Make sure your volume is up
    * Make sure the notes you’re trying to play are actually playable by the GarageBand instrument you are using 
    * Run your program in PyView (make sure the console says “Starting advertising”)
    * Open the Audio MIDI App and follow the directions in 5.c.iii
* If, when you run your ble_instrument.py program in the REPL, the code won’t run and it just sits at the final Instrument() function call, without outputting “Starting Advertising”, you may need to download your ble_instrument.py code on your hub. To do so:
    * Download the program to the hub
    * In the REPL, type: \
	f = open(“ble_instrument.py”)  \
	exec(f.read())
    * And then when you’re done with the code, make sure to close the file!  \
	f.close()
    * You WILL need to re-download and re-open the code every time you make edits. 
* **Sound sanity check (to make sure hub is properly connected to computer via USB and speaker works for hub beeps)**
    * `import sound`
    * `sound.beepPlay()`
* **Find out modules in Atlantis in PyView**
    * `help('modules')`
    * `*** `Beware of module names in Atlantis, to avoid naming files and variables by module names (Alan says Python will prioritize the module over a variable or file)
* **To find out what functions a module has, type into the REPL:**
    * `help(module_name)`
* ERROR:` AttributeError … BLESimplePerhipheral not found`
    * **Solution (ish):**
        * Double check that ble_CBR.py is on the hub (in SPIKE Browser on PyView) and is not blank
        * Run the **ble_CBR.py** file that holds the function **BLESimplePeripheral** _in_ PyVIEW/whatever repl you’re using. Then try running your program again.
        * IF THAT DOESN’T WORK:  Run ble_advertising.py then ble_CBR.py in the REPL, then try again.
        * IF THAT DOESN’T WORK: Run ble_advertising.py and ble_CBR.py on the actual hub (if you’re running the ble_instrument.py program on the hub)
* To find errors by line in Pyview, the lines counted are only lines that have actual code (line count doesn’t include blank lines or all comment lines, do include line to define a function).
* To select all in PyVIEW, triple click (CTRL + A doesn’t work).
* Be careful when re-running MIDI BLE code—if you’ve previously connected the SPIKE as a BLE peripheral to GarageBand and don’t disconnect the SPIKE from GarageBand/Audio MIDI (for Mac) before re-running any program, the next program you run won’t tell you “Starting advertising,” because your SPIKE hub is still connected to GarageBand. 