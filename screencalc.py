#!/usr/bin/env python3
"""Helper functions and classes to calculate resolution/dpi/size of screens
with varying aspect ratios."""
from __future__ import print_function
from __future__ import division
from termcolor import colored

import math
from math import sqrt

def get_diag(a, b):
    return math.hypot(a, b)

def in_to_cm(x):
    return x * 2.54

def cm_to_in(x):
    return x / 2.54

def parse_ratio(ratio):
    """Ducktype helper!
    [16, 9] -> 16/9.0
    (16, 9) -> 16/9.0
    1.33 -> 1.33
    """
    if isinstance(ratio, tuple) or isinstance(ratio, list):
        if len(ratio) != 2:
            raise Exception("[parse_ratio] argument ratio must be number"
                " or tuple/list with 2 elements")
        else:
            ratio = ratio[0] / float(ratio[1])
    return ratio

def get_dpi(x_res, y_res, diagonal_in):
    """diagonal is in inch!"""
    total_number_of_pixels = x_res * y_res
    ratio = x_res / float(y_res)
    
    width, height = diag_to_ab(diagonal_in, ratio)
    total_area_in_inch = width * height
    
    dpi = math.sqrt(total_number_of_pixels / total_area_in_inch)
    return dpi

def diag_to_ab(c, ratio):
    """Takes a diagonal and a ratio (of format e.g. 1.33 or [16, 9])
    and returns the sides (a, b), where a is the width and b is the height.
    """
    ratio = parse_ratio(ratio)
            
    """ Calculation: a**2 + b**2 = c**2. a/b = ratio => a = b * ratio
    => b**2  = c**2 / (ratio**2 + 1) => b = sqrt(c**2 / (ratio**2 + 1))"""
    b = sqrt(c**2 / (ratio**2 + 1.0))
    a = b * ratio
    return (a, b)

def _gt_colorize(xy_str, diag_str, dpi_str, size_str,
        resolution1, resolution2,
        color_better="green", color_worse="red"):
    """Analyses the two values of the lists xy_str, diag_str, dpi_str
    and size_str, colorizing them with colored() depending on
    pixel count et.c.
    """
    def recolor_array(arr, index, color):
        arr[index] = colored(arr[index], color)
        
    num_pixels = resolution1.x * resolution1.y
    num_pixels_other = resolution2.x * resolution2.y
        
    #Recoloring xy_str
    if num_pixels > num_pixels_other:
        recolor_array(xy_str, 0, color_better)
        recolor_array(xy_str, 1, color_worse)
    elif num_pixels < num_pixels_other:
        recolor_array(xy_str, 1, color_better)
        recolor_array(xy_str, 0, color_worse)
    else:
        pass #no need to change colors
    
    #Recoloring diag_str
    if resolution1.diag > resolution2.diag:
        recolor_array(diag_str, 0, color_better)
        recolor_array(diag_str, 1, color_worse)
    elif resolution1.diag < resolution2.diag:
        recolor_array(diag_str, 0, color_worse)
        recolor_array(diag_str, 1, color_better)
        
    #Recoloring dpi_str
    if all(dpi_str): #only recolor if both has dpi
        if resolution1.dpi > resolution2.dpi:
            recolor_array(dpi_str, 0, color_better)
            recolor_array(dpi_str, 1, color_worse)
        elif resolution1.dpi < resolution2.dpi:
            recolor_array(dpi_str, 0, color_worse)
            recolor_array(dpi_str, 1, color_better)
            
    #Recoloring size_str
    if all(size_str): #only recolor if both has size
        X, Y = 0, 1
        
        size = []
        for i in [X, Y]:
            if resolution1.size[i] > resolution2.size[i]:
                size.append([
                    colored(str(resolution1.size[i]), color_better),
                    colored(str(resolution2.size[i]), color_worse)])
            elif resolution1.size[i] < resolution2.size[i]:
                size.append([
                    colored(str(resolution1.size[i]), color_better),
                    colored(str(resolution2.size[i]), color_worse)])
            else:
                size.append([
                    str(resolution1.size[i]),
                    str(resolution2.size[i])])
        
                size_str = [size[0:2], size[2:4]]
        
        if resolution1.size > resolution2.size:
            recolor_array(size_str, 0, color_better)
            recolor_array(size_str, 1, color_worse)
        elif resolution1.size < resolution2.size:
            recolor_array(size_str, 0, color_worse)
            recolor_array(size_str, 1, color_better)

