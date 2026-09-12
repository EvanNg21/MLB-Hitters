import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
pitch_type = tk.StringVar()
pitch_types = ["All"] + data['pitch_name'].dropna().unique().tolist()
pitch_type_dropdown = ttk.Combobox(
    frame, 
    textvariable=pitch_type,
    values = pitch_types
)
pitch_type_dropdown.current(0)
pitch_type_dropdown.grid(row=2, column=1, padx=10, pady=10)

#Pitch Call
ttk.Label(frame, text="Select Pitch Call:").grid(row=3, column=0, padx=10, pady=10)
pitch_call = tk.StringVar()
pitch_called = ["All"] + data['description'].dropna().unique().tolist()
pitch_call_dropdown = ttk.Combobox(
    frame,
    textvariable=pitch_call,
    values = pitch_called
)
pitch_call_dropdown.current(0)
pitch_call_dropdown.grid(row=3, column=1, padx=10, pady=10)

#Pitch Result
ttk.Label(frame, text="Select Pitch Result:").grid(row=4, column=0, padx=10, pady=10)
pitch_result = tk.StringVar()
pitch_results = ["All"] + data['events'].dropna().unique().tolist()
pitch_result_dropdown = ttk.Combobox(
    frame,
    textvariable=pitch_result,
    values = pitch_results
)
pitch_result_dropdown.current(0)
pitch_result_dropdown.grid(row=4, column=1, padx=10, pady=10)

plot_button = ttk.Button(frame, text="Plot")
plot_button.grid(row=5, column=0, columnspan=2)

root.mainloop()