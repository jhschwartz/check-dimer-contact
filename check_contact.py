import os
import subprocess
import tempfile

import pathlib
dir_ = pathlib.Path(__file__).parent.resolve()




def check_contact_from_file(pairs_list_file, thresh_max_dist=8, thresh_min_pairs=10, exe_path=f'{dir_}/check_contact.exe'):
    if not os.path.exists(exe_path):
        raise FileNotFoundError('check contact executable not found!')

    with tempfile.NamedTemporaryFile('w+b') as tf:
        cmd = f'{exe_path} {pairs_list_file} {tf.name} {thresh_max_dist} {thresh_min_pairs}'
        exe_result = subprocess.run(cmd.split())
        if exe_result.returncode != 0:
            raise RuntimeError(f'encountered error from {exe_path}: {exe_result.stderr} {exe_result.stdout}')

        tf.seek(0)

        results = []
        for line in tf:
            results.append(line.strip() == b'1')

        return results



def check_contact_many(pairs_list, thresh_max_dist, thresh_min_pairs, exe_path=f'{dir_}/check_contact.exe'):
    with tempfile.NamedTemporaryFile('w') as tf:
        for chain1_path, chain2_path in pairs_list:
            tf.write(f'{chain1_path} {chain2_path}\n')
        tf.seek(0)
        return check_contact_from_file(tf.name, thresh_max_dist, thresh_min_pairs, exe_path)



def check_contact_pair(chain1_path, chain2_path, thresh_max_dist=8, thresh_min_pairs=10, exe_path=f'{dir_}/check_contact.exe'):
    with tempfile.NamedTemporaryFile('w') as tf:
        tf.write(f'{chain1_path} {chain2_path}\n')
        tf.seek(0)
        result = check_contact_from_file(tf.name, thresh_max_dist, thresh_min_pairs, exe_path)
        return result[0]
