import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from ipywidgets import Dropdown, interact, DatePicker, widgets, interactive_output
from PIL import Image
from scipy.ndimage import gaussian_filter
import tkinter as tk
from tkinter import ttk
import mplcursors
import os
from IPython.display import display

#Load Data in Folder__________________________________________________________________________________________________________________________________
data_dir = 'Data'
files_list = os.listdir(data_dir)
csv_files = [file for file in files_list if file.endswith('.csv')]

if csv_files:
    file_to_read = os.path.join(data_dir, csv_files[0])
    print(f"reading data from {file_to_read}")
    data = pd.read_csv(file_to_read)
else:
    print("No CSV files found in the data directory.")


#plot functions________________________________________________________________________________________________________________________________________
def on_plot():
    date = date_var.get()
    pitch_type = pitch_type_var.get()
    pitch_call = pitch_call_var.get()
    pitch_result = pitch_result_var.get()
    plot_data(data, date, pitch_type, pitch_call, pitch_result)

def plot_data(data, date, pitch_type, pitch_call, pitch_result):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    topZone = data["sz_top"].iloc[0]
    bottomZone = data["sz_bot"].iloc[0]
    zoneHeight = topZone - bottomZone
    filtered_data =  data[(data['game_date'] == date) & (data['pitch_name'] == pitch_type) & (data['description'] == pitch_call) & (data['events'] == pitch_result)]
    strikeZone = matplotlib.patches.Rectangle((-0.708, bottomZone), 1.416, zoneHeight, color='red', zorder=10, alpha=0.4)
    pitch_colors = {'4-Seam Fastball': '#d22d49', 'Sinker': '#fe9e00', 'Cutter': '#943f2c', 'Changeup': '#1dbe3a',
                    'Split-Finger': '#3badad', 'Forkball': '#55ccac', 'Screwball': '#60db33', 'Curveball': '#00d1ee',
                    'Knuckle-Curve': '#6236cd', 'Slow-Curve': '#0068ff', 'Slider': '#eee817', 'Sweeper': '#deb33a',
                    'Slurve': '#94afd5', 'Knuckleball': '#3c44cd'}
    colors = filtered_data['pitch_name'].map(pitch_colors).fillna('#000000')
    ax.add_patch(strikeZone)
    ax.vlines(0.236, bottomZone, bottomZone+zoneHeight, color='red', zorder=11, alpha=0.5)
    ax.vlines(-0.236, bottomZone, bottomZone+zoneHeight, color='red', zorder=11, alpha=0.5)
    ax.hlines(bottomZone+zoneHeight/3, -0.708, 0.708, color='red', zorder=11, alpha=0.5)
    ax.hlines(bottomZone+2*zoneHeight/3, -0.708, 0.708, color='red', zorder=11, alpha=0.5)

    plt.xlim([-3.5,3.5])
    plt.ylim([-0.5,5])
    plt.xticks(np.arange(-3.5, 3.51, 0.5))
    plt.yticks(np.arange(-0.5, 5.1, 0.5))
    plt.title(f"Pitch Map for {data['player_name'].iloc[0]}")
    plt.xlabel("Horizontal Distance (feet)")
    plt.ylabel("Vertical Distance (feet)")
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=pitch) for pitch, color in pitch_colors.items()]
    ax.scatter(filtered_data['plate_x'], filtered_data['plate_z'], marker='o', s=207, linewidth=0.5, edgecolor='black', c= colors)
    ax.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(True, zorder=1)
    ax.set_aspect('equal')
    manager = plt.get_current_fig_manager()
    manager.window.state("zoomed")
    plt.show()

#Selection Window______________________________________________________________________________________________________________________________________
player = data['player_name'].iloc[0]
root = tk.Tk()
root.title(f"Pitch Map for {player}")
root.geometry("400x200")

frame = ttk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor="center")

#Dropdowns

#Date
ttk.Label(frame, text="Select Date:").grid(row=0, column=0, padx=10, pady=10)
date_var = tk.StringVar()
dates = ["All"] + data['game_date'].dropna().unique().tolist()
date_dropdown = ttk.Combobox(
    frame,
    textvariable=date_var,
    values = dates,
)
date_dropdown.current(0)
date_dropdown.grid(row=0, column=1, padx=10, pady=10)

#Pitch Type
ttk.Label(frame, text="Select Pitch Type:").grid(row=2, column=0, padx=10, pady=10)
pitch_type_var = tk.StringVar()
pitch_types = ["All"] + data['pitch_name'].dropna().unique().tolist()
pitch_type_dropdown = ttk.Combobox(
    frame, 
    textvariable=pitch_type_var,
    values = pitch_types
)
pitch_type_dropdown.current(0)
pitch_type_dropdown.grid(row=2, column=1, padx=10, pady=10)

#Pitch Call
ttk.Label(frame, text="Select Pitch Call:").grid(row=3, column=0, padx=10, pady=10)
pitch_call_var = tk.StringVar()
pitch_called = ["All"] + data['description'].dropna().unique().tolist()
pitch_call_dropdown = ttk.Combobox(
    frame,
    textvariable=pitch_call_var,
    values = pitch_called
)
pitch_call_dropdown.current(0)
pitch_call_dropdown.grid(row=3, column=1, padx=10, pady=10)

#Pitch Result
ttk.Label(frame, text="Select Pitch Result:").grid(row=4, column=0, padx=10, pady=10)
pitch_result_var = tk.StringVar()
pitch_results = ["All"] + data['events'].dropna().unique().tolist()
pitch_result_dropdown = ttk.Combobox(
    frame,
    textvariable=pitch_result_var,
    values = pitch_results
)
pitch_result_dropdown.current(0)
pitch_result_dropdown.grid(row=4, column=1, padx=10, pady=10)

plot_button = ttk.Button(frame, text="Plot", command=on_plot)
plot_button.grid(row=5, column=0, columnspan=2)


root.mainloop()
