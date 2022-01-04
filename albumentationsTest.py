import cv2
import matplotlib.pyplot as plt
import re
import os
from utils import *
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt

import albumentations as A

BOX_COLOR = (255, 0, 0)  # Red
TEXT_COLOR = (255, 255, 255)  # White


def visualize_bbox(img, bbox, class_name, color=BOX_COLOR, thickness=2):
    """Visualizes a single bounding box on the image"""
    x_min, y_min, w, h = bbox
    x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)

    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)

    ((text_width, text_height), _) = cv2.getTextSize(
        class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1
    )
    cv2.rectangle(
        img,
        (x_min, y_min - int(1.3 * text_height)),
        (x_min + text_width, y_min),
        BOX_COLOR,
        -1,
    )
    cv2.putText(
        img,
        text=class_name,
        org=(x_min, y_min - int(0.3 * text_height)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.35,
        color=TEXT_COLOR,
        lineType=cv2.LINE_AA,
    )
    return img


def visualize(image, bboxes, category_ids, category_id_to_name):
    img = image.copy()
    for bbox, category_id in zip(bboxes, category_ids):
        class_name = category_id_to_name[category_id]
        img = visualize_bbox(img, bbox, class_name)
    plt.figure(figsize=(12, 12))
    plt.axis("off")
    plt.imshow(img)


image = cv2.imread("canvas.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

root = tk.Tk()
root.withdraw()

# test = "./10000718_1_on_RelineCore1LevelB"
test = filedialog.askopenfilenames()[0]
testName = re.search(r"\/(\w+)(?!.*\/)", test)[1]

img = cv2.imread(test)
print(testName)

toolBoundingBoxData = f"{testName}.txt"

with open(toolBoundingBoxData) as f:
    lines = f.readlines()

toolLabel, *dimensions = lines[0].split()

x, y, width, height = [int(dimension) for dimension in dimensions]
print(toolLabel, width, height, x, y)

cv2.rectangle(
    img,
    (x, y),
    (x + width, y + height),
    color=(0, 100, 200),
    thickness=2,
)

cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.imshow("image", img)
cv2.waitKey()
