# Kick-ya-chop

A really simple bot that is designed to play the game [Kick Ya Chop](https://www.addictinggames.com/clicker/kick-ya-chop).
This project was made just to get familiar with the d3dshot library along with template matching within OpenCV.

## Installation
This project just contains the script, you just need to make sure you have all of the dependencies installed.
To install all the dependencies, run:
```
pip install -r requirements.txt
```
Please note that that this project will require a python version >=3.6 and <3.9, due to the d3dshot library not updating the requirements in their pyproject.toml file.
You can find out more details in this [issue](https://github.com/SerpentAI/D3DShot/issues/44).
This poject will also work on Windows only since d3dshot has been designed to capture the screen using the [Windows Desktop Duplication API](https://docs.microsoft.com/en-us/windows/desktop/direct3ddxgi/desktop-dup-api).

## Usage
You can run the script by running:
```
python kick_ya_chop.py
```
**Please read below before running!**

At the top of the script you will see a number of constants defined.
Only the top section of the constants should be configured by the user.
Since everyone will be working with different hardware and peripherals, these need to be tuned to your specific devices.

For example, I have two 1440p screens and I had the game open on my second screen.
The pixel values therefore will be different depending on the resolution of your display(s) and where the game will be located on your screen.
In case you have multiple monitors with varying resolutions, I would just have the game open on your first monitor to make things simpler.

You may need to supply your own images for the left_branch.png and the right_branch.png since these were images taken from a 1440p display, they might not match your resolution and size when it comes to template matching.

If for some reason the script becomes unruly and you want to stop while it is executing, simply press `q` and the script will exit.

## User Configurable Parameters
### Units for the below variables are in pixels
- `MONITOR_W`: the width of your monitor that the game will be open in 
- `MONITOR_H`: the height of your monitor that the game will be open in
- `TOP`: the "y" coordinate of the top-most point of your capture area
- `LEFT`: the "x" coordinate of the left-most point of your capture area
- `BOTTOM`: the "y" coordinate of the bottom-most point of your capture area
- `RIGHT`: the "x" coordinate of the right-most point of your capture area
### In seconds
- `SLEEP`: how much should the bot sleep during each loop (this will vary from system to system)
### Just an integer
- `MONITOR`: which monitor will the game be on, set to 0 for first monitor, set to 1 for second monitor, etc.

## Demo
You can see the bot in action playing the game!

![demo](./data/demo.gif)
