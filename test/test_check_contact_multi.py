import unittest
import pathlib
import os
import sys

sys.path.append('..')
from check_contact import check_contact_many, check_contact_many_parallel


test_dir = pathlib.Path(__file__).parent.resolve()
test_data = os.path.join(test_dir, 'data')

check_contact_exe = '../check_contact.exe'


class TestCheckContactMany(unittest.TestCase):
    def test_check_from_list(self):
        pairs = [ ('data/1pv4A.pdb', 'data/1pv4B.pdb'),   
                  ('data/1pv4A.pdb', 'data/1pv4C.pdb'),
                  ('data/1pv4D.pdb', 'data/1pv4C.pdb'),
                  ('data/3r12A.pdb', 'data/3r12B.pdb')
                 ]
        result = check_contact_many(pairs, 8, 10)
        expected = [True, False, True, True]
        self.assertEqual(result, expected)


    def test_check_from_list_parallel(self):
        pairs = [ ('data/1pv4A.pdb', 'data/1pv4B.pdb'),
                  ('data/1pv4A.pdb', 'data/1pv4C.pdb'),
                  ('data/1pv4D.pdb', 'data/1pv4C.pdb'),
                  ('data/3r12A.pdb', 'data/3r12B.pdb')
                 ]
        expected = [True, False, True, True]
        
        for _ in range(8):
            pairs += pairs
            expected += expected

        result = check_contact_many_parallel(pairs_list=pairs, num_series=5, cores=16)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
