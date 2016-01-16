"""Testing for screencalc module
"""
import unittest
from math import sqrt
import math

import screencalc

class FunctionsTests(unittest.TestCase):
    """Tests the standalone functions in screencalc
    """
    def test_get_diag(self):
        """Testing of function get_diag"""
        self.assertAlmostEqual(screencalc.get_diag(3, 4), 5)
        self.assertAlmostEqual(screencalc.get_diag(1, 1), sqrt(2))
        
    def test_unit_conversions(self):
        """Testing of cm_to_in and in_to_cm functions"""
        self.assertAlmostEqual(screencalc.cm_to_in(2.54), 1.0)
        self.assertAlmostEqual(screencalc.in_to_cm(1.0), 2.54)
        
    def test_get_dpi(self):
        """Testing of function get_dpi"""
        dpi = screencalc.get_dpi(x_res=1, y_res=1, diagonal=sqrt(2))
        self.assertAlmostEqual(dpi, 1)
        
        dpi_2 = screencalc.get_dpi(x_res=100, y_res=100, diagonal=sqrt(2))
        self.assertAlmostEqual(dpi_2, 100)
        
        dpi_3 = screencalc.get_dpi(1680, 1050, 22)
        self.assertAlmostEqual(dpi_3, 90.05, places=2)
        
class ResolutionTests(unittest.TestCase):
    """Tests the Resolution class"""
    def test_size(self):
        """Tests size calculations done by Resolution"""
        diagonal_in_inches = screencalc.cm_to_in(sqrt(2))
        resolution = screencalc.Resolution(x_res=10, y_res=10,
            diag=diagonal_in_inches)
        
        # ratio is 10/10 == 0, diagonal is sqrt(2) cm, size should be 1x1 cm
        self.assertAlmostEqual(resolution.size[0], 1)
        self.assertAlmostEqual(resolution.size[1], 1)
        
def main():
    unittest.main()
    
if __name__ == "__main__":
    main()
