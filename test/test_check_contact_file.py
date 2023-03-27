import unittest
import pathlib
import os
import sys

sys.path.append('..')
from check_contact import check_contact_from_file


test_dir = pathlib.Path(__file__).parent.resolve()
test_data = os.path.join(test_dir, 'data')

check_contact_exe = '../check_contact.exe'


class TestCheckContactFromFile(unittest.TestCase):
    def test_from_file(self):
        infile = os.path.join(test_data, 'testin.txt')
        results = check_contact_from_file(infile, 8, 10)
        expected = [False, False, True, True, True, False, True, True]
        self.assertEqual(results, expected)

