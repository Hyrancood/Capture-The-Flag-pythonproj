"""Тесты readmap"""
import unittest

import readmap

class MyTestCase(unittest.TestCase):
    def test_value_parser(self):
        self.assertEqual(readmap.parse_value("10"), 10)
        self.assertEqual(readmap.parse_value("10a"), "10a")
        self.assertEqual(readmap.parse_value("005"), 5)
        self.assertEqual(readmap.parse_value("-10"), "-10")
        with self.assertRaises(TypeError):
            readmap.parse_value(10)
        with self.assertRaises(TypeError):
            readmap.parse_value(None)
        with self.assertRaises(ValueError):
            readmap.parse_value("")

    def test_object_parser(self):
        self.assertEqual(readmap.parse_object("x:5, y:  8"), {'x':5, 'y':8})
        self.assertEqual(readmap.parse_object("x:105, y:b"), {'x': 105, 'y': 'b'})
        with self.assertRaises(TypeError):
            readmap.parse_object(10)
        with self.assertRaises(ValueError):
            readmap.parse_object("")
        with self.assertRaises(SyntaxError):
            readmap.parse_object("x:b,")
        with self.assertRaises(SyntaxError):
            readmap.parse_object("x::b")
        with self.assertRaises(ValueError):
            readmap.parse_object("x:,")
        with self.assertRaises(SyntaxError):
            readmap.parse_object("x: 15, x: 33")

    def test_file_parser(self):
        self.assertEqual(readmap.parse_file(["key:", "- x: 5, y:10"]), {'key': [{'x': 5, 'y': 10}]})
        self.assertEqual(readmap.parse_file(["key:", "second:"]), {'key': [], 'second': []})
        self.assertEqual(readmap.parse_file(["key:", "- x: 5, y:10", "-x: 15"]), {'key': [{'x': 5, 'y': 10}, {'x':15}]})
        with self.assertRaises(SyntaxError):
            readmap.parse_file(["key", "-x:5"])

    def test_name_validator(self):
        self.assertEqual(readmap.is_name_valid(["ru:название", "en: name"]), True)
        self.assertEqual(readmap.is_name_valid(["ru:название,en: name"]), True)
        self.assertEqual(readmap.is_name_valid(["ru: название"]), True)
        with self.assertRaises(ValueError):
            readmap.is_name_valid([])
        with self.assertRaises(ValueError):
            readmap.is_name_valid(["rue:название,en: name"])
        with self.assertRaises(SyntaxError):
            readmap.is_name_valid(["ru: название, ru: звание"])

    def test_sizes_validator(self):
        self.assertEqual(readmap.is_sizes_valid(["x: 10, y: 7"]), (True, 10, 7))
        self.assertEqual(readmap.is_sizes_valid(["x: 010", "y: 7"]), (True, 10, 7))
        with self.assertRaises(ValueError):
            readmap.is_sizes_valid(["x: 15"])
        with self.assertRaises(ValueError):
            readmap.is_sizes_valid(["x: 15, y: 10, w: 5"])
        with self.assertRaises(ValueError):
            readmap.is_sizes_valid(["x: 15, y: 0"])
        with self.assertRaises(TypeError):
            readmap.is_sizes_valid(["x: 15, y: ab"])
        with self.assertRaises(ValueError):
            readmap.is_sizes_valid(["x: 15, y: 30"])
        with self.assertRaises(ValueError):
            readmap.is_sizes_valid(["x: 55, y: 10"])

    def test_map_point_checker(self):
        self.assertEqual(readmap.check_if_point_in_map((3, 3), (5, 7)), True)
        self.assertEqual(readmap.check_if_point_in_map((5, 7), (5, 7)), True)
        self.assertEqual(readmap.check_if_point_in_map((1, 1), (5, 7)), True)
        with self.assertRaises(ValueError):
            readmap.check_if_point_in_map((0, 3), (10, 8))
        with self.assertRaises(ValueError):
            readmap.check_if_point_in_map((3, 0), (10, 8))
        with self.assertRaises(ValueError):
            readmap.check_if_point_in_map((11, 3), (10, 8))

    def test_platform_validator(self):
        gmap = [[False for _ in range(10)] for __ in range(10)]
        self.assertEqual(readmap.is_platforms_valid(["x:1, y:1"], 10, 10, gmap), True)
        self.assertEqual([[x == 0 and y == 9 for x in range(10)] for y in range(10)], gmap)
        self.assertEqual(readmap.is_platforms_valid(["x:2, y:2, w: 5"], 10, 10, gmap), True)
        self.assertEqual([[(x == 0 and y == 9) or (x in range(1, 1+5) and y ==8) for x in range(10)] for y in range(10)], gmap)
        with self.assertRaises(ValueError):
            readmap.is_platforms_valid(["x: 5"], 10, 10, [[False for _ in range(10)] for __ in range(10)])
        with self.assertRaises(ValueError):
            readmap.is_platforms_valid(["y: 5"], 10, 10, [[False for _ in range(10)] for __ in range(10)])
        with self.assertRaises(ValueError):
            readmap.is_platforms_valid(["x: 7, y: 5, w: 5"], 10, 10, [[False for _ in range(10)] for __ in range(10)])
        with self.assertRaises(ValueError):
            readmap.is_platforms_valid(["x: 7, y: 5, w: 3, h:7"], 10, 10, [[False for _ in range(10)] for __ in range(10)])

    def test_thorns_validator(self):
        gmap = [[False for _ in range(10)] for __ in range(10)]
        readmap.is_platforms_valid(["x:1, y:1, w:10"], 10, 10, gmap)
        self.assertEqual(readmap.is_thorns_valid(["x:2, y:2", "x:3, y:2"], 10, 10, gmap), True)
        with self.assertRaises(ValueError):
            readmap.is_thorns_valid(["x:2, y:2", "x:3, y:1"], 10, 10, gmap)
        with self.assertRaises(ValueError):
            readmap.is_thorns_valid(["x:2, y:2", "x:3, y:5"], 10, 10, gmap)
        with self.assertRaises(ValueError):
            readmap.is_thorns_valid(["x:11, y:2"], 10, 10, gmap)
        with self.assertRaises(ValueError):
            readmap.is_thorns_valid(["x:11"], 10, 10, gmap)

    def test_flags_validator(self):
        gmap = [[False for _ in range(10)] for __ in range(10)]
        readmap.is_platforms_valid(["x:1, y:1, w:10"], 10, 10, gmap)
        self.assertEqual(readmap.is_flags_valid(["color:red, x: 1, y:2", "color:blue, x:10, y:2"], 10, 10, gmap), True)
        with self.assertRaises(ValueError):
            readmap.is_flags_valid(["color:red, x: 1, y:1", "color:blue, x:10, y:2"], 10, 10, gmap)
        with self.assertRaises(ValueError):
            readmap.is_flags_valid(["color:red, x: 1, y:1", "color:blue, x:11, y:2"], 10, 10, gmap)
        with self.assertRaises(ValueError):
            readmap.is_flags_valid(["color:red, x: 1, y:1"], 10, 10, gmap)
        with self.assertRaises(ValueError):
            readmap.is_flags_valid(["color:red, x: 1, y:1", "color:bluu, x:10, y:2"], 10, 10, gmap)


if __name__ == '__main__':
    unittest.main()
