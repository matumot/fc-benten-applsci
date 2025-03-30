

# FC-BENTEN: Synchrotron X-ray Experimental Database for Polymer-Electrolyte Fuel-Cell Material Analysis

## 1. Overview

This repository accompanies the MDPI Applied Sciences Review Paper:
**"FC-BENTEN: Synchrotron X-ray Experimental Database for Polymer-Electrolyte Fuel-Cell Material Analysis"**

It includes experimental data, scripts, and visual outputs for the figures presented in the paper. The repository aims to support reproducibility and transparency by providing access to data and tools used in the study.

------

## 2. Repository Contents

The repository is organized as follows:

- [data/](./data/): Raw experimental data files for each figure.
- [code/](./code/): Python scripts used for processing the data and generating plots.
- [figures/](./figures/): Visualizations included in the paper (PNG files).
- [README.md](./README.md): Documentation for understanding and utilizing the repository.

------

## 3. Figure Descriptions

Below is a summary of the figures included in this repository.

**Note:**   Figures such as 1, 2, 6, 13, and 16–19 are conceptual diagrams or photographs without associated data and are therefore not included here.

------

### Figure 3: Cyclic voltammetry (CV) Results

- **Data**: `data/cv_TEC10V30E-CVdata.xlsx`
- **Code**: `code/cv_curve.py`
- **Figure**: `figures/cv_curve.png`
- **Description**: Cyclic voltammetry results for Pt/C catalyst samples, showing the relationship between working electrode potential (Ewe) and current (I) under specific operational conditions.

------

### Figure 4: XAFS spectra

- **Data**:
  -  XANES:   `data/xafs_TEC10E50E_20231031_H.nor`
  -  k-space:  `data/xafs_TEC10E50E_20231031_H.chik`
  -  R-space:  `data/xafs_TEC10E50E_20231031_H.chir`
- **Code**: 
  - XANES:  `code/xafs_norm.py`
  - k-space:  `code/xafs_chik.py`
  - R-space:  `code/xafs_chir.py`
- **Figure**:
  -  XANES: `figures/xafs_norm.png`
  -  k-space: `figures/xafs_chik.png` 
  -  R-space:`figures/xafs_chir.png` 
- **Description**: Pt L3-edge XAFS spectra acquired from Pt/C catalyst samples, illustrating electronic states, local structures, and radial distributions.

------

### Figure 5: EXAFS Fitting Results

- **Data**:
  -  k-space:  `data/xafs_TEC10E50E_H_03.k2`
  -  R-space:  `data/xafs_TEC10E50E_H_03.rmag`
- **Code**: 
  - k-space: `code/xafs_chik_fit.py` 
  - R-space: `code/xafs_chir_fit.py` 
- **Figure**:
  -  k-space: `figures/xafs_chik_fit.png` 
  -  R-space: `figures/xafs_chir_fit.png` 
- **Description**: EXAFS fitting results for Pt/C catalysts, showing experimental data and fitted spectra for structural analysis.

------

### Figure 7:  HAXPES Energy Calibration

- **Data**:
  -  10V (reference):  `data/haxpes_VB_10VE_0001.txt`
  -  TEC36F52 (target):  `data/haxpes_VB_TEC36F52_0001.txt`
- **Code**:  `code/haxpes_energy_calibration.py`
- **Figure**: `figures/haxpes_energy_calibration.png`
- **Description**:  Binding energy calibration using valence band profiles of reference and target samples.

------

### Figure 8:  HAXPES profiles

- **Data**:
  -  Valence band:
     -  TEC10F50E: `data/haxpes_VB_TEC10F50E_H_0001.csv`
     -  TEC10F50E-HT: `data/haxpes_VB_TEC10F50E-HT_H_0001.csv`
     -  TEC10E50E: `data/haxpes_VB_TEC10E50E_H_0001.csv`
     -  TEC10EA50E: `data/haxpes_VB_TEC10EA50E_H_0001.csv`
  -  Pt-4f:
     -  TEC10F50E:  `data/haxpes_Pt4f_TEC10F50E_H_0001.csv`
     -  TEC10F50E-HT: `data/haxpes_Pt4f_TEC10F50E-HT_H_0001.csv`
     -  TEC10E50E: `data/haxpes_Pt4f_TEC10E50E_H_0001.csv`
     -  TEC10EA50E:  `data/haxpes_Pt4f_TEC10EA50E_H_0001.csv`
- **Code**:  
  - Valence band: `code/haxpes_vb.py`
  - Pt-4f:  `code/haxpes_pt4f.py`
- **Figure**:
  -  Valence band:`figures/haxpes_vb.png`
  -  Pt-4f: `figures/haxpes_pt4f.png`  
- **Description**: HAXPES spectra for hydrogen-reduced Pt/C catalysts, including valence band and Pt 4f regions after calibration and normalization.

------

### Figure 9: XRD Spectra

- **Data:** `data/xrd_data.xlsx` (data1 sheet)
- **Code**:  `code/xrd_data1.py`
- **Figure:** `figures/xrd_data1.png`
- **Description**: XRD spectra obtained from Pt/C catalyst samples, an empty capillary, and cerium oxide reference. The diffraction patterns reflect structural characteristics of the catalyst.

------

### Figure 10: XRD Spectra and Williamson-Hall analysis

