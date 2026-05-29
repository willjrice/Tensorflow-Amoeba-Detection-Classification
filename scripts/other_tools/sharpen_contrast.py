#Code to sharpen, enhance, brighten, and saturate images
import os
from PIL import Image, ImageEnhance

directory_path = "/path/to/your/images"
for subdir, dirs, files in os.walk(directory_path):
    for file in files:
        file_path = os.path.join(subdir, file)
        #Check if file is an image
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            #Open the image
            img = Image.open(file_path)

            #Enhance sharpness
            enhancer = ImageEnhance.Sharpness(img)
            sharpened_img = enhancer.enhance(1.1) #Adjust factor to your liking

            #Save sharpened image to directory
            output_path = os.path.join(subdir, file)
            sharpened_img.save(output_path)
            print(f"Sharpened and saved: {file}")

for subdir, dirs, files in os.walk(directory_path):
    for file in files:
        file_path = os.path.join(subdir, file)
        #Check if file is an image
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            #Open the image
            img = Image.open(file_path)

            #Enhance contrast
            enhancer = ImageEnhance.Contrast(img)
            contrasted_img = enhancer.enhance(1.1) #Adjust factor to your liking

            #Save contrasted image to directory
            output_path = os.path.join(subdir, file)
            contrasted_img.save(output_path)
            print(f"Contrasted and saved: {file}")

for subdir, dirs, files in os.walk(directory_path):
    for file in files:
        file_path = os.path.join(subdir, file)
        #Check if the file is an image
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            #Open the image
            img = Image.open(file_path)

            #Enhance brightness
            enhancer = ImageEnhance.Brightness(img)
            brightened_img = enhancer.enhance(1.1) #Adjust factor to your liking

            #Save brightened image to directory
            output_path = os.path.join(subdir, file)
            brightened_img.save(output_path)
            print(f"Brightened and saved: {file}")

for subdir, dirs, files in os.walk(directory_path):
    for file in files:
        file_path = os.path.join(subdir, file)
        #Check if the file is an image
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            #Open the image
            img = Image.open(file_path)

            #Enhance saturation
            enhancer = ImageEnhance.Color(img)
            saturated_img = enhancer.enhance(1.1) #Adjust factor to your liking

            #Save the saturated image to the output directory
            output_path = os.path.join(subdir, file)
            saturated_img.save(output_path)
            print(f"Saturated and saved: {file}")
