from os import listdir
from os.path import isfile, join
import numpy as np

# Read serial data
data_path = 'data/to_process/'
data_to_process = [data_path + f for f in listdir(data_path) if isfile(join(data_path, f))]

for raw_data in data_to_process:
  with open(raw_data, 'r') as file:
      hex = file.read().replace(" ", "")

  new_line_pos = 0
  while new_line_pos != -1:
    new_line_pos = hex.find("\n", new_line_pos)
    time_stamp = hex[new_line_pos:new_line_pos+13]
    hex = hex.replace(time_stamp, "")

  hex.replace("\n", "")

  measurements = []

  # Separate the frames
  header_1 = hex.find("55AAEB90", 0)
  header_2 = hex.find("55AAEB90", header_1+8)

  while header_2 != -1:
    measurements.append(hex[header_1:header_2])
    header_1 = header_2
    header_2 = hex.find("55AAEB90", header_1+8)

prev_frame = np.zeros(600)
current_frame = np.zeros(600)
prev_diff = np.nan * np.ones(600)

start_time = bytes.fromhex(measurements[0][388:396])
start_time_parsed = int.from_bytes(start_time, byteorder='little', signed=False)

for m in measurements:
  print('-----------------------------------')
  diff = 0
  frame_counter = int(m[10:12], 16)

  time = bytes.fromhex(m[388:396])
  time_parsed = int.from_bytes(time, byteorder='little', signed=False)
  print(frame_counter, time_parsed - start_time_parsed)