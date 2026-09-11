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

data_dir = 'Data'
files_list = os.listdir(data_dir)
csv_files = [file for file in files_list if file.endswith('.csv')]

if csv_files:
    file_to_read = os.path.join(data_dir, csv_files[0])
    print(f"reading data from {file_to_read}")
    data = pd.read_csv(file_to_read)
else:
    print("No CSV files found in the data directory.")
