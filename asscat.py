# -*- coding: utf-8 -*-
import os, sys, math 
import numpy as np
from PIL import Image
from skimage.util.shape import view_as_blocks

class Muncher:
    ''' turns an image file into a unicode string representing that image 

        Keyword arguments:
        image_filename  -- the image filename
        char_pallet     -- an array of size 255 from light characters to dark
    ''' 
    def __init__(self, pallet_array, image_filename):
        self.pallet_array = pallet_array
        pixel_array = self.getPixels(image_filename)
        bw_pixel_array = self.grayscale(pixel_array)
        bw_pixel_array_mini = self.shrink(bw_pixel_array, 5)
        print self.munch(bw_pixel_array_mini)

    def munch(self, bw_pixels):
        text = ""
        for row in bw_pixels:
            for pixel in row:
                text += self.getChar(pixel/255) + " " 
            text += '\n'
        return text

    def getChar(self, ratio):
        i = int(len(self.pallet_array)*ratio)
        return self.pallet_array[i]

    def shrink(self, bw_array, n):
        width = bw_array.shape[0]
        blocked = view_as_blocks(bw_array, (n, n));
        shaped = blocked.reshape(-1, n*n)
        averaged = shaped.mean(axis=-1)
        reshaped = averaged.reshape(width/n, -1)
        return reshaped

    def grayscale(self, rgb_array):
        GREYIFY = np.array([0.3,0.59,0.11])
        return np.dot(rgb_array, GREYIFY)

    def getPixels(self, image_filename):
        img = Image.open(image_filename)
        img_array = np.array(img)
        return img_array
    
if __name__ == "__main__":
    if len(sys.argv) == 3:
        pallet_filename = sys.argv[1]
        image_filename = sys.argv[2]
        print "~★ welcome to asscat ★~"
        
        # setup 
        pallet_array = [line.rstrip('\n') for line in open(pallet_filename)]
        for i in range(1000):
            m = Muncher(pallet_array, image_filename)
    else:
        print "-× Usage: python asscat <pallet_filename> <image_filename> ×-"  
        exit(0)

