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
This script processes and visualizes HAXPES (Hard X-ray Photoelectron Spectroscopy) data 
to compare the valence band profiles of a target sample (TEC36F52) and a reference sample (10V). 
The script calculates the energy offset between the target and reference samples by 
interpolating at a specific intensity level (y=0.4) and applies the correction to align the Fermi edges.

Purpose:
- Normalize the intensity values of both target and reference data for comparison.
- Calculate the energy offset using linear interpolation of the data.
- Generate a comparative plot showing the original and energy-corrected target data 
  along with the reference data and a visual guide at the interpolated level.

Key Features:
- Reads metadata and numerical data from text files for processing.
- Performs normalization to maximum intensity for direct comparisons.
- Uses linear interpolation to calculate the leading energy at a specified intensity.
- Applies energy correction to the target data based on the calculated offset.
- Produces a clear and informative plot with inverted x-axis, labeled axes, 
  and distinct line styles for clarity.

Plot Specifications:
- x-axis: Binding energy (eV), inverted direction.
- y-axis: Normalized intensity (a.u.), range [-0.1, 1.2].
- Line styles and colors:
  - Reference sample: Red, solid line.
  - Target sample: Black, solid line.
  - Energy-corrected target: Black, dashed line.
  - Interpolated level (y=0.4): Green, dotted line.
- No plot title is specified.

Output:
- Saves a PNG plot to "figures/haxpes_energy_calibration.png" for further analysis or publication.

Input:
- Data files for the target and reference samples in plain text format, 
  containing binding energy and intensity values.

