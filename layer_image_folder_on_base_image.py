import PIL
import numpy as np
from PIL import Image
from csv import reader
from pathlib import Path
import logging
import os
import concurrent.futures
from PIL import ImageEnhance

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

base_image = Image.open("D:/reddit_place_final_image.png")
#base_image.putalpha(40)
base_image = ImageEnhance.Contrast(base_image).enhance(0.05)

dir = "D:/communities_CPM_no_adjacency_0000065/logs/images/"

def create_image(full_file):
    cluster_image = Image.open(full_file)
    composite_img = PIL.Image.alpha_composite(base_image, cluster_image)

    os.makedirs(dir + "composite_images/", exist_ok=True)
    composite_img.save(dir + "composite_images/" + full_file.name + '.png')
    logging.info("wrote " + full_file.name)

if __name__ == '__main__':
    logging.info("starting " + dir)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        files = Path(dir).glob('*.png')
        pool = executor.map(create_image, files)


