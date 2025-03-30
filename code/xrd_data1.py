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
This script processes X-ray diffraction (XRD) data, calculates 2θ values for specific lattice planes of target materials,
and generates a plot of intensity vs. 2θ. It includes comparisons with a CeO2 standard and incorporates offsets
for clarity in visual representation.

Key Features:
- Computes 2θ values for specified lattice planes (hkl) using Bragg's Law.
- Loads and processes XRD data from an Excel file.
- Applies offsets to data series for visual clarity in overlapping plots.
- Annotates the plot with hkl indices of reflections for target materials and CeO2.
- Saves the final plot as './figures/xrd_data1.png'.

Input:
- './data/xrd_data.xlsx': An Excel file containing columns for 2θ and intensity data.

Dependencies:
- math
- pandas
- matplotlib
"""

import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams

# Update matplotlib settings to match the MDPI article format
rcParams.update(
    {
        "font.family": "serif",  # Use a serif font like Times New Roman
        "mathtext.fontset": "stix",  # Use STIX fonts for math
        "font.size": 12,  # General font size
        "axes.titlesize": 20,  # Axis title size
        "axes.labelsize": 20,  # Axis label size
        "xtick.labelsize": 14,  # X-axis tick label size
        "ytick.labelsize": 14,  # Y-axis tick label size
        "legend.fontsize": 14,  # Legend font size
        "figure.figsize": (8, 6),  # Default figure size
    }
)


# Constants for Bragg's Law and material properties
class Const:
    hbarc = 1.97  # Reduced Planck constant (keV·Å)
    E = 24.0  # X-ray energy (keV)
    n = 1  # Diffraction order


a_target = 3.918  # Lattice constant for the target material (Å)
a_CeO2 = 5.411  # Lattice constant for CeO2 (Å)

# Reflection data dictionaries for the target material and CeO2
p_target_dict = {
    (1, 1, 1): [None, -0.5, 260000],
    (2, 0, 0): [None, -0.5, 185000],
    (2, 2, 0): [None, -0.5, 170000],
    (3, 1, 1): [None, -0.5, 180000],
    (2, 2, 2): [None, -0.3, 150000],
    (4, 0, 0): [None, -0.5, 140000],
    (3, 3, 1): [None, -0.8, 155000],
    (4, 2, 0): [None, -0.2, 155000],
    (4, 2, 2): [None, -0.5, 145000],
    (5, 1, 1): [None, -0.5, 145000],
    (5, 3, 1): [None, -0.5, 145000],
}

p_CeO2_dict = {
    (1, 1, 1): [None, -0.5, 75000],
    (2, 0, 0): [None, -0.5, 25000],
    (2, 2, 0): [None, -0.5, 50000],
    (3, 1, 1): [None, -0.5, 45000],
    (2, 2, 2): [None, -0.5, 15000],
    (4, 0, 0): [None, -0.5, 15000],
    (3, 3, 1): [None, -0.8, 20000],
    (4, 2, 0): [None, -0.2, 15000],
    (4, 2, 2): [None, -0.5, 20000],
    (5, 1, 1): [None, -0.5, 20000],
    (4, 4, 0): [None, -0.5, 10000],
    (5, 3, 1): [None, -0.5, 15000],
    (6, 2, 0): [None, -0.5, 15000],
}

# Calculate 2θ values for the target material
for hkl, v in p_target_dict.items():
    d = a_target / math.sqrt(sum(x**2 for x in hkl))
    twotheta = 2.0 * math.degrees(
        math.asin(Const.n * Const.hbarc * math.pi / (d * Const.E))
    )
    v[0] = twotheta

# Calculate 2θ values for CeO2
for hkl, v in p_CeO2_dict.items():
    d = a_CeO2 / math.sqrt(sum(x**2 for x in hkl))
    twotheta = 2.0 * math.degrees(
        math.asin(Const.n * Const.hbarc * math.pi / (d * Const.E))
    )
    v[0] = twotheta

# Load the Excel file containing XRD data
file_path = "./data/xrd_data.xlsx"  # Path to the input Excel file
excel_data = pd.ExcelFile(file_path)

# Extract data from the 'data1' sheet
data1 = excel_data.parse("data1")

# Extract relevant columns from the data
twotheta = data1["twotheta"]
TEC10V50E = data1["TEC10V50E"]
background = data1["Background - Lindemann glass capillary"]
twotheta_CeO2 = data1["twotheta CeO2"]
CeO2 = data1["CeO2"]

# Apply offset adjustments for clarity
TEC10V50E_offset = TEC10V50E + 120000
background_offset = background + 90000

# Plot creation
plt.figure(figsize=(10, 6))  # Define figure size

# Plot each dataset with distinct colors and labels
plt.plot(twotheta, TEC10V50E_offset, color="red", label=r"$\mathrm{TEC10V50E}$")
plt.plot(
    twotheta,
    background_offset,
    color="green",
    label=r"$\mathrm{Background \,\, - \,\, Lindemann \,\, glass \,\, capillary}$",
)
plt.plot(
    twotheta_CeO2,
    CeO2,
    color="black",
    label=r"$\mathrm{CeO_2}$",
)

# Set x and y axis limits for the plot
plt.xlim(2, 60)  # X-axis range
plt.ylim(0, 300000)  # Y-axis range

plt.xlabel(r"$2\theta \ (\mathrm{degree})$")  # X-axis label
plt.ylabel(r"$\mathrm{Intensity} \ (\mathrm{a.u.})$")  # Y-axis label

# Customize x-axis ticks and labels
plt.gca().set_xticks(range(2, 61, 1), minor=True)  # Minor ticks at multiples of 1
plt.gca().set_xticks(range(5, 61, 5), minor=False)  # Major ticks at multiples of 5
plt.gca().set_xticklabels([str(i) for i in range(5, 61, 5)])  # Major tick labels

# Add comma formatting for y-axis tick labels
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{int(x):,}"))

# Add vertical grid lines for major ticks
plt.grid(axis="x", which="major", color="gray", linestyle="--", linewidth=0.5)

# Annotate the plot with reflection indices for target material
for hkl, v in p_target_dict.items():
    plt.text(
        v[0] + v[1],
        v[2],
        rf"$({hkl[0]}{hkl[1]}{hkl[2]})$",
        rotation=90,
        fontsize=12,
        verticalalignment="baseline",
    )

# Annotate the plot with reflection indices for CeO2
for hkl, v in p_CeO2_dict.items():
    plt.text(
        v[0] + v[1],
        v[2],
        rf"$({hkl[0]}{hkl[1]}{hkl[2]})$",
        rotation=90,
        fontsize=12,
        verticalalignment="baseline",
    )

# Add legend to the plot
plt.legend()

# Specify the output file path
output_file_path = "./figures/xrd_data1.png"  # Path to save the plot
print(f"The plot will be saved to: {output_file_path}")

# Save the plot as a PNG file
plt.savefig(output_file_path, dpi=300)

# Display the plot
plt.show()
