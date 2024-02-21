import unittest
from mehditor.validators import LineNumber


class TestLineNumber(unittest.TestCase):

    def setUp(self):
        self.lineNumber = LineNumber()

    def test_validate_success_separated(self):
        self.assertTrue(self.lineNumber.validate("10:3").is_valid)

    def test_validate_success_simple(self):
        self.assertTrue(self.lineNumber.validate("10").is_valid)

    def test_validate_failure_wrong_format(self):
        self.assertFalse(self.lineNumber.validate("10:3:5").is_valid)

    def test_validate_failure_non_number(self):
        self.assertFalse(self.lineNumber.validate("a:b").is_valid)

if __name__ == '__main__':
    unittest.main()

