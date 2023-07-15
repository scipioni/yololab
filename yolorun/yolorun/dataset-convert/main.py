import argparse
import glob
import os
import pathlib
from pathlib import Path

import labelconverter as lconvert

parser = argparse.ArgumentParser()
parser.add_argument("sdir", type=str, help="input directory")
parser.add_argument(
    "labelformat",
    type=str,
    help="label output format",
)
args = parser.parse_args()
args_dict = vars(args)


class Automator:
    def __init__(self):
        self.sdir = args.sdir
        self.labelext = [".txt", ".xml", ".json"]
        self.imgext = [".jpg", ".png"]
        self.labdir = []
        self.imgdir = []
        self.labsample = []
        

    def dirscan(self, dir, labelext, imgext):

        subfolders = []

        for f in os.scandir(dir):
            if f.is_dir():
                # print(f'======== {Path(f)} =======')
                subfolders.append(f.path)
            if f.is_file():
                if os.path.splitext(f.name)[-1].lower() in self.labelext and Path(f.path).parent not in self.labdir:
                    sample = Path(f.path)
                    labfolder = sample.parent
                    self.labsample.append(sample)
                    self.labdir.append(labfolder)
                    break

                if os.path.splitext(f.name)[-1].lower() in self.imgext and Path(f.path).parent not in self.imgdir:
                    imgfolder = Path(f.path).parent

                    self.imgdir.append(imgfolder)
                    break

        for dir in list(subfolders):
            # print(f'-------{Path(dir)}-------')
            sf = self.dirscan(dir, self.labelext, self.imgext)

        return subfolders


    def autoConvert(self, labdir, imgdir):

        for img, lbl, sample in zip(self.imgdir, self.labdir, self.labsample):
            if img.parent == lbl.parent and sample.parent == lbl:
                print(f'Converting {lbl.parent}')
                importer = lconvert.Importer(sample, img)
                converter = lconvert.Conversion(lbl, img, args.labelformat, importer.dataset)
                exported = converter.toSelected()

    def main(self):
        scan = self.dirscan(self.sdir, self.labelext, self.imgext)
        automatedConversion = self.autoConvert(self.labdir, self.imgdir)


automator = Automator()
conversion = automator.main()
