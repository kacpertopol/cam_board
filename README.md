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

### TODO

- clean up code
- pack reusable code to functions
- implement filtering using expression built from | and &
- implement directory choice via fzf


