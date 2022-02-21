import os
import cv2
import matplotlib.pyplot as plt
import re
import time
import random
import math
from utils import *
from skimage.io import imread_collection
import shutil

col_dir = "./testTools/RelineCore1LevelB/*.png"

# Specify number of images to generate
generationCount = 5
emptyTrayGeneration = None

# Creating a collection with the available images
col = imread_collection(col_dir)
trayPath = "emptyTrays/RelineCore1LevelB_crop.jpeg"
trayName = re.search(r"[\/\\](\w+)", trayPath)[1]
tray = cv2.imread(trayPath)

outputFolder = "./testOutput/"
fileName = None
timestr = time.strftime("%Y%m%d-%H%M%S")

# tool = cv2.rotate(tool, cv2.cv2.ROTATE_90_CLOCKWISE)


results = []
for i in range(generationCount):
    trayCopy = tray.copy()

    # Each generated image name in sequence will have an index differentiating it
    fileName = f"{trayName}_{i}_{timestr}"
    for _ in range(random.randint(1, len(col) - 1)):
        randomIndex = random.randint(0, len(col) - 1)
        tool = col[randomIndex].copy()
        toolCopy = tool.copy()

        # Random scaling
        scaleLowerBound = 0.5
        scaleUpperBound = 0.8
        randomScale = random.uniform(scaleLowerBound, scaleUpperBound)
        # print(f"Original Tool shape {tool.shape[:2]}")
        tool = image_resize(toolCopy, scale=randomScale, reference=tool)
        # print(f"New Tool shape {tool.shape[:2]}")

        # Random Rotation
        tool = randomOrientaton(tool)

        tool = tool[:, :, :4]

        alpha_mask = (tool[:, :, 3].copy()) / 255.0
        img_overlay = tool[:, :, :3].copy()

        trayHeight, trayWidth, _ = tray.shape
        toolHeight, toolWidth = alpha_mask.shape

        # Bounds for placing tools within
        lowerBound = 0.02
        # upperBound = 0.8

        # x, y = (
        #     random.randint(
        #         math.floor(lowerBound * trayWidth),
        #         math.ceil(upperBound * trayWidth),
        #     ),
        #     random.randint(
        #         math.floor(lowerBound * trayHeight), math.ceil(upperBound * trayHeight)
        #     ),
        # )

        # New Bounds system based on tool width and height (Tool size < Tray size)
        toolWidthUpperBound = trayWidth - toolWidth
        toolHeightUpperBound = trayHeight - toolHeight
        x, y = (
            random.randint(
                math.floor(lowerBound * trayWidth),
                toolWidthUpperBound,
            ),
            random.randint(math.floor(lowerBound * trayHeight), toolHeightUpperBound),
        )

        # Overlay tool on tray on x and y coordinates
        overlay_image_alpha(trayCopy, img_overlay, x, y, alpha_mask)

        # Set file saving path
        path = os.path.join(outputFolder + fileName)

        # Save generated image
        cv2.imwrite(path + ".jpg", trayCopy)

        # Find tool name from tool file path and save its bounding box data
        toolName = re.search(r"\\(\w+)[^\.]*", col.files[randomIndex])[1]

        with open((path + ".txt"), "a") as f:
            f.write(f"{toolName} {x} {y} {toolWidth} {toolHeight}\n")

    results.append(trayCopy)


if type(emptyTrayGeneration) == int:
    for i in range(emptyTrayGeneration):
        fileName = f"{trayName}_empty_{i}_{timestr}"
        path = os.path.join(outputFolder + fileName)
        shutil.copyfile(trayPath, path + ".jpg")
        with open((path + ".txt"), "a") as f:
            pass
# cv2.namedWindow("image", cv2.WINDOW_NORMAL)
# cv2.imshow("image", trayCopy)
# cv2.resizeWindow("image", math.ceil(trayWidth / 2), math.floor(trayHeight / 2))
# cv2.waitKey(0)


# Display resultant images code
# w = 10
# h = 10
# fig = plt.figure(figsize=(5, 1))
# columns = 5
# rows = 1

# imgIndex = 0
# print(len(results))
# for i in range(1, columns * rows + 1):
#     print(imgIndex)
#     img = results[imgIndex]
#     imgIndex += 1
#     fig.add_subplot(rows, columns, i)
#     plt.imshow(img)
# plt.show()