- **Data:** `data/xrd_data.xlsx`  (data2 and data2_williamson_hall sheet)
- **Code**:  `code/xrd_data2.py`
- **Figure:** `figures/xrd_data2.png`
- **Description**: XRD spectra and Williamson-Hall analysis for Pt/C catalyst samples, used to evaluate lattice strain effects.

------

### Figure 11: PDF Profiles (Intensity, S(Q))

- **Data:**
  - Intensity: `data/pdf_data.xlsx` 
  - S(Q): `data/pdf_S_q_fpd.txt` 
- **Code**: 
  - Intensity: `code/pdf_data.py` 
  - S(Q): `code/pdf_sq.py` 
- **Figure**: 
  - Intensity: `figures/pdf_data.png` 
  - S(Q): `figures/pdf_sq.png`
- **Description**: PDF intensity profiles and structure factors S(Q) for hydrogen-reduced Pt/C catalyst samples, showing corrected scattering signals and high-Q features.

------

### Figure 12: PDF Profiles (G(r), T(r))

- **Data:**
  - G(r): `data/pdf_bigG_r.txt` 
  - T(r): `data/pdf_T_r.txt` 
- **Code**: 
  - G(r): `code/pdf_Gr.py` 
  - T(r): `code/pdf_tr_fit.py` 
- **Figure**: 
  - G(r): `figures/pdf_Gr.png` 
  - T(r): `figures/pdf_tr_fit.png`
- **Description**: Pair Distribution Functions G(r) and T(r) derived from hydrogen-reduced Pt/C catalyst data, including Gaussian fitting for coordination analysis.

------

### Figure 14: SAXS Intensity Profiles

- **Data:**
  - `data/saxs_Particle 1.33 .05_2024-11-21_17-24-29_profileV.txt`
  - `data/saxs_Particle 1.33 .38_2024-11-21_17-25-43_profileV.txt`
  - `data/saxs_C10V30E_As_FE_00001__sum_Connected.txt`
- **Code**: `code/saxs_profile.py`
- **Figure**: `figures/saxs_profile.png`
- **Description**: SAXS intensity profiles for Pt/C catalyst samples, compared to simulated data with different particle size distributions.

------

### Figure 15: SAXS particle size Evaluation

- **Data**:
  - McSAS profile: `data/saxs_TEC10V30E_As_FE_00001__sum_Connected 2023-02-09_13-41-55_fit.dat`  
  - McSAS particle size: `data/saxs_TEC10V30E_As_FE_00001__sum_Connected 2023-02-09_13-41-55_hist-radius-True-0(nm)-10(nm)-50-lin-vol.dat` 
- **Code**: 
  - McSAS profile: `code/mcsas_profile.py` 
  - McSAS particle size: `code/saxs/mcsas_radius.py` 
- **Figure**:
  - McSAS profile: `figures/mcsas_profile.png`
  - McSAS particle size:  `figures/mcsas_radius.png`
- **Description**: McSAS analysis results for Pt/C catalysts, including scattering profile fitting and particle size distribution histograms.

------

### Figure 20: Correlation Between SAXS Particle Sizes and XRD Scherrer Sizes

- **Data**: `data/fcbenten_standard_sample_data.xlsx`
- **Code**: `code/fcbenten_particle_size.py`
- **Figure**: `figures/fcbenten_particle_size.png`
- **Description**: Correlation plot of SAXS-determined particle sizes  and XRD-determined Scherrer sizes, with different markers representing specific sample treatments. Strong correlation is observed, with post-treatment samples showing size increases for Pt-based samples.

------

### Figure 21: Correlation Between SAXS Particle Sizes and XRD Lattice Strain

- **Data**: `data/fcbenten_standard_sample_data.xlsx`
- **Code**: `code/fcbenten_lattice_strain.py`
- **Figure**: `figures/fcbenten_lattice_strain.png`
- **Description**: Correlation plot showing SAXS-determined particle sizes and XRD-determined lattice strain. Strain relaxation trends are observed in smaller particle sizes, particularly in Pt-based samples undergoing treatment transitions.

------

## 4.  How to Use

1. **Download Necessary Data Files**
   Ensure that all required data files are downloaded and placed in the appropriate directories as specified in the scripts.

2. **Install Python Dependencies**:
   Required Python libraries include `matplotlib`, `pandas`, `openpyxl`, and `scipy`, as specified in [requirements.txt](./requirements.txt).   You can set up the environment using:

   ```
   pip install -r requirements.txt
   ```

3. **Run Scripts**: Generate plots or analyze data by running the corresponding Python scripts. For example:

   ```
   python code/cv_curve.py
   ```

------

## 5. Additional Notes

### Figure and Data Documentation

- For specific details about each figure, refer to the figure descriptions provided in this README or within the corresponding directories.
- Where applicable, comments within the scripts explain the methods and steps used for data processing and visualization.

### Licensing and Attribution

- **Code:** Licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)  
  - The full license text is provided in the [LICENSE](./LICENSE) file located at the root of this repository.  
  - Please ensure compliance with the license terms when using or modifying the code.

- **Data and Figures:** Licensed under the [Creative Commons Attribution 4.0 International (CC-BY)](https://creativecommons.org/licenses/by/4.0/)  
  - To acknowledge the use of data or figures, please provide appropriate attribution.  
  - Detailed attribution guidelines are available in the [CREDIT.md](./CREDIT.md) file.
