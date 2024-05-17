import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read serial data
with open('data/serial_20240516_224436.txt', 'r') as file:
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

results = pd.DataFrame(columns=['frame', 'cell number', 'voltage', 'resistance', 'current', 'power'])

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
  current_parsed = int.from_bytes(bytes, byteorder='little', signed=True) * 0.001 

  average_voltage = np.mean(voltages_parsed)
  power_parsed = average_voltage * current_parsed

  frame_counter = int(m[10:12], 16)

  for i in range(len(voltages_parsed)):
    results.loc[index] = [frame, f'cell_{i+1}', voltages_parsed[i], resistances_parsed[i], current_parsed, power_parsed]
    index += 1

  results.loc[index] = [frame, 'cell_average', average_voltage, np.mean(resistances_parsed), current_parsed, power_parsed]
  index += 1
  frame += 1

print(results)

# plotting

# plot voltages
f, axes = plt.subplots(4, 1, sharex=True)
ax_volt = axes[0]
ax_res = axes[1]
ax_cur = axes[2]
ax_power = axes[3]

sns.lineplot(results, x='frame', y='voltage', hue='cell number', ax=ax_volt)
ax_volt.set_title('Voltages')
ax_volt.set_ylabel('Voltage (V)')

# plot resistances
sns.lineplot(results, x='frame', y='resistance', hue='cell number', ax=ax_res, legend=True)
ax_res.set_title('Resistances')
ax_res.set_ylabel('Resistance ($\Omega$)')

# plot current
sns.lineplot(results, x='frame', y='current', ax=ax_cur)
ax_cur.set_title('Current')
ax_cur.set_ylabel('Current (A)')

sns.lineplot(results, x='frame', y='power', ax=ax_power)
ax_power.set_title('Power')
ax_power.set_ylabel('Power (W)')

plt.show()