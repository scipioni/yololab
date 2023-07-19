import argparse
import sys, os, glob
import imagesize
import shutil

def export(txt, valids, config):
    txt_out = os.path.join(config.out, os.path.basename(txt))
    print(f"save {txt_out} with {valids}")
    with open(txt_out, "w") as f:
        for valid in valids:
            f.write(" ".join(valid))
            f.write("\n")
    jpg = txt.replace("txt", "jpg")
    jpg_out = os.path.join(config.out, os.path.basename(jpg))
    shutil.copy(jpg, jpg_out)


def filter_classes(txt, classes, classes_to_filter, classes_out, config):
    with open(txt) as f:
        objs = [[classes[int(s.split()[0])], s.split()[1:]] for s in f.readlines()]
    
    img_w, img_h = 0,0

    valids = []
    for obj in objs:
        if obj[0] in classes_to_filter:
            if obj[0] in ("person","man","woman","boy"):
                obj[0] = "up"
                if img_w == 0:
                    jpg = txt.replace("txt", "jpg")
                    img_w, img_h = imagesize.get(jpg)
                w, h = obj[1][2:]
                if w*img_w > h*img_h:
                    obj[0] = "down"
            if obj[0] == "sofa bed":
                obj[0] = "sofa"
            if "table" in obj[0]: # openimage 
                obj[0] = "diningtable" # coco
            valids.append([str(classes_out.index(obj[0])), obj[1][0], obj[1][1], obj[1][2], obj[1][3]])
    if valids:
        export(txt, valids, config)

def process(config):
    classes_to_filter = config.classes.split(",")
    with open(os.path.join(config.sdir, "obj.names")) as f:
        classes = [c.strip().lower() for c in f.readlines()]

    if not os.path.exists(config.out):
        os.makedirs(config.out)
    with open(config.coco) as f:
        classes_out = [c.strip() for c in f.readlines()]
    with open(os.path.join(config.out, "classes.txt"), "w") as f:
        f.write("\n".join(classes_out))

def main():


    parser = argparse.ArgumentParser()
    parser.add_argument('sdir', help='folder')
    parser.add_argument("--classes", default="bed,sofa bed,person,man,woman,boy,kitchen & dining room table,table,chair")
    parser.add_argument("--coco", default="/archive/dataset/fp/classes.txt")
    parser.add_argument("--out", default="/tmp/dataset")
    config = parser.parse_args()

    process(config)
    
    #for txt in glob.glob(os.path.join(config.sdir, "data", "*.txt")):
    #    if "classes.txt" in txt:
    #        continue
    #    filter_classes(txt, classes, classes_to_filter, classes_out, config)

if __name__ == '__main__':
    main()
