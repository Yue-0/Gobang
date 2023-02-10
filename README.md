__English__ | [简体中文](docs/README_cn.md)

## Brief Introduction

This project is the midterm assignment of
my sophomore Python programming course.
This project contents include:

* Use NumPy to realize Gobang;
* Use PyGame to display Gobang interface;
* Implementation of a Gobang AI based on Alpha-Beta pruning algorithm.

The programming language used in this project is Python 3.9.

## File Structure

```
Gobang
├── AI                     # Gobang AI code package
    ├── config.py          # Configuration of AI
    ├── search.py          # Alpha-Beta pruning algorithm code
    └── __init__.py
├── docs                   # Project Documents
    ├── images             # Images folder
        └── interface.png
    └── README_cn.md       # Chinese description document
├── font.ttf               # Font file
├── game.py                # Back-end program of Gobang
├── icon.jpeg              # Interface icon
├── main.py                # Front--end program of Gobang
├── README.md              # English description document
└── requirements.txt       # List of requirements
```

## Quick Start

### 1.Clone

```shell
git clone https://github.com/Yue-0/Gobang.git
cd ./Gobang
```

### 2.Install requirements

Requirements are include：
* numpy
* pygame

```shell
pip install -r requirements.txt
```

### 3.Run

```shell
python main.py
```

The initial interface is shown below.

![initial interface](docs/images/interface.png)

You can select black and white chess roles on the left side of the interface,
the supported games include：
* Human vs AI
* Human vs Human

After selection, "Play" in the lower right corner of the
interface will turn green. Click "Play" to start the game.


During the game, you can click the "Repent" in the lower left corner to repent,
and you can click the "Restart" in the lower right corner to restart the game.
