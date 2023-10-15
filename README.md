# Custom Resolution and Refresh Rate Configuration Script for Steam Deck and Arch Linux System Based

This script was created to solve the issue of the native refresh rate of the monitor not being listed in the video settings when the Steam Deck is in the dock. The script uses the `setcustomres` tool available in the AUR (Arch User Repository) to configure a custom resolution.

## Prerequisites

- `yay` (Yet Another Yaourt) package manager installed. If not installed, you can install it using the following command:

```bash
sudo pacman -S yay
```

- `setcustomres` tool installed. You can install it using `yay` with the following command:

```bash
yay -S setcustomres
```

## Usage

1. Clone the repository or download the script.
2. Open a terminal and navigate to the directory where the script is located.
3. Run the script using the following command:

python custom_resolution_script.py -w [width] -H [height] -o [output] -r [refresh_rate]

## Note

Replace `[width]`, `[height]`, `[output]`, and `[refresh_rate]` with your desired values. If no parameters are provided, default values will be used.

To see available video outputs, you can use the command:

xrandr --query

Make sure to run the script with administrative privileges to install necessary packages and configure custom resolution.

## Manual Alternative

If you prefer not to use `setcustomres`, you can manually configure the resolution and refresh rate using the following steps:

You can try this to use cvt and xrandr:
```bash
python custom_resolution_script.py -w [width] -H [height] -o [output] -r [refresh_rate] --manual
```

or

1. Generate a new display mode using `cvt`:
```bash
cvt 2560 1080 120
```

2. Add the new display mode using xrandr:
```bash
xrandr --newmode "2560x1080_120.00"  703.25  2560 2728 3000 3440  1080 1083 1093 1120 -hsync +vsync
```

3. Find out the name of your output using:
```bash
xrandr
``` 

4.Associate the new display mode with your output using:
```bash
xrandr --addmode YourOutputName 2560x1080_120.00
``` 

5.Finally, set the resolution and refresh rate using:
```bash
xrandr --output YourOutputName --mode 2560x1080_120.00
```

## NOTE



This script was specifically designed for the JSAUX HB0801 dock model and the LG 34GL750 monitor using Steam Deck.

DISCLAIMER: This operation may cause display issues or a black screen. I am not responsible for any potential hardware damage. Proceed at your own risk.
