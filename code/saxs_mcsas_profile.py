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
This script generates a log-log scattering intensity profile plot for SAXS data, comparing measured and 
fitted profiles. The data includes experimental results with associated errors and fitted profiles 
for detailed analysis.

Key Features:
- Reads scattering intensity data from a specified text file with flexible column formatting.
- Supports log-log scaling for axes and customizable tick formatting for better readability.
- Automatically adjusts X-axis tick labels to the data range and formats them for log scales.
- Saves the plot as './figures/saxs_mcsas_profile.png' with a resolution of 300 dpi.

Output:
- A PNG plot saved as './figures/saxs_mcsas_profile.png'.

Input:
- The script processes scattering intensity data from a specified file path.

Dependencies:
- pandas
- numpy
- matplotlib
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib import rcParams

# Configure font and style settings for the plot
rcParams.update(
    {
        "font.family": "serif",  # Use a serif font family (e.g., Times New Roman)
        "mathtext.fontset": "stix",  # Use STIX fonts for math text
        "font.size": 16,  # Base font size for the plot
        "axes.titlesize": 20,  # Font size for axis titles
        "axes.labelsize": 20,  # Font size for axis labels
        "xtick.labelsize": 16,  # Font size for X-axis tick labels
        "ytick.labelsize": 16,  # Font size for Y-axis tick labels
        "legend.fontsize": 20,  # Font size for the legend
        "figure.figsize": (8, 6),  # Default figure size (width, height)
    }
)


def format_log_ticks(value, _):
    """
    Format log-scale tick labels for better readability.
    Special formatting for 0.1, 1, and 10, and simple rounding for others.
    """
    if value == 0.1:
        return r"$10^{-1}$"
    elif value == 1.0:
        return r"$10^{0}$"
    elif value == 10.0:
        return r"$10^{1}$"
    elif 0.1 < value < 1.0:
        # Scale and display ticks between 0.1 and 1.0
        return f"{int(value * 10)}"
    elif 1.0 < value < 10.0:
        # Display integer tick values between 1 and 10
        return f"{int(value)}"
    else:
        # Hide other values
        return ""


# Load the data file into a pandas DataFrame
file_path = (
    "./data/saxs_TEC10V30E_As_FE_00001__sum_Connected 2023-02-09_13-41-55_fit.dat"
)
data = pd.read_csv(file_path, sep=r"\s+", header=None)

# Extract and convert data columns to appropriate types
x = data.iloc[1:, 0].astype(float)
y1 = data.iloc[1:, 1].astype(float)
y1_error = data.iloc[1:, 2].astype(float)
y2 = data.iloc[1:, 3].astype(float)
y2_error = data.iloc[1:, 4].astype(float)

# Scale the X values for better readability (divide by 1e9)
x_scaled = x / 1e9

# Create a figure with a specific size
plt.figure(figsize=(8, 6))

# Plot measured values with error bars
plt.errorbar(
    x_scaled,
    y1,
    yerr=y1_error,
    fmt="s",  # Use square markers
    color="black",
    label=r"$\mathrm{Measured}$",
    markersize=6,  # Slightly larger marker size
    linewidth=0.7,  # Thinner error bar lines
    alpha=0.7,  # Transparency for better visibility
    capsize=3,  # Size of the caps on error bars
)

# Plot fitted values with error bars
plt.errorbar(
    x_scaled,
    y2,
    yerr=y2_error,
    fmt="o",  # Use circle markers
    color="red",
    label=r"$\mathrm{Fitted}$",
    markersize=5,  # Marker size
    linewidth=0.7,  # Thinner error bar lines
    alpha=0.7,  # Transparency
    capsize=3,
)

# Set logarithmic scale for both X and Y axes
plt.xscale("log")
plt.yscale("log")

# Set axis labels
plt.xlabel(r"$Q \, \, (\mathrm{nm}^{-1})$")
plt.ylabel(r"$I \, \, ((\mathrm{m \,\, sr})^{-1})$")

# Define the X-axis tick values based on the data range
x_min = x_scaled.min()
x_max = x_scaled.max()

# Possible tick values for a log-scale axis
xticks = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 2, 3, 4, 5, 6, 7, 8, 10]
# Keep only those within the actual data range
xticks = [tick for tick in xticks if x_min <= tick <= x_max]

# Apply custom ticks and formatter
plt.gca().set_xticks(xticks)
plt.gca().xaxis.set_major_formatter(FuncFormatter(format_log_ticks))

# Add a legend
plt.legend()

# Get the current axis
ax = plt.gca()

# Add the text in the lower-left corner of the plot (axes coordinates)
ax.text(
    0.05,  # x-position in axes fraction
    0.05,  # y-position in axes fraction
    r"$0.3 \leq Q \,\, (\mathrm{nm}^{-1}) \leq 4$",  # The text to display
    transform=ax.transAxes,  # Coordinates are given in axis fractions
    verticalalignment="bottom",  # Align text from the bottom
    horizontalalignment="left",  # Align text to the left
)

# Optionally adjust tick parameters if needed
ax.tick_params(axis="x")
ax.tick_params(axis="y")

# Add grid lines for better readability (both major and minor ticks)
plt.grid(which="both", linestyle="--", linewidth=0.5)

# Set the x-axis range
plt.xlim(0.3, 4)

# Adjust layout so labels, titles, and legends do not overlap
plt.tight_layout()

# Define the output file path and save the figure
output_file_path = "./figures/saxs_mcsas_profile.png"
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path, dpi=300, bbox_inches="tight")

# Display the plot on screen
plt.show()
