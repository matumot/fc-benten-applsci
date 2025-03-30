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
This script processes XAFS data to generate a publication-ready plot of k²χ(k) for the standard sample TEC10E50E.
The plot illustrates k²χ(k) as a function of the wavenumber k (in Å⁻¹), with values shown in Å⁻², highlighting key oscillatory features.

Key Features:
- Reads k and k²χ(k) data from a text file, skipping comment lines.
- Extracts and processes the 4th column of data (k²χ(k)) for analysis.
- Generates a high-quality plot with proper mathematical notation, labeled axes, and a grid.
- Customizes axis ranges for better data visualization.
- Saves the resulting plot as './plots/xafs_chik.png' in 300 dpi resolution.

Input:
- A data file specified by the 'file_path' variable, containing wavenumber k and k²χ(k) values.

Output:
- A PNG file './figures/xafs_chik.png' with a visual representation of k²χ(k) as a function of k.

Dependencies:
- matplotlib
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
        "figure.figsize": (
            8,
            6,
        ),  # Define default figure size (width, height in inches)
    }
)


# File path to the input data file
file_path = "./data/xafs_TEC10E50E_20231031_H.chik"

# Path to save the output plot
output_file_path = "./figures/xafs_chik.png"

# Define x-axis and y-axis ranges for the plot
x_min, x_max = 0, 17  # Wavenumber range in Å⁻¹
y_min, y_max = -0.8, 1.0  # k²χ(k) value range in Å⁻²

# Specify the sample name for labeling in the plot
sample_name = r"$\mathrm{TEC10E50E}$"

# Initialize lists to store wavenumber (k) and k²χ(k) values
k = []
chik3 = []

# Read the data file and parse the content
with open(file_path, "r") as file:
    print(f"Reading data from: {file_path}")
    for line in file:
        if not line.startswith("#"):  # Ignore comment lines (starting with '#')
            parts = line.split()  # Split line into parts based on whitespace
            if len(parts) >= 2:  # Ensure the line has at least two columns
                try:
                    # Append parsed values to the respective lists
                    k.append(float(parts[0]))  # Wavenumber (k) values
                    chik3.append(float(parts[3]))  # k²χ(k) values from column 4
                except ValueError:
                    # Skip lines with non-numeric values
                    continue

# Plot the parsed data
plt.figure(figsize=(8, 6))  # Create a figure with specified size
plt.plot(k, chik3, "k-", label=sample_name)  # Plot data with a black solid line

# Update axis labels with proper math notation and font sizes
plt.xlabel(r"$\mathrm{Wavenumber} \,\, (\mathrm{\AA}^{-1})$")
plt.ylabel(r"$k^{2} \chi(k) \,\, (\mathrm{\AA}^{-2})$")


# plt.legend(fontsize=12)  # Add legend with specified font size
plt.grid(True, linestyle=":")  # Add grid with dotted lines

# Set x-axis and y-axis ranges for better focus on the data
plt.xlim(x_min, x_max) 
plt.ylim(y_min, y_max) 

# Save the plot as a PNG file with high resolution
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path, dpi=300)  # Save the figure as PNG (300 DPI)

# Display the plot on the screen
plt.show()
