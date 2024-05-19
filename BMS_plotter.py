import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join

data_path = 'Results/to_plot/'
data_to_plot = [data_path + f for f in listdir(data_path) if isfile(join(data_path, f))][0]

results = pd.read_csv(data_to_plot)

# plot voltages
f, axes = plt.subplots(3, 1, sharex=True, figsize=(20, 10))
ax_volt = axes[0]
# ax_res = axes[1]
ax_cur = axes[1]
ax_power = axes[2]

sns.lineplot(results, x='frame', y='voltage', hue='cell number', ax=ax_volt)
ax_volt.set_title('Voltages')
ax_volt.set_ylabel('Voltage (V)')

# # plot resistances
# sns.lineplot(results, x='frame', y='resistance', hue='cell number', ax=ax_res, legend=True)
# ax_res.set_title('Resistances')
# ax_res.set_ylabel('Resistance ($\Omega$)')

# plot current
sns.lineplot(results, x='frame', y='current', ax=ax_cur)
ax_cur.set_ylim([results['current'][0], np.max(results['current'])])
ax_cur.set_title('Current')
ax_cur.set_ylabel('Current (A)')

sns.lineplot(results, x='frame', y='power', ax=ax_power)
ax_power.set_ylim([results['power'][0], np.max(results['power'])])
ax_power.set_title('Power')
ax_power.set_ylabel('Power (W)')

plot_name = data_to_plot.replace(data_path, "").replace("results_", "").replace(".csv", "")
f.savefig(f'Results/plots/plot_{plot_name}.png', dpi=300)
plt.show()