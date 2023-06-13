import unittest
import pathlib
import os
import subprocess
import tempfile

test_dir = pathlib.Path(__file__).parent.resolve()
test_data = os.path.join(test_dir, 'data')

check_contact_exe = os.path.join(test_dir, '..', 'check_contact.exe')


class TestCheckContactUsingLibArg(unittest.TestCase):
    def test_exe(self):
        infile = os.path.join(test_data, 'testin_names_only.txt')
        rcsbpath = os.path.join(test_data, 'fakercsb')
        with tempfile.TemporaryDirectory() as td:
            outfile = os.path.join(td, 'out.txt')
            cmd = f'{check_contact_exe} {infile} {outfile} 8 10 {rcsbpath}'
            subprocess.run(cmd.split(), check=True)
            
            with open(outfile, 'r') as f:
                line = f.readline()
                a, b = line.split()
                self.assertEqual((a,b), ('1', '44'))
                line = f.readline()
                a, b = line.split()
                self.assertEqual((a,b), ('0', '0'))
                line = f.readline()
                a, b = line.split()
                self.assertEqual((a,b), ('1', '62'))
                line = f.readline()
                a, b = line.split()
                self.assertEqual((a,b), ('1', '116'))

