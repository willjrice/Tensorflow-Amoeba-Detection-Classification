#Code to crop images by a specified amount
import os
from PIL import Image

directory = '/path/to/your/images'
for root, dirs, files in os.walk(directory):
    for file in files:
        if file != '.DS_Store':
            img = Image.open(str(root) + '/' + str(file))
            width, height = img.size
            crop_amount = 4 #change this to liking
            # Calculate the new dimensions after cropping
            new_width = width - crop_amount
            new_height = height - crop_amount
            # Define the cropping box (left, upper, right, lower)
            crop_box = (crop_amount, crop_amount, width - crop_amount, height - crop_amount)
            cropped_img = img.crop(crop_box)
            cropped_img.save(str(root) + '/' + str(file))