class Resolution(object):
    def __init__(self, x_res, y_res, diag=None, size=None):
        """
        :param x_res: resolution width
        :param y_res: resolution height
        :param diag: diagonal size in inches
        :param size: 2-tuple with size, (w, h), in cm
        """
        self.x = x_res
        self.y = y_res
        self.diag = diag
        self.dpi = None
        self.size = None  #w, h, in mm
        try:
            self.recalculate()
        except TypeError as e:
            print("TypeError: '{}' on {}"\
                .format(e, self.__repr__()))
            
    def __gt__(self, other):
        """resolution1 > resolution2 returns a string showing where
        they differ.
        
        
        >>> x220_res =   screencalc.Resolution(1366, 768, 12.5)
        >>> l412_res =   screencalc.Resolution(1366, 768, 14.1)
        >>> x220_res / l412_res
        "<1920x1080 @24", ppi=91.79, size=531*299>"
        "<1920x1080 @24", ppi=91.79, size=531*299>"
        """
        def _get_xy_diag_dpi_size_str(resolution):
            xy_str = "{0.x}x{0.y}".format(resolution)
            diag_str = ""
            dpi_str = ""
            size_str = ""
        
            if resolution.diag is not None:
                diag_str = ' @{0.diag}"'.format(resolution)
                if resolution.dpi is not None:
                    dpi_str = ", ppi={0.dpi:.2f}".format(resolution)
                    
                if resolution.size is not None:
                    size_str = ", size={w:.0f}*{h:.0f}".format(
                        w=resolution.size[0] * 10, h=resolution.size[1] * 10)
                    
            return xy_str, diag_str, dpi_str, size_str
        
        xy_str = []
        diag_str = []
        dpi_str = []
        size_str = []
        for i, resolution in enumerate([self, other]):
            xy_str_temp, diag_str_temp, dpi_str_temp, size_str_temp = \
                _get_xy_diag_dpi_size_str(resolution)
            xy_str.append(xy_str_temp)
            diag_str.append(diag_str_temp)
            dpi_str.append(dpi_str_temp)
            size_str.append(size_str_temp)
        
        _gt_colorize(xy_str, diag_str, dpi_str, size_str, self, other)

        diff_strings = ['<{}{}{}{}>'.format(
                xy_str[i], diag_str[i], dpi_str[i], size_str[i])
            for i, resolution in enumerate([self, other])]
        return "\n".join(diff_strings)
        
    def recalculate(self):
        if self.x is not None and self.y is not None and self.diag is not None:
            self.dpi = get_dpi(self.x, self.y, self.diag)
            
        if self.x is not None and self.y is not None and self.size is None:
            if self.diag is None:
                raise TypeError("self.diag is None")
            if self.x is None:
                raise TypeError("self.x is None")
            if self.y is None:
                raise TypeError("self.y is None")
            
            w_in, h_in = diag_to_ab(self.diag, [self.x, self.y])
            self.size = (in_to_cm(w_in), in_to_cm(h_in))
    
    def __repr__(self):
        """
        Example:
        "<1920x1080">"           #only resolution known
        "<1920x1080 @24">"       #only resolution and screen dimensions known
        "<1920x1080 @24", ppi=91.79>"      #unknown size
        "<1920x1080 @24", size=531*299>"   #unknown ppi
        "<1920x1080 @24", ppi=91.79, size=531*299>" #everything known
        """
        if self.diag is not None:
            dpi_str = ""
            
            if self.dpi is not None:
                dpi_str = ", ppi={0.dpi:.2f}".format(self)
                
            size_str = ""
            if self.size is not None:
                size_str = ", size={w:.0f}*{h:.0f}".format(
                    w=self.size[0] * 10,
                    h=self.size[1] * 10)
            
            return '<{0.x}x{0.y} @{0.diag}"{dpi_str}{size_str}>'.format(
                self, dpi_str=dpi_str, size_str=size_str)
        else:
            return '<{0.x}x{0.y}>'.format(self)

