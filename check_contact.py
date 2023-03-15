import os
import subprocess


def check_contact(chain1_path, chain2_path, thresh_max_dist=8, thresh_min_pairs=10, exe_path='./check_contact'):
    if not os.path.exists(exe_path):
        raise FileNotFoundError('check contact executable not found!')

    cmd = f'{exe_path} --c1 {chain1_path} --c2 {chain2_path} --threshold-max-contact-distance {thresh_max_dist} --threshold-min-pairs {thresh_min_pairs}'
    result = subprocess.run(cmd.split())

    if result.returncode == 0:
        return False
    elif result.returncode == 1:
        return True
    
    raise RuntimeError(f'unexpected check_contact executable result: {result.stdout} {result.stderr}')


