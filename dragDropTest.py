import cv2
import matplotlib.pyplot as plt
import re
import os
import time
from utils import *
from PIL import Image
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


# Actual mouse callback function
def move_line(event, x, y, flags, param):

    # Controls and image need to be global
    global diff, img, img_copy, img_overlay, alpha_mask, tool, hold, l, t, width, height, scale, key, result, move_increment

    if event != 0:
        print(event)
    # img_overlay = tool[:, :, :3].copy()
    # alpha_mask = (tool[:, :, 3].copy()) / 255.0

    if flags == cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_LBUTTON and scale < 1.0:
        print("SCALE UP")
        diff = (x - l, y - t)
        l, t = (x - diff[0], y - diff[1])
        img_copy = img.copy()

        scale += 0.1
        key = "`"
        result = image_resize(tool.copy(), scale, reference=tool)
        alpha_mask = (result[:, :, 3].copy()) / 255.0
        height, width = alpha_mask.shape
        img_overlay = result[:, :, :3]
        overlay_image_alpha(
            img_copy, img_overlay, l + move_increment, t + move_increment, alpha_mask
        )
        cv2.rectangle(
            img_copy,
            (l + move_increment, t + move_increment),
            (l + width + move_increment, t + height + move_increment),
            color=(221, 62, 187),
            thickness=2,
        )
        cv2.imshow("image", img_copy)
        print(scale)

    elif flags == cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_RBUTTON and scale > 0.1:
        print("SCALE DOWN")
        diff = (x - l, y - t)
        l, t = (x - diff[0], y - diff[1])
        img_copy = img.copy()

        scale -= 0.1
        key = "`"
        result = image_resize(tool.copy(), scale, reference=tool)
        alpha_mask = (result[:, :, 3].copy()) / 255.0
        height, width = alpha_mask.shape
        img_overlay = result[:, :, :3]
        overlay_image_alpha(
            img_copy, img_overlay, l + move_increment, t + move_increment, alpha_mask
        )
        cv2.rectangle(
            img_copy,
            (l + move_increment, t + move_increment),
            (l + width + move_increment, t + height + move_increment),
            color=(221, 62, 187),
            thickness=2,
        )
        cv2.imshow("image", img_copy)
        print(scale)

    elif event == cv2.EVENT_RBUTTONDOWN:
        print("ROTATE")
        diff = (x - l, y - t)
        l, t = (x - diff[0], y - diff[1])
        img_copy = img.copy()
        result = cv2.rotate(result, cv2.cv2.ROTATE_90_CLOCKWISE).copy()
        alpha_mask = (result[:, :, 3].copy()) / 255.0
        height, width = alpha_mask.shape
        img_overlay = result[:, :, :3]
        overlay_image_alpha(
            img_copy, img_overlay, l + move_increment, t + move_increment, alpha_mask
        )
        cv2.rectangle(
            img_copy,
            (l + move_increment, t + move_increment),
            (l + width + move_increment, t + height + move_increment),
            color=(221, 62, 187),
            thickness=2,
        )
        cv2.imshow("image", img_copy)

    # Left mouse button down: Save mouse position where line was dragged
    elif (
        (event == cv2.EVENT_LBUTTONDOWN)
        and (x >= l)
        and (x <= l + width)
        and (y >= t)
        and (y <= t + height)
    ):
        diff = (x - l, y - t)
        print(f"x = {x}, y = {y}\tl = {l}, t = {t}")
        hold = True

    # Left mouse button up: Stop dragging
    elif event == cv2.EVENT_LBUTTONUP:
        hold = False

    # During dragging: Update line w.r.t. mouse position; show image
    if hold:
        l, t = (x - diff[0], y - diff[1])
        img_copy = img.copy()

        # overlay_image_alpha(img_result2, img_overlay, 330, 1350, alpha_mask)
        # cv2.rectangle(img_copy, (l, t), (l + 400, t + 9), (0, 0, 255), cv2.FILLED)

        overlay_image_alpha(
            img_copy, img_overlay, l + move_increment, t + move_increment, alpha_mask
        )
        # cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.rectangle(
            img_copy,
            (l + move_increment, t + move_increment),
            (l + width + move_increment, t + height + move_increment),
            color=(221, 62, 187),
            thickness=2,
        )
        cv2.imshow("image", img_copy)


keepMerging = True
trayPath = "emptyTrays/RelineCore1LevelB.JPEG"
trayName = re.search(r"[\/\\](\w+)", trayPath)[1]
fileName = None
timestr = time.strftime("%Y%m%d-%H%M%S")

while keepMerging:
    userInput = None
    if fileName != None:
        trayPath = f"{fileName}.jpg"
        trayName = re.search(r"(\w+)_", trayPath)[1]
    # Set up some image; work on copy
    # trayPath = "emptyTrays/RelineCore1LevelB.JPEG"
    # trayPath = filedialog.askopenfilenames()[0]
    img = cv2.imread(trayPath)
    img_copy = img.copy()

    print(trayName)

    # toolPath = "testTools/10000718_1.png"
    toolPath = filedialog.askopenfilenames()[0]

    tool = cv2.imread(toolPath, cv2.IMREAD_UNCHANGED)
    toolName = re.search(r"\/(\w+)(?!.*\/)", toolPath)[1]
    print(toolName)

    tool = tool[:, :, :4]
    tool = cv2.rotate(tool, cv2.cv2.ROTATE_90_CLOCKWISE)

    alpha_mask = (tool[:, :, 3].copy()) / 255.0
    img_overlay = tool[:, :, :3].copy()

    # Initialize controls
    diff = (0, 0)
    hold = False
    l, t = (0, 100)
    scale = 1.0
    height, width = alpha_mask.shape
    move_increment = 50
    result = tool.copy()

    overlay_image_alpha(img_copy, img_overlay, l, t, alpha_mask)
    cv2.rectangle(
        img_copy,
        (l, t),
        (l + width, t + height),
        color=(0, 200, 50),
        thickness=2,
    )
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", img_copy)
    cv2.setMouseCallback("image", move_line)
    key = "`"
    img_copy = img.copy()
    fileName = f"{trayName}_{timestr}"
    # Loop until the 'c' key is pressed
    while True:

        # Wait for keypress
        key = cv2.waitKey(1) & 0xFF

        # If 'c' key is pressed, break from loop
        if key == ord("c"):
            break
        if key == ord("s"):
            # Image.fromarray(img_copy).save("img_result.jpg")
            cv2.rectangle(
                img_copy,
                (l + move_increment, t + move_increment),
                (l + width + move_increment, t + height + move_increment),
                color=(0, 0, 200),
                thickness=2,
            )
            cv2.imshow("image", img_copy)
            print(
                f"Bounding box drawn!\nl = {l}, t = {t}\nheight = {height}, width = {width}\n\nPress any key"
            )
            # cv2.waitKey()

            path = os.path.join(fileName)
            cv2.imwrite(path + ".jpg", img_copy)
            with open((path + ".txt"), "a") as f:
                f.write(
                    f"{toolName} {width} {height} {l + move_increment} {t + move_increment}\n"
                )
            print("Image Saved!")
            break
    userInput = input(f"Would you like to continue merging with {fileName} (Y)?")
    keepMerging = userInput == "Y" or userInput == "y"
    cv2.destroyAllWindows()

print("Have an amazing day!")


# cv2.namedWindow("image", cv2.WINDOW_NORMAL)
# cv2.imshow("image", img_result2)
# cv2.waitKey()

"""
"workbench.editorAssociations": [
    {
        "viewType": "jupyter-notebook",
        "filenamePattern": "*.ipynb"
    }
],
"""