def main():
    """See if 13.5" 3:2 Surface book has a greater height than 14.1" 16:9
    w_surface, h_surface = diag_to_ab(13.5, [3, 2])
    
    w_thinkpad, h_thinkpad = diag_to_ab(14.1, [16, 9])
    
    print("h_surface: %s, h_thinkpad: %s" % (h_surface, h_thinkpad))
    print("h_surface/h_thinkpad: %s" % (h_surface / h_thinkpad))
    print()
    print("w_surface: %s, w_thinkpad: %s" % (w_surface, w_thinkpad))
    print("w_surface/w_thinkpad: %s" % (w_surface / w_thinkpad))
    """
    
    print("Laptops:")
    print(Resolution(1366, 768, 12.5))
    print(Resolution(1366, 768, 14.1))
    print(Resolution(1600, 900, 14.1))
    print(Resolution(1920, 1080, 14.1))
    print('\nMacBook 12"')
    print(Resolution(2304, 1440, 12.0), "Native")
    print(Resolution(1440, 900, 12.0))
    print(Resolution(1280, 800, 12.0))
    print(Resolution(1024, 640, 12.0))
    print('\nMacBook 13.3"')
    print(Resolution(2560, 1600, 13.3), "Native")
    print(Resolution(1920, 1200, 13.3))
    print(Resolution(1680, 1050, 13.3), "Highest default max")
    print(Resolution(1560, 975, 13.3), "Custom, between two highest")
    print(Resolution(1440, 900, 13.3), "Second highest default max")
    print(Resolution(1280, 800, 13.3), "2x scale")
    print('\nMacBook 15.4"')
    print(Resolution(2880, 1800, 15.4), "Native")
    print(Resolution(2560, 1600, 15.4))
    print(Resolution(1920, 1200, 15.4))
    print(Resolution(1800, 1125, 15.4), "Between 1680 and 1920")
    print(Resolution(1680, 1050, 15.4))
    print(Resolution(1560, 975, 15.4))
    print(Resolution(1440, 900, 15.4), "2x scale")
    print(Resolution(1280, 800, 15.4))
    print("\nScreens:")
    print(Resolution(1680, 1050, 22))
    print(Resolution(1920, 1080, 24))
    print(Resolution(1920, 1200, 25.5))
    print(Resolution(1920, 1080, 32))
    print(Resolution(3840, 2160, 32))  #<3840x2160 @32", ppi=137.68>
    x = 1440 / 2560.
    print(Resolution(int(3840 * x), int(2160 * x), 28),\
        "4k, with scaling as 1440/2560=0.5625")
    print(Resolution(int(3840 * x), int(2160 * x), 27),\
        "4k, with scaling as 1440/2560=0.5625")
    x2 = 1680 / 2560.
    print(Resolution(int(3840 * x2), int(2160 * x2), 28),\
        "4k, with scaling as 1680/2560=0.65625")
    x2 = 1680 / 2560.
    print(Resolution(3008, 1692, 28), "scaled 4k, 3008/3840=0.7833")
    print("\nTv:s:")
    print(Resolution(3840, 2160, 40))
    print(Resolution(3840, 2160, 42))
    print(Resolution(3840, 2160, 43))
    print(Resolution(3840, 2160, 48))
    print(Resolution(3840, 2160, 50))
    print(Resolution(3840, 2160, 55))
    print(Resolution(3008, 1692, 43), "scaled 4k, 3008/3840=0.7833")
    print("\nUltrawides:")
    print(Resolution(3440, 1440, diag=34))
    print(Resolution(3840, 1600, diag=38))
    print(Resolution(2 * 2560, 1440, diag=50), "(not real)")
    print()
    print("Custom:")
    print(Resolution(2560, 1600, diag=30), "custom, (not real)")
    print(Resolution(1440, 900, diag=14.1))
    print()
    print("4k (3840x2160) at different sizes:")
    for size in range(30, 51):
        if size in [31,33,34,35,36,37,38]: # Only print sizes that exist
            continue
        print(Resolution(3840, 2160, diag=size))

if __name__ == "__main__":
    main()
