# To process data
- Put raw hex data into 'data/raw' folder
- Put data you want to process into 'data/to_process' (multiple files can be put here)
- Run the `BMS_decoder.py` script
  - This will process all the data in the folder and output the processed data into 'results/processed'

# To plot data
- Put the processed data you want to plot into `results/to_plot`
- It will plot when readfy and saves the figures into `results/plots`

# Command line arguments
## The arguments can be used in any order
- `temp` : Plots temperature data
- `res` : Plots resistance data
- `save` : Saves the plots