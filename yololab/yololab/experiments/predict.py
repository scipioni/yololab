from super_gradients.training import models

# download to $HOME/.cache/torch/hub/checkpoints/yolo_nas_s_coco.pth
model = models.get("yolo_nas_s", pretrained_weights="coco")

from torchinfo import summary

summary(model=model, 
        input_size=(16, 3, 640, 640),
        col_names=["input_size", "output_size", "num_params", "trainable"],
        col_width=20,
        row_settings=["var_names"]
)

url = "https://previews.123rf.com/images/freeograph/freeograph2011/freeograph201100150/158301822-group-of-friends-gathering-around-table-at-home.jpg"
model.predict(url, conf=0.25).show()