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

opencv rolling to fix some older CPUs 
```
pip install -U opencv-python-rolling<5.0.0
```

### ultralytics config

edit ~/.config/Ultralytics/settings.yaml to use <yololab> root dir for `dataset` and `runs` 


## test fpds



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
