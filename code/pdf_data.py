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
This script processes PDF measurement data and generates a plot of 2θ vs. intensity.
The script is tailored for presenting corrected, raw, and background data from PDF experiments.

Key Features:
- Loads and processes PDF data from an Excel file with separate sheets for corrected, raw, and background data.
- Generates a publication-quality plot of intensity vs. 2θ for the datasets.
- Saves the final plot as a high-resolution PNG file.

Input:
- './data/pdf_data.xlsx': An Excel file containing the following sheets:
  - 'corrected_data': Corrected intensity data with columns for 2θ and intensity.
  - 'raw_data': Raw intensity data with columns for 2θ and intensity.
  - 'background_data': Background intensity data with columns for 2θ and intensity.

Output:
- './figures/pdf_data.png': A PNG image file of the intensity vs. 2θ plot.

Dependencies:
- pandas: For loading and processing Excel data.
- matplotlib: For generating and customizing plots.
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

# Update matplotlib settings to match the MDPI article format
rcParams.update(
    {
        "font.family": "serif",  # Set font family to serif for a professional appearance
        "mathtext.fontset": "stix",  # Use STIX font for math expressions
        "font.size": 10,  # General font size
        "axes.titlesize": 18,  # Title font size for axes
        "axes.labelsize": 18,  # Label font size for axes
        "xtick.labelsize": 14,  # Font size for x-axis ticks
        "ytick.labelsize": 14,  # Font size for y-axis ticks
        "legend.fontsize": 14,  # Font size for legend text
        "figure.figsize": (8, 6),  # Default figure size
    }
)

# Load the Excel file containing the data
file_path = "./data/pdf_data.xlsx"

# Read data from specific sheets into separate DataFrames
corrected_data = pd.read_excel(file_path, sheet_name="corrected_data")  # Corrected data
raw_data = pd.read_excel(file_path, sheet_name="raw_data")  # Raw data
background_data = pd.read_excel(file_path, sheet_name="quartz_cap")  # Background data

# Initialize the plot
plt.figure(figsize=(8, 6))  # Create a new figure with specified dimensions


# Define a function to process and plot concatenated data from multiple columns
def plot_concatenated_data(
    data, label_prefix, color, x_range, scale_factors, offset_factors=[0.0] * 8
):
    """
    Prepare and plot concatenated data from multiple columns in a dataset.

    Parameters:
    - data: DataFrame containing the dataset.
    - label_prefix: Prefix for the label in the legend.
    - color: Color of the plot line.
    - x_range: List of x-axis ranges for each set.
    - scale_factors: Scaling factors to adjust the intensity.
    - offset_factors: Offset factors to adjust the baseline of the intensity.
    """
    combined_twotheta = []  # List for concatenated 2θ values
    combined_count = []  # List for concatenated intensity values

    # Iterate through columns for Twotheta and Count
    for i in range(1, 8):
        col_twotheta = f"Twotheta{i}"  # Name of the 2θ column
        col_count = f"Count{i}/I0"  # Name of the intensity column

        if col_twotheta in data.columns and col_count in data.columns:
            # Filter data based on the specified x_range
            data_filtered = data[
                (data[col_twotheta] >= x_range[i][0])
                & (data[col_twotheta] <= x_range[i][1])
            ]

            # Scale and offset the intensity values
            scaled_count = (
                data_filtered[col_count] * scale_factors[i] + offset_factors[i]
            )
            combined_twotheta.extend(data_filtered[col_twotheta])  # Append 2θ values
            combined_count.extend(scaled_count)  # Append intensity values

    # Combine and sort the data for smooth plotting
    combined_data = pd.DataFrame(
        {"Twotheta": combined_twotheta, "Count": combined_count}
    )
    combined_data = combined_data.sort_values(by="Twotheta")  # Sort by 2θ

    # Plot the concatenated data
    plt.plot(
        combined_data["Twotheta"],
        combined_data["Count"],
        label=label_prefix,
        color=color,
        alpha=0.7,
    )


# Initialize scaling and offset factors, and x-axis ranges for data continuity
scale_factors = [1.0] * 8
offset_bkg_factors = [0.0] * 8
x_range = [[0.0, 0.0]] * 8

# Calculate scaling factors and x-axis ranges
for i in range(1, 8):
    # Default range for overlaps
    overlap_start = 0.0
    overlap_end = 60.0
    x_range[i] = [overlap_start, overlap_end]

    if i >= 2:
        # Adjust the range for overlaps based on neighboring datasets
        overlap_start = 0.5 * (
            raw_data[f"Twotheta{i-1}"].max() + raw_data[f"Twotheta{i}"].min()
        )
    if i <= 6:
        overlap_end = 0.5 * (
            raw_data[f"Twotheta{i}"].max() + raw_data[f"Twotheta{i+1}"].min()
        )

    if i >= 2 and overlap_start < overlap_end:
        # Calculate scaling factors for continuity between datasets
        count1_interp = np.interp(
            overlap_start, raw_data[f"Twotheta{i-1}"], raw_data[f"Count{i-1}/I0"]
        )
        count2_interp = np.interp(
            overlap_start, raw_data[f"Twotheta{i}"], raw_data[f"Count{i}/I0"]
        )
        scale_factors[i] = scale_factors[i - 1] * count1_interp / count2_interp
        x_range[i] = [overlap_start, overlap_end]

        # Calculate offset factor for background data
        count1_bkg_interp = np.interp(
            overlap_start,
            background_data[f"Twotheta{i-1}"],
            background_data[f"Count{i-1}/I0"],
        )
        count2_bkg_interp = np.interp(
            overlap_start,
            background_data[f"Twotheta{i}"],
            background_data[f"Count{i}/I0"],
        )
        offset_bkg_factors[i] = (
            offset_bkg_factors[i - 1]
            + scale_factors[i - 1] * count1_bkg_interp
            - scale_factors[i] * count2_bkg_interp
        )

# Plot raw, background, and corrected data
plot_concatenated_data(
    raw_data, r"$\mathrm{Raw \,\, data}$", "red", x_range, scale_factors
)
plot_concatenated_data(
    background_data,
    r"$\mathrm{Background}$",
    "blue",
    x_range,
    scale_factors,
    offset_bkg_factors,
)
plot_concatenated_data(
    corrected_data, r"$\mathrm{Corrected \, data}$", "black", x_range, scale_factors
)

# Customize plot appearance
plt.xlabel(r"$2\theta \,\, (\mathrm{degree})$")
plt.ylabel(r"$\mathrm{Intensity} \,\, (\mathrm{a.u.})$")
plt.yscale("log")
plt.xlim(0, 55.5)
plt.ylim(1e-5, 1e-1)
plt.legend()
plt.grid(True, linestyle=":")
plt.tight_layout()

# Save the plot to a file
output_file_path = "./figures/pdf_data.png"
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path, dpi=300)
plt.show()
