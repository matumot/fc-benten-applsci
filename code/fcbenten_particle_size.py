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
This script visualizes the transitions of particle size (SAXS) and crystallite size (XRD) for Pt-based 
and Pt-Co-based samples. It plots the changes from 'AsMade' to 'H' to 'EC' treatments using arrows 
and custom markers/colors for different sample types.

Key Features:
- Pt-based and Pt-Co-based samples are distinguished with different markers and colors.
- Transitions are represented with arrows: solid green for 'H' and dashed gray for 'EC'.
- The plot adheres to MDPI specifications for font sizes and aesthetics.
- Includes error bars for SAXS_d_width of 'AsMade' samples (if data is available).
- A diagonal reference line (x = y) is included for comparison.

Output:
- A publication-ready plot saved as './figures/fcbenten_particle_size.png' in 300 dpi.

Input:
- The script reads data from an Excel file: './data/fcbenten_standard_sample_data.xlsx'.
- The required sheet name is 'data'.

Dependencies:
- pandas
- matplotlib
- openpyxl
"""
import matplotlib.pyplot as plt
import pandas as pd  # Import the pandas library
from matplotlib import rcParams

# Set font style for MDPI article format
rcParams.update(
    {
        "font.family": "serif",  # Use a serif font like Times New Roman
        "mathtext.fontset": "stix",  # Use STIX fonts for math
        "font.size": 12,  # Adjust font size to MDPI recommendations
        "axes.titlesize": 14,  # Larger title size
        "axes.labelsize": 16,  # Axis label size
        "xtick.labelsize": 12,  # X-axis tick label size
        "ytick.labelsize": 12,  # Y-axis tick label size
        "legend.fontsize": 10,  # Legend font size
        "figure.figsize": (8, 6),  # Default figure size
    }
)

# Specify the path of the Excel file to load.
file_path = "./data/fcbenten_standard_sample_data.xlsx"

# Print the file paths being used
print(f"Reading data from: {file_path}")

# Check the sheet names contained in the Excel file.
excel_file = pd.ExcelFile(file_path)  # Load the entire Excel file
print("Available sheets in the Excel file:")
print(excel_file.sheet_names)  # Display the list of sheet names

# Specify and load the required sheet.
df = pd.read_excel(file_path, sheet_name="data")  # 'data' is the target sheet name

# Create the plot
fig, ax = plt.subplots(figsize=(8, 6))  # Maintain a square plotting area

# Categorize samples into Pt and Pt-Co groups
pt_co_samples = ["TEC35V31E", "TEC36E52", "TEC36F52"]
pt_samples = [sample for sample in df["Sample"].unique() if sample not in pt_co_samples]

pt_co_samples_latex = [rf"$\mathrm{{{sample}}}$" for sample in pt_co_samples]
pt_samples_latex = [rf"$\mathrm{{{sample}}}$" for sample in pt_samples]

# Define marker styles and colors for each sample
all_markers = [
    "o",
    "s",
    "^",
    "D",
    "v",
    "P",
    "*",
    "X",
    "<",
    ">",
    "h",
    "H",
    "8",
    "|",
    "_",
]  # 15 different marker shapes
pt_markers = all_markers[: len(pt_samples)]  # Markers for Pt samples
pt_co_markers = all_markers[
    len(pt_samples) : len(pt_samples) + len(pt_co_samples)
]  # Markers for Pt-Co samples

# Define color palettes
pt_colors = plt.cm.Reds(
    range(50, 250, int(200 / len(pt_samples)))
)  # Warm colors for Pt
pt_co_colors = plt.cm.Blues(
    range(50, 250, int(200 / len(pt_co_samples)))
)  # Cool colors for Pt-Co

# Define arrow colors (distinct from red/blue)
h_arrow_color = "darkgreen"  # Color for H transition arrows
ec_arrow_color = "darkslategray"  # Color for EC transition arrows

sample_styles = {}

# Plot transitions for each sample: AsMade -> H -> EC
for sample in df["Sample"].unique():
    subset = df[df["Sample"] == sample]
    if {"AsMade", "H", "EC"}.issubset(set(subset["pretreatment"])):
        asmade = subset[subset["pretreatment"] == "AsMade"]
        h = subset[subset["pretreatment"] == "H"]
        ec = subset[subset["pretreatment"] == "EC"]

        x0, y0 = asmade["SAXS_d"].values[0], asmade["XRD_sd"].values[0]
        x1, y1 = h["SAXS_d"].values[0], h["XRD_sd"].values[0]
        x2, y2 = ec["SAXS_d"].values[0], ec["XRD_sd"].values[0]

        # Distinguish styles for Pt and Pt-Co samples
        if sample in pt_samples:
            marker = pt_markers[pt_samples.index(sample)]
            color = pt_colors[pt_samples.index(sample)]
        else:
            marker = pt_co_markers[pt_co_samples.index(sample)]
            color = pt_co_colors[pt_co_samples.index(sample)]

        sample_styles[sample] = {"marker": marker, "color": color}
        style = sample_styles[sample]

        # Represent transitions with arrows (H: solid green; EC: dashed gray with transparency)
        ax.annotate(
            "",
            xy=(x1, y1),
            xytext=(x0, y0),
            arrowprops=dict(color=h_arrow_color, arrowstyle="-|>", lw=0.7, alpha=0.5),
        )
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x0, y0),
            arrowprops=dict(
                color=ec_arrow_color,
                linestyle=(0, (3, 5, 1, 5)),
                lw=0.7,
                arrowstyle="-|>",
                alpha=0.5,
            ),
        )

        # Plot each point (small size, with specific shape and color)
        ax.scatter(
            [x0, x1, x2],
            [y0, y1, y2],
            s=30,
            label=sample,
            marker=style["marker"],
            color=style["color"],
            alpha=0.7,
        )

        # Plot SAXS_d_width for AsMade
        if "SAXS_d_width" in asmade.columns:
            x_error = asmade["SAXS_d_width"].values[0]
            ax.errorbar(
                x0,
                y0,
                xerr=x_error,
                fmt="none",
                ecolor=style["color"],
                linestyle=":",
                alpha=0.5,
                capsize=2,
            )

# Add a guideline for x = y (dashed line)
max_limit = 13  # Extend the line to the maximum value
ax.plot(
    [0, max_limit],
    [0, max_limit],
    linestyle="--",
    color="gray",
    linewidth=0.7,
    alpha=0.7,
)

# Set axis labels and title
ax.set_xlabel(r"$\mathrm{Particle \,\, Size \,\, by \,\, SAXS \,\, (nm)}$")
ax.set_ylabel(r"$\mathrm{Scherrer \,\, Size \,\, by \,\, XRD \,\, (nm)}$")

ax.set_title(
    r"$\mathrm{Transition \,\, of \,\, Particle \,\, and \,\, Scherrer \,\, Sizes:}$"
    "\n"
    r"$\mathrm{From \,\, AsMade \,\, to \,\, H \,\, (Solid \,\, Green) \,\, and \,\, EC \,\, (Dashed \,\, Gray)}$"
)

# Set axis scales and grid
ax.set_xlim(0, max_limit)
ax.set_ylim(0, max_limit)
ax.grid(visible=True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

# Place legend on the right side of the plot and display all sample names
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))  # Remove duplicates
ax.legend(
    by_label.values(),
    by_label.keys(),
    title=r"$\mathrm{Sample}$",
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    frameon=False,
)

# Adjust layout: enable constrained_layout
plt.tight_layout()

# Save the plot: export at 300 dpi
output_file_path = "./figures/fcbenten_particle_size.png"
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path, dpi=300, bbox_inches="tight")
plt.show()
