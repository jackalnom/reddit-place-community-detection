from PIL import Image
import os

# The directory containing the images
image_dir = 'D:/good/images/'
output_dir = 'D:/good/'

# The color of the background (dark grey)
background_color = (50, 50, 50, 255)

# Iterate over all files in the directory
for filename in os.listdir(image_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):  # Add more conditions if there are other image file types
        # Open the image file
        img = Image.open(os.path.join(image_dir, filename))

        # Create a new image with the same size and the background color
        background = Image.new('RGBA', img.size, background_color)

        # Superimpose the original image onto the new image
        background.paste(img, (0, 0), img)

        # Save the new image
        background.save(os.path.join(output_dir, filename))
