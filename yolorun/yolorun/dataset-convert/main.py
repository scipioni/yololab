import argparse
import glob
import os
import pathlib
from pathlib import Path
import multiprocessing

import labelconverter as lconvert

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
                if (
                    os.path.splitext(f.name)[-1].lower() in self.labelext
                    and Path(f.path).parent not in self.labdir
                ):
                    sample = Path(f.path)
                    labfolder = sample.parent
                    self.labsample.append(sample)
                    self.labdir.append(labfolder)
                    break

                if (
                    os.path.splitext(f.name)[-1].lower() in self.imgext
                    and Path(f.path).parent not in self.imgdir
                ):
                    imgfolder = Path(f.path).parent

                    self.imgdir.append(imgfolder)
                    break

        for dir in list(subfolders):
            # print(f'-------{Path(dir)}-------')
            sf = self.dirscan(dir, self.labelext, self.imgext)

        return subfolders



    def toConvert(self, labdir, imgdir, labsample):
        print(f'imgdir {self.imgdir}, labdir {self.labdir}, labsample {self.labsample}')
        for img, lbl, sample in zip(self.imgdir, self.labdir, self.labsample):
            if img.parent == lbl.parent and sample.parent == lbl:
                return lbl, img, sample

    def autoConvert(self, lbl, img, sample):
        print(f"Converting {lbl.parent}")
        importer = lconvert.Importer(sample, img)
        converter = lconvert.Conversion(
            lbl, img, args.labelformat, importer.dataset
        )
        exported = converter.toSelected()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sdir", type=str, help="input directory")
    parser.add_argument(
        "labelformat",
        type=str,
        help="label output format",
    )

    args = parser.parse_args()
    args_dict = vars(args)

    automator = Automator()
    scanning = automator.dirscan(automator.sdir, automator.labelext, automator.imgext)
    img, lbl, sample = automator.toConvert(automator.labdir, automator.imgdir, automator.labsample)
    conversion = automator.autoConvert(img, lbl, sample)
    # processing_args = [for i in list(automator.toConvert(automator.labdir, automator.imgdir, automator.labsample))]
    # print(f'Processing args are {processing_args}')


    # with multiprocessing.Pool(os.cpu_count()) as pool:
    #     pool.starmap(automator.autoConvert, processing_args)
    # pool.close()