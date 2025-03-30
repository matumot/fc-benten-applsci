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
This script processes XAFS data to generate a publication-ready plot of |χ(R)| for the standard sample TEC10E50E.
The plot illustrates |χ(R)| as a function of radial distance r (in Å), with values shown in Å⁻³, focusing on both experimental and fitted data.

Key Features:
- Reads radial distance (r), experimental χ(R), and fitted χ(R) values from a text file, skipping comment lines.
- Generates a high-quality plot with:
  - Labeled axes using LaTeX-style math notation.
  - A grid for better readability.
  - Legends distinguishing experimental and fitted data.
- Customizes axis ranges for radial distance and χ(R) values to focus on the region of interest.
- Saves the resulting plot as a PNG file with 300 dpi resolution.

Input:
- A data file specified by the 'file_path' variable, containing columns for radial distance (r), χ(R), and fitted χ(R) values.

Output:
- A PNG file './figures/xafs_chir_fit.png' showing the comparison between experimental and fitted |χ(R)| as a function of r.

Dependencies:
- matplotlib
"""

import matplotlib.pyplot as plt
from matplotlib import rcParams

# Update matplotlib settings to match the MDPI article format
rcParams.update(
    {
        "font.family": "serif",  # Use serif font style (e.g., Times New Roman)
        "mathtext.fontset": "stix",  # Use STIX fonts for rendering mathematical expressions
        "font.size": 12,  # Set the base font size for all text elements
        "axes.titlesize": 20,  # Set the font size for the axes titles
        "axes.labelsize": 20,  # Set the font size for the axes labels
        "xtick.labelsize": 14,  # Set the font size for x-axis tick labels
        "ytick.labelsize": 14,  # Set the font size for y-axis tick labels
        "legend.fontsize": 20,  # Set the font size for the legend
        "figure.figsize": (8, 6),  # Define the default figure size (width, height in inches)
    }
)

# File path to the input data file
file_path = "./data/xafs_TEC10E50E_H_03.rmag"

# Path to save the output plot as a PNG file
output_file_path = "./figures/xafs_chir_fit.png"

# Define the range for the x-axis (radial distance in Å)
x_min, x_max = 0, 6  # Minimum and maximum x-axis values

# Define the range for the y-axis (|χ(R)| values in Å⁻³)
y_min, y_max = -0.8, 1.0  # Minimum and maximum y-axis values

# Specify the sample name for display in the plot legend
sample_name = r"$\mathrm{TEC10E50E}$"  # Rendered in LaTeX-style math font

# Initialize lists to store parsed data from the input file
r = []         # Radial distance values
chir = []      # χ(R) values (experimental data)
chir_fit = []  # χ(R) fit values (fitted data)

# Read the input data file and parse its contents
with open(file_path, "r") as file:
    print(f"Reading data from: {file_path}")
    for line in file:
        if not line.startswith("#"):  # Ignore lines starting with '#' (comments)
            parts = line.split()  # Split the line into parts based on whitespace
            if len(parts) >= 3:  # Ensure the line contains at least three columns
                try:
                    # Parse and append numerical values to respective lists
                    r.append(float(parts[0]))         # First column: radial distance
                    chir.append(float(parts[1]))      # Second column: χ(R) values
                    chir_fit.append(float(parts[2]))  # Third column: χ(R) fit values
                except ValueError:
                    # Skip the line if it contains non-numeric values
                    continue

# Create a figure with the specified dimensions
plt.figure(figsize=(8, 6))

# Plot the experimental χ(R) data as a black solid line
plt.plot(
    r, chir, "k-", label=r"$\mathrm{Exp.}$", alpha=0.7, linewidth=1.5
)

# Plot the fitted χ(R) data as a red dashed line
plt.plot(
    r, chir_fit, "r--", label=r"$\mathrm{Fit}$", alpha=0.7, linewidth=1.5
)

# Add labels to the axes using LaTeX-style formatting
plt.xlabel(r"$\mathrm{Radial \,\, distance} \,\, (\mathrm{\AA})$")  # x-axis label
plt.ylabel(r"$|\chi(R)| \,\, (\mathrm{\AA}^{-3})$")  # y-axis label

# Add a legend to the plot
plt.legend()

# Enable the grid with dotted lines for better readability
plt.grid(True, linestyle=":")

# Set the range of the x-axis to focus on the region of interest
plt.xlim(x_min, x_max)

# Save the resulting plot to the specified output file with high resolution (300 DPI)
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path, dpi=300)

# Display the plot on the screen
plt.show()
