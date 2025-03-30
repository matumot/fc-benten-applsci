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
This script generates a plot of the structure factor S(Q) for the standard sample TEC10V30E.
The plot displays S(Q) as a function of Q (in Å⁻¹), highlighting the high-Q oscillations, with values
shown in arbitrary units. The script reads the input data, processes it, and outputs a publication-ready plot.

Key Features:
- Reads Q and S(Q) data from a text file, skipping header lines.
- Generates a log-log plot with labeled axes and gridlines.
- Saves the resulting plot as './plots/pdf_sq.png' in 300 dpi.

Output:
- A PNG file './figures/pdf_sq.png' containing the publication-ready S(Q) plot.

Input:
- The script processes Q and S(Q) data from the file specified by the 'file_path' variable.

Dependencies:
- pandas
- matplotlib
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
file_path = "./data/pdf_S_q_fqd.txt"  # Specify the file path
print(f"Reading data from: {file_path}")

# Load the data
# Read from the 3rd line onwards
data = pd.read_csv(file_path, sep=r"\s+", skiprows=2, header=None)

# Extract the required columns
Q = data.iloc[:, 0]
S_Q = data.iloc[:, 1]

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(Q, S_Q, "k-", label=r"$\mathrm{TEC10V30E}$", linewidth=2)

plt.xlabel(r"$Q \,\, (\mathrm{\AA}^{-1})$")
plt.ylabel(r"$S(Q)$")

plt.legend()

# Add grid lines
# plt.grid(axis="x", which="major", color="gray", linestyle="--", linewidth=0.5)
plt.grid(True, linestyle=":")

# Set the x-axis ranges
plt.xlim(0, 27)  # Set the x-axis range

# Specify the output file path
output_file_path = "./figures/pdf_sq.png"
print(f"The plot will be saved to: {output_file_path}")

# Save the plot as a PNG file
plt.savefig(output_file_path, dpi=300)

# Display the plot
plt.show()
