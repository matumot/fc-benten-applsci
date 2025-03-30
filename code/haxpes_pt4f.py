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
This script processes and visualizes Pt 4f core-level spectra for multiple standard samples 
(TEC10F50E, TEC10F50E-HT, TEC10E50E, TEC10EA50E). It generates a comparative plot 
to highlight the normalized intensity variations with respect to binding energy.

Overview:
- Reads experimental data from CSV files containing binding energy (in eV) and intensity 
  values (arbitrary units).
- Excludes metadata lines starting with '#' during preprocessing.
- Applies Shirley background correction for baseline adjustment.
- Normalizes intensity values to enable comparative analysis across samples.

Plot Features:
- Binding energy (x-axis) is plotted in reverse order to emphasize the 
  high binding energy region.
- Intensity values (y-axis) are normalized to a peak value
- Line colors (black, red, blue, green) distinguish between the four standard samples.
- Includes a labeled legend, gridlines, and a title ('Pt 4f') placed inside the plot area 
  for clarity.
- Outputs a high-resolution PNG file suitable for publication or presentation.

Key Parameters:
- Shirley background correction ensures accurate baseline alignment.
- Axis labels and tick intervals are customized for improved readability.
- The y-axis displays relative intensity, while x-axis ticks alternate between labeled 
  and unlabeled for visual simplicity.

Dependencies:
- pandas: For data manipulation.
- matplotlib: For plotting the spectra.
- numpy: For numerical operations.

Output:
- A PNG file ('./figures/haxpes_pt4f.png') showing the processed Pt 4f core-level 
  spectra.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import warnings

# Plot settings for MDPI style
rcParams.update(
    {
        "font.family": "serif",
        "mathtext.fontset": "stix",  # Use STIX fonts for math
        "font.size": 18,
        "axes.titlesize": 18,
        "axes.labelsize": 18,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "legend.fontsize": 12,
        "figure.figsize": (8, 6),
    }
)


# Function to apply Shirley background correction with iterative convergence
def shirley_background_correction(
    binding_energy, intensity, x_min, x_max, eps=1e-7, max_iters=50
):
    # Ensure binding_energy and intensity are numpy arrays
    binding_energy = np.array(binding_energy)
    intensity = np.array(intensity)

    # Identify the indices for x_min and x_max
    idx_min = np.argmin(np.abs(binding_energy - x_min))
    idx_max = np.argmin(np.abs(binding_energy - x_max))

    # Ensure idx_min < idx_max
    if idx_min > idx_max:
        idx_min, idx_max = idx_max, idx_min

    # Initialize Shirley background array
    bg = np.zeros_like(intensity)

    # Set boundary values
    i_left = intensity[idx_min]
    i_right = intensity[idx_max]

    # Iterative calculation of the Shirley background
    for iter_count in range(max_iters):
        cumulative_bg = np.cumsum(bg)
        cumulative_intensity = np.cumsum(intensity)

        new_bg = np.zeros_like(bg)
        k = (i_left - i_right) / (
            cumulative_intensity[idx_min] - cumulative_intensity[idx_max]
        )

        for i in range(len(binding_energy)):
            new_bg[i] = i_right + k * (
                cumulative_intensity[idx_min]
                - cumulative_intensity[i]
                - cumulative_bg[idx_min]
                + cumulative_bg[i]
            )

        # Check for convergence
        if np.max(np.abs(new_bg - bg)) < eps:
            break

        bg = new_bg

    if (iter_count + 1) == max_iters:
        warnings.warn(
            "Shirley background calculation did not converge after {} iterations!".format(
                max_iters
            )
        )

    # Correct the intensity by subtracting the background
    corrected_intensity = intensity - bg

    return corrected_intensity


# File path list
file_path_list = [
    "./data/haxpes_Pt4f_TEC10F50E_H_0001.csv",
    "./data/haxpes_Pt4f_TEC10F50E-HT_H_0001.csv",
    "./data/haxpes_Pt4f_TEC10E50E_H_0001.csv",
    "./data/haxpes_Pt4f_TEC10EA50E_H_0001.csv",
]

# Legends and colors
legends = [
    r"$\mathrm{TEC10F50E}$",
    r"$\mathrm{TEC10F50E{-}HT}$",
    r"$\mathrm{TEC10E50E}$",
    r"$\mathrm{TEC10EA50E}$",
]

colors = ["black", "red", "blue", "green"]

title = "Pt 4f"
title = r"$\mathrm{Pt \,\, 4f}$"

x_min, x_max = 78, 68  # Set the x-axis range
y_min, y_max = -0.1, 1.3  # Set the y-axis range

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

    # Apply Shirley background correction
    data["Corrected Intensity"] = shirley_background_correction(
        data["Binding energy"].to_numpy(), data["Intensity"].to_numpy(), x_min, x_max
    )

    # Normalize the intensity by the peak value
    data["Normalized Intensity"] = (
        data["Corrected Intensity"] / data["Corrected Intensity"].max()
    )

    # Plot the data with adjusted transparency and line width
    plt.plot(
        data["Binding energy"],
        data["Normalized Intensity"],
        label=legend,
        color=color,
        linewidth=1.5,
        alpha=0.7,
    )

# Adjust plot settings
plt.xlabel(r"$\mathrm{Binding \,\, energy} \,\, (\mathrm{eV})$")
plt.ylabel(r"$\mathrm{Intensity} \,\, (\mathrm{a.u.})$", labelpad=10)

plt.gca().invert_xaxis()
plt.gca().yaxis.set_ticks_position("left")
plt.gca().xaxis.set_ticks_position("both")
plt.tick_params(axis="both", which="major")
# yticks = plt.gca().get_yticks()  # Get current y-axis ticks
# plt.gca().set_yticks(yticks)  # Explicitly set the y-axis ticks
# plt.gca().set_yticklabels(['' for _ in plt.gca().get_yticks()])  # Replace y-axis labels with dots
# plt.gca().set_yticks(yticks)
plt.grid(axis="x", linestyle="--", alpha=0.7)

all_ticks = np.arange(x_min, x_max - 1, -1)
labels = [str(tick) if tick % 2 == 0 else "" for tick in all_ticks]
plt.gca().set_xticks(all_ticks)
plt.gca().set_xticklabels(labels)

plt.grid(axis="x", linestyle="--", alpha=0.7)

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.text(0.04, 0.94, title, ha="left", transform=plt.gca().transAxes)
plt.legend(loc="upper left", bbox_to_anchor=(0.01, 0.93))
plt.tight_layout()

# Specify the output file path
output_file_path = "./figures/haxpes_pt4f.png"
print(f"The plot will be saved to: {output_file_path}")

# Save the plot as a PNG file
plt.savefig(output_file_path, dpi=300)
plt.show()
