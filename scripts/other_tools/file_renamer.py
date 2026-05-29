#Code for appending a prefix to all images in a directory
import os

folder_path = "/path/to/your/images"
prefix = "prefix_"

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.xml')):
        if not filename.startswith(prefix):
            old_path = os.path.join(folder_path, filename)
            new_name = prefix + filename
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            print(new_name)


