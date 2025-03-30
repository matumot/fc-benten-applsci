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
This script performs peak fitting for the total radial distribution function T(r) data using a combination of Gaussian functions, a physical baseline (4πρr), and an additional term f(r) = Ar^n * exp(-λr). The script calculates peak areas and integrates only the primary Gaussian component for each peak without contributions from adjacent Gaussians. It also provides clear visualization and detailed output of the fitted results, including errors.

### Key Features:
1. **Peak Detection**:
   - Identifies peaks within a user-specified x-range (`peak_find_range_x_min` to `peak_find_range_x_max`) and separates them by a minimum distance (`peak_find_distance_min`).
   - Limits the number of peaks for fitting to `peak_find_count_max` for clarity.
   - Automatically selects the most prominent peaks within the specified range.

2. **Fitting Process**:
   - Simultaneously fits all detected peaks using Gaussian models, a physical baseline, and an additional term.
   - Ensures physical relevance by applying constraints: A < 0, n > 0, λ > 0.
   - Provides error estimates for all fitted parameters using the covariance matrix of the optimization process.

3. **Area Calculation**:
   - Calculates the area under each peak by integrating only the primary Gaussian component within `±3σ` of the peak center, combined with the baseline and additional term contributions.
   - Ignores contributions from adjacent Gaussian components to ensure accurate peak-specific integration.
   - Provides error estimates for the calculated areas based on the uncertainty of the Gaussian amplitude.

4. **Visualization**:
   - Plots the experimental data, the overall fitted curve, and individual peak regions with hatches representing the integrated areas.
   - Only the first `peak_used_count` peaks are displayed with hatches to maintain clarity in visualization.
   - Adjustable plot ranges (`plot_x_min`, `plot_x_max`, `plot_y_min`, `plot_y_max`) for better visualization.

5. **Outputs**:
   - Saves the resulting figure as a high-resolution image (`./figures/pdf_tr_fit.png`).
   - Prints detailed fitted parameters, including peak positions, widths (σ), areas, and their respective errors.

### Dependencies:
- numpy, pandas: Data handling and numerical computations.
- matplotlib: Plotting results.
- scipy: Optimization and signal processing.

### Parameters to Tune:
- `peak_find_range_x_min`, `peak_find_range_x_max`: Defines the x-range for peak detection.
- `peak_find_distance_min`: Minimum distance between detected peaks.
- `peak_find_count_max`: Maximum number of peaks to fit.
- `peak_used_count`: Number of most prominent peaks to visualize with hatches.
- `plot_x_min`, `plot_x_max`, `plot_y_min`, `plot_y_max`: Adjust plot display range.
- `fit_curve_visible_x_max`: Defines the x-range for visualizing the fitted curve.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.optimize import least_squares
from scipy.signal import find_peaks

# Set font style

rcParams.update(
    {
        "font.family": "serif",  # Use a serif font such as Times New Roman
        "mathtext.fontset": "stix",  # Use STIX fonts for math text
        "font.size": 10,  # General font size
        "axes.titlesize": 18,  # Font size for axis titles
        "axes.labelsize": 18,  # Font size for axis labels
        "xtick.labelsize": 14,  # Font size for x-axis tick labels
        "ytick.labelsize": 14,  # Font size for y-axis tick labels
        "legend.fontsize": 12,  # Font size for the legend
        "figure.figsize": (8, 6),  # Default figure size (width, height in inches)
    }
)


# Function for Ax^n exp(-lambda x)
def additional_term(x, A, n, lambda_):
    return A * x**n * np.exp(-lambda_ * x)


# Multi-Gaussian with baseline and additional term
def multi_gaussian_with_baseline_and_additional(x, params):
    rho = params[0]
    num_peaks = (len(params) - 4) // 3
    baseline = 4 * np.pi * x * rho
    gaussians = sum(
        params[i] * np.exp(-((x - params[i + 1]) ** 2) / (2 * params[i + 2] ** 2))
        for i in range(1, 3 * num_peaks + 1, 3)
    )
    A, n, lambda_ = params[-3], params[-2], params[-1]
    additional = additional_term(x, A, n, lambda_)
    return baseline + additional + gaussians, baseline + additional, gaussians


# Residual function for least squares
def residuals(params, x, y):
    y_model, _, _ = multi_gaussian_with_baseline_and_additional(x, params)
    return y - y_model


# Function to calculate area with y > 0 within ±3σ
def calculate_area(x, y):
    mask = y > 0
    return np.trapezoid(y[mask], x[mask])


# Function to calculate standard errors
def calculate_standard_errors(result):
    jacobian = result.jac
    cov_matrix = np.linalg.inv(jacobian.T @ jacobian)
    errors = np.sqrt(np.diag(cov_matrix))
    return errors


# Load data
file_path = "./data/pdf_T_r.txt"
data = pd.read_csv(file_path, sep=r"\s+", header=None, names=["x", "y"])
x = data["x"].values
y = data["y"].values

# Parameters to tune
plot_x_min = 0
plot_x_max = 10
plot_y_min = -10
plot_y_max = 70
peak_find_range_x_min = 2
peak_find_range_x_max = 8
peak_find_distance_min = 0.5
peak_used_count = 5
peak_find_count_max = 6
fit_curve_visible_x_max = 6.9

# Initial guesses
rho_initial = 0.01
A_initial = -1.0
n_initial = 1.0
lambda_initial = 1.0

# Find peaks
valid_indices = (x > peak_find_range_x_min) & (x < peak_find_range_x_max)
x_valid = x[valid_indices]
y_valid = y[valid_indices]
peaks, _ = find_peaks(
    y_valid, distance=peak_find_distance_min / (x_valid[1] - x_valid[0])
)
selected_peaks = x_valid[peaks]

