import tarfile
import glob
import re

reT = re.compile(r'.*?.txt')

for tar_filename in glob.glob(r'D:\*.tar'):
    try:
        t = tarfile.open(tar_filename, 'r')
    except IOError as e:
        print(e)
    else:
        print("Oh god")
        t.extractall('outdir', members=[m for m in t.getmembers() if reT.search(m.name)])