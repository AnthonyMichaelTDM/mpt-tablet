#!/usr/bin/ruby

# ./grox.rb <dir>
#   +left, +right, flip: relative movement
#   left, right, normal, inverted: absolute movement

# devices to manipulate
$screen = 'eDP'
$touchscreen = 'ELAN0732:00 04F3:2650 touch'
$touchpad = 'SynPS/2 Synaptics Touchpad'
$stylus = 'ELAN0732:00 04F3:2650 Stylus stylus'
$eraser = 'ELAN0732:00 04F3:2650 Stylus eraser' 
$keyboard = 'AT Translated Set 2 keyboard'

# disable keypad and touchpad on all but normal orientation
$controlKeys = true

# runs cmd and greps output to find orientation
$orientationCmd = 'xrandr --query --verbose'
$orientationRE = /#{$screen}.*\) (normal|left|inverted|right) \(/

# default direction
$defaultDirection = 'normal'


# CODE

def main()
    direction = $defaultDirection

    if ARGV.length > 0
        direction = ARGV[0]
    end

    doOrientate(getNewOrientation(direction))
end


def orientateCmd(orientation, transform)
    rotateScreen = "xrandr --output #{$screen}" +
                         " --rotate #{orientation}";
    rotateTouchscreen = "xinput --set-prop '#{$touchscreen}'" +
                              " --type=float" +
                              " 'Coordinate Transformation Matrix'" +
                              " #{transform}"
    rotateStylus = "xinput --set-prop '#{$stylus}'" +
                              " --type=float" +
                              " 'Coordinate Transformation Matrix'" +
                              " #{transform}"
    rotateEraser = "xinput --set-prop '#{$eraser}'" +
                              " --type=float" +
                              " 'Coordinate Transformation Matrix'" +
                              " #{transform}"
    controlKeys = ""
    if $controlKeys
        setCmd = orientation == 'normal' ? 'xinput --enable ' 
                                         : 'xinput --disable '
        # disable keyboard because we don't want stray keyboard inputs on a TWM, but don't disable touchpad because we need a way to recover if touchscreen breaks
        #controlKeys = "#{setCmd} '#{$keyboard}';"
        controlKeys = "#{setCmd} '#{$touchpad}'; #{setCmd} '#{$keyboard}';"
    end

    return controlKeys +
           rotateScreen + ';' +
           rotateTouchscreen + ';' + 
           rotateStylus + ';' +
           rotateEraser + ';'
end


def doOrientate(orientation)
    case orientation
    when 'normal'
        `#{orientateCmd('normal', '1 0 0 0 1 0 0 0 1')}`
    when 'left'
        `#{orientateCmd('left', '0 -1 1 1 0 0 0 0 1')}`
    when 'right'
        `#{orientateCmd('right', '0 1 0 -1 0 1 0 0 1')}`
    when 'inverted'
        `#{orientateCmd('inverted', '-1 0 1 0 -1 1 0 0 1')}`
    else
        raise "Don't know how to orientate to #{orientation}"
    end
end


# returns direction of $screen: left, right, normal or invert
def getOrientation()
    if `#{$orientationCmd}` =~ $orientationRE
        return $1 == '' ? 'normal' : $1
    else
        raise "Could not determine orientation of #{$screen} from #{$orientationCmd}"
    end
end


# direction should be +left, +right, flip, left, right, normal, or inverted
def getNewOrientation(direction)
    clockwise = ['normal', 'right', 'inverted', 'left']

    if clockwise.include?(direction)
        return direction
    else
        curdir = clockwise.find_index(getOrientation())

        shift = case direction
                when '+left' then -1
                when '+right' then 1
                when 'flip' then 2
                else
                    raise "Unrecognised rotate direction #{direction}"
                end
       
        newdir = (curdir + shift) % 4

        return clockwise[newdir]
    end
end


# DO
main()


