from __future__ import annotations
from typing import Tuple
import cv2 as cv
import d3dshot
import keyboard
import os
import mouse
import time

from d3dshot import D3DShot

# CONSTANTS YOU WILL NEED TO ADJUST BASED ON YOUR ENV ----------------------------------

# Monitor dimensions in pixels
MONITOR_W = 2560
MONITOR_H = 1440

# Coordinates of game-> These must be set by the user (AKA you LOL)
# I have two 1440p monitors (these are the true pixel values)
TOP, LEFT, BOTTOM, RIGHT = 650, 3395, 1020, 3872

# Sleep had to slow down since frames were too fast
SLEEP = 0.08

# Monitor, 0 for first, 1 for second, etc.
MONITOR = 1


# DO NOT CHANGE REST OF THE CONSTANTS BELOW --------------------------------------------

# Directory of where the file is
FILE_DIR = os.path.dirname(__file__)

# Get coordinates for clicking locations, these are based on the game box
L_CLICK = L_CLICK_X, L_CLICK_Y = (
    (RIGHT - LEFT) // 4 + LEFT,
    3 * (BOTTOM - TOP) // 4 + TOP,
)
R_CLICK = R_CLICK_X, R_CLICK_Y = (
    3 * (RIGHT - LEFT) // 4 + LEFT,
    3 * (BOTTOM - TOP) // 4 + TOP,
)

# Get the left and right branches
L_BRANCH = cv.imread(os.path.join(FILE_DIR, "data/left_branch.png"))
L_BRANCH_H, L_BRANCH_W, _ = L_BRANCH.shape

R_BRANCH = cv.imread(os.path.join(FILE_DIR, "data/right_branch.png"))
R_BRANCH_H, L_BRANCH_W, _ = R_BRANCH.shape

# Game over color
GAME_OVER = cv.imread(os.path.join(FILE_DIR, "data/game_over.png"))

# Threshold for match template
THRESHOLD = 0.9


# Function to click button based on absolute position
def click_mouse(pos: Tuple[int, int], button: str) -> None:
    x, y = pos
    mouse.move(x, y, absolute=True)
    mouse.click(button=button)


# Main bot loop
def main() -> None:

    # Create d3dshot object
    d: D3DShot = d3dshot.create(capture_output="numpy")

    # Set display, want to take screenshot of second monitor (0 indexed)
    d.display = d.displays[MONITOR]

    # Used to get FPS
    loop_time = time.time()

    cur_pos = L_CLICK

    while True:

        # Take screenshot and RGB -> BGR
        img = d.screenshot(region=(LEFT % MONITOR_W, TOP, RIGHT % MONITOR_W, BOTTOM))
        img = img[..., ::-1].copy()

        # Match template w/ left branch
        l_result = cv.matchTemplate(L_BRANCH, img, method=cv.TM_CCOEFF_NORMED)
        _, max_val_l, _, max_loc_l = cv.minMaxLoc(l_result)

        # Match template w/ right branch
        r_result = cv.matchTemplate(R_BRANCH, img, method=cv.TM_CCOEFF_NORMED)
        _, max_val_r, _, max_loc_r = cv.minMaxLoc(r_result)

        # Match template w/ game over
        go_result = cv.matchTemplate(GAME_OVER, img, method=cv.TM_CCOEFF_NORMED)
        _, max_val_go, _, _ = cv.minMaxLoc(go_result)

        # Check if over the thresholds
        if max_val_l > THRESHOLD:
            bot_right = (max_loc_l[0] + L_BRANCH_W, max_loc_l[1] + L_BRANCH_H)
            cv.rectangle(img, max_loc_l, bot_right, color=(0, 0, 255), thickness=2)
            click_mouse(R_CLICK, button="left")
            cur_pos = R_CLICK

        elif max_val_r > THRESHOLD:
            bot_right = (max_loc_r[0] + L_BRANCH_W, max_loc_r[1] + L_BRANCH_H)
            cv.rectangle(img, max_loc_r, bot_right, color=(0, 0, 255), thickness=2)
            click_mouse(L_CLICK, button="left")
            cur_pos = L_CLICK

        elif max_val_go > THRESHOLD:
            break

        else:
            click_mouse(cur_pos, button="left")

        # Show the image to the screen
        cv.imshow("Window", img)

        # Print FPS
        print(f"\rFPS: {round(1/(time.time() - loop_time), 2)}", end="")
        loop_time = time.time()

        if cv.waitKey(1) == ord("q") or keyboard.is_pressed("q"):
            break

        time.sleep(SLEEP)

    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
