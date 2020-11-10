# DESCRIPTION

Point your laptop web cam at a piece of paper
and the program will stretch the printable area
over the whole screen.

![](demo.gif)

# REQUIREMENTS

- python 3
- opencv

# USAGE

## Prepare paper

Print **to_print/a4.pdf** or **to_print/a4.svg**
on A4 paper. The small circle marks
the top left part of the page.
If the aspect ratio of your web cam is different
from 16:9 or you want to use paper with a different size
see [setting up page with markers](#custom-page)

## Setup web cam 

Tilt your web cam so that all 4 ARUCO markers are in it's field of view.

## Run cam_board

In the terminal navigate to the **cam_board** directory.

- To launch the script:
```
<USER> $ ./cam_board 
```
- To run in full screen mode:
```
<USER> $ ./cam_board -f
```
- To run in full screen mode and invert colors:
```
<USER> $ ./cam_board -fi
```
- To run in full screen mode and white board mode:
```
<USER> $ ./cam_board -fd
```
- To run in black board mode:
```
<USER> $ ./cam_board -di
```
- To display command line options:
```
<USER> $ ./cam_board -h
```

## Key bindings

- "q" - quit
- "s" - save screen to PNG files to create slide show
  - the names are chosen automatically **0000.png**, **0001.png**, ...
  - by default the files are saved in the current working directory

## Adjust the configuration file

Edit **aruco_cam_config** to change settings. 

# Custom page

You can make your own marker page with the markers
from **to_print/symbols**. They should be placed
in corners of a rectangle that matches the
aspect ratio of your web cam. Careful: the
orientation of the symbols is important and
they might require rotation - see **a4.svg**
for reference.


