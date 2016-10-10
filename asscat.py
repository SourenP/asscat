# -*- coding: utf-8 -*-
import os, sys, math 
import numpy as np
from PIL import Image
from skimage.util.shape import view_as_blocks
import cv2
import curses

class Muncher:
    ''' Displays webcam in text 
        @param  pallet_array    An array of characters to be used as pixels sorted from dark to light
        @param  resolution      The number of pixels each text character represents in the original webcam image
        @param  frame_count     Number of frames displayed

        Note that resolution might cause errors if image size or terminal size is change (going to fix this) 
    '''
    def __init__(self, pallet_array, resolution, frame_count):

        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

        self.getCamera()
        self.pallet_array = pallet_array

        for i in range(frame_count):
            frame = self.getFrame()
            text = self.munch(frame, resolution)

            stdscr.addstr(0, 0, text) 
            stdscr.refresh()

    def restart_line(self):
        sys.stdout.write('\r')
        sys.stdout.flush()

    def munch(self, frame, resolution):
        pixel_array = self.getPixels(frame)
        bw_pixel_array = self.grayscale(pixel_array)
        bw_pixel_array_mini = self.shrink(bw_pixel_array, resolution)
        text = self.toText(bw_pixel_array_mini)
        return text
        

    def getCamera(self):        
        print "Preparing camera..."
        camera_port = 0
        ramp_frames = 30
        self.camera = cv2.VideoCapture(camera_port)
        for i in xrange(ramp_frames):
            temp = self.getFrame() 
     
    def getFrame(self):
        retval, im = self.camera.read()
        return im

    def toText(self, bw_pixels):
        text = ""
        for row in bw_pixels:
            for pixel in row:
                text += self.getChar(pixel/255) + " " 
            text += '\n'
        return text

    def getChar(self, ratio):
        i = int((len(self.pallet_array)-1)*ratio)
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

    def getPixels(self, cv2_im):
        #pil_im = Image.fromarray(cv2_im)
        #img_array = np.array(pil_im)
        return cv2_im
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        pallet_filename = sys.argv[1]
        print "~★ welcome to asscat ★~"
        
        # setup 
        pallet_array = [line.rstrip('\n') for line in open(pallet_filename)]
   
        # run
        Muncher(pallet_array, 8, 100)

    else:
        print "Usage: python asscat <pallet_filename>"  
        exit(0)

