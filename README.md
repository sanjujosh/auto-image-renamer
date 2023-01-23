# Auto-image-renamer
Rename images using deep learning

![Image for demo](images/gif.gif)

Auto-image-renamer automates the task of renaming images with meaningful names. It uses Microsoft Computer Vision APIs deep learning algorithms to rename the images


## Update Jan 2023
Microsoft changed the old API, so I have updated the same in here. Also removed python2 support.

## Dependencies

- Python 3 (Tested under Windows Python 3.10.2) 

## Usage 

### 1) Get a Microsoft API Key for Free

[Sign Up](https://azure.microsoft.com/en-gb/products/cognitive-services/computer-vision/)

### 2) Create a computer vision

Replace API Key with `MICROSOFT_VISION_API_KEY` and end point with `MICROSOFT_VISION_API_ENDPOINT` in renamer.py

## Usage

```
python renamer.py path_to_images_dir
```

EXAMPLE `python3 renamer.py /home/sanju/images`

NOTICE: Do not use a trailing slash in dir

## 4) Enjoy!

All the images in the given directory will be renamed with meaningful names now. 


## How It was Built

1. Find all the images in the given directory
2. Images will be sent to Microsoft API, they process the image and sent back a caption.
3. Rename the files with new name from the VISION API


## Disclaimer

It uploads the images to Microsoft servers, do not use it with personal images. (or use it with caution) 

## Credits

Originally inspired from https://github.com/ParhamP/altify
