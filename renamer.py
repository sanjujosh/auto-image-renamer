#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import json
import urllib
import argparse
import requests
from os import listdir
from os.path import isfile, join

_ver = sys.version_info
# Python 2.6+
is_py2 = (_ver[0] == 2)
# Python 3.x
is_py3 = (_ver[0] == 3)

if is_py2:
    from urllib import urlencode
    import httplib

if is_py3:
    from urllib.parse import urlencode
    import http.client as httplib


MICROSOFT_VISION_API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ALLOWED_IMAGE_EXTENSIONS = ['.jpeg', '.jpg', '.png']


def is_exists(path):
    if os.path.exists(path):
        return True
    else:
        print("Could not find the given file - ", path)
        return False


def get_all_images(dir):
    if is_exists(dir):
        files = [f for f in listdir(dir) if isfile(join(dir, f))]
        images = [f for f in files for ext in ALLOWED_IMAGE_EXTENSIONS if f.lower().endswith(ext.lower())]
        return images


def get_extension(file):
    file, ext = os.path.splitext(file)
    return ext


def rename_img(old, new, base_dir):
    if is_exists(old):
        ext = get_extension(old).lower()
        os.rename(old, join(base_dir,new + ext))
        print("Renaming ", old, "to ",  new + ext)


def get_caption(image_file):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': MICROSOFT_VISION_API_KEY,
    }
    params = urlencode({
        'maxCandidates': '1',
    })
    data = open(image_file, 'rb')
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/vision/v1.0/describe?%s" % params, data, headers)
        response = conn.getresponse()
        response_data = response.read().decode('utf-8')
        json_data = json.loads(response_data)
        caption_text = json_data['description']['captions'][0]['text']
        conn.close()
        return caption_text
    except Exception as e:
        print("Exception while communicating with vision api- ", str(e))


def full_path(base, file):
    return base + "/" + file


def init(dir):
    images = get_all_images(dir)
    for image in images:
        file = full_path(dir, image)
        print("Processing image - ", image)
        new_name = get_caption(file)
        rename_img(file, new_name, dir)


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

