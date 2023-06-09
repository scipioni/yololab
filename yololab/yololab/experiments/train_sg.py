# https://www.kaggle.com/general/409402
# https://colab.research.google.com/drive/1y3WizmNlta6J6BWm46ZfFw1fqpFBSyYM?usp=sharing#scrollTo=9dYhaydLvuCO

import sys

from super_gradients.training import Trainer, dataloaders, models
from super_gradients.training.dataloaders.dataloaders import (
    coco_detection_yolo_format_train,
    coco_detection_yolo_format_val,
)
from super_gradients.training.losses import PPYoloELoss
from super_gradients.training.metrics import DetectionMetrics_050
from super_gradients.training.models.detection_models.pp_yolo_e import (
    PPYoloEPostPredictionCallback,
)

CHECKPOINT_DIR = "checkpoints"
try:
    CHECKPOINT_NAME = sys.argv[1]
except:
    CHECKPOINT_NAME = "test1"
EPOCHS = 1

dataset_params = {
    "data_dir": "./datasets/fpds",
    "train_images_dir": "train/split1",
    "train_labels_dir": "train/split1",
    "val_images_dir": "valid/split12",
    "val_labels_dir": "valid/split12",
    "test_images_dir": "test/split4",
    "test_labels_dir": "test/split4",
    "classes": ["up", "down"],
    "batch_size": 16,
}


train_data = coco_detection_yolo_format_train(
    dataset_params={
        "data_dir": dataset_params["data_dir"],
        "images_dir": dataset_params["train_images_dir"],
        "labels_dir": dataset_params["train_labels_dir"],
        "classes": dataset_params["classes"],
    },
    dataloader_params={"batch_size": dataset_params["batch_size"], "num_workers": 2},
)

val_data = coco_detection_yolo_format_val(
    dataset_params={
        "data_dir": dataset_params["data_dir"],
        "images_dir": dataset_params["val_images_dir"],
        "labels_dir": dataset_params["val_labels_dir"],
        "classes": dataset_params["classes"],
    },
    dataloader_params={"batch_size": dataset_params["batch_size"], "num_workers": 2},
)


# train_data.dataset.plot()

model = models.get(
    "yolo_nas_s", num_classes=len(dataset_params["classes"]), pretrained_weights="coco"
)


train_params = {
    # ENABLING SILENT MODE
    "silent_mode": False,
    "average_best_models": True,
    "warmup_mode": "linear_epoch_step",
    "warmup_initial_lr": 1e-6,
    "lr_warmup_epochs": 3,
    "initial_lr": 5e-4,
    "lr_mode": "cosine",
    "cosine_final_lr_ratio": 0.1,
    "optimizer": "Adam",
    "optimizer_params": {"weight_decay": 0.0001},
    "zero_weight_decay_on_bias_and_bn": True,
    "ema": True,
    "ema_params": {"decay": 0.9, "decay_type": "threshold"},
    # ONLY TRAINING FOR 10 EPOCHS FOR THIS EXAMPLE NOTEBOOK
    "max_epochs": EPOCHS,
    "mixed_precision": True,
    "loss": PPYoloELoss(
        use_static_assigner=False,
        # NOTE: num_classes needs to be defined here
        num_classes=len(dataset_params["classes"]),
        reg_max=16,
    ),
    "valid_metrics_list": [
        DetectionMetrics_050(
            score_thres=0.1,
            top_k_predictions=300,
            # NOTE: num_classes needs to be defined here
            num_cls=len(dataset_params["classes"]),
            normalize_targets=True,
            post_prediction_callback=PPYoloEPostPredictionCallback(
                score_threshold=0.01,
                nms_top_k=1000,
                max_predictions=300,
                nms_threshold=0.7,
            ),
        )
    ],
    "metric_to_watch": "mAP@0.50",
}


trainer = Trainer(experiment_name=CHECKPOINT_NAME, ckpt_root_dir=CHECKPOINT_DIR)


trainer.train(
    model=model,
    training_params=train_params,
    train_loader=train_data,
    valid_loader=val_data,
)
