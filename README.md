__English__ | [简体中文](docs/README_cn.md)

## Brief Introduction

This project is the midterm assignment of
my sophomore Python programming course.
The project contents include:

* Use NumPy to realize Gobang;
* Use PyGame to display Gobang interface;
* Implementation of a Gobang AI based on Alpha-Beta pruning algorithm.

The programming language used in this project is Python 3.9.

## File Structure

```
Gobang
├── AI                     # 五子棋AI代码包
    ├── config.py          # AI的配置参数
    ├── search.py          # Alpha-Beta剪枝算法代码
    └── __init__.py
├── docs                   # 项目文档文件夹
    ├── images             # 图片文件夹
        └── interface.png
    └── README_cn.md       # 中文说明文件
├── font.ttf               # 字体文件
├── game.py                # 五子棋后端程序
├── icon.jpeg              # 界面图标
├── main.py                # 五子棋前端程序
├── README.md              # 英文说明文件
└── requirements.txt       # 依赖库列表
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
