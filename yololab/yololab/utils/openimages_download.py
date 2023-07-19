classes=["Bed", "Sofa bed", "Kitchen & dining room table", "Table", "Chair"]

import fiftyone as fo
import fiftyone.zoo as foz
#from fiftyone import ViewField as F
import fiftyone.utils.openimages as openimages
import argparse


def process(config):
    dataset = foz.load_zoo_dataset(
        "open-images-v7",
        split=config.split,
        classes=classes,
        shuffle=True,
        seed=51,
        max_samples=config.max,
        label_types=["detections"],
    )

    dataset.export(
        export_dir=config.out,
        dataset_type=fo.types.YOLOv4Dataset,
        label_field="ground_truth",
        )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", default="train", help="train or validation")
    parser.add_argument("--fiftyone", default="/archive/dataset/openimages", help="openimages cache directory")
    parser.add_argument("--out", default="/tmp/openimages", help="where put dataset")
    parser.add_argument("--show-classes", default="", help="show classes")
    parser.add_argument("--max", default=20000, type=int, help="maximum sample to download")
    config = parser.parse_args()

    fo.config.dataset_zoo_dir = config.fiftyone
    
    if config.show_classes:
        for c in openimages.get_classes():
            print(c)
    else:
        process(config)

if __name__ == '__main__':
    main()
