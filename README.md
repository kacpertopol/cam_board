# useful_scripts

## mkFromCode

Generate markdown from source code files. 
In conjunction with *pandoc* this is 
a useful tool to create lecture notes
and presentations.

Examples of annotation are available in:

```
example.py
```

To generate markdown from this file run:

```bash
$ ./mkFromCode -i example.py -o example.md
```

For more information run:

```bash
$ ./mkFromCode --help
```

### STATUS

- very poorly tested

### TODO

- clean up code, esp loops and nested if elseif ...
- pack reusable code to functions

## keyDir

Simple file manager. Directories can be tagged
and have keywords associated with them via a 
hidden .hdKeys file. 
Methods for filtering these directories using
logical | and & operators will be added (TODO).
Directory choice will be via fzf (TODO).

Additional functions can be added to a .bashrc
file from the output of:

```bash
$ ./keyDir --bashrc
```
For more information run:

```bash
$ ./keyDir --help
```

### STATUS

- very poorly tested

### TODO

- clean up code
- pack reusable code to functions
- implement directory choice via fzf (letting go of this one)

## xoj_present

Turn files created using xournal or xournalpp into beamer style presentations.

Example of turning notes into a presentation:

```bash
$ ./xoj_present notes.xopp presentation_from_notes.xopp simpleparse
```

Example of turning notes into a fancy presentation with sections and subsections (more documentation is needed):

```bash
$ ./xoj_present notes.xopp fancy_presentation_from_notes.xopp parse
```

More information (needs more documentation):

```bash
$ ./xoj_present --help
```

### STATUS

- using an xml parser in python scrambles the order of key value pairs in <... key = value ...>
  this causes xounnal (not sure if xournalpp) to crash, the xml files are reshuffled line by line.

### TODO

- add more documentation to --help 
- clean up code

## setWacom

Maps a Wacom graphical tablet to a window and conserves the
tablets aspect ratio.

Additionally, you can rotate the tablet clockwise:

```bash
$ ./setWacom -c
```

or anti-clockwise:

```bash
$ ./setWacom -a
```

### STATUS

- may not work on all systems
- not tested extensively

### TODO

- clean up code
- add dependency checks (*xsetwacom* and *xdotool*)
- clean up code

## simpleCal

Simple calendar application. Uses a single text file
from *simpleCal.config* to read calendar events.

Examples and more information can be obtained using:

```bash
$ ./simplecal --help
```

### STATUS

- not tested extensively

### TODO

- clean up code

## rssReader

Small application to scan feeds. TODO

## cam

Presentations using webcam. More info
in cam/README.md.

- print page with markers
- tilt laptop webcam to see all markers on page
- run

```
aruco_cam
```

More info:

```
aruco_cam -h
```
and cam/README.md.
