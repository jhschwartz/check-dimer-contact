import unittest
import pathlib
import os
import sys

sys.path.append('..')
from check_contact import count_contact_many, count_contact_many_parallel


test_dir = pathlib.Path(__file__).parent.resolve()
test_data = os.path.join(test_dir, 'data')

check_contact_exe = '../check_contact.exe'


class TestCountContactMany(unittest.TestCase):
    def test_check_from_list(self):
        pairs = [ ('data/dummy_one-ca.pdb', 'data/dummy_one-cb.pdb'),   
                  ('data/dummy_10-far.pdb', 'data/dummy_one-ca.pdb.pdb'),
                  ('data/dummy_one-cb.pdb', 'data/dummy_10-close.pdb'),
                  ('data/dummy_10-close.pdb', 'data/dummy_10-close.pdb')
                 ]
        result = count_contact_many(pairs, 8, 10)
        expected = [1, 0, 10, 78]
        self.assertEqual(result, expected)


    def test_check_from_list_parallel(self):
        pairs = [ ('data/dummy_one-ca.pdb', 'data/dummy_one-cb.pdb'),   
                  ('data/dummy_10-far.pdb', 'data/dummy_one-ca.pdb.pdb'),
                  ('data/dummy_one-cb.pdb', 'data/dummy_10-close.pdb'),
                  ('data/dummy_10-close.pdb', 'data/dummy_10-close.pdb')
                 ]
        expected = [1, 0, 10, 78]
        
        for _ in range(8):
            pairs += pairs
            expected += expected

        result = count_contact_many_parallel(pairs_list=pairs, num_series=2, cores=16)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
