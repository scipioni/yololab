# yolorun

## autolabel of dataset

```
yolorun --model models/yolov8x.pt /tmp/openimages/*jpg --filter-classes 0,56,57,59,60 --save /archive/dataset/
```

## filter a dataset

any
```
yolorun --save /tmp/dataset-with-2-or-3 --filter-classes 2,3 /dataset-orig/*jpg

```


strict
```
yolorun --save /tmp/dataset-with-only-2-3 --filter-classes-strict 2,3 /dataset-orig/*jpg

```

## convert classes.txt

```
find ./train -name "*txt" | xargs -n1 sed -i 's/^0/80/; s/^1/81/; s/^2/57/; s/^3/59/'
```

## example

```
# autolabel di persone, letti, sofa, tavoli e sedie
yolorun --model models/yolov8x.pt /archive/dataset/fp/train/sofabed/*jpg  --filter-classes 0,56,57,59,60 --save /archive/dataset/fp/sofabed.autolabel
```