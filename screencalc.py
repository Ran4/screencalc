"""Helper functions and classes to calculate resolution/dpi/size of screens
with varying aspect ratios."""
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

def get_dpi(x_res, y_res, diagonal):
    """diagonal is in inch!"""
    total_number_of_pixels = x_res * y_res
    ratio = x_res / float(y_res)
    
    width, height = diag_to_ab(diagonal, ratio)
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
        self.recalculate()
        
    def recalculate(self):
        if self.x is not None and self.y is not None and self.diag is not None:
            self.dpi = get_dpi(self.x, self.y, self.diag)
            
        if self.x is not None and self.y is not None and self.size is None:
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
    
    print "h_surface: %s, h_thinkpad: %s" % (h_surface, h_thinkpad)
    print "h_surface/h_thinkpad: %s" % (h_surface / h_thinkpad)
    print
    print "w_surface: %s, w_thinkpad: %s" % (w_surface, w_thinkpad)
    print "w_surface/w_thinkpad: %s" % (w_surface / w_thinkpad)
    """
    
    lg = Resolution(3840, 2160, 40)
    print lg
    
    # _4k = Resolution(3840, 2160, 32)
    print "Laptops:"
    print Resolution(1366, 768, 12.5)
    print Resolution(1366, 768, 14.1)
    print Resolution(1600, 900, 14.1)
    print Resolution(1920, 1080, 14.1)
    print "\nScreens:"
    print Resolution(1680, 1050, 22)
    print Resolution(1920, 1080, 24)
    print Resolution(1920, 1200, 25.5)
    print Resolution(1920, 1080, 32)
    print Resolution(3840, 2160, 32)  #<3840x2160 @32", ppi=137.68>
    print "\nTv:s:"
    print Resolution(3840, 2160, 40)
    print Resolution(3840, 2160, 42)
    print Resolution(3840, 2160, 43)
    print Resolution(3840, 2160, 48)
    print Resolution(3840, 2160, 50)
    print Resolution(3840, 2160, 55)

def test():
    import test_screencalc
    test_screencalc.main()
    
if __name__ == "__main__":
    # test()
    main()
