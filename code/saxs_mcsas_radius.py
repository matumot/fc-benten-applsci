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
This script generates a plot of sphere radius distribution and cumulative distribution function (CDF) 
from SAXS data, including volume fraction histograms and associated errors for analysis.

Key Features:
- Reads radius distribution data from a specified text file with flexible column formatting.
- Visualizes data with a bar chart (volume fraction) and error bars for measured values.
- Overlays additional data, including the minimum visibility limit and cumulative distribution function (CDF).
- Dual Y-axis configuration for plotting volume fraction and CDF on the same graph.
- Saves the plot as './figures/saxs_mcsas_radius.png' with a resolution of 300 dpi.

Output:
- A PNG plot saved as './figures/saxs_mcsas_radius.png'.

Input:
- The script processes radius distribution data from a specified file path.

Dependencies:
- pandas
- matplotlib
"""
import pandas as pd  # Pandas for data loading and manipulation
import matplotlib.pyplot as plt  # Matplotlib for creating figures and plots
from matplotlib import rcParams  # rcParams for customizing plot styles

# Configure overall font and style settings for the plot
rcParams.update(
    {
        "font.family": "serif",  # Use a serif font family (e.g., Times New Roman)
        "mathtext.fontset": "stix",  # Use STIX fonts for math text (LaTeX-like appearance)
        "font.size": 10,  # Base font size for all text
        "axes.titlesize": 12,  # Font size for axis titles
        "axes.labelsize": 18,  # Font size for axis labels
        "xtick.labelsize": 14,  # Font size for X-axis tick labels
        "ytick.labelsize": 14,  # Font size for Y-axis tick labels
        "legend.fontsize": 16,  # Font size for the legend text
        "figure.figsize": (8, 6),  # Default figure dimensions (width, height in inches)
    }
)

# Specify the path to the input data file
file_path = "./data/saxs_TEC10V30E_As_FE_00001__sum_Connected 2023-02-09_13-41-55_hist-radius-True-0(nm)-10(nm)-50-lin-vol.dat"

# Load the data from a text file into a pandas DataFrame.
# - 'header=None' means there is no header row in the file.
# - 'skiprows=1' skips the first row.
# - 'sep=r'\s+'' tells pandas the file is space-separated.
data = pd.read_csv(file_path, header=None, skiprows=1, sep=r"\s+")

# Extract columns from the DataFrame into separate variables:
# x: radius in meters -> convert to nanometers by multiplying by 1e9
# y: volume fraction histogram
# y_err: error of the histogram
# obs: minimum visibility limit
# cdf: cumulative distribution function
# cdf_err: error of the CDF
x = data.iloc[:, 0] * 1e9
y = data.iloc[:, 2]
y_err = data.iloc[:, 3]
obs = data.iloc[:, 4]
cdf = data.iloc[:, 5]
cdf_err = data.iloc[:, 6]

# Create a figure and a set of axes for plotting. We use subplots to have
# better control over the figure and axes objects.
fig, ax1 = plt.subplots(figsize=(8, 6))

# Plot the histogram (left Y-axis)
bar_width = 0.2  # Width of each bar in the histogram
ax1.bar(
    x,
    y,
    width=bar_width,
    color="darkkhaki",
    alpha=0.6,
    label=r"$\mathrm{MC \,\, size \,\, histogram}$",
)
ax1.errorbar(
    x, y, yerr=y_err, fmt="o", color="darkkhaki", capsize=3
)  # Error bars for the histogram
ax1.plot(
    x, obs, "s-", color="red", label=r"$\mathrm{Minimum \,\, visibility \,\, limit}$"
)  # Plot 'obs' data as a red line with square markers

# Label the X-axis and the left Y-axis
ax1.set_xlabel(r"$\mathrm{radius} \,\, (\mathrm{nm})$")
ax1.set_ylabel(r"$[\mathrm{Rel.}] \,\, \mathrm{Volume \,\, Fraction}$")

# Configure ticks for the left Y-axis
ax1.tick_params(axis="y")

# Enable grid lines on the left axis
ax1.grid()

# Set the range for the X-axis (0 to 10 nm)
ax1.set_xlim(0, 10)

# Set the range for the left Y-axis (0 to 10)
ax1.set_ylim(0, 10)

# Configure tick parameters for both axes
ax1.tick_params(axis="x")
ax1.tick_params(axis="y")

# Create a second Y-axis (right side) that shares the same X-axis
ax2 = ax1.twinx()

# Plot the CDF (right Y-axis) with error bars
# fmt="^-" indicates triangle markers connected by lines
ax2.errorbar(
    x, cdf, yerr=cdf_err, fmt="^-", label=r"$\mathrm{CDF}$", color="green", capsize=3
)

# Label and style the right Y-axis
ax2.set_ylabel(
    r"$\mathrm{CDF \,\, (Cumulative \,\, Distribution \,\, Function)}$", color="green"
)
ax2.tick_params(axis="y", labelcolor="green")
ax2.set_ylim(0, 1.3)  # Y-axis range for the CDF

# Add a legend that combines both axes' plots.
# loc='upper right' places the legend in the upper-right corner,
# bbox_to_anchor=(0.8, 0.96) adjusts the exact position inside the figure.
fig.legend(loc="upper right", bbox_to_anchor=(0.8, 0.96))

# Adjust layout to prevent overlap of labels, titles, and legends
plt.tight_layout()

# Define the output file path and save the plot as a PNG with 300 dpi resolution
output_file_path = "./figures/saxs_mcsas_radius.png"
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path, dpi=300, bbox_inches="tight")

# Show the plot on the screen
plt.show()