Dependencies:
- matplotlib
- numpy
- scipy
"""
import matplotlib.pyplot as plt
import numpy as np
import re

from scipy import interpolate
from matplotlib import rcParams

# Set font style for MDPI article format
rcParams.update(
    {
        "font.family": "serif",  # Use a serif font like Times New Roman
        "mathtext.fontset": "stix",  # Use STIX fonts for math
        "font.size": 20,  # Adjust font size to MDPI recommendations
        "axes.titlesize": 18,  # Larger title size
        "axes.labelsize": 20,  # Axis label size
        "xtick.labelsize": 14,  # X-axis tick label size
        "ytick.labelsize": 14,  # Y-axis tick label size
        "legend.fontsize": 14,  # Legend font size
        "figure.figsize": (8, 6),  # Default figure size
    }
)


# Function to read HAXPES data from a file
# Extracts metadata and numerical data for further analysis
def read_haxpes_data(filename_data, fermi_energy=None):
    tag = None
    vmeta = {}  # Dictionary to store metadata
    vdata = {}  # Dictionary to store numerical data
    with open(filename_data, "r") as f:
        for line in f:
            # Detect tags (e.g., [Data]) to categorize sections in the file
            m = re.search(r"\[(Data|DATA).*\]", line)
            if m:
                tag = m.group(0)[1:-1]

            if tag is None:
                # Parse metadata lines in the format key=value
                sline = line.split("=")
                if len(sline) == 2:
                    key = sline[0].strip()
                    val = sline[1].strip()
                    vmeta[key] = val
            else:
                # Parse numerical data within the tagged sections
                sline = line.split()
                if not m and len(sline) == 2:
                    v1 = float(sline[0])
                    v2 = float(sline[1])
                    if tag not in vdata:
                        vdata[tag] = []
                    else:
                        # Adjust data if Fermi energy is provided
                        if fermi_energy:
                            vdata[tag].append((fermi_energy - v1, v2))
                        else:
                            vdata[tag].append((v1, v2))
        return vmeta, vdata


# Function to normalize data and apply energy offset
def get_normalized_data(filename, fermi_energy, energy_offset=0.0, upper_limit=None):
    # Read the data and extract key information
    vmeta, vdata = read_haxpes_data(filename, fermi_energy)
    key = list(vdata.keys())[0]
    datalist = vdata[key]

    xarray = []
    yarray = []

    # Process and normalize the data
    for data in datalist:
        if upper_limit and data[0] > upper_limit:
            continue
        xarray.append(data[0] - energy_offset)
        yarray.append(data[1])

    # Normalize the intensity values to max = 1
    ymax = np.amax(yarray)
    yarray /= ymax

    return xarray, yarray


# Function to interpolate and find leading energy for a given intensity
def get_leading_energy_at_y_interpolate(
    xarray, yarray, y_interpolate_min, y_interpolate_max, y_interpolate
):
    xarray_sub = []
    yarray_sub = []

    # Extract the subset of data for interpolation
    for i in range(len(xarray))[::-1]:
        x = xarray[i]
        y = yarray[i]
        if y > y_interpolate_min:
            xarray_sub.append(x)
            yarray_sub.append(y)
        if y > y_interpolate_max:
            break

    # Perform linear interpolation
    f = interpolate.interp1d(yarray_sub, xarray_sub, kind="linear")
    value = f([y_interpolate])[0]
    return value


# Function to extract photon energy from metadata
def get_photon_energy(filename_data):
    vmeta, _ = read_haxpes_data(filename_data)
    photon_energy = float(vmeta["Excitation Energy"])
    return photon_energy


# Input parameters and filenames
beamline = "BL09XU"
filename_target = "data/haxpes_VB_TEC36F52_0001.txt"
filename_ref = "data/haxpes_VB_10VE_0001.txt"

sample_target = r"$\mathrm{TEC36F52}$"
sample_ref = r"$\mathrm{10V}$"

# Experimental photon energies
incident_photon_energy = 7940.0
incident_photon_energy_ref = get_photon_energy(filename_ref)

# Energy offset and upper limit for data processing
offset_energy = 0.02
upper_limit = 13.0

# Normalize data for target and reference samples
xarray, yarray = get_normalized_data(
    filename_target, incident_photon_energy, offset_energy, upper_limit
)
xarray_ref, yarray_ref = get_normalized_data(
    filename_ref, incident_photon_energy_ref, offset_energy, upper_limit
)

# Internal parameters for interpolation
y_interpolate = 0.4
y_interpolate_min = 0.05
y_interpolate_max = 0.75

# Plot range settings
x_min, x_max = 1.5, -1.0
y_min, y_max = -0.1, 1.2

# Create a constant y array for the interpolated line
xarray_int = xarray_ref
yarray_int = [y_interpolate] * len(xarray_int)

# Calculate energy offsets using interpolation
leading_energy_target = get_leading_energy_at_y_interpolate(
    xarray, yarray, y_interpolate_min, y_interpolate_max, y_interpolate
)
leading_energy_ref = get_leading_energy_at_y_interpolate(
    xarray_ref, yarray_ref, y_interpolate_min, y_interpolate_max, y_interpolate
)
energy_offset = leading_energy_ref - leading_energy_target

# Print results
print("=== results  ===")
print(f"... leading energy (target) = {leading_energy_target}")
print(f"... leading energy (reference) = {leading_energy_ref:g}")
print(f"... energy offset = {energy_offset:g}")

# Apply the energy correction to the target data
xarray_corr = xarray + energy_offset

# Plot settings and visualization
figsize = (8, 6)
fig = plt.figure(figsize=figsize)
axis = plt.subplot(111)

plt.plot(
    xarray_ref,
    yarray_ref,
    label=r"$\mathrm{Reference \,\, [10V]}$",
    color="red",
    linestyle="-",
    alpha=0.7,
)

plt.plot(
    xarray,
    yarray,
    label=r"$\mathrm{Target \,\, [TEC36F52]}$",
    color="black",
    linestyle="-",
    alpha=0.7,
)

plt.plot(
    xarray_corr,
    yarray,
    label=rf"$\mathrm{{Target \,\, with \,\, Energy \,\, corr. \,\, ({energy_offset:.2g} \,\, eV)}}$",
    color="black",
    linestyle="--",
    alpha=0.7,
)

plt.plot(
    xarray_int,
    yarray_int,
    label=r"$\mathrm{Interpolated \, \, Line \,\, (0.4)}$",
    color="green",
    linestyle=":",
    linewidth=2.5,
    alpha=0.9,
)

# Customize plot appearance
plt.xlabel(r"$\mathrm{Binding \,\, energy} \,\, (\mathrm{eV})$")
plt.ylabel(r"$\mathrm{Intensity} \,\, (\mathrm{a.u.})$", labelpad=10)

plt.gca().invert_xaxis()  # Reverse x-axis for conventional display
plt.gca().yaxis.set_ticks_position("left")
plt.gca().xaxis.set_ticks_position("both")
plt.tick_params(axis="both", which="major")
yticks = plt.gca().get_yticks()
plt.gca().set_yticks(yticks)
plt.grid(axis="x", linestyle="--", alpha=0.7)

# Set axis limits
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

# Add a label for the valence band
plt.text(
    0.70,
    0.93,
    r"$\mathrm{Valence \,\, band}$",
    ha="left",
    transform=plt.gca().transAxes,
)

# Add legend for clarity
plt.legend(loc="lower left", bbox_to_anchor=(0.01, 0.05))

plt.tight_layout()

# Display and save the plot
output_file_path = "./figures/haxpes_energy_calibration.png"
print(f"The plot will be saved to: {output_file_path}")
plt.savefig(output_file_path)

plt.show()
