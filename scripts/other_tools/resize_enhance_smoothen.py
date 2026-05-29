#This is a program to adjust the images of amoeba that have been cut from an object identificaiton program.
#The program starts by enhancing the contrast in the well image, then counts the number of pixels that exceed a threshold set by the user.
#It was written by Helen Murphy in September 2025 and uses the sci-kit image package.


#import all the necessary libraries
import os
import glob
from skimage import data, util, filters, restoration, io, img_as_ubyte, exposure
#import skimage.io as io
from skimage.morphology import disk, ball
from skimage.transform import resize
import numpy as np

for dir in ['eaten', 'not_eaten', 'not_amoeba']:
    #finds the file
    #In the same directory, make sure there are directories called "gray", "resized", "enhanced" and "smoothed".
    os.chdir('/Users/willamrice/Downloads/Tensorflow/testspace/amoebas_og/' + dir)
    if not os.path.exists('/Users/willamrice/Downloads/Tensorflow/testspace/resized/'+dir): 
        os.makedirs('/Users/willamrice/Downloads/Tensorflow/testspace/resized/'+dir)
    if not os.path.exists('/Users/willamrice/Downloads/Tensorflow/testspace/enhanced/'+dir): 
        os.makedirs('/Users/willamrice/Downloads/Tensorflow/testspace/enhanced/'+dir)
    if not os.path.exists('/Users/willamrice/Downloads/Tensorflow/testspace/smoothened/'+dir): 
        os.makedirs('/Users/willamrice/Downloads/Tensorflow/testspace/smoothened/'+dir)
    #Create empty list to be populated with file names
    final_list = []

    #Get list of files in the directory
    final_list = os.listdir()
    #For some reason, some have this file. The name needs to be removed.
    final_list.remove('.DS_Store')

    #Lists all the files on the screen.
    print(final_list)

    #Loop through the names in the file list.
    for images in final_list:
        #gives files to skimage
        Amoeba = io.imread(images)

        #Resize image
        #Define new size (multiply height and width by 5)
        new_shape = (Amoeba.shape[0] * 5, Amoeba.shape[1] * 5, Amoeba.shape[2])
        #Resize the image (anti_aliasing helps smooth/interpolate)
        Amoeba_resize = resize(Amoeba, new_shape, anti_aliasing = True)
        #Make  0 to 255 scale, instead of 0 to 1
        Amoeba_resize_ubyte = img_as_ubyte(Amoeba_resize)
        io.imsave('/Users/willamrice/Downloads/Tensorflow/testspace/resized/'+dir+'/'+images, Amoeba_resize_ubyte)

        #Enhance the image
        Amoeba_enhanced = exposure.rescale_intensity(Amoeba_resize_ubyte, in_range='image', out_range='dtype')
        Amoeba_enhanced_ubyte = img_as_ubyte(Amoeba_enhanced)
        #Save the image
        io.imsave('/Users/willamrice/Downloads/Tensorflow/testspace/enhanced/'+dir+'/'+images, Amoeba_enhanced_ubyte)

        #Smooth the image
        Amoeba_smooth = filters.unsharp_mask(Amoeba_enhanced_ubyte, radius = 5, amount = 1)
        Amoeba_smooth_ubyte = img_as_ubyte(Amoeba_smooth)
        #Save the image
        io.imsave('/Users/willamrice/Downloads/Tensorflow/testspace/smoothened/'+dir+'/'+images, Amoeba_smooth_ubyte)
    print('Done')