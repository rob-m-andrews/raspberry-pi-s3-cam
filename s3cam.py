#!/usr/bin/env python3
from datetime import datetime
from time import sleep
import picamera
import os
import tinys3
import yaml

# testing
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# photo props
image_width = cfg['image_settings']['horizontal_res']
image_height = cfg['image_settings']['vertical_res']
file_extension = cfg['image_settings']['file_extension']
file_name = cfg['image_settings']['file_name']
photo_interval = cfg['image_settings']['photo_interval'] # Interval between photo (in seconds)
image_folder = cfg['image_settings']['folder_name']

# camera setup
camera = picamera.PiCamera()
camera.resolution = (image_width, image_height)
camera.rotation = cfg['image_settings']['rotation']
camera.zoom = (cfg['image_settings']['zoom'][0],cfg['image_settings']['zoom'][1],cfg['image_settings']['zoom'][2],cfg['image_settings']['zoom'][3])
camera.awb_mode = cfg['image_settings']['awb_mode']

# verify image folder exists and create if it does not
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# camera warm-up time
sleep(2)

# endlessly capture images awwyiss
while True:
    # Build filename string
    filepath = image_folder + '/' + file_name + file_extension

    if cfg['debug'] == True:
        print('[debug] Taking photo and saving to path ' + filepath)

    # Take Photo
    camera.capture(filepath)
    
    if cfg['debug'] == True:
        print('[debug] Uploading ' + filepath + ' to s3')

    # Upload to S3
    conn = tinys3.Connection(cfg['s3']['access_key_id'], cfg['s3']['secret_access_key'],tls=True,endpoint='s3-' + cfg['s3']['region'] + '.amazonaws.com')
    f = open(filepath, 'rb')
    conn.upload(filepath, f, cfg['s3']['bucket_name'],
               headers={
               'x-amz-meta-cache-control': 'max-age=' + str(photo_interval)
               })

    # Cleanup
    if os.path.exists(filepath):
        os.remove(filepath)

    # sleep
    sleep(photo_interval)

