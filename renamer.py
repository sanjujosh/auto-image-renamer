#!/usr/bin/env python

import os
import json
import urllib
import argparse
import requests
from os import listdir
from os.path import isfile, join
import http.client as httplib

MICROSOFT_VISION_API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
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


def get_caption(image_src):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': MICROSOFT_VISION_API_KEY,
    }
    params = urllib.parse.urlencode({
        'maxCandidates': '1',
    })
    data = json.dumps({"Url": image_src}, separators=(',', ':'))
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
        print("Exception while communicating with vision api- ", e)


def upload(image_address):
    if is_exists(image_address):
        url = "http://uploads.im/api"
        files = {'media': open(image_address, 'rb')}
        request = requests.post(url, files=files)
        data = json.loads(request.text)
        image_url = data[u'data'][u'img_url']
        main_url = image_url.encode('ascii', 'ignore')
        return main_url.decode('utf-8')


def full_path(base, file):
    return base + "/" + file


def init(dir):
    images = get_all_images(dir)
    for image in images:
        file = full_path(dir, image)
        print("Processing image - ", image)
        image_url = upload(file)
        new_name = get_caption(image_url)
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
