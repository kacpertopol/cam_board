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
