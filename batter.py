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
    root = tk.Tk()
    root.title("Select CSV File")
    root.geometry("400x200")
    ttk.Label(root, text="Select a CSV file:").grid(row=0, column=0, padx=10, pady=10)
    dataset_var = tk.StringVar()
    dataset_dropdown = ttk.Combobox(
        root,
        textvariable=dataset_var,
        values = csv_files,
        state = "readonly"
    )
    dataset_dropdown.current(0)
    dataset_dropdown.grid(row=0, column=1, padx=10, pady=10)

    def load_dataset():
        global data
        file_to_read = os.path.join(data_dir, dataset_var.get())
        print(f"Reading From {file_to_read}")
        data = pd.read_csv(file_to_read)
        root.destroy()

    dataset_button =ttk.Button(root, text="Load Dataset", command=load_dataset)
    dataset_button.grid(row=1, column=0, columnspan=2)
    root.mainloop()
else:
    print("No CSV files found in the data directory.")

idDir = 'mlbid'
idFile = 'razzball.csv'
idPath = os.path.join(idDir, idFile)
mlbids = pd.read_csv(idPath)


#plot functions________________________________________________________________________________________________________________________________________

#plot button function
def on_plot():
    date = date_var.get()
    pitch_type = pitch_type_var.get()
    pitch_call = pitch_call_var.get()
    pitch_result = pitch_result_var.get()
    pitcher_hand = pitcher_hand_var.get()
    plot_data(data, date, pitch_type, pitch_call, pitch_result, pitcher_hand)

#plot function
def plot_data(data, date, pitch_type, pitch_call, pitch_result, pitcher_hand):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    topZone = data["sz_top"].iloc[0]
    bottomZone = data["sz_bot"].iloc[0]
    zoneHeight = topZone - bottomZone
    filtered_data =  data[((data['game_date'] == date) | (date == "All")) & 
        ((data['pitch_name'] == pitch_type) | (pitch_type == "All")) &
        ((data['p_throws'] == pitcher_hand) | (pitcher_hand == "Both")) & 
        (
            (data['description'] == pitch_call) | 
            (pitch_call == "All") | 
            ((data['description'].isin(['swinging_strike', 'called_strike']) & (pitch_call == "strike")))) & 
        (
            (data['events'] == pitch_result) | 
            (pitch_result == "All") |
            ((data['events'].isna()) & (pitch_result == "N/A")) |
            ((data['events'].isin(['single', 'double', 'triple', 'home_run'])) & (pitch_result == "hit"))
        )
    ]

    total_pitches = len(filtered_data)
        
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
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=(f"{pitch} : {len(filtered_data[filtered_data['pitch_name'] == pitch])}")) for pitch, color in pitch_colors.items()] + [plt.Line2D([0], [0], marker='o',markerfacecolor='black', color='w', markersize=10, label="Other")]
    legend_handles2 = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black',markersize=10, label=f"# of PItches: {total_pitches}"),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black',markersize=10, label=f"Date: {date}"),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black',markersize=10, label=f"Pitch-Type: {pitch_type}"),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black',markersize=10, label=f"Pitch-Call: {pitch_call}"),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black',markersize=10, label=f"Pitch-Result: {pitch_result}"),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black',markersize=10, label=f"Pitcher-Handedness: {pitcher_hand}")
    ]
    ax.scatter(filtered_data['plate_x'], filtered_data['plate_z'], marker='o', s=207, linewidth=0.5, edgecolor='black', c=colors, zorder=5, picker=True)
    legend1 = ax.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1, 0.5))
    legend2 = ax.legend(handles=legend_handles2, loc='center right', bbox_to_anchor=(-0.1, 0.5))
    ax.add_artist(legend1)
    ax.add_artist(legend2)
    ax.grid(True, zorder=1)
    ax.set_aspect('equal')
    manager = plt.get_current_fig_manager()
    manager.window.state("zoomed")
    
    def on_key(event):
        if event.key == 'escape':
            for annotation in ax.texts:
                annotation.remove()
            plt.draw()
    def on_pick(event):
        for annotation in ax.texts:
            annotation.remove()
        ind = event.ind[0]
        row = filtered_data.iloc[ind]
        pitcher_names = dict(zip(mlbids['MLBAMID'], mlbids['Name']))
        pitcher_id = filtered_data['pitcher'].iloc[ind]
        pitcher_name = pitcher_names.get(pitcher_id, "Unknown")
        annotation = ax.annotate(
            f"Date: {row['game_date']}\n"
            f"Pitcher: {pitcher_name}\n"
            f"Pitch_Hand: {row['p_throws']}\n"
            f"Pitch: {row['pitch_name']}\n"
            f"Speed: {row['release_speed']}\n"
            f"Pitch_Call: {row['description']}\n"
            f"Pitch_Result: {row['events']}\n",
            xy=(row['plate_x'], row['plate_z']),
            xytext=(20, 20),
            textcoords='offset points',
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"),
            zorder=13
        )
        plt.draw()
    fig.canvas.mpl_connect('pick_event', on_pick)
    fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()

    
#Selection Window______________________________________________________________________________________________________________________________________
player = data['player_name'].iloc[0]
root = tk.Tk()
root.title(f"Pitch Map for {player}")
root.geometry("400x300")

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
pitch_called = ["All"] + ["strike"] + data['description'].dropna().unique().tolist()
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
pitch_results = ["All"] + ["N/A"] + ["hit"] + data['events'].dropna().unique().tolist()
pitch_result_dropdown = ttk.Combobox(
    frame,
    textvariable=pitch_result_var,
    values = pitch_results
)
pitch_result_dropdown.current(0)
pitch_result_dropdown.grid(row=4, column=1, padx=10, pady=10)

#Pitcher Handedness
ttk.Label(frame, text="Pitcher Handedness: ").grid(row=5, column=0, padx=10, pady=10)
pitcher_hand_var = tk.StringVar()
pitcher_hand = ["Both"] + data['p_throws'].dropna().unique().tolist()
pitcher_hand_dropdown = ttk.Combobox(
    frame,
    textvariable=pitcher_hand_var,
    values = pitcher_hand
)
pitcher_hand_dropdown.current(0)
pitcher_hand_dropdown.grid(row=5, column=1, padx=10, pady=10)


plot_button = ttk.Button(frame, text="Plot", command=on_plot)
plot_button.grid(row=6, column=0, columnspan=2)


root.mainloop()
