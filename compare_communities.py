from PIL import Image
import numpy as np
import os
from itertools import combinations
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

def compare_images(image_path_1, image_path_2):
    # Open the images
    img1 = Image.open(image_path_1)
    img2 = Image.open(image_path_2)

    # Ensure images have the same size
    if img1.size != img2.size:
        print("Images must be the same size")
        return

    # Convert images to numpy arrays
    img1_np = np.array(img1)
    img2_np = np.array(img2)

    # Compute mask for overlapping non-transparent pixels with different RGB values
    overlap_mask = (img1_np[:, :, :3] != img2_np[:, :, :3])
    alpha_mask = (img1_np[:, :, 3] > 0) & (img2_np[:, :, 3] > 0)

    # The final mask considers both RGB differences and non-zero alpha values
    mask = np.all(overlap_mask, axis=2) & alpha_mask

    # Compute the overlap score
    score = np.sum(mask * ((img1_np[:, :, 3] / 255.0) * (img2_np[:, :, 3] / 255.0)))

    # Sum of the alpha values for non-transparent pixels
    alpha_sum = np.sum(img1_np[:, :, 3][alpha_mask])

    # Normalize the score
    if alpha_sum != 0:
        normalized_score = score / (alpha_sum / 255.0)
    else:
        normalized_score = 0

    return normalized_score

def compare_all_images(directory):
    # Get a list of all image files in the directory
    image_files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Initialize a dictionary to hold the scores
    scores = {}

    # Compute the score for each pair of images
    for img1, img2 in combinations(image_files, 2):
        logging.info(f"comparing {img1} and {img2}")
        score = compare_images(os.path.join(directory, img1), os.path.join(directory, img2))
        scores[(img1, img2)] = score

    return scores

# Test the function
directory = 'D:/CPM_no_adjacency_000003/logs/images'
scores = compare_all_images(directory)
# Sort the dictionary by values (scores)
sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

for pair, score in sorted_scores:
    print(f'Overlap score for {pair[0]} and {pair[1]}: {score}')
