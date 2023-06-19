# Required arguments

```--sdir <path>``` The directory where the program reads txt files

```--ddir <path>``` The directory where the program saves modified files

```--iw <wrapper>``` Input Wrapper

```--ow <wrapper>``` Output Wrapper

# Available Wrappers

- voc
- fpds
- labelme
- yolo
- coco (**only one image per .json file**)

# API Usage
```
from api.DatasetConverterAPI import DatasetConverterAPI

api = DatasetConverterAPI()
api.convert(SOURCE_DIR, DESTINATION_DIR, INPUT_WRAPPER, OUTPUT_WRAPPER)
```
where:

**SOURCE_DIR** and **DESTINATION_DIR** are both dir paths

**INPUT_WRAPPER** and **OUTPUT_WRAPPER** are both strings