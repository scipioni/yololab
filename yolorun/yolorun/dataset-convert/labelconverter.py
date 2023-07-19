import os
import pathlib
from pylabel import importer, exporter, visualize, analyze


class WhatFormat:
    def __init__(self, sample):
        self.sample = sample
        self.sformat = ""
        self.Voc = self.isVoc()
        self.Coco = self.isCoco()
        self.Yolo = self.isYolo()

    def isVoc(self):
        if os.path.splitext(self.sample)[-1].lower() == ".xml":
            print(f"Detected Voc format")
            self.sformat = "voc"
            return self.sformat

    def isCoco(self):
        if os.path.splitext(self.sample)[-1].lower() == ".json":
            print(f"Detected Coco format")
            self.sformat = "coco"
            return self.sformat

    def isYolo(self):
        if os.path.splitext(self.sample)[-1].lower() == ".txt":
            print(f"Detected Yolo format")
            self.sformat = "yolo"
            return self.sformat


class Importer:
    def __init__(self, sample, imgdir):
        self.imgdir = imgdir
        self.sample = sample
        self.labdir = sample.parent
        self.lblext = WhatFormat(self.sample)
        self.isVoc = True if self.lblext.sformat == "voc" else False
        self.isCoco = True if self.lblext.sformat == "coco" else False
        self.isYolo = True if self.lblext.sformat == "yolo" else False
        self.dataset = None
        self.dataset = self.importVoc(self.dataset)
        self.dataset = self.importCoco(self.dataset)
        self.dataset = self.importYolo(self.dataset)

    def importVoc(self, dataset):
        if self.isVoc:
            return importer.ImportVOC(path=self.labdir, path_to_images=self.imgdir)
        return dataset

    def importCoco(self, dataset):
        if self.isCoco:
            return importer.ImportCoco(path=self.sample, path_to_images=imgdir)
        return dataset

    def importYolo(self, dataset):
        if self.isYolo:
            return importer.ImportYoloV5(path=self.labdir, path_to_images=self.imgdir)
        return dataset


class Conversion:
    def __init__(self, labdir, imgdir, output_format, dataset):
        self.output_format = output_format
        self.dataset = dataset
        self.imgdir = imgdir
        self.labdir = labdir

    def toSelected(self):
        if self.output_format == "voc":
            print(f'Processing: {self.labdir.parent}')
            self.dataset.export.ExportToVoc(
                output_path=self.labdir,
                segmented_=False,
                path_=self.labdir,
                database_=False,
                folder_=False,
                occluded_=False,
            )

        if self.output_format == "coco":
            print(f'Processing: {self.labdir.parent}')
            self.dataset.export.ExportToCoco(cat_id_index=-1)

        if self.output_format == "yolo":
            print(f'Processing: {self.labdir.parent}')
            self.dataset.export.ExportToYoloV5(
                output_path=self.imgdir,
                yaml_file="dataset.yaml",
                copy_images=False,
                use_splits=False,
                cat_id_index=None,
                segmentation=False,
            )
