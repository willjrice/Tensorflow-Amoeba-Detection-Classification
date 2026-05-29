#Code to split annotated images into quarters, alongside their associated xml files
#You probably want to split images then annotate them; I was a bit late in the game...
from PIL import Image
import os
import xml.etree.ElementTree as ET
import pathlib

def update_xml_for_tile(original_xml_path, image_width, image_height, tile_coords, output_xml_path, tile_name):
    tree = ET.parse(original_xml_path)
    root = tree.getroot()

    # Update image dimensions in the XML
    size_node = root.find('size')
    size_node.find('width').text = str(tile_coords[2] - tile_coords[0])  # tile_width
    size_node.find('height').text = str(tile_coords[3] - tile_coords[1]) # tile_height

    # Filter and adjust bounding box annotations
    for obj in root.findall('object'):
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)

        # Check if the object is within the current tile
        if xmin < tile_coords[2] and xmax > tile_coords[0] and ymin < tile_coords[3] and ymax > tile_coords[1]:
            # Adjust coordinates relative to the tile's top-left corner
            bbox.find('xmin').text = str(max(0, xmin - tile_coords[0]))
            bbox.find('ymin').text = str(max(0, ymin - tile_coords[1]))
            bbox.find('xmax').text = str(str(min(tile_coords[2] - tile_coords[0], xmax - tile_coords[0])))
            bbox.find('ymax').text = str(str(min(tile_coords[3] - tile_coords[1], ymax - tile_coords[1])))
        else:
            # Remove objects outside the current tile
            root.remove(obj)

    for element in root.iter('filename'): # Iterate through elements with the tag 'filename'  # Replace "old" with "new" in the filename
        element.text = tile_name  # Update the text of the element

    tree.write(output_xml_path)

def split_image(image_path, output_dir, xml_path):
    img = Image.open(image_path) #open image
    width, height = img.size #get dimensions

    # Calculate tile dimensions
    tile_width = width // 2 #split half width
    tile_height = height // 2 #split half length

    # Create tiles and save them
    for i in range(2): # rows
        for j in range(2): # columns
            left = j * tile_width
            top = i * tile_height
            right = (j + 1) * tile_width
            bottom = (i + 1) * tile_height

            # Ensure coordinates don't exceed image boundaries for the last tiles
            right = min(right, width)
            bottom = min(bottom, height)

            tile = img.crop((left, top, right, bottom))
            tile_name = f"{os.path.splitext(os.path.basename(image_path))[0]}_{i}_{j}.jpg"
            tile.save(os.path.join(output_dir, tile_name))

            tile_coords = (left, top, right, bottom)
            output_xml = tile_name[:-4] + '.xml'
            output_xml_path = os.path.join(output_dir, output_xml)
            update_xml_for_tile(xml_path, width, height, tile_coords, output_xml_path, tile_name)

directory_path = "/Users/willamrice/Desktop/Run_3_2/" #current images
output_path = "/Users/willamrice/Desktop/Run_3_2_Split/" #split images
for (root,dirs,files) in os.walk(directory_path): #for each letter
    for dir in dirs: #current letter
        print(dir)
        cur_dir = directory_path + dir #full path of dir
        cur_out = output_path + dir #full path for where to put
        for filename in os.listdir(cur_dir): #for an files in current letter
            if filename.lower().endswith('.jpg'):
                full_image = os.path.join(cur_dir, filename) #full image path
                xml_name = filename[:-4] + '.xml'
                full_xml = os.path.join(cur_dir, xml_name)
                split_image(full_image, cur_out, full_xml) #split procedure

