import argparse
import os
import shutil
import glob


def main(sdir, ddir):

    for file_name in glob.glob(sdir + '/**/*', recursive=True):
        if os.path.isfile(file_name):
            if file_name.endswith("txt") or file_name.endswith("jpg") or file_name.endswith("png"):
                shutil.copy(file_name, ddir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdir")
    parser.add_argument("--ddir")
    args = parser.parse_args()
    main(args.sdir, args.ddir)




