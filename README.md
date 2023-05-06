# Self finding bot
This program implements self finding bot in maze. Semestral project in subjects BI-PYT (Python) and BI-ZUM (Artificial Intelligence Fundamentals) at FIT CTU.

## Maze file format
For this project I used mazes from first task in subject BI-ZUM (https://courses.fit.cvut.cz/BI-ZUM/labs/01/index.html). But any file with maze can be used.
This file must contain only `X, ' ', \n`. Where `X` is maze wall and `' '` is place which bot can enter.
Maze must be rectangular and at the end of each row must be `\n`. Edge of the rectangle must consist only of `X` characters.

Example of valid maze:
```
XXXXX
X   X
X X X
X   X
XXXXX
```

Example of invalid maze:
```
XXXXXXXX
X      X
X X XXXX
X   X
XXX
```
## How to run
Prepare environment
```bash
conda env update
conda activate bipyt_semestral
```

Help
```bash
python3 -m app -h
```
Examples
```bash
python3 -m app maps/zum/4.txt --pos -1 2 --dir 1 0 --print_map True
python3 -m app maps/zum/26.txt --print_map True
python3 -m app maps/zum/36.txt --print_map True
python3 -m app maps/zum/72.txt
```

## How to run tests
Prepare environment
```bash
conda env update
conda activate bipyt_semestral
```
Run tests
```bash
pytest
```
