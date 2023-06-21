$ dynamic-cropper /input_directory 

args:
- 'DIRECTORY', type=str, help='input directory'
- '-e', '--image-ext', type=str, required=False, help='extension of dataset images - default: .png'
- '-s', '--size', type=int, required=False, help='cropped image size'
- '-r', '--recursive', required=False, action='store_true', help='treat input directory as a dataset, recursively processing all subdirectories'