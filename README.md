# I3wm Monitor Selector Python Script

## Info
A simple script helps you make some adjustments to your monitors by rofi !
>The script is based on python, rofi and command ```xrandr```
  - Select primary monitor
  - Select resolution
  - choose extense or same
  - switching the monitor on and off
  - choose the position of monitors ( relative to the position of primary monitor )

## ScreenShots
  - Main Page
  - Menu Page for primary monitor
  - Menu Page for other monitors
  - Resolution page

## Requirement
  - Using [I3wm](https://github.com/i3/i3) as your window manager
  - [Rofi](https://github.com/davatorium/rofi)
  - [Python (>=3.5)](https://www.python.org/)

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
  You can build key binding to this script

## TODO 
  - Make no chages to the user's i3 config file
  - Custom resolution




