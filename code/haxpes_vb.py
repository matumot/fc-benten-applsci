# Copyright 2025 Takahiro Matsumoto, Japan Synchrotron Radiation Research Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This script generates a comparative plot of the valence band profiles for multiple standard 
samples (TEC10F50E, TEC10F50E-HT, TEC10E50E, TEC10EA50E). Each profile is represented 
by normalized intensity as a function of binding energy (in eV), enabling the visualization 
of valence band structure differences across samples.

Key Features:
- Reads binding energy and intensity data from CSV files, excluding metadata lines starting 
  with '#' for preprocessing.
- Normalizes intensity values for each dataset to facilitate direct comparisons.
- Generates a publication-quality plot with inverted x-axis, labeled axes, customized tick 
  intervals, and a legend for sample identification.
- Adjusts font sizes, axis ranges, and gridline settings to enhance clarity and aesthetic 
  appeal.
- Saves the resulting plot as a PNG file with high resolution (300 dpi), suitable for 
  publications or presentations.

Plot Specifications:
- Line colors: black, red, blue, green (for each sample, respectively).
- Title: 'Valence band' (positioned inside the plot area).

Output:
- A PNG file saved to './figures/haxpes_vb.png', containing the valence band profile plot.

Input:
- CSV files specified in 'file_path_list', containing binding energy (eV) and intensity 
  (arbitrary units) data for the respective samples.

Dependencies:
- pandas
- matplotlib
- numpy
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# Set font style for MDPI article format
rcParams.update(
    {
        "font.family": "serif",  # Use a serif font like Times New Roman
        "mathtext.fontset": "stix",  # Use STIX fonts for math
        "font.size": 18,  # Adjust font size to MDPI recommendations
        "axes.titlesize": 18,  # Larger title size
        "axes.labelsize": 18,  # Axis label size
        "xtick.labelsize": 14,  # X-axis tick label size
        "ytick.labelsize": 14,  # Y-axis tick label size
        "legend.fontsize": 12,  # Legend font size
        "figure.figsize": (8, 6),  # Default figure size
    }
)

# File path list
file_path_list = [
    "./data/haxpes_VB_TEC10F50E_H_0001.csv",
    "./data/haxpes_VB_TEC10F50E-HT_H_0001.csv",
    "./data/haxpes_VB_TEC10E50E_H_0001.csv",
    "./data/haxpes_VB_TEC10EA50E_H_0001.csv",
]

# Legends and colors
legends = [
    r"$\mathrm{TEC10F50E}$",
    r"$\mathrm{TEC10F50E{-}HT}$",
    r"$\mathrm{TEC10E50E}$",
    r"$\mathrm{TEC10EA50E}$",
]

colors = ["black", "red", "blue", "green"]

title = r"$\mathrm{Valence \,\, band}$"

x_min, x_max = 14, -1  # Set the x-axis range
y_min, y_max = -0.1, 1.2  # Set the y-axis range

plt.figure(figsize=(8, 6))  # Increase figure size for better readability

# Loop through each file and plot
for file_path, legend, color in zip(file_path_list, legends, colors):
    print(f"Reading data from: {file_path}")
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Filter out metadata lines (starting with '#')
    data_lines = [line for line in lines if not line.startswith("#") and line.strip()]

    # Convert data lines to a DataFrame
    data = pd.DataFrame(
        [list(map(float, line.split(","))) for line in data_lines],
        columns=["Binding energy", "Intensity"],
    )

    # Normalize the intensity by the peak value
    data["Intensity"] /= data["Intensity"].max()

    # Plot the data with adjusted transparency and line width
    plt.plot(
        data["Binding energy"],
        data["Intensity"],
        label=legend,
        color=color,
        linewidth=1.5,
        alpha=0.7,
    )  # Add transparency here

# Adjust plot settings
plt.xlabel(r"$\mathrm{Binding \,\, energy} \,\, (\mathrm{eV})$")
plt.ylabel(r"$\mathrm{Intensity} \,\, (\mathrm{a.u.})$", labelpad=10)

plt.gca().invert_xaxis()  # Reverse the x-axis direction for display only
plt.gca().yaxis.set_ticks_position("left")  # Show ticks on y-axis
plt.gca().xaxis.set_ticks_position(
    "both"
)  # Add ticks to both top and bottom of the x-axis
plt.tick_params(axis="both", which="major")  # Increase tick label size
# yticks = plt.gca().get_yticks()  # Get current y-axis ticks
# plt.gca().set_yticks(yticks)  # Explicitly set the y-axis ticks
# plt.gca().set_yticklabels(['' for _ in plt.gca().get_yticks()])  # Replace y-axis labels with dots
plt.grid(axis="x", linestyle="--", alpha=0.7)

# Adjust x-axis tick interval
all_ticks = np.arange(x_min, x_max - 1, -1)  # Generate ticks every 1 unit
labels = [
    str(tick) if tick % 2 == 0 else "" for tick in all_ticks
]  # Show label for every 2nd tick
plt.gca().set_xticks(all_ticks)  # Apply the new tick positions
plt.gca().set_xticklabels(labels)  # Apply the new tick labels

plt.xlim(x_min, x_max)  # Set the x-axis range
plt.ylim(y_min, y_max)  # Set the y-axis range

# Place 'Valence band' inside the plot area above the legend
plt.text(0.04, 0.94, title, ha="left", transform=plt.gca().transAxes)

# Adjust legend to be in the top-left, slightly below the 'Valence band' label
plt.legend(loc="upper left", bbox_to_anchor=(0.01, 0.93))
plt.tight_layout()


# Specify the output file path
output_file_path = "./figures/haxpes_vb.png"
print(f"The plot will be saved to: {output_file_path}")

# Save the plot as a PNG file
plt.savefig(output_file_path, dpi=300)

plt.show()
