import fiftyone as fo
import fiftyone.zoo as foz

fo.config.dataset_zoo_dir = "/run/media/francesco/DATASET/datasets/openimages_v7"

dataset = foz.load_zoo_dataset(
              "open-images-v7",
              split="train",
              label_types=["detections"],
              classes=["Person", "Bed", "Sofa bed"],
              shuffle=False,
          )