if len(selected_peaks) > peak_find_count_max:
    selected_peaks = selected_peaks[np.argsort(y_valid[peaks])[-peak_find_count_max:]]
selected_peaks = np.sort(selected_peaks)

# Initialize parameters
initial_params = [rho_initial]
for peak in selected_peaks:
    initial_params.extend([1.0, peak, 0.1])
initial_params.extend([A_initial, n_initial, lambda_initial])

# Define bounds
lower_bounds = [-np.inf]
upper_bounds = [np.inf]
for peak in selected_peaks:
    lower_bounds.extend([0, peak - 0.1, 0])
    upper_bounds.extend([np.inf, peak + 0.1, np.inf])
lower_bounds.extend([-np.inf, 0, 0])
upper_bounds.extend([0, np.inf, np.inf])

# Fit the data
try:
    result = least_squares(
        residuals,
        initial_params,
        args=(x, y),
        bounds=(lower_bounds, upper_bounds),
        max_nfev=20000,
    )
    params = result.x

    # Calculate standard errors
    try:
        errors = calculate_standard_errors(result)
    except Exception as e:
        print(f"Error estimating standard errors: {e}")
        errors = np.full_like(params, np.nan)

    # Extract parameters
    A, n, lambda_ = params[-3:]
    A_err, n_err, lambda_err = errors[-3:]
    rho = params[0]
    rho_err = errors[0]
    print(
        f"Fitted A: {A:.4f} ± {A_err:.4f}, n: {n:.4f} ± {n_err:.4f}, lambda: {lambda_:.4f} ± {lambda_err:.4f}"
    )
    print(f"Fitted rho: {rho:.4f} ± {rho_err:.4f}")

    # Calculate peak parameters, areas, and errors
    fitted_peaks = []
    for i in range(1, len(params) - 3, 3):
        a, x0, sigma = params[i : i + 3]
        a_err, x0_err, sigma_err = errors[i : i + 3]

        # Define the range for the current peak
        x_gaussian = x[(x >= x0 - 3 * sigma) & (x <= x0 + 3 * sigma)]

        # Calculate contribution of the specific gaussian
        y_gaussian = a * np.exp(-((x_gaussian - x0) ** 2) / (2 * sigma**2))

        # Include only the baseline and additional term
        y_baseline = 4 * np.pi * x_gaussian * rho + additional_term(
            x_gaussian, A, n, lambda_
        )
        y_combined = y_gaussian + y_baseline

        # Clip to positive values only
        y_combined = y_combined.clip(min=0)

        # Calculate the area under the peak
        area = calculate_area(x_gaussian, y_combined)
        area_err = abs(a_err / a) * area  # Approximate error for area

        # Append results
        fitted_peaks.append((x0, x0_err, sigma, sigma_err, area, area_err))

    # Print results with errors
    print("Fitted Peak Positions, Sigmas, Areas, and Errors:")
    for i, (x0, x0_err, sigma, sigma_err, area, area_err) in enumerate(fitted_peaks):
        print(
            f"Peak {i + 1}: Position: {x0:.3f} ± {x0_err:.3f}, Sigma: {sigma:.3f} ± {sigma_err:.3f}, Area: {area:.2f} ± {area_err:.2f}"
        )

    # Plot results with hatch regions
    plt.figure(figsize=(8, 6))
    plt.plot(
        x,
        y,
        label=r"$\mathrm{Experimental \,\, Data}$",
        color="black",
        linestyle="-",
        alpha=0.8,
    )

    x_range = np.linspace(min(x), max(x), 1000)
    y_fitted, _, _ = multi_gaussian_with_baseline_and_additional(x_range, params)

    mask = x_range <= fit_curve_visible_x_max
    plt.plot(
        x_range[mask],
        y_fitted[mask],
        label=r"$\mathrm{Gaussian \,\, + \,\, Baseline \, Fit}$",
        color="red",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
    )

    for i, (x0, _, sigma, _, area, _) in enumerate(fitted_peaks):
        # Define the range for the current peak
        x_hatch = x_range[(x_range >= x0 - 3 * sigma) & (x_range <= x0 + 3 * sigma)]

        # Calculate contribution of the specific gaussian
        a = params[1 + 3 * i]
        y_gaussian = a * np.exp(-((x_hatch - x0) ** 2) / (2 * sigma**2))

        # Include only the baseline and additional term
        y_baseline = 4 * np.pi * x_hatch * rho + additional_term(x_hatch, A, n, lambda_)
        y_hatch = y_gaussian + y_baseline

        # Clip to positive values only
        y_hatch = y_hatch.clip(min=0)

        if i >= peak_used_count:
            break

        # Add hatch region
        plt.fill_between(
            x_hatch, y_hatch, alpha=0.15, label=rf"$\mathrm{{Peak \,\, {i + 1}}}$"
        )

    # Plot settings
    plt.xlabel(r"$r \,\, (\mathrm{\AA})$")
    plt.ylabel(r"$T(r) \,\, (\mathrm{\AA}^{-2})$")
    plt.xlim(plot_x_min, plot_x_max)
    plt.ylim(plot_y_min, plot_y_max)
    # Adjust the tick intervals
    plt.xticks(
        ticks=[i * 1 for i in range(plot_x_max + 1)]
    )  # X-axis ticks at 1 intervals

    plt.legend(loc="upper right")

    # Add grid lines
    # plt.grid(axis="x", which="major", color="gray", linestyle="--", linewidth=0.5)
    plt.grid(True, linestyle=":")

    plt.savefig("./figures/pdf_tr_fit.png", dpi=300)
    plt.show()
except Exception as e:
    print(f"Fit failed: {e}")
