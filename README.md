# leftwm-theme-main
leftwm theme based on https://github.com/AnthonyMichaelTDM/master-pywal-theme
contains all the wallpapers in backgrounds, and allows you to cycle through them

also makes use of the [grox.py](https://github.com/AnthonyMichaelTDM/grox) script
## (example) Screenshot
![desktop](./desktop.jpg)

## Dependencies

- [leftwm](https://github.com/leftwm/leftwm)
- [picom](https://github.com/yshui/picom)
- [polybar](https://github.com/polybar/polybar)
- [pywal](https://github.com/dylanaraps/pywal)

## Installation
### without leftwm-theme
1. Install all required dependencies
2. Make a copy of this project in your themes folder

```BASH
cp -r ./master-pywal-theme ~/.config/leftwm/themes
```

3. Remove the symlink to your current theme if set

```BASH
rm ~/.config/leftwm/themes/current
```
4. Set this as your current theme

```BASH
ln -s ~/.config/leftwm/themes/master-pywal-theme ~/.config/leftwm/themes/current
```

5. Restart your window manager

```Default shortcut
$MOD + Shift + r
```
