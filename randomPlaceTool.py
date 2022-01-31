import cv2
import matplotlib.pyplot as plt
import numpy as np
import re
import os
import time
import glob, random
import math

from utils import *
from PIL import Image
import tkinter as tk

from tkinter import filedialog
from skimage.io import imread_collection

root = tk.Tk()
root.withdraw()

import os, random

col_dir = "./testTools/*.png"

# creating a collection with the available images
col = imread_collection(col_dir)
trayPath = "emptyTrays/RelineCore1LevelB_crop.jpeg"
tray = cv2.imread(trayPath)
# tool = cv2.rotate(tool, cv2.cv2.ROTATE_90_CLOCKWISE)

generationCount = 5
results = []
for n in range(generationCount):
    trayCopy = tray.copy()
    for i in range(random.randint(0, len(col) - 1)):
        randomIndex = random.randint(0, len(col) - 1)
        # print(randomIndex)
        tool = col[randomIndex].copy()
        toolCopy = tool.copy()
        tool = image_resize(toolCopy, scale=0.75, reference=tool)
        tool = tool[:, :, :4]
        alpha_mask = (tool[:, :, 3].copy()) / 255.0
        img_overlay = tool[:, :, :3].copy()

        trayHeight, trayWidth, _ = tray.shape
        # print(trayHeight, trayWidth)

        lowerBound = 0.2
        upperBound = 0.8

        x, y = (
            random.randint(
                math.floor(lowerBound * trayWidth),
                math.ceil(upperBound * trayWidth),
            ),
            random.randint(
                math.floor(lowerBound * trayHeight), math.ceil(upperBound * trayHeight)
            ),
        )
        overlay_image_alpha(trayCopy, img_overlay, x, y, alpha_mask)
    results.append(trayCopy)

# cv2.namedWindow("image", cv2.WINDOW_NORMAL)
# cv2.imshow("image", trayCopy)
# cv2.resizeWindow("image", math.ceil(trayWidth / 2), math.floor(trayHeight / 2))
# cv2.waitKey(0)


# Display resultant images code
w = 10
h = 10
fig = plt.figure(figsize=(5, 1))
columns = 5
rows = 1

imgIndex = 0
print(len(results))
for i in range(1, columns * rows + 1):
    print(imgIndex)
    img = results[imgIndex]
    imgIndex += 1
    fig.add_subplot(rows, columns, i)
    plt.imshow(img)
plt.show()
