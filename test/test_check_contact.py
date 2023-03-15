import unittest
import pathlib
import os
import sys

sys.path.append('..')
from check_contact import check_contact

test_dir = pathlib.Path(__file__).parent.resolve()
test_data = os.path.join(test_dir, 'data')

check_contact_exe = '../check_contact.exe'

class TestCheckContact(unittest.TestCase):
    def test_real_contact_true_1(self):
        chain1 = os.path.join(test_data, '3r12A.pdb')
        chain2 = os.path.join(test_data, '3r12B.pdb')
        self.assertTrue(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe))

    def test_real_contact_true_2(self):
        chain1 = os.path.join(test_data, '1pv4B.pdb')
        chain2 = os.path.join(test_data, '1pv4A.pdb')
        self.assertTrue(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe))

    def test_real_contact_true_3(self):
        chain1 = os.path.join(test_data, '1pv4B.pdb')
        chain2 = os.path.join(test_data, '1pv4C.pdb')
        self.assertTrue(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe))

    def test_real_contact_false_1(self):
        chain1 = os.path.join(test_data, '1pv4A.pdb')
        chain2 = os.path.join(test_data, '1pv4C.pdb')
        self.assertFalse(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe))

    def test_real_contact_false_2(self):
        chain1 = os.path.join(test_data, '1pv4B.pdb')
        chain2 = os.path.join(test_data, '1pv4D.pdb')
        self.assertFalse(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe))

    def test_dummy_contact_true_1(self):
        chain1 = os.path.join(test_data, 'dummy_one-ca.pdb')
        chain2 = os.path.join(test_data, 'dummy_10-close.pdb')
        self.assertTrue(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe))
    
    def test_dummy_contact_true_2(self):
        chain1 = os.path.join(test_data, 'dummy_one-cb.pdb')
        chain2 = os.path.join(test_data, 'dummy_10-close.pdb')
        self.assertTrue(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe))

    def test_dummy_contact_false_1(self):
        chain1 = os.path.join(test_data, 'dummy_one-cb.pdb')
        chain2 = os.path.join(test_data, 'dummy_9-close-1-far.pdb')
        self.assertFalse(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe))
    
    def test_dummy_contact_false_2(self):
        chain1 = os.path.join(test_data, 'dummy_one-cb.pdb')
        chain2 = os.path.join(test_data, 'dummy_10-far.pdb')
        self.assertFalse(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe))

    def test_dummy_thresh_modify_dist_TtoF(self):
        chain1 = os.path.join(test_data, 'dummy_one-cb.pdb')
        chain2 = os.path.join(test_data, 'dummy_10-close.pdb')
        self.assertFalse(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe, thresh_max_dist=7.9))

    def test_dummy_thresh_modify_dist_FtoT(self):
        chain1 = os.path.join(test_data, 'dummy_one-cb.pdb')
        chain2 = os.path.join(test_data, 'dummy_9-close-1-far.pdb')
        self.assertTrue(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe, thresh_max_dist=8.1))

    def test_dummy_thresh_modify_pairs_TtoF(self):
        chain1 = os.path.join(test_data, 'dummy_one-cb.pdb')
        chain2 = os.path.join(test_data, 'dummy_10-close.pdb')
        self.assertFalse(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe, thresh_min_pairs=11))

    def test_dummy_thresh_modify_pairs_FtoT(self):
        chain1 = os.path.join(test_data, 'dummy_one-cb.pdb')
        chain2 = os.path.join(test_data, 'dummy_9-close-1-far.pdb')
        self.assertTrue(check_contact(chain1_path=chain1, chain2_path=chain2, exe_path=check_contact_exe, thresh_min_pairs=9))

    def test_dummy_true_flipargs(self):
        chain1 = os.path.join(test_data, 'dummy_one-ca.pdb')
        chain2 = os.path.join(test_data, 'dummy_10-close.pdb')
        self.assertTrue(check_contact(chain1_path=chain2, chain2_path=chain1, exe_path=check_contact_exe))

    def test_dummy_false_flipargs(self):
        chain1 = os.path.join(test_data, 'dummy_one-cb.pdb')
        chain2 = os.path.join(test_data, 'dummy_9-close-1-far.pdb')
        self.assertFalse(check_contact(chain1_path=chain2, chain2_path=chain1, exe_path=check_contact_exe))

    def test_no_exe(self):
        chain1 = os.path.join(test_data, '3r12A.pdb')
        chain2 = os.path.join(test_data, '3r12B.pdb')
        with self.assertRaises(FileNotFoundError):
            check_contact(chain1_path=chain1, chain2_path=chain2, exe_path='./notarealfile')
