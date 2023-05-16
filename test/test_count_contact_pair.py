import unittest
import pathlib
import os
import sys

sys.path.append('..')
from check_contact import count_contact_pair

test_dir = pathlib.Path(__file__).parent.resolve()
test_data = os.path.join(test_dir, 'data')

check_contact_exe = '../check_contact.exe'

class TestCountContact(unittest.TestCase):
    def test_count_10(self):
        chain1 = os.path.join(test_data, 'dummy_one-ca.pdb')
        chain2 = os.path.join(test_data, 'dummy_10-close.pdb')
        self.assertEqual(count_contact_pair(chain1_path=chain2, chain2_path=chain1, exe_path=check_contact_exe), 10)

    def test_count_9(self):
        chain1 = os.path.join(test_data, 'dummy_one-cb.pdb')
        chain2 = os.path.join(test_data, 'dummy_9-close-1-far.pdb')
        self.assertEqual(count_contact_pair(chain1_path=chain2, chain2_path=chain1, exe_path=check_contact_exe), 9)

