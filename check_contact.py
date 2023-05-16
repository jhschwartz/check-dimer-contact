import os
import subprocess
import tempfile
import multiprocessing
import itertools

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

        results_in_contact = []
        results_num_contact = []
        for line in tf:
            results_in_contact.append(line.split()[0] != b'0')
            results_num_contact.append(int(line.split()[1]))

        return results_in_contact, results_num_contact



def check_contact_many(pairs_list, thresh_max_dist, thresh_min_pairs, exe_path=f'{dir_}/check_contact.exe'):
    with tempfile.NamedTemporaryFile('w') as tf:
        for chain1_path, chain2_path in pairs_list:
            tf.write(f'{chain1_path} {chain2_path}\n')
        tf.seek(0)
        in_contact, _ = check_contact_from_file(tf.name, thresh_max_dist, thresh_min_pairs, exe_path)
        return in_contact



def count_contact_many(pairs_list, thresh_max_dist, thresh_min_pairs, exe_path=f'{dir_}/check_contact.exe'):
    with tempfile.NamedTemporaryFile('w') as tf:
        for chain1_path, chain2_path in pairs_list:
            tf.write(f'{chain1_path} {chain2_path}\n')
        tf.seek(0)
        _, counts = check_contact_from_file(tf.name, thresh_max_dist, thresh_min_pairs, exe_path)
        return counts



def count_contact_many_parallel(pairs_list, thresh_max_dist=8, thresh_min_pairs=10, exe_path=f'{dir_}/check_contact.exe', cores=8, num_series=1000):
    sub_lists = (pairs_list[i:i+num_series] for i in range(0, len(pairs_list), num_series))
    args = ((sl, thresh_max_dist, thresh_min_pairs, exe_path) for sl in sub_lists)
    with multiprocessing.Pool(processes=cores) as p:
        results = p.starmap(count_contact_many, args)
    return list(itertools.chain(*results))



def check_contact_many_parallel(pairs_list, thresh_max_dist=8, thresh_min_pairs=10, exe_path=f'{dir_}/check_contact.exe', cores=8, num_series=1000):
    sub_lists = (pairs_list[i:i+num_series] for i in range(0, len(pairs_list), num_series))
    args = ((sl, thresh_max_dist, thresh_min_pairs, exe_path) for sl in sub_lists)
    with multiprocessing.Pool(processes=cores) as p:
        results = p.starmap(check_contact_many, args)
    return list(itertools.chain(*results))



def check_contact_pair(chain1_path, chain2_path, thresh_max_dist=8, thresh_min_pairs=10, exe_path=f'{dir_}/check_contact.exe'):
    with tempfile.NamedTemporaryFile('w') as tf:
        tf.write(f'{chain1_path} {chain2_path}\n')
        tf.seek(0)
        result, _ = check_contact_from_file(tf.name, thresh_max_dist, thresh_min_pairs, exe_path)
        return result[0]


def count_contact_pair(chain1_path, chain2_path, thresh_max_dist=8, thresh_min_pairs=10, exe_path=f'{dir_}/check_contact.exe'):
    with tempfile.NamedTemporaryFile('w') as tf:
        tf.write(f'{chain1_path} {chain2_path}\n')
        tf.seek(0)
        _, result = check_contact_from_file(tf.name, thresh_max_dist, thresh_min_pairs, exe_path)
        return result[0]


