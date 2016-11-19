# Auto-image-renamer
Rename images using deep learning

![Image for demo](images/gif.gif)

Auto-image-renamer automates the task of renaming images with meaningful names. It uses Microsoft Computer Vision API's deep learning algorithms to rename the images


## Dependencies

- Python 3.5 (Tested under Ubuntu Python 3.5) 


## Usage 

### 1) Get a Microsoft API Key for Free
[https://www.microsoft.com/cognitive-services/en-us/sign-up](https://www.microsoft.com/cognitive-services/en-us/sign-up "API Key").


### 2) Usage

`python3 renamer.py path_to_images_dir`

NOTICE: Do not use a triling slash in dir

EXAMPLE `python3 renamer.py /home/sanju/images`

### 4) Enjoy!

All the images in the given directory will be renamed with meaningful names now. 


## How It was Built

1. Find all the images in the given directory
2. Stream images using uploads.im API, and then with its URL, send request to Microsoft's API to caption.
3. Rename the files with new name from the VISION API


## Disclaimer

It uses uploads.im api to stream the files, do not use it with personal images. 

## Credits

Originally inspired from https://github.com/ParhamP/altify
