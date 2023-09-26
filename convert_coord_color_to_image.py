import csv
from PIL import Image
import numpy as np
# read most common colors csv

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

with open("D:/most_common_colors_canada.csv", 'r') as f:
    reader = csv.reader(f)
    most_common_colors = list(reader)

    # write to image
    w, h = 61, 33
    data = np.zeros((h, w, 4), dtype=np.uint8)
    for pixel in most_common_colors:
        row = int(pixel[0])-91
        col = int(pixel[1])-151
        data[col, row] = hex_to_rgb(pixel[2]) + (255,)
    img = Image.fromarray(data, 'RGBA')
    img.save("D:/most_common_colors.png")
    print("done")
