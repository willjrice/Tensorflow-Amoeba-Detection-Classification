#Code to uniformly cut out specific parts of the names of all images in a directory
import os
folder_path = '/path/to/your/images/'

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.xml')):
        old_path = os.path.join(folder_path, filename)
        new_name = filename[:4] + '.jpg' #adjust the string slicing based on your needs
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)

