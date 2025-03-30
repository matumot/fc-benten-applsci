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
This script visualizes the transitions of particle size (SAXS) and lattice strain (XRD) 
for Pt-based and Pt-Co-based samples. The changes from 'AsMade' to 'H' to 'EC' treatments 
are represented with arrows and plotted with distinct markers and colors for each sample type.

Key Features:
- Pt-based and Pt-Co-based samples are differentiated by markers and color schemes.
- Transitions are indicated by arrows: solid green for 'H' and dashed gray for 'EC'.
- MDPI-style font sizes and colors are applied for academic presentation.
- Error bars for SAXS_d_width of 'AsMade' samples are included if data is available.

Output:
- A publication-ready plot saved as './figures/fcbenten_lattice_strain.png' in 300 dpi.

Input:
- The script reads data from an Excel file: './data/fcbenten_standard_sample_data.xlsx'.
- The required sheet name is 'data'.

Dependencies:
- pandas
- matplotlib
- openpyxl
"""
import matplotlib.pyplot as plt
import pandas as pd  # Import pandas library
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

# 1. Specify the path of the Excel file to load.
file_path = "./data/fcbenten_standard_sample_data.xlsx"

# Print the file paths being used
print(f"Reading data from: {file_path}")

# 2. Check the sheet names in the Excel file.
excel_file = pd.ExcelFile(file_path)  # Load the entire Excel file
print("Available sheets in the Excel file:")
print(excel_file.sheet_names)  # Display the list of sheet names

# 3. Specify and load the required sheet.
df = pd.read_excel(file_path, sheet_name="data")  # 'data' is the target sheet name

# 4. Display the DataFrame content to verify the data.
# print(df.head())  # Check the first 5 rows


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

        x0, y0 = asmade["SAXS_d"].values[0], asmade["XRD_ws"].values[0]
        x1, y1 = h["SAXS_d"].values[0], h["XRD_ws"].values[0]
        x2, y2 = ec["SAXS_d"].values[0], ec["XRD_ws"].values[0]

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

# Add gridlines
ax.grid(visible=True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

# Add labels and title
ax.set_xlabel(r"$\mathrm{Particle \,\,Size \,\, by \,\, SAXS \,\, (nm)}$")
ax.set_ylabel(r"$\mathrm{Lattice \,\, Strain}$")
ax.set_title(
    r"$\mathrm{Transition \,\, of \,\, Particle \,\, Size \,\, and \,\, Lattice \,\, Strain:}$"
    "\n"
    r"$\mathrm{From \,\, AsMade \,\, to \,\, H \,\, (Solid \,\, Green) \,\, and \,\, EC \,\, (Dashed \,\, Gray)}$"
)

# Ensure 0 is included in both x and y ticks
ax.set_xticks(sorted(set(ax.get_xticks()).union({0})))  # Include 0 in x-axis ticks
ax.set_yticks(sorted(set(ax.get_yticks()).union({0})))  # Include 0 in y-axis ticks

# Add the legend to the right of the plot
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))  # Remove duplicates
ax.legend(
    by_label.values(),
    by_label.keys(),
    title="Sample",
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    frameon=False,
)

# Adjust layout and save plot
plt.tight_layout()
output_file_path = "./figures/fcbenten_lattice_strain.png"
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path, dpi=300, bbox_inches="tight")
plt.show()
