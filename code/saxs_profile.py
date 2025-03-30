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
This script generates a log-log scattering intensity profile plot for Pt catalysts based on experimental
and simulated data. The data includes experimental profiles for carbon-supported Pt catalysts and
simulated profiles for unsupported Pt catalysts with varying size dispersions.

Key Features:
- Reads scattering intensity data from text files, skipping header lines.
- Supports log-log scale for axes and customizable tick formatting.
- Plots experimental and simulated profiles with distinct colors and labels.
- Saves the plot as './figures/saxs_profile.png' with a resolution of 300 dpi.

Output:
- A publication-ready PNG plot saved as './figures/saxs_profile.png'.

Input:
- The script processes scattering intensity data specified in the 'files' dictionary.

Dependencies:
- numpy
- matplotlib
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib import rcParams

# Set font style for MDPI article format
rcParams.update(
    {
        "font.family": "serif",  # Use a serif font like Times New Roman
        "mathtext.fontset": "stix",  # Use STIX fonts for math text
        "font.size": 10,  # Adjust font size to MDPI recommendations
        "axes.titlesize": 18,  # Larger title size
        "axes.labelsize": 18,  # Axis label size
        "xtick.labelsize": 14,  # X-axis tick label size
        "ytick.labelsize": 14,  # Y-axis tick label size
        "legend.fontsize": 14,  # Legend font size
        "figure.figsize": (8, 6),  # Default figure size
    }
)


# Function to read data from file
def read_data(file_path):
    """
    Read Q and Intensity values from a file, skipping the first 4 lines.

    Parameters:
        file_path (str): Path to the data file.

    Returns:
        numpy.ndarray: Array of [Q, Intensity].
    """
    data = []
    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            if i < 4:  # Skip header lines
                continue
            if "NAN" in line or line.strip() == "":
                continue
            parts = line.split()
            if len(parts) >= 2:  # At least Q and Intensity are required
                q_value = float(parts[0])
                intensity = float(parts[1])
                data.append((q_value, intensity))
    return np.array(data)


# Customize X-axis tick labels
def format_log_ticks(value, _):
    if value == 0.1:
        return r"$10^{-1}$"
    elif value == 1.0:
        return r"$10^{0}$"
    elif value == 10.0:
        return r"$10^{1}$"
    elif 0.1 < value < 1.0:
        return f"{int(value * 10)}"
    elif 1.0 < value < 10.0:
        return f"{int(value)}"
    else:
        return ""


# Define file paths and plot colors
files = {
    "Particle 1.33±0.38": (
        "./data/saxs_Particle1.33.38_2024-11-21_17-25-43_profileV.txt",
        "red",
    ),
    "Particle 1.33±0.05": (
        "./data/saxs_Particle1.33.05_2024-11-21_17-24-29_profileV.txt",
        "blue",
    ),
    "TEC10V30E": ("./data/saxs_TEC10V30E_As_FE_00001__sum_Connected.txt", "green"),
}

# Print file paths being used
for label, (file_path, _) in files.items():
    print(f"Processing file for {label}: {file_path}")

# Initialize plot
fig, ax = plt.subplots()

# Plot each dataset
for label, (file_path, color) in files.items():
    data = read_data(file_path)
    if data.size > 0:
        q_values = data[:, 0]
        intensities = data[:, 1]
        ax.plot(q_values, intensities, label=label, color=color, linestyle="-")

# Set log-log scale for axes
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.1, 10)
ax.set_ylim(1e-1, 1e7)

xticks = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 2, 3, 4, 5, 6, 7, 8, 10]
ax.set_xticks(xticks)
ax.xaxis.set_major_formatter(FuncFormatter(format_log_ticks))

# Add axis labels
plt.xlabel(r"$Q \, \, (\mathrm{nm}^{-1})$")
plt.ylabel(r"$\mathrm{Intensity} \,\, (\mathrm{a.u.})$")

# Add right-side Y-axis (without labels)
ax_right = ax.twinx()
ax_right.set_yscale("log")
ax_right.set_ylim(1e-1, 1e7)
ax_right.tick_params(
    axis="y", which="both", direction="in", labelleft=False, labelright=False
)

# Add grid
ax.grid(True, which="both", linestyle="--", linewidth=0.5)

legend_labels = [
    r"$\mathrm{Simulated: \,\, Particle \, Radius} \,\, 1.33 \pm 0.05 \,\, \mathrm{nm}$",
    r"$\mathrm{Simulated: \,\, Particle \, Radius} \,\, 1.33 \pm 0.38 \,\, \mathrm{nm}$",
    r"$\mathrm{Experimental: \,\, TEC10V30E}$",
]

handles, _ = ax.get_legend_handles_labels()
ordered_handles = [handles[1], handles[0], handles[2]]  # Rearrange legend order
ax.legend(ordered_handles, legend_labels, loc="best")

# Save figure to PNG file
output_file_path = "./figures/saxs_profile.png"
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path, dpi=300, bbox_inches="tight")
plt.show()
