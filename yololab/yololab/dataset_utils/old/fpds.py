import sys
from pathlib import Path
import os

import imagesize
from pascal import BndBox, PascalObject, PascalVOC, size_block

lookup = {-1: "up", 1: "down"}

label_map = {
    lookup[-1]: 0,
    lookup[1]: 1,
}


class Convert:
    def add_file(self, filename, ext=".png"):
        fileimg = str(filename).replace(".txt", ext)
        try:
            w,h = imagesize.get(fileimg)
            objs = []
            with open(filename) as f:
                counter_box = 0
                for row in f.readlines():
                    box = [int(s.strip()) for s in row.split(" ")]
                    if not((0 < box[1] < w) or (0 < box[2] < h) or (0 < box[3] < w) or (0 < box[4] < h)):
                        raise
                    objs.append(
                        PascalObject(
                            lookup[box[0]],
                            "person",
                            truncated=False,
                            difficult=False,
                            bndbox=BndBox(box[1], box[3], box[2], box[4]),
                        )
                    )
            print(f"convert {filename}")
        except:
            print(f"skip {fileimg}")
            os.remove(str(filename))
            os.remove(str(fileimg))
            return


        # save pascal voc
        pascal_ann = PascalVOC(filename.name, size=size_block(w, h, 3), objects=objs)
        filexml = str(filename).replace(".txt", ".xml")
        pascal_ann.save(filexml)

        # save yolo
        yolo = pascal_ann.to_yolo(label_map)
        with open(str(filename), "w") as f:
            f.write(yolo)


    def add_folder(self, folder: str):
        ds = Path(folder)
        for p in ds.rglob("*.txt"):
            self.add_file(p)

def main():
    convert = Convert()
    for folder in sys.argv[1:]:
        convert.add_folder(folder)


if __name__ == "__main__":
    main()
