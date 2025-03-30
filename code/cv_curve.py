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
'''
This script processes Cyclic Voltammetry (CV) data to generate plots for electrochemical analysis.

Key Features:
- Generates a CV curve plot displaying the relationship between electrode potential and current response.
- Ensures clarity with labeled axes and a structured grid.

Input:
- An Excel file specified by the 'file_path' variable, containing:
  - Column 'Ewe/V' for electrode potential (vs. RHE).
  - Column '<I>/mA' for measured current in milliamperes.

Output:
- A PNG file './figures/cv_curve.png' containing the CV plot in a visually appealing format.

Dependencies:
- pandas
- matplotlib
'''
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Set font style for MDPI article format
rcParams.update(
    {
        "font.family": "serif",  # Use serif font style (e.g., Times New Roman)
        "mathtext.fontset": "stix",  # Use STIX fonts for math
        "font.size": 12,  # Set base font size
        "axes.titlesize": 18,  # Set size of axis titles
        "axes.labelsize": 18,  # Set size of axis labels
        "xtick.labelsize": 14,  # Set size of x-axis tick labels
        "ytick.labelsize": 14,  # Set size of y-axis tick labels
        "legend.fontsize": 18,  # Set size of legend text
        "figure.figsize": (
            8,
            6,
        ),  # Define default figure size (width, height in inches)
    }
)

# Specify the path to the Excel file and sheet name
file_path = "./data/cv_TEC10V30E-CVdata.xlsx"
sheet_name = "TEC10V30E"
output_file_path = "./figures/cv_curve.png"

# Print the file paths being used
print(f"Reading data from: {file_path}, sheet: {sheet_name}")

# Load the Excel data
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Extract data for plotting
x = data["Ewe/V"]
y = data["<I>/mA"]

# Plot the CV curve
plt.figure(figsize=(8, 6))
plt.plot(x, y, color="black", linewidth=1.5)

plt.xlabel(r"$E_{\mathrm{we}} \, \mathrm{vs.} \, \mathrm{RHE} \, (\mathrm{V})$")
plt.ylabel(r"$\langle I \rangle \, (\mathrm{mA})$")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

# Save the plot as a PNG file
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path, dpi=300)

# Display the plot
plt.show()
