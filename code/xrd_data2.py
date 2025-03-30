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
This script processes XRD data to generate publication-ready plots for analyzing material structure.

Key Features:
- Generates a main plot displaying the XRD pattern, including observed, calculated, background, and difference profiles.
- Annotates Bragg reflection peaks with hkl indices for clarity and publication-quality presentation.
- Creates an inset plot (Williamson-Hall plot) to analyze crystallite size and lattice strain.
- Applies a linear regression to Williamson-Hall data and visualizes the results with error bounds.

Input:
- An Excel file specified by the 'file_path' variable, containing:
  - XRD pattern data (2θ and intensity profiles).
  - Williamson-Hall plot data (sinθ/λ and βcosθ/λ values).

Output:
- A PNG file './figures/xrd_data2.png' that combines the XRD pattern and Williamson-Hall plot in a visually appealing layout.

Dependencies:
- pandas
- matplotlib
- numpy
- scipy
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams
import numpy as np
from scipy.stats import linregress

# Update matplotlib settings to match the MDPI article format
# Customize fonts, figure size, and other style settings
rcParams.update(
    {
        "font.family": "serif",  # Use a serif font like Times New Roman
        "mathtext.fontset": "stix",  # Use STIX fonts for math
        "font.size": 14,
        "axes.titlesize": 18,
        "axes.labelsize": 18,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "legend.fontsize": 12,
        "figure.figsize": (8, 6),
    }
)

# Load data for both plots
# Load XRD data from an Excel file
file_path = "./data/xrd_data.xlsx"
data = pd.ExcelFile(file_path)
data2 = data.parse("data2")  # Main dataset for plot 1
data2_williamson_hall = pd.read_excel(
    file_path, sheet_name="data2_williamson_hall"
)  # Dataset for Williamson-Hall plot

# Extract data for plot 1
# Data needed for the main plot
twotheta = data2["twotheta"]
observed = data2["Observed"]
calculated = data2["Calculated"]
background = data2["Background"]
difference_profiles = data2["Difference profiles"]
bragg_peaks_twotheta = data2["bragg peaks_twotheta"]
bragg_peaks = data2["bragg peaks"]

# Reflection data for annotations
# Dictionary of Bragg reflection peaks with their positions and annotation details
p_target_dict = {
    (1, 1, 1): [13.1645, -0.5, 55000],
    (2, 0, 0): [15.212, -0.5, 30000],
    (2, 2, 0): [21.5761, -0.5, 25000],
    (3, 1, 1): [25.3568, -0.5, 25000],
    (2, 2, 2): [26.5043, -0.3, 15000],
    (4, 0, 0): [30.6977, -0.5, 10000],
    (3, 3, 1): [33.5294, -0.8, 15000],
    (4, 2, 0): [34.4271, -0.2, 15000],
    (4, 2, 2): [37.8314, -0.5, 10000],
}

# Extract data for plot 2
# Data needed for the Williamson-Hall plot
sin_theta_lambda = data2_williamson_hall.iloc[0, 2:].astype(float)
beta_cos_theta_lambda = data2_williamson_hall.iloc[1, 2:].astype(float)

# Perform linear regression to calculate slope, intercept, and other stats
slope, intercept, r_value, p_value, std_err = linregress(
    sin_theta_lambda, beta_cos_theta_lambda
)

# Calculate the regression line and error bounds
x_fit = np.linspace(2.0, 7.0, 100)
y_fit = slope * x_fit + intercept
y_fit_upper = y_fit + 3 * std_err
y_fit_lower = y_fit - 3 * std_err

# Create the main figure and axis for plot 1
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot observed data
ax1.plot(twotheta, observed, color="cyan", linewidth=2, label=r"$\mathrm{Observed}$")

# Plot calculated data
ax1.plot(
    twotheta, calculated, color="brown", linewidth=2, label=r"$\mathrm{Calculated}$"
)

# Plot background data
ax1.plot(
    twotheta, background, color="black", linewidth=1, label=r"$\mathrm{Background}$"
)


# Plot difference profiles
ax1.plot(
    twotheta,
    difference_profiles,
    color="blue",
    linewidth=1,
    label=r"$\mathrm{Difference \,\, profiles}$",
)


# Plot Bragg peaks
label = r"$\mathrm{Bragg \,\, peaks \,\, (Pt \,\, fcc \,\, structure)}$"
for x, y in zip(bragg_peaks_twotheta, bragg_peaks):
    if pd.notna(x):
        ax1.plot([x, x], [0, y], color="green", linestyle="-", label=label)
        if label:
            label = None  # Ensure the label is only shown once in the legend

# Annotate the plot with reflection indices
for hkl, v in p_target_dict.items():
    ax1.text(
        v[0] + v[1],
        v[2],
        rf"$({hkl[0]}{hkl[1]}{hkl[2]})$",
        rotation=90,
        verticalalignment="baseline",
    )

# Add labels and grid
ax1.set_xlim(2, 60)
ax1.set_ylim(0, 60000)
ax1.set_xlabel(r"$2\theta \ (\mathrm{degree})$", fontsize=20)
ax1.set_ylabel(r"$\mathrm{Intensity} \ (\mathrm{a.u.})$", fontsize=20)
ax1.grid(axis="x", which="major", color="gray", linestyle="--", linewidth=0.5)

# Add comma formatting for y-axis tick labels
ax1.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: f"{int(x):,}" if x >= 10000 else f"{int(x)}")
)

# Add legend
ax1.legend(loc="upper center", bbox_to_anchor=(0.35, 1))

# Customize x-axis ticks and labels
ax1.set_xticks(range(2, 61, 1), minor=True)  # Minor ticks at multiples of 1
ax1.set_xticks(range(5, 61, 5), minor=False)  # Major ticks at multiples of 5
ax1.set_xticklabels([str(i) for i in range(5, 61, 5)])  # Major tick labels

# Create inset axis for plot 2
# Add an inset for the Williamson-Hall plot
ax_inset = fig.add_axes([0.58, 0.55, 0.31, 0.31])  # [left, bottom, width, height]

# Plot data points for Williamson-Hall plot
ax_inset.scatter(sin_theta_lambda, beta_cos_theta_lambda, color="blue")

# Plot the regression line
ax_inset.plot(x_fit, y_fit, color="blue", linestyle="--")

# Plot error bounds
ax_inset.fill_between(x_fit, y_fit_lower, y_fit_upper, color="peachpuff", alpha=0.6)

# Add text annotations to the inset
ax_inset.text(4.3, 0.480, r"$y = 0.0152 x + 0.3544$")
ax_inset.text(2.2, 0.345, r"$(111)$")
ax_inset.text(6.2, 0.420, r"$(422)$")
ax_inset.text(3.8, 0.350, r"$\mathrm{Crystallite \, size: \, 2.4(1) \, \mathrm{\AA}}$")
ax_inset.text(3.8, 0.325, r"$\mathrm{Lattice \, strain: \, 0.004(1)}$")

# Label the axes of the inset plot
ax_inset.set_xlabel(r"$\sin\theta/\lambda \ (\text{nm}^{-1})$")
ax_inset.set_ylabel(r"$\beta\cos\theta/\lambda \ (\text{nm}^{-1})$")
ax_inset.set_xlim(2, 7)
ax_inset.set_ylim(0.3, 0.5)
ax_inset.grid(True)

# Save and display the combined plot
output_file_path = "./figures/xrd_data2.png"
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path, dpi=300)
plt.show()
