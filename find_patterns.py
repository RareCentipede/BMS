from os import listdir
from os.path import isfile, join

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

for m in measurements:
  bytes_to_explore = bytes.fromhex(m[328:330])
  parsed_bytes = int.from_bytes(bytes_to_explore, byteorder='little', signed=False) * 0.1
  print(bytes_to_explore, parsed_bytes)