import unittest

from main import add, greet


class TestAdd(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)

    def test_add_zero(self):
        self.assertEqual(add(0, 5), 5)


class TestGreet(unittest.TestCase):
    def test_greet_returns_expected_message(self):
        self.assertEqual(greet("world"), "Hello, world!")

    def test_greet_with_empty_name(self):
        self.assertEqual(greet(""), "Hello, !")


if __name__ == "__main__":
    unittest.main()
