import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join

import sys

num_axes = 3

display_temp = False
display_res = False

args = sys.argv
if 'temp' in args:
    display_temp = True
    num_axes += 1

if 'res' in args:
    display_res = True
    num_axes += 1

data_path = 'Results/to_plot/'
data_to_plot = [data_path + f for f in listdir(data_path) if isfile(join(data_path, f))][0]

results = pd.read_csv(data_to_plot)

# plot voltages
f, axes = plt.subplots(num_axes, 1, sharex=True, figsize=(20, 10))
ax_volt = axes[0]
ax_cur = axes[1]
ax_power = axes[2]

if display_temp:
    ax_temp = axes[3]

if display_res:
    ax_res = axes[4]

sns.lineplot(results, x='frame', y='voltage', hue='cell number', ax=ax_volt)
ax_volt.set_title('Voltage')
ax_volt.set_ylabel('Voltage (V)')


# plot current
sns.lineplot(results, x='frame', y='current', ax=ax_cur)

current_lower_bound = float(results[results['current'] > 0]['current'].min()) - 0.5
current_upper_bound = float(results['current'].max()) + 0.5

if np.isnan(current_lower_bound):
    current_lower_bound = -0.5

ax_cur.set_ylim([current_lower_bound, current_upper_bound])
ax_cur.set_title('Current')
ax_cur.set_ylabel('Current (A)')

sns.lineplot(results, x='frame', y='power', ax=ax_power)
power_lower_bound = float(results[results['power'] > 0]['power'].min()) - 2
power_upper_bound = float(results['power'].max()) + 2

if np.isnan(power_lower_bound):
    power_lower_bound = -2

ax_power.set_ylim([power_lower_bound, power_upper_bound])
ax_power.set_title('Power')
ax_power.set_ylabel('Power (W)')

if display_temp:
    sns.lineplot(results, x='frame', y='temperature_1', ax=ax_temp, label="Pack 1")
    sns.lineplot(results, x='frame', y='temperature_2', ax=ax_temp, label="Pack 2")
    ax_temp.set_title('Temperature')
    ax_temp.set_ylabel('Temperature (°C)')

# plot resistances
if display_res:
    sns.lineplot(results, x='frame', y='resistance', hue='cell number', ax=ax_res, legend=True)
    ax_res.set_title('Resistances')
    ax_res.set_ylabel('Resistance ($\Omega$)') # type: ignore

plot_name = data_to_plot.replace(data_path, "").replace("results_", "").replace(".csv", "")

if 'save' in args:
    f.savefig(f'Results/plots/plot_{plot_name}.png', dpi=300)

plt.show()