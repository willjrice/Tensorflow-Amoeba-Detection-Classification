#Code for making all images in a directory grayscale
import os
from PIL import Image, ImageEnhance

directory_path = "/path/to/your/images"
for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Check if the file is an image (you can add more extensions as needed)
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Open the image file
            img = Image.open(file_path)

            # Black and white
            grayscale_img = img.convert('L')

            # Save 
            output_path = os.path.join(directory_path, filename)
            grayscale_img.save(output_path)
            print(f"Image saved as grayscale: {filename}")