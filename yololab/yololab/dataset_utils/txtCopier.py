import shutil
import os
import argparse

def main(sdir, ddir):
    for file in os.listdir(sdir):
        if file.endswith('.txt'):
            shutil.copy(os.path.join(sdir, file), ddir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdir')
    parser.add_argument('--ddir')
    args = parser.parse_args()
    main(args.sdir, args.ddir)