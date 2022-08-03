# Setting up SPIKE Prime as a MIDI instrument over **BLE**


#### STEP ONE: SET UP FILES
1. On the device you are using to download code onto your SPIKE hub, access this [repository](https://github.com/ceeoinnovations/musicalInstruments/Setting%20Up%20MIDI/BLE%20MIDI/). 
2. Download the following programs onto your computer:  
    a. [ble_CBR.py](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/BLE%20MIDI/ble_CBR.py)  
    b. [ble_advertising.py](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/BLE%20MIDI/ble_advertising.py)  
    c. Your instrument code to run (e.g. [ble_piano.py](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/BLE%20MIDI/Starter%20Code/ble_piano.py), or a modified version of [ble_atlantis_template.py](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/BLE%20MIDI/Starter%20Code/ble_basic_template.py))  
3. Move all of these downloaded files into the LabVIEW folder on your computer (so that they are visible in the file tree once LabVIEW opens).  
    a. This is a folder that is automatically created when you download LabVIEW and stores all of your LabVIEW projects and files.
4. Connect to GarageBand.

<hr>

#### STEP TWO: SET UP GARAGEBAND
FOR MAC:

1. Open GarageBand on Mac:
    1. If you haven’t already started a new project, create a new project.
    2. Choose “Software Instrument” for track type.
    3. Choose your instrument sound from the sound library.
    4. Make sure your volume is on (so you can hear the program play later on).
    
    ![](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/BLE%20MIDI/assets/garageband.gif)

FOR IPHONE / IPAD:

_(you can follow the same instructions for both iPhone and iPad!)_

1. Open GarageBand on iPhone/iPad:
    1. If you haven’t already started a new project, select the "+" icon in the upper right of the screen to add a new project:  
        a. Select which instrument ‘category’ you’d like for your instrument. If you don’t see one close to your desired instrument, select “Keyboard,” and there will be many non-keyboard instrument options that you simply play with the keyboard keys.  
    2. To change the instrument you wish to play through your program:  
        a. **iPhone:** Select the down arrow in the upper left of the screen.  
        b. **iPad:** Select the instrument image in the middle of the screen.  
        c. Click on the current instrument to see other options.  
    3. Ensure your volume is on (so you can hear the program play later on).  
    
<hr>

#### STEP THREE: CONNECT SPIKE HUB WITH PYVIEW AND START RUNNING CODE

1. Turn on SPIKE Prime. 
2. Connect SPIKE Prime to your computer via USB cord (to later download programs onto the hub). 
3. Open PyView on your code-running computer, and find ble_advertising.py, ble_CBR.py, and ble_piano.py in your file tree on the left of your screen.  
    a. If the files don’t show up, go to the toolbar, select “Tools” > “Reload File Tree.”
4. Click on ‘SPIKE Browser’ in the upper left corner.  
    a. If ble_advertising.py and ble_CBR.py are not already downloaded onto the hub, go back to the main PyView screen, select and download each program onto the hub.  
5. Run ble_piano.py (or the instrument code that you want to run). The console should say “Starting advertising,” (the SPIKE is now advertising itself to the world as a Bluetooth peripheral device).

<hr>

#### STEP FOUR: CONNECT SPIKE TO YOUR MIDI DEVICE

FOR MAC:

1. If Bluetooth is not already on, turn it on in settings. 
2. Find and open the Audio MIDI App (it’s built in on Mac laptops). 
3. In the Audio MIDI App:  
    a. In the toolbar, select “Window” > “Show MIDI Studio.”  
    b. Hit the Bluetooth button on the top bar of the window.  
    c. A “Bluetooth Configuration” window should appear.  
    d. Connect to your SPIKE Prime.  
![](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/BLE%20MIDI/assets/spike.gif)
4. Back in PyView, you should see in the console something like “New connection 1025” (and you may see a few strange hex codes, which are just reporting the kind of MIDI device connected). 
5. You should see a pop-up in the upper-right corner of your screen saying “Changed number of MIDI inputs, 1 input is available” (this means that GarageBand is now connected to the SPIKE). 

FOR IPHONE/IPAD:

1. If Bluetooth is not already on, turn it on in settings. 
2. Go to GarageBand:  
    a. Click the settings icon in the upper right corner.  
    b. Go to Advanced (It may be under “Song Settings”)   
    c. Click “Bluetooth MIDI Devices”.  
    d. If there is a pop-up saying ‘“GarageBand” Would Like to Use Bluetooth,’ select “OK”.  
    e. The hub should show up as an option as something like “MySPIKE”. If multiple options are available and you have connected to a hub previously on GarageBand, any hub you have previously connected to should have its sub-text of “Input/Output” show up as white (rather than gray-colored).   
    f. Click on the name “MySPIKE” to connect the hub to the iPhone/iPad.   
3. Back in PyView, the console should say something like “New connection 1025” (and you may see a few strange hex codes, which are just reporting the kind of MIDI device connected).  

<hr>

#### FINAL STEPS

1. Your program should play! (You should hear audio through GarageBand).  
2. Click on “Abort” in PyView to end the program.  
    a. To run the program again, make sure you DISCONNECT from the SPIKE in the MIDI app first.   
    b. After hitting “Disconnect”, hit “Abort” in PyView again.  
    c. You should now be able to run the program in the REPL again.  
3. FOR MAC: If your hub disconnects from GarageBand at any point (or you turn it off on purpose), you’ll see a pop-up in the upper-right corner of your screen saying “Change number of MIDI inputs, 0 inputs are available.”   

<br> <br>

## Modifying the template

There is a template and a folder of useful functions that you can use in the [Starter Code](https://github.com/ceeoinnovations/musicalInstruments/tree/main/Setting%20Up%20MIDI/BLE%20MIDI/Starter%20Code) folder. 

<br> <br>

## Tips & Tricks

* We recommend using Atlantis (SPIKE 3.0) for BLE MIDI, because one of the required files ([ble_CBR.py](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/BLE%20MIDI/ble_CBR.py)) is quite large and usually too large for SPIKE 2.0 to handle (SPIKE 2.0 doesn’t have a lot of memory, and even when it gets a little fragmented, there’s not enough space for the ble_CBR.py file
* Make sure both the ble_CBR.py and ble_advertising.py files that you download don’t have any errors when they do download!
    * THE ONE OKAY ERROR: `ENOENT`
        * The download button erases a file and then writes a new one. If there isn’t a file that exists with that name already, it can’t delete that file, and therefore will throw this error.
    * Any other error is not good! Especially memory allocation and fatal errors :(
* If you run the [ble_advertising.py](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/BLE%20MIDI/ble_advertising.py) file you may get one error (It’s okay! Your programs will still work)
![](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/BLE%20MIDI/assets/Name%20Error%20-%20ADV_TYPE_FLAGS%20error.png)
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
![](https://github.com/ceeoinnovations/musicalInstruments/blob/main/Setting%20Up%20MIDI/BLE%20MIDI/assets/Attribute%20Error.png)
    * **Solution (ish):**
        * Double check that ble_CBR.py is on the hub (in SPIKE Browser on PyView) and is not blank
        * Run the **ble_CBR.py** file that holds the function **BLESimplePeripheral** _in_ PyVIEW/whatever repl you’re using. Then try running your program again.
        * IF THAT DOESN’T WORK:  Run ble_advertising.py then ble_CBR.py in the REPL, then try again.
        * IF THAT DOESN’T WORK: Run ble_advertising.py and ble_CBR.py on the actual hub (if you’re running the ble_instrument.py program on the hub)
* To find errors by line in Pyview, the lines counted are only lines that have actual code (line count doesn’t include blank lines or all comment lines, do include line to define a function).
* To select all in PyVIEW, triple click (CTRL + A doesn’t work).
* Be careful when re-running MIDI BLE code—if you’ve previously connected the SPIKE as a BLE peripheral to GarageBand and don’t disconnect the SPIKE from GarageBand/Audio MIDI (for Mac) before re-running any program, the next program you run won’t tell you “Starting advertising,” because your SPIKE hub is still connected to GarageBand. 
