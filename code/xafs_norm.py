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
This script processes XAFS data to generate a publication-ready plot of normalized μ(E) for the standard sample TEC10E50E.
The plot focuses on a specific energy range (in eV), showcasing normalized absorption values with clarity.

Key Features:
- Reads energy and normalized μ(E) data from a text file, skipping comment lines.
- Generates a high-quality plot with labeled axes, grid lines, and a legend.
- Customizes axis ranges and tick labels for better data visualization.
- Saves the plot as a PNG file in 300 dpi resolution.

Input:
- A data file specified by the 'file_path' variable, containing energy and normalized μ(E) values.

Output:
- A PNG file './figures/xafs_norm.png' that visually represents the normalized μ(E) data.

Dependencies:
- matplotlib
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from matplotlib import rcParams

# Update matplotlib settings to match the MDPI article format
rcParams.update(
    {
        "font.family": "serif",  # Use serif font style (e.g., Times New Roman)
        "mathtext.fontset": "stix",  # Use STIX fonts for math
        "font.size": 12,  # Set base font size
        "axes.titlesize": 20,  # Set size of axis titles
        "axes.labelsize": 20,  # Set size of axis labels
        "xtick.labelsize": 14,  # Set size of x-axis tick labels
        "ytick.labelsize": 14,  # Set size of y-axis tick labels
        "legend.fontsize": 20,  # Set size of legend text
        "figure.figsize": (
            8,
            6,
        ),  # Define default figure size (width, height in inches)
    }
)

# File path to the input data file
file_path = "./data/xafs_TEC10E50E_20231031_H.nor"

# Path to save the output plot
output_file_path = "./figures/xafs_norm.png"

# Define x-axis range for the plot (Energy range in eV)
x_min, x_max = 11530, 11615

# Specify the sample name for labeling in the plot
# (Change as per the data being analyzed)
sample_name = r"$\mathrm{TEC10E50E}$"

# Initialize lists to store energy and normalized μ(E) values
energy = []
normalized_mut = []

# Read the data file and parse the content
with open(file_path, "r") as file:
    print(f"Reading data from: {file_path}")
    for line in file:
        if not line.startswith("#"):  # Ignore comment lines (starting with '#')
            parts = line.split()  # Split line into parts based on whitespace
            if len(parts) >= 2:  # Ensure the line has at least two columns
                try:
                    # Append parsed values to the respective lists
                    energy.append(float(parts[0]))  # Energy values
                    normalized_mut.append(float(parts[1]))  # Normalized μ(E) values
                except ValueError:
                    # Skip lines with non-numeric values
                    continue

# Plot the parsed data
plt.figure(figsize=(8, 6))  # Create a figure with specified size
plt.plot(
    energy, normalized_mut, "k-", label=sample_name
)  # Plot data with a black solid line

plt.xlabel(r"$\mathrm{Energy} \, (\mathrm{eV})$")
plt.ylabel(r"Normalized $\mu(E)$ (a.u.)")

plt.legend()

plt.grid(True, linestyle=":")  # Add grid with dotted lines

# Set x-axis range for better focus on the region of interest
plt.xlim(x_min, x_max)

# Add comma separators to x-axis ticks (e.g., 10000 → 10,000)
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))


# Save the plot as a PNG file
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path, dpi=300)  # Save the figure with high resolution (300 DPI)

# Display the plot on the screen
plt.show()
