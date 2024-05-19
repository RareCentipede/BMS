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

temp1 = 328
temp2 = 343

for m in measurements:
  # for i in range(0, len(m)-2):
  #   bytes_to_explore = bytes.fromhex(m[i:i+2])
  #   parsed_bytes = int.from_bytes(bytes_to_explore, byteorder='little', signed=False) * 0.1
  #   print(i, parsed_bytes)
  temp_1 = int.from_bytes(bytes.fromhex(m[temp1:temp1+2]), byteorder='little', signed=False) * 0.1
  temp_2 = int.from_bytes(bytes.fromhex(m[temp2:temp2+2]), byteorder='little', signed=False) * 0.1
  print(temp_1, temp_2)