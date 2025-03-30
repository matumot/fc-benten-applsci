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
This script generates a plot of the pair distribution function G(r) for the standard sample TEC10V30E.
The plot displays G(r) as a function of r (in Å⁻¹), showcasing key structural features. The script reads
input data, processes it, and produces a publication-ready plot formatted for academic articles.

Key Features:
- Reads r and G(r) data from a text file, skipping header lines.
- Generates a detailed plot with labeled axes and gridlines for clarity.
- Saves the resulting plot as a high-resolution PNG file.

Output:
- A PNG file './figures/pdf_Gr.png' containing the publication-ready G(r) plot.

Input:
- The script processes r and G(r) data from the file specified by the 'file_path' variable.

Dependencies:
- pandas: For data reading and processing.
- matplotlib: For generating and customizing plots.
"""

import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import rcParams

# Set font style for MDPI article format

rcParams.update(
    {
        "font.family": "serif",  # Use a serif font such as Times New Roman
        "mathtext.fontset": "stix",  # Use STIX fonts for math text
        "font.size": 10,  # General font size
        "axes.titlesize": 18,  # Font size for axis titles
        "axes.labelsize": 18,  # Font size for axis labels
        "xtick.labelsize": 14,  # Font size for x-axis tick labels
        "ytick.labelsize": 14,  # Font size for y-axis tick labels
        "legend.fontsize": 20,  # Font size for the legend
        "figure.figsize": (8, 6),  # Default figure size (width, height in inches)
    }
)

# Specify the file path for input data
file_path = "./data/pdf_bigG_r.txt"  # Specify the file path
print(f"Reading data from: {file_path}")

# Load the data
# Read from the 3rd line onwards
data = pd.read_csv(file_path, sep=r"\s+", skiprows=2, header=None)

# Extract the required columns
Q = data.iloc[:, 0]
S_Q = data.iloc[:, 1]

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(Q, S_Q, "k-", label=r"$\mathrm{TEC10V30E}$")

plt.xlabel(r"$r \,\, (\mathrm{\AA})$")
plt.ylabel(r"$G(r) \,\, (\mathrm{\AA}^{-2})$")

plt.legend()

# Add grid lines
# plt.grid(axis="x", which="major", color="gray", linestyle="--", linewidth=0.5)
plt.grid(True, linestyle=":")

# Set the x-axis ranges
plt.xlim(0, 63)  # Set the x-axis range

# Specify the output file path
output_file_path = "./figures/pdf_Gr.png"
print(f"The plot will be saved to: {output_file_path}")

# Save the plot as a PNG file
plt.savefig(output_file_path, dpi=300)

# Display the plot
plt.show()
