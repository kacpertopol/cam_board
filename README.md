# DESCRIPTION

Point your laptop web cam at a piece of paper
and the programm will streach the printable area
over the whole screen.

<center>
[VIDEO DEMONSTRATION](./demo.mp4)
</center>


# USAGE

## Prepare paper

Print **to_print/a4.pdf** or **to_print/a4.svg**
on A4 paper. The small circle markes
the top left part of the page.
If the aspect ration of your web cam is different
from 16:9 or you want to use paper with a different size
see [setting up page with markers](#setuppage)

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

## Adjust the configuration file

Edit **aruco_cam_config** to change settings. 

# Custom page with markers {#setuppage}

You can make your own marker page with the markers
from **to_print/symbols**. They schould be placed
in corners of a rectangle that matches the
aspect ratio of your web cam. Carefull: the
orientation of the symbols is important and
they might require rotation - see **a4.svg**
for refference.


