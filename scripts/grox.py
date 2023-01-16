#!/usr/bin/env python

# ./grox.py <dir>
#   +left, +right, flip: relative movement
#   left, right, normal, inverted: absolute movement

# devices to manipulate
import re
import subprocess
import sys


screen: str = "eDP"
touchscreen: str = "ELAN0732:00 04F3:2650 touch"
touchpad: str = "SynPS/2 Synaptics TouchPad"
stylus: str = "ELAN0732:00 04F3:2650 Stylus stylus"
eraser: str = "ELAN0732:00 04F3:2650 Stylus eraser" 
keyboard: str = "AT Translated Set 2 keyboard"

# should the script disable the keyboard on all but normal orientation
doControlKeys:bool = True
# should the script disable the touchpad on all but normal orientation
doControlTouchpad:bool = True

# cmd to get xrandr info
orientationCmd: str = "xrandr --query --verbose"
# regex to extract orientation from above command
orientationRE: str = fr"{screen}.*\) (normal|left|inverted|right) \("

#default direction
defaultDirection: str = "normal"

#code
    
def main():
    direction: str = defaultDirection 
    
    if len(sys.argv) > 1:
        direction = sys.argv[1]
        
    doOrientate(getNewOrientation(direction))
    

def doOrientate(orientation: str):
    match orientation:
        case 'normal':
            subprocess.check_call(orientateCmd('normal', '1 0 0 0 1 0 0 0 1'), shell=True)
        case 'left':
            subprocess.check_call(orientateCmd('left', '0 -1 1 1 0 0 0 0 1'), shell=True)
        case 'right':
            subprocess.check_call(orientateCmd('right', '0 1 0 -1 0 1 0 0 1'), shell=True)
        case 'inverted':
            subprocess.check_call(orientateCmd('inverted', '-1 0 1 0 -1 1 0 0 1'), shell=True)
        case _:
            raise ValueError(fr"Don't know how to orientate to {orientation}")
    
    
def orientateCmd(orientation: str, transform: str) -> str:
    rotateScreen: str = fr"xrandr --output {screen}" + \
        fr" --rotate {orientation}"
        
    rotateTouchscreen: str = fr"xinput --set-prop '{touchscreen}'" + \
        " --type=float" + \
        " 'Coordinate Transformation Matrix'" + \
        fr" {transform}"
        
    rotateStylus: str = fr"xinput --set-prop '{stylus}'" + \
        " --type=float" + \
        " 'Coordinate Transformation Matrix'" + \
        fr" {transform}"
        
    rotateEraser: str = fr"xinput --set-prop '{eraser}'" + \
        " --type=float" + \
        " 'Coordinate Transformation Matrix'" + \
        fr" {transform}"
        
    controlTouchpad: str = "" if not doControlTouchpad else fr"xinput --enable '{touchpad}';" if orientation == 'normal' else fr"xinput --disable '{touchpad}';"
    
    controlKeys: str = "" if not doControlKeys else fr"xinput --enable '{keyboard}';" if orientation == 'normal' else fr"xinput --disable '{keyboard}';"
        
    return controlTouchpad + \
        controlKeys + \
        rotateScreen + ';' + \
        rotateTouchscreen + ';' + \
        rotateStylus + ';' + \
        rotateEraser + ';'
  
    
def getNewOrientation(direction) -> str:
    clockwise: list[str] = ['normal', 'right', 'inverted', 'left']
    
    if clockwise.__contains__(direction):
        return direction
    else:
        curdir: int = clockwise.index(getOrientation())
        
        shift: int = 0
        match direction:
            case "+left":
                shift = -1
            case "+right":
                shift = 1
            case "flip":
                shift = 2
            case _:
                raise ValueError(fr"Unrecognized rotate direction {direction}")
            
        newdir: int = (curdir + shift) % 4
        
        return clockwise[newdir]       
      
      
def getOrientation() -> str:
    orientationRegexMatches = \
        re.compile(orientationRE) \
        .search( 
               subprocess.check_output(orientationCmd, shell=True)
               .decode('utf-8') 
               ) \

    return "normal" if orientationRegexMatches is None else orientationRegexMatches.group(1)

if __name__ == "__main__":
    main()
    