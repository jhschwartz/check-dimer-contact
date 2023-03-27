from check_contact_OLD import check_contact as check_contact_pair_old
from check_contact_NEW import check_contact_from_file as check_contact_file_new

import time
import tempfile
import pickle
import sys

N = int(sys.argv[1])
out = sys.argv[2]

exe_old = './check_contact.exe_OLD'
exe_new = './check_contact.exe_NEW'

def bench_old(c1, c2):
    t = time.time()
    for _ in range(N):
        contacting = check_contact_pair_old(c1, c2, 8, 10, exe_old)
    e = time.time() - t
    return e / N


def bench_new(c1, c2):
    with tempfile.NamedTemporaryFile('w') as tf:
        for _ in range(N):
            tf.write(f'{c1} {c2}')
        tf.seek(0)

        t = time.time()
        results = check_contact_file_new(tf.name, 8, 10, exe_new)
        e = time.time() - t
        return e / N


results = [] 

with open('samples.txt') as f:
    for line in f:
        c1, c2, size = line.split()
        t_old_avg = bench_old(c1, c2)
        t_new_avg = bench_new(c1, c2)
        results.append( (size, t_old_avg, t_new_avg) )
        print(f'size: {size} | old: {round(t_old_avg, 6)} | new: {round(t_new_avg, 6)} | N: {N}')

with open(out, 'wb') as f:
    pickle.dump(results, f)




