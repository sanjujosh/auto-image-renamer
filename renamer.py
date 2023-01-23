#!/usr/bin/env python

import argparse
import http.client
import json
import os
import urllib.parse
from os import listdir
from os.path import isfile, join

# Change here
MICROSOFT_VISION_API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
MICROSOFT_VISION_API_ENDPOINT = 'eastus.api.cognitive.microsoft.com'

ALLOWED_IMAGE_EXTENSIONS = ['.jpeg', '.jpg', '.png']


def is_exists(path):
    if os.path.exists(path):
        return True
    else:
        print("Could not find the given file - ", path)
        return False


def get_all_images(directory):
    if is_exists(directory):
        files = [f for f in listdir(directory) if isfile(join(directory, f))]
        images = [f for f in files for ext in ALLOWED_IMAGE_EXTENSIONS if f.lower().endswith(ext.lower())]
        return images


def get_extension(file):
    file, ext = os.path.splitext(file)
    return ext


def rename_img(old, new, base_dir):
    if is_exists(old):
        ext = get_extension(old).lower()
        os.rename(old, join(base_dir, new + ext))
        print("Renaming ", old, "to ", new + ext)


def get_caption(image_file):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': MICROSOFT_VISION_API_KEY,
    }

    params = urllib.parse.urlencode({
        'maxCandidates': '1',
        'language': 'en',
        'model-version': 'latest',
    })
    data = open(image_file, 'rb')
    try:
        conn = http.client.HTTPSConnection(MICROSOFT_VISION_API_ENDPOINT)
        conn.request("POST", "/vision/v3.2/describe?%s" % params, data, headers)
        response = conn.getresponse()
        data = response.read()
        json_data = json.loads(data)
        caption_text = json_data['description']['captions'][0]['text']
        conn.close()
        return caption_text
    except Exception as e:
        print("Exception while communicating with vision api- ", str(e))


def full_path(base, file):
    return base + "/" + file


def init(directory):
    images = get_all_images(directory)
    for image in images:
        file = full_path(directory, image)
        print("Processing image - ", image)
        new_name = get_caption(file)
        rename_img(file, new_name, directory)


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help="Absolute path of image directory", type=str)
    args = parser.parse_args()

    try:
        init(args.dir)
    except ValueError:
        print("Try again")


if __name__ == '__main__':
    arg_parser()
