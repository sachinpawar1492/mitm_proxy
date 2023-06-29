import os
import json
import time
from flask import jsonify
from mitmproxy import http

PATH = os.path.dirname(__file__)


# Print in Red Colour Font
def print_in_red(statement):
    print("\033[91m {}\033[00m".format(statement))


# Print in Yellow Colour Font
def print_in_yellow(statement):
    print("\033[93m {}\033[00m".format(statement))


# Print in Green Colour Font
def print_in_green(statement):
    print("\033[92m {}\033[00m".format(statement))


# Creating global variable and assigning value to it
def create_var(var_name, var_value):
    globals()[var_name] = var_value


# Getting the full path based on the relative path
def get_path(rel_path):
    full_path = os.path.join(PATH, rel_path)
    return full_path


# Getting the content from a file by providing the complete file path
def read_data(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return jsonify(data)


# Getting the content from a file by providing the relative file path
def get_data(rel_path):
    full_path = os.path.join(PATH, rel_path)
    with open(full_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data


# Writing the data to the file by providing the file path and the expected data
def write_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=False)


# Getting the current time in milliseconds
def get_current_time():
    current_time = time.time()
    current_time_in_ms = int(current_time * 1000)

    return current_time_in_ms


# Creating the fake json response by providing the status code and response body
def make_response(status_code, response_body):
    fake_response = http.Response.make(
        status_code,
        content=json.dumps(response_body),
        headers={'Content-Type': 'application/json'}
    )

    return fake_response
