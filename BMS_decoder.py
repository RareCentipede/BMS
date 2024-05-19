import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

  start_time = int(measurements[0][492:492+4], 16)

  res = []
  index = 0
  frame = 1

  start_time = bytes.fromhex(measurements[0][388:396])
  start_time_parsed = int.from_bytes(start_time, byteorder='little', signed=False)
  prev_time = 0

  results = pd.DataFrame(columns=['frame', 'time', 'cell number', 'voltage', 'resistance', 'current', 'power', 'temperature_1', 'temperature_2'])

  # Parse the data
  for m in measurements:
    voltages = bytes.fromhex(m[12:12+24])
    voltages_parsed = []
    for i in range(0, len(voltages), 2):
      v = int.from_bytes(voltages[i:i+2], byteorder='little', signed=False) * 0.001
      voltages_parsed.append(v)

    resistances = bytes.fromhex(m[160:160+24])
    resistances_parsed = []
    for i in range(0, len(resistances), 2):
      r = int.from_bytes(resistances[i:i+2], byteorder='little', signed=False) * 0.001
      resistances_parsed.append(r)
    res.append((voltages_parsed, resistances_parsed))

    bytes = bytes.fromhex(m[316:316+8])
    current_parsed = np.abs(int.from_bytes(bytes, byteorder='little', signed=True) * 0.001) 

    average_voltage = np.mean(voltages_parsed)
    power_parsed = np.sum(voltages_parsed) * current_parsed

    temperature_1 = bytes.fromhex(m[324:328])
    temp_1_parsed = int.from_bytes(temperature_1, byteorder='little', signed=False) * 0.1

    temperature_2 = bytes.fromhex(m[328:332])
    temp_2_parsed = int.from_bytes(temperature_2, byteorder='little', signed=False) * 0.1

    frame_counter = int(m[10:12], 16)

    time = bytes.fromhex(m[388:396])
    time_parsed = int.from_bytes(time, byteorder='little', signed=False)
    time_elapsed = time_parsed - start_time_parsed

    if time_parsed == prev_time:
      time_elapsed += 0.5

    prev_time = time_parsed

    for i in range(len(voltages_parsed)):
      results.loc[index] = [frame, time_elapsed, f'cell_{i+1}', voltages_parsed[i], resistances_parsed[i], current_parsed, power_parsed, temp_1_parsed, temp_2_parsed]
      index += 1

    results.loc[index] = [frame, time_elapsed, 'cell_average', average_voltage, np.mean(resistances_parsed), current_parsed, power_parsed, temp_1_parsed, temp_2_parsed]
    index += 1
    frame += 1

  data_name = raw_data.replace(data_path, "").replace(".txt", "").replace("results_", "")
  results.to_csv(f'./Results/processed/results_{data_name}.csv')