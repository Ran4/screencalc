"""Testing for screencalc module
"""
import unittest
from math import sqrt
import math

import screencalc
from screencalc import Resolution

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
        dpi = screencalc.get_dpi(x_res=1, y_res=1, diagonal_in=sqrt(2))
        self.assertAlmostEqual(dpi, 1)
        
        dpi_2 = screencalc.get_dpi(x_res=100, y_res=100, diagonal_in=sqrt(2))
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
        
    def test_gt(self):
        """resolution1 > resolution2 returns a string showing where
        they differ.
        """
        x220_res =   screencalc.Resolution(1366, 768, 12.5)
        l412_res =   screencalc.Resolution(1366, 768, 14.1)
        l412_hires = screencalc.Resolution(1600, 900, 14.1)
        mbpr13 = screencalc.Resolution(2560, 1600, 13.3)
        
        r1 = l412_hires
        r2 = mbpr13
        string_diff = r1 > r2
        
        #~ print("\n")
        #~ print(r1)
        #~ print(r2)
        #~ print(string_diff)
        
        self.assertIsInstance(string_diff, str)
        
class GuessResolutionFromStringTests(unittest.TestCase):
    def test_guess_diag_from_string(self):
        for fr, to in [
            ('22"', 22), ('2"', 2), ('400"', 400),
            ("22'", 22), ("2'", 2), ("400'", 400),
            ("22 inch", 22), ("2 inch", 2), ("400 inch", 400),
            ("22 inches", 22), ("2 inches", 2), ("400 inches", 400),
            ("22. inch", 22), ("2. inch", 2), ("400. inch", 400),
            ("22.3 inch", 22.3), ("2.4 inch", 2.4), ("400.5 inch", 400.5),
            ("22.3 inches", 22.3), ("2.4 inches", 2.4), ("400.5 inches", 400.5)
            ]:
            self.assertEqual(screencalc._guess_diag_from_string(fr), to)
            
            
    def _assert_res_has_diag_x_y_size(self, res, diag, x, y, size):
        if res.diag is not None:
            self.assertEqual(res.diag, diag)
        if x and y:
            self.assertEqual((res.x, res.y), (x, y))
        if size is not None:
            self.assertEqual(res.size, size)
            
    def test_functionally(self):
        self._assert_res_has_diag_x_y_size(
            res=screencalc.guess_resolution_from_string('24" 1920x1080'),
            diag=24, x=1920, y=1080, size=None)
        
        self._assert_res_has_diag_x_y_size(
            res=screencalc.guess_resolution_from_string('24" 1920*1080'),
            diag=24, x=1920, y=1080, size=None)
        
        self._assert_res_has_diag_x_y_size(
            res=screencalc.guess_resolution_from_string('40" 4k'),
            diag=40, x=3840, y=2160, size=None)
        
        self._assert_res_has_diag_x_y_size(
            res=screencalc.guess_resolution_from_string('32" 1080p'),
            diag=32, x=1920, y=1080, size=None)
        
def main():
    unittest.main()
    
if __name__ == "__main__":
    main()
