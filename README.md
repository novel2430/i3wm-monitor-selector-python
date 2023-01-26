# I3wm Monitor Selector Python Script

## Introduction
A simple script helps you make some adjustments to your monitors by rofi !
>The script is based on python, rofi and command ```xrandr```
  - Select primary monitor
  - Select resolution
  - choose extense or same
  - switching the monitor on and off
  - choose the position of monitors ( relative to the position of primary monitor )

## Output
  - Main page
  > Extend Mode : extend or same

  ![](https://github.com/novel2430/i3wm-monitor-selector-python/raw/main/pic/001.png)
  
  - Menu Page for primary monitor
  > On Status : on-off status of current select
  
  ![](https://github.com/novel2430/i3wm-monitor-selector-python/raw/main/pic/002.png)

  - Menu Page for other monitors
  > same : same output with primary monitor\
  > left, right, above, below : relative position of primary monitor

  ![](https://github.com/novel2430/i3wm-monitor-selector-python/raw/main/pic/003.png)

  - Resolution Page
  > Select resolution

  ![](https://github.com/novel2430/i3wm-monitor-selector-python/raw/main/pic/004.png)

## Requirement
  - Using [I3wm](https://github.com/i3/i3) as your window manager
  - [Rofi](https://github.com/davatorium/rofi)
  - [Python (>=3.5)](https://www.python.org/)

## Installation
  ```bash
  git clone https://github.com/novel2430/i3wm-monitor-selector-python
  ```
  move ```src/monitor-selector.py``` to anywhere you want 

## How to use
### I3 Config
  In order for the script to get workspaces owned by each monitor, we need to map your workspace names to numbers in the i3 config file

  > It will not have any effect on your current workspace names

  Normally, we use follow lines to assign our workspace name

  ```bash
  set $ws1 "Terminal"
  set $ws2 "Chromium"
  ```
  
  Now, we need to write lines in these way
  \
  Simply add ```number:``` in front of your workspace name

  ```bash
  set $ws1 "1:Terminal"
  set $ws2 "2:Chromium"
  ```

  \
  Also, you should add ```strip_workspace_number yes``` in the ```bar``` block
  ```bash
  bar {
        strip_workspace_number yes
        ...
  }
  ```

### Config the script
  Open the script you will find the class name ```Config```, put your command line for setting background in the variable ```cmd_set_background```
  \
  Class ```Config``` is at line 6
  \
  Example :
  ```python
  class Config:
      def __init__(self) -> None:
          # You need to put the command or script in <cmd_set_background>
          self.cmd_set_background = '/home/novel2430/.config/i3/background.sh'
  ```

### Usage
  Simply run the script by
  ```bash
  python monitor-selector.py
  ```
  or (need ```chmod +x monitor-selector.py```)
  ```bash
  monitor-selector.py
  ```
  You can set key binding to this script

## TODO 
  - Make no chages to the user's i3 config file
  - Custom resolution




