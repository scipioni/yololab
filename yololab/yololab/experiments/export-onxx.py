# https://www.kaggle.com/general/409402
# https://github.com/Hyuto/yolo-nas-onnx


import os

import torch
from super_gradients.training import Trainer, dataloaders, models
from super_gradients.training.dataloaders.dataloaders import (
    coco_detection_yolo_format_val,
)
from super_gradients.training.metrics import DetectionMetrics_050
from super_gradients.training.models.detection_models.pp_yolo_e import (
    PPYoloEPostPredictionCallback,
)
from torchinfo import summary

CHECKPOINT_DIR = "checkpoints"
CHECKPOINT_NAME = "my_first_yolonas_run"


dataset_params = {
    "data_dir": "./datasets/fpds",
    "test_images_dir": "test/split4",
    "test_labels_dir": "test/split4",
    "classes": ["up", "down"],
    "batch_size": 16,
}


best_model = models.get(
    "yolo_nas_s",
    num_classes=len(dataset_params["classes"]),
    checkpoint_path=os.path.join(CHECKPOINT_DIR, CHECKPOINT_NAME, "ckpt_best.pth"),
)


summary(
    model=best_model,
    input_size=(1, 3, 640, 640),
    col_names=["input_size", "output_size", "num_params", "trainable"],
    col_width=20,
    row_settings=["var_names"],
)

net = models.get("yolo_nas_s", pretrained_weights="coco")

onnx_filename = "models/yolo_nas_s_640.onnx"
models.convert_to_onnx(model=net, input_shape=(3,640,640), out_path=onnx_filename)
print(f"saved {onnx_filename}")

# model = best_model.cpu()
# model.eval()
# model.prep_model_for_conversion(input_size=(1, 3, 640, 640))

# dummy_input = torch.randn(1, 3, 640, 640, device="cpu")



# dummy_input = torch.randn(1, 3, 640, 640)
# # torch_out = torch_model(dummy_input)

# # Export the model
# torch.onnx.export(
#     model,  # model being run
#     dummy_input,  # model input (or a tuple for multiple inputs)
#     onnx_filename,  # where to save the model (can be a file or file-like object)
#     verbose=True,
#     input_names=["input"],
#     output_names=["output"],
#     opset_version=12,

#     #   export_params=True,        # store the trained parameter weights inside the model file
#     #   opset_version=12,          # the ONNX version to export the model to
#     #   do_constant_folding=True,  # whether to execute constant folding for optimization
#     #   input_names = ['input'],   # the model's input names
#     #   output_names = ['output'], # the model's output names
#     #   dynamic_axes={'input' : {0 : 'batch_size'},    # variable length axes
#     #                 'output' : {0 : 'batch_size'}}
# )

# torch.onnx.export(model, dummy_input, onnx_filename, opset_version=12)


# ## prediction
# # img_url = "https://www.mynumi.net/media/catalog/product/cache/2/image/9df78eab33525d08d6e5fb8d27136e95/s/e/serietta_usa_2_1/www.mynumi.net-USASE5AD160-31.jpg"

# from pathlib import Path

# p = Path("datasets/fpds")

# for filename in p.rglob("*png"):
#     print(f"predict on {filename}")
#     best_model.predict(str(filename)).show()
#     break


# ## evaluate model
# test_data = coco_detection_yolo_format_val(
#     dataset_params={
#         "data_dir": dataset_params["data_dir"],
#         "images_dir": dataset_params["test_images_dir"],
#         "labels_dir": dataset_params["test_labels_dir"],
#         "classes": dataset_params["classes"],
#     },
#     dataloader_params={"batch_size": dataset_params["batch_size"], "num_workers": 2},
# )

# trainer = Trainer(experiment_name=CHECKPOINT_NAME, ckpt_root_dir=CHECKPOINT_DIR)

# trainer.test(
#     model=best_model,
#     test_loader=test_data,
#     test_metrics_list=DetectionMetrics_050(
#         score_thres=0.1,
#         top_k_predictions=300,
#         num_cls=len(dataset_params["classes"]),
#         normalize_targets=True,
#         post_prediction_callback=PPYoloEPostPredictionCallback(
#             score_threshold=0.01, nms_top_k=1000, max_predictions=300, nms_threshold=0.7
#         ),
#     ),
# )
