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
This script processes XAFS data to generate a high-quality plot of k²χ(k) for the standard sample TEC10E50E.
The plot illustrates k²χ(k) as a function of the wavenumber k (in Å⁻¹), with values shown in Å⁻², highlighting both experimental and fitted curves for visual comparison.

Key Features:
- Reads k, experimental k²χ(k), and fitted k²χ(k) data from a specified input file, skipping comment lines.
- Visualizes the experimental and fitted k²χ(k) data with distinct line styles:
  - Experimental data: black solid line.
  - Fitted data: red dashed line with transparency for better visibility of overlaps.
- Customizes plot aesthetics, including labeled axes, a lightly transparent grid, and proper mathematical notation.
- Adjusts axis ranges for enhanced focus on relevant data regions.
- Saves the plot as './plots/xafs_chik_fit.png' in 300 dpi resolution for publication-quality output.

Input:
- A data file specified by the 'file_path' variable, containing three columns:
  1. Wavenumber (k, in Å⁻¹)
  2. Experimental k²χ(k) values (in Å⁻²)
  3. Fitted k²χ(k) values (in Å⁻²)

Output:
- A PNG file './figures/xafs_chik_fit.png' displaying the experimental and fitted k²χ(k) as a function of the wavenumber.

Dependencies:
- matplotlib: Used for creating and customizing the plot.

Usage Notes:
- Ensure the input data file is properly formatted with numeric values in the required columns, and comment lines prefixed with '#'.
- Modify the axis ranges or styles in the code if the dataset requires different visualization settings.
"""

import matplotlib.pyplot as plt
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
        "figure.figsize": (8, 6),  # Default figure size (width, height in inches)
    }
)

# File path to the input data file
file_path = "./data/xafs_TEC10E50E_H_03.k2"

# Path to save the output plot
output_file_path = "./figures/xafs_chik_fit.png"

# Define axis ranges for the plot
x_min, x_max = 0, 17  # Wavenumber range in Å⁻¹
y_min, y_max = -0.8, 1.0  # k²χ(k) value range in Å⁻²

# Specify the sample name for labeling in the plot
sample_name = r"$\mathrm{TEC10E50E}$"

# Initialize lists to store wavenumber (k) and k²χ(k) values
k = []
chik3 = []
chik3_fit = []

# Read and parse the data file
with open(file_path, "r") as file:
    print(f"Reading data from: {file_path}")
    for line in file:
        if not line.startswith("#"):  # Ignore comment lines (starting with '#')
            parts = line.split()  # Split line into columns based on whitespace
            if len(parts) >= 3:  # Ensure the line has at least two columns
                try:
                    # Append parsed values to the respective lists
                    k.append(float(parts[0]))  # Wavenumber (k) values
                    chik3.append(float(parts[1]))  # Experimental k²χ(k) values
                    chik3_fit.append(float(parts[2]))  # Fitted k²χ(k) values
                except ValueError:
                    # Skip lines with non-numeric values
                    continue

# Create a new figure for the plot
plt.figure(figsize=(8, 6))

# Plot experimental data with a black solid line and transparency
plt.plot(
    k, chik3, "k-", label=r"$\mathrm{Exp.}$", alpha=0.7, linewidth=1.5
)

# Plot fitted data with a red dashed line and transparency
plt.plot(
    k, chik3_fit, "r--", label=r"$\mathrm{Fit}$", alpha=0.7, linewidth=1.5
)

# Set axis labels with proper math notation
plt.xlabel(r"$\mathrm{Wavenumber} \,\, (\mathrm{\AA}^{-1})$")
plt.ylabel(r"$k^{2} \chi(k) \,\, (\mathrm{\AA}^{-2})$")

# Add a legend to the plot
plt.legend()

# Add a grid with dotted lines and slight transparency
plt.grid(True, linestyle=":", alpha=0.6)

# Set axis limits for better focus on the data
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

# Save the plot as a PNG file with high resolution
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path, dpi=300)

# Display the plot
plt.show()
