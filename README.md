# YOLOLAB


https://github.com/ultralytics/ultralytics

## prereq

- python >= 3.9
- wget
- taskfile https://taskfile.dev

for CUDA suppor on arch
- sudo pacman -S opencv-cuda python-opencv

## setup

```
go-task venv
```

custom opencv
```
# install fake (dummy) opencv-python
pip install -e opencv-python

# build opencv
scripts/build-build.sh
```

### ultralytics config

edit ~/.config/Ultralytics/settings.yaml to use <yololab> root dir for `dataset` and `runs` 


## export engine format

```
pip install nvidia-tensorrt
yolo export model=models/yolov8n.pt imgsz=640 format=engine device=0
```

## test fpds

## label studio

convert from yolo
```
pip install label-studio-converter

cd /archive/dataset/fp/unused/granny/
ln -s . images
ln -s . labels
label-studio-converter import yolo -i /archive/dataset/fp/unused/granny/ -o /tmp/ls-granny.json
```

```
yolo-folder
  images
   - 1.jpg
   - 2.jpg
   - ...
  labels
   - 1.txt
   - 2.txt

  classes.txt
```

## dataset

### pothole

https://learnopencv.com/train-yolov8-on-custom-dataset/

```
task download
```

### fpds fallen people data set

https://gram.web.uah.es/data/datasets/fpds/index.html


### CAUCAFall 

dataset for human fall recognition in an uncontrolled environment

https://www.sciencedirect.com/science/article/pii/S2352340922008162



### VFP290K

```
dsconvert --sdir datasets/GOPR0802/images/ --ddir datasets/GOPR0802/images/ --iw voc --ow yolo
```
