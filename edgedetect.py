from kivy.clock import mainthread
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
import numpy as np
import cv2
from camera4kivy import Preview
from kivy.logger import Logger
import image_processing as image_processing
from main_logic import main_logic

class EdgeDetect(Preview):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyzed_texture = None
        self.count = 0

    ####################################
    # Analyze a Frame - NOT on UI Thread
    ####################################

    def analyze_pixels_callback(self, pixels, image_size, image_pos, scale, mirror):
        # pixels : analyze pixels (bytes)
        # image_size   : analyze pixels size (w,h)
        # image_pos    : location of Texture in Preview (due to letterbox)
        # scale  : scale from Analysis resolution to Preview resolution
        # mirror : true if Preview is mirrored

        # Logger.info(f"Image Processing: Start")
        
        rgba   = np.fromstring(pixels, np.uint8).reshape(image_size[1],
                                                         image_size[0], 4)
        # Note, analyze_resolution changes the result. Because with a smaller
        # resolution the gradients are higher and more edges are detected.
        
        rgba1  = main_logic.main_logic(rgba)
            
        del(rgba)
        pixels = rgba1.tostring()
        # Logger.info(f"Image Processing: End")

        self.make_thread_safe(pixels, image_size) 

    @mainthread
    def make_thread_safe(self, pixels, size):
        if not self.analyzed_texture or\
           self.analyzed_texture.size[0] != size[0] or\
           self.analyzed_texture.size[1] != size[1]:
            self.analyzed_texture = Texture.create(size=size, colorfmt='rgba')
            self.analyzed_texture.flip_vertical()
        self.analyzed_texture.blit_buffer(pixels, colorfmt='rgba') 

    ################################
    # Annotate Screen - on UI Thread
    ################################

    def canvas_instructions_callback(self, texture, tex_size, tex_pos):
        # texture : preview Texture
        # size    : preview Texture size (w,h)
        # pos     : location of Texture in Preview Widget (letterbox)
        # Add the analyzed image
        if self.analyzed_texture:
            Color(1,1,1,1)
            Rectangle(texture= self.analyzed_texture,
                      size = tex_size, pos = tex_pos)










