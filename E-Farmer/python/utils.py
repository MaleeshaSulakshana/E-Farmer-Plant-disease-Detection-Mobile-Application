import json
import os
import random
from datetime import datetime


# Function for read config json
def read_config_json(json_path):

    config = []

    # Read json
    if os.path.exists(json_path):
        with open(json_path, "r") as read_file:
            config = json.load(read_file)

    return config


# Function for get current date
def date_picker():
    current_datetime = datetime.now()
    date = str(current_datetime.strftime("%Y-%m-%d"))
    return date


# Function for genarate random number
def random_number():
    rand_no = str(random.randint(100000, 999999))
    return rand_no


# Function for save deseases images
def file_save(image, save_folder):
    if image != None:
        image_name = image.filename
        image.save(save_folder + image_name)

    else:
        image_name = None

    return str(image_name)
