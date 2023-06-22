import shutil
import os
import argparse

def main(cartella1, cartella2):
    for file in os.listdir(cartella1):
        if file.endswith('.txt'):
            shutil.copy(os.path.join(cartella1, file), cartella2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdir')
    parser.add_argument('--ddir')
    args = parser.parse_args()
    main(args.sdir, args.ddir)