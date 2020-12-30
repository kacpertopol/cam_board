# DESCRIPTION

Point your laptop web cam at a piece of paper
and the program will stretch the writable area
over the whole screen.

![](demo.gif)

**Video demonstrating some of the new features available [here](https://youtu.be/zO3oriB2N70).**

# REQUIREMENTS

- python 3
- opencv (with the aruco module, see eg. the `opencv-contrib-python` pip package), numpy

# USAGE

## Prepare paper

For camera aspect ratio 16:9 print:
- **to_print/a4_16_by_9.pdf** or **to_print/a4_16_by_9.svg**
  on *A4* paper
- **to_print/letter_16_by_9.pdf** or **to_print/letter_16_by_9.svg**
  on *letter* paper

For camera aspect ratio 4:3 print:
- **to_print/a4_4_by_3.pdf** or **to_print/a4_4_by_3.svg**
  on *A4* paper
- **to_print/letter_4_by_3.pdf** or **to_print/letter_4_by_3.svg**
  on *letter* paper

The small circle marks
the top left part of the page.
If the aspect ratio of your web cam is different
from 16:9 or you want to use paper with a different size
see [custom page](#custom-page)

## Setup web cam 

Tilt your web cam so that all 4 ARUCO markers are in it's field of view.

**IMPORTANT**: To use the script with *Zoom*, *Skype*, *MS Teams*, ...
Disable the camera in these programs first, before running the script.
Otherwise a "camera busy" error will be thrown.

## Run cam_board

In the terminal navigate to the **cam_board** directory.

- To launch the script:
```
<USER> $ ./cam_board 
```

- To display command line options:
```
<USER> $ ./cam_board -h
```

## Key bindings

- "q" - quit
- "s" - save screen to PNG files to create slide show
  - the names are chosen automatically **0001.png**, **0002.png**, ...
  - by default the files are saved in the current working directory
- "a" - smooth the image by calculating an average of recent frames on / off
- "i" - invert image on / off
- "d" - de-noise on / off
- "l" - de-noise with colors on / off
- "w" - warp camera image to ARUCO markers on / off
- "k" - apply sharpening kernel on / off
- "f" - full screen mode / windowed mode

## Adjust the configuration file

Edit **aruco_cam_config** to change settings. 

## Custom page

You can make your own marker page with the markers
from **to_print/symbols**. They should be placed
in corners of a rectangle that matches the
aspect ratio of your web cam. Careful: the
orientation of the symbols is important and
they might require rotation - see **a4.svg**
for reference.

## Conserve printer ink / toner

- tape one printout with the 4 markers to desk surface (make sure the circle is positioned correctly and use tape that can later be removed from the desk 
  surface without damaging it)
- once the script recognizes the 4 ARUCO markers and stretches them to the whole screen 
  place a blank sheet of paper over the taped printout
- if the camera moves, remove any paper covering the printout and the program will recalculate
  how to warp the camera image
  
## Better resolution at the bottom

- laptop stands that allow tilting might help position the camera more perpendicular to the printout with markers resulting in better resolution
  at the bottom of the printable area
- manipulating the position of the laptop might damage it, be careful :-)

## Python version error

In some linux distributions python 3 is the default. If that is not the case on your system you can:
- adjust the first, hashbang, line of *cam_board* or ...
- ... run through python 3:
```
<user> $ python3 ./cam_board
```

# MISCELLANEOUS 

- ArUco markers made using [this](https://chev.me/arucogen/)
- This is a simple script bodged togather from various opencv tutorials, [here](https://docs.opencv.org/master/d9/df8/tutorial_root.html) is a good place to start
- Sharpening kernel see [wiki](https://en.wikipedia.org/wiki/Kernel_(image_processing)) and [this](https://www.codingame.com/playgrounds/2524/basic-image-manipulation/filtering)
