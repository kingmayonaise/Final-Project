'''
Final Project
'''
from collections import Counter
from math import floor
from ggame import App, Color, LineStyle, Sprite, RectangleAsset, CircleAsset, EllipseAsset, PolygonAsset, ImageAsset, MouseEvent, Frame

red = Color(0xff0000, 1.0)
green = Color(0x00ff00, 1.0)
black = Color(0x000000, 1.0)
white=Color(0xffffff,1.0)
yellow=Color(0xffff00,1.0)

thinline = LineStyle(1, black)
noline=LineStyle(0,white)

class Background(App):
    def __init__(self):
        RectangleAsset(noline,black)

myapp=Background()
myapp.run()