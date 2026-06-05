# LiDAR Vertical Datum Transformation using PDAL + Python

Transform LAS/LAZ Point Cloud files from:

**WGS84 / UTM Zone 38N + Ellipsoidal Heights**

to:

**GRF17 / UTM Zone 38N + KSA Geoid21 Orthometric Heights**

using Python and PDAL.

---

# Overview

This project automates the transformation of massive LiDAR Point Cloud datasets from ellipsoidal heights into the official Saudi vertical datum using the KSA Geoid21 model.

The workflow was developed for real production datasets containing thousands of LAS files that needed to be delivered in:

* GRF17
* UTM Zone 38N
* Orthometric Heights
* KSA Geoid21

---

# The Problem

Many LiDAR datasets are delivered with:

* Horizontal Datum:
  `WGS84 / UTM Zone 38N`

* Vertical Datum:
  `Ellipsoidal Height`

However, many engineering and surveying projects in Saudi Arabia require:

* `GRF17`
* `KSA Geoid21`
* Orthometric Heights

This creates a vertical datum mismatch problem.

Without applying geoid correction, elevation values will not match the official Saudi reference system.

---

# Solution

The workflow performs the following operations automatically:

1. Read LAS/LAZ files
2. Reproject coordinates:

   * From `EPSG:32638`
   * To `EPSG:9358`
3. Apply geoid correction using:
   `filters.hag_dem`
4. Replace ellipsoidal Z values with orthometric heights
5. Export corrected LAS files

---

# Workflow Diagram

```text
LAS Files
   ↓
PDAL Readers
   ↓
Reprojection (EPSG:32638 → EPSG:9358)
   ↓
Geoid Correction using KSA Geoid21 Raster
   ↓
Orthometric Height Conversion
   ↓
Corrected LAS Output
```

---

# Requirements

## Software

* Python 3.9+
* PDAL
* GDAL
* Conda (Recommended)

---

# Python Libraries

Install required libraries:

```bash
pip install pdal
```

---

# Recommended Environment Installation

Using Conda:

```bash
conda create -n pdal_env python=3.9
conda activate pdal_env

conda install -c conda-forge pdal
conda install -c conda-forge gdal
```

---

# Input Requirements

## 1. LAS/LAZ Files

Input point cloud files must be:

* LAS or LAZ
* WGS84 / UTM Zone 38N
* Ellipsoidal Heights

Example:

```text
EPSG:32638
```

---

## 2. Geoid Raster

A GeoTIFF raster representing:

* KSA Geoid21
* GRF17
* EPSG:9358

Example:

```text
Geoid_KSA21_EPSG_9358.tif
```

---

# Generating the Geoid Raster

Geoid values were extracted from the official Saudi GRF17 Geoportal:

🔗 https://gds.geoportal.sa/GRF17

Typical workflow:

1. Generate grid points covering the study area
2. Extract geoid heights
3. Convert points into GeoTIFF raster
4. Use raster inside PDAL pipeline

---

# Project Structure

```text
project/
│
├── input_las/
├── output_las/
├── Geoid_KSA21_EPSG_9358.tif
├── transform_lidar.py
└── README.md
```

---

# Example Code

```python
{
    "type":"filters.reprojection",
    "in_srs":"EPSG:32638",
    "out_srs":"EPSG:9358"
}
```

Apply geoid correction:

```python
{
    "type":"filters.hag_dem",
    "raster":geoid_raster
}
```

Replace Z values:

```python
{
    "type":"filters.assign",
    "value":"Z = HeightAboveGround"
}
```

---

# Running the Script

Edit paths inside the script:

```python
input_folder = r"D:\LAS_Files"

geoid_raster = r"Geoid_KSA21_EPSG_9358.tif"

output_folder = r"D:\LAS_Output"
```

Run:

```bash
python transform_lidar.py
```

---

# Output

The script generates corrected LAS files:

```text
*_GRF17_Geoid21.las
```

Each file will contain:

* GRF17 coordinates
* Orthometric Heights
* KSA Geoid21 correction

---

# Features

✅ Batch processing for thousands of LAS files

✅ Automated geoid correction

✅ PDAL-based workflow

✅ Production-ready processing pipeline

✅ Reusable for other geoid models

---

# Technologies Used

* Python
* PDAL
* GDAL
* LiDAR
* GIS
* Geomatics Engineering

---

# References

## PDAL

🔗 https://pdal.io

## Saudi GRF17 Geoportal

🔗 https://gds.geoportal.sa/GRF17

---

# Author

Mohamed Mokashifi

Geomatics Engineer | GIS Developer | LiDAR Specialist

---

# License

This project is open-source and available under the MIT License.
