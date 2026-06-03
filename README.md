# 🌡️ Urban Heat Island Mapping & Predictive GIS Analytics System

Welcome to the **Urban Heat Island (UHI) Mapping & Analytics System**. This repository serves as a modular, high-end collaborative codebase designed for **Theory Project Group 4 (CSE 3-2)**.

The system focuses on a high-resolution micro-analysis of **Mirpur 12** as the baseline ground-truth deployment and scales dynamically to divisional boundaries across Bangladesh: **Entire Dhaka Metropolitan Area**, **Sylhet**, **Rajshahi**, and **Chittagong**. It fuses satellite remote sensing data (specifically Land Surface Temperature and vegetation canopy ratios) with ground-truth sensor parameters to process thermal anomalies, apply machine learning models to predict future temperatures, and support sustainable urban planning. The system processes everything using a unified Python data pipeline and serves an interactive spatial dashboard.

---

## 📂 Rearranged Project Architecture & Directory Layout

To align with the project syllabus requirements (specifically Section 9 of the guidelines), the codebase has been rearranged into the following clean, modular structure:

```text
Urban-Heat-Island-Mapping-with-GIS/
│
├── README.md                           # Master instructions, stack overview, and role guide
├── main.py                             # Master entry-point running the entire pipeline sequentially
├── project-4.md                        # Official project description and guidelines
│
├── field_data/                         # 🌍 CENTRAL DATA REPOSITORY (Role 1 & 2 Workspace)
│   ├── mirpur12_ground_data.csv        # The baseline ground-truth CSV database (20 points with photos)
│   ├── mirpur_unified_environmental_data.csv       # Raw high-resolution dataset (11k rows)
│   ├── mirpur_unified_environmental_data_clean.csv # Cleaned high-resolution dataset
│   ├── mirpur_calculated_environmental_indices.csv # Calculated high-resolution dataset
│   ├── mirpur_ml_ready_data_clean.csv  # Preprocessed & encoded ML-ready dataset
│   ├── mirpur_encoding_dictionary_clean.csv # Category encoding map dictionary
│   ├── mirpur_preprocessing_report.md  # Generated preprocessing analysis report
│   ├── mirpur_historical_temperatures.csv # Historical daily temperature logs
│   └── {region}_data_calculated.csv    # Pipeline-calculated regional datasets for the dashboard
│
├── gps_coordinates/                    # 📍 FIELD GPS COORDINATES (Role 1 Workspace)
│   └── mirpur12_gps_coordinates.csv    # GPS-tagged field coordinate records extracted from survey
│
├── satellite_data/                     # 🛰️ REMOTE SENSING PRESETS (Role 1 & 2 Workspace)
│   ├── placeholders.js                 # Regional bounding vectors and city coordinate presets
│   └── templates/                      # Data ingestion templates for field, history, and satellite
│
├── gis_maps/                           # 🎨 VISUALIZATIONS & SPATIAL LAYERS (Role 3 Workspace)
│   ├── {region}_heatmap.html           # Standalone Folium Leaflet.js interactive maps
│   └── graphs/
│       └── {region}_concrete_vs_veg_scatter.png # Comparative scatter plots of LST vs NDVI
│
├── ml_models/                          # 🧠 MACHINE LEARNING METRICS (Role 4 Workspace)
│   └── {region}_reg_metrics.json       # Serialized AI model accuracies, formulas, and parameters
│
├── pipeline/                           # ⚙️ PYTHON PIPELINE LOGIC MODULES (Collaborative Core)
│   ├── __init__.py                     # Package initialization and function exports
│   ├── preprocessing.py                # Role 1: Ingests, cleans, and merges CSV & satellite datasets
│   ├── calculation.py                  # Role 2: Implements LST & NDVI mathematical calculations
│   ├── plotting.py                     # Role 3: Generates Folium heatmaps & Matplotlib graphs
│   └── prediction.py                   # Role 4: Trains AI / ML regressors for heat prediction
│
├── backend/                            # 💻 FLASK WEB APP BACKEND (Backend Integration)
│   ├── app.py                          # Serving index.html and exposing unified regional API
│   └── models/
│       └── analytics.py                # Core mathematical helper analytics
│
├── frontend/                           # 🌐 INTERACTIVE DASHBOARD FRONTEND (Frontend Integration)
│   ├── index.html                      # Glassmorphic responsive analytics layout
│   ├── css/
│   │   └── styles.css                  # Custom styling, responsive grids, and animations
│   ├── js/
│   │   └── app.js                      # Leaflet.js map renderer, dynamic tables, and Chart.js integration
│   └── images/
│       └── *.jpeg                      # 20 geotagged site verification photos of Mirpur 12
│
├── dashboard/                          # 🚀 WEB SERVER RUNNER
│   └── run_dashboard.py                # Server launcher script to run the Flask application
│
├── presentation/                       # 📊 SLIDES & PRESENTATION OUTLINES
│   └── presentation_outline.md         # PowerPoint outline and Viva prep guide
│
└── documentation/                      # 📝 DOCUMENTATION & REPORT WRITING
    ├── Heat Map.md                     # LaTeX equations and visualization constraints
    ├── project_architecture.md         # Master architectural workflow document
    ├── regional_summaries_report.md    # Geographic explanations for divisional profiles
    └── Report writting/
        └── ESL Group 4 Report.md      # Flawless academic report containing all thesis chapters
```

---

## 👥 Collaborative Boundaries & Role Instructions

To ensure seamless progress without Git merge conflicts, the codebase has been structured with clear workspace boundaries. Here is exactly what each role needs to do, where they must do it, and how:

### 📡 Role 1: Data Collection & Data Preprocessing
* **Assigned Members:** Sayed, Nusair
* **Primary Objective:** Ingest, clean, and align raw ground sensor coordinates and satellite parameters.
* **Workspace Folder & Boundary:**
  - Files to modify: [pipeline/preprocessing.py](file:///Users/punam/Desktop/varsity/3-2/Theory/ESL/Project/pipeline/preprocessing.py) and [scripts/preprocess_mirpur_data.py](file:///Users/punam/Desktop/varsity/3-2/Theory/ESL/Project/scripts/preprocess_mirpur_data.py).
  - Target directories: `field_data/`, `gps_coordinates/`, `satellite_data/`.
  - Boundary: You manage raw data inputs. Do not touch math equations, plotting libraries, or ML model fitting scripts.
* **Technical Guidelines:**
  1. Load field temperature measurements, sensor outputs, and GPS logs using Pandas.
  2. Implement text normalization, remove duplicates, filter out coordinate points outside the boundary boxes, and handle missing values.
  3. Ensure that the ingestion loader outputs a unified Pandas DataFrame adhering to the **Shared Data Contract**.

---

### ✍️ Role 2: Calculation & Report Writing
* **Assigned Members:** Punam, Nafiz
* **Primary Objective:** Implement core physical calculations for NDVI and LST and author the academic report.
* **Workspace Folder & Boundary:**
  - Files to modify: [pipeline/calculation.py](file:///Users/punam/Desktop/varsity/3-2/Theory/ESL/Project/pipeline/calculation.py), [scripts/calculate_mirpur_indices.py](file:///Users/punam/Desktop/varsity/3-2/Theory/ESL/Project/scripts/calculate_mirpur_indices.py), and reports inside `documentation/`.
  - Boundary: You manage the mathematical transformations of inputs and documentation. Do not modify plotting engines or ML regressors.
* **Technical Guidelines:**
  1. Implement the mathematical models for NDVI using red and near-infrared (NIR) bands:
     $$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}$$
  2. Implement the Land Surface Temperature (LST) calculation based on vegetation canopy index:
     $$\text{Predicted Temperature} = \alpha - (\beta \times \text{NDVI})$$
  3. Generate data validation checks to ensure average temperature, hotspots, and coolspots reflect physical realities.

---

### 🎨 Role 3: Dataset Plotting & Visualization
* **Assigned Members:** Spondon, Rushafi
* **Primary Objective:** Build comparative graphs and GIS mapping coordinate layers.
* **Workspace Folder & Boundary:**
  - Files to modify: [pipeline/plotting.py](file:///Users/punam/Desktop/varsity/3-2/Theory/ESL/Project/pipeline/plotting.py) (specifically the static plots and point marker mapping functions).
  - Target directory: `gis_maps/graphs/` and coordinate points in Leaflet.
  - Boundary: You govern static plotting, comparison charts, and point markers. You do not write predictive ML scripts or generate the density Heatmap layers.
* **Technical Guidelines:**
  1. Use **Matplotlib** and **Seaborn** to build comparative graphs, including Temperature vs. NDVI scatter plots with fitted regression lines, boxplots of surface types, and traffic heat bars.
  2. Implement coordinate-based GIS mapping overlays mapping site locations, surface profiles, and photos.
  3. Export static graphs to `gis_maps/graphs/`.

---

### 🧠 Role 4: Predictive Analysis (ML)
* **Assigned Members:** Ajwad, Sabbir
* **Primary Objective:** Develop machine learning prediction models, run future forecasts, and generate thermal GIS Heatmaps.
* **Workspace Folder & Boundary:**
  - Files to modify: [pipeline/prediction.py](file:///Users/punam/Desktop/varsity/3-2/Theory/ESL/Project/pipeline/prediction.py) and Leaflet/Folium heat maps inside [pipeline/plotting.py](file:///Users/punam/Desktop/varsity/3-2/Theory/ESL/Project/pipeline/plotting.py).
  - Target directory: `ml_models/` and `gis_maps/{region}_heatmap.html`.
  - Boundary: You govern the ML model files, JSON metrics, and the spatial Heatmap density visual layers.
* **Technical Guidelines:**
  1. Train **Linear Regression**, **Decision Tree**, and **Random Forest** regressors on NDVI to predict temperatures.
  2. Compute evaluation metrics (R², RMSE, MAE) and write outputs to `ml_models/{region}_reg_metrics.json`.
  3. Generate the Folium interactive **Heatmap** overlays showing predicted localized heat risks, saving them as `gis_maps/{region}_heatmap.html`.

---

## 📊 Shared Data Contract (Pipeline Schema)

To maintain flawless coordination across preprocessing, calculation, mapping, and ML modeling, the standardized data dictionary structure returned by the pipeline and served via `/api/heat-data` adheres to this contract:

```json
{
  "region": "mirpur12",
  "name": "Mirpur 12",
  "description": "Hyper-local baseline micro-analysis...",
  "analytics": {
    "alpha_intercept": 30.88,
    "beta_slope": 15.16,
    "avg_temp": 30.86,
    "r2_score": 0.4485,
    "rmse": 5.541,
    "mae": 4.9998,
    "peak_hotspot": {
      "name": "Mirpur-10 Roundabout",
      "temp": 43.991,
      "lat": 23.8248,
      "lng": 90.3621
    },
    "peak_coolspot": {
      "name": "National Botanical Garden",
      "temp": 10.0,
      "lat": 23.827,
      "lng": 90.363
    }
  },
  "records": [
    {
      "LocationID": 1,
      "LocationName": "Mirpur-12 Metrorail station",
      "Latitude": 23.826606,
      "Longitude": 90.364136,
      "Temperature": 32.5,
      "SurfaceType": "Concrete",
      "NDVI": 0.1,
      "TrafficDensity": "High",
      "Time": "Afternoon",
      "Image": "Mirpur-12 Metrorail station, 23.826606, 90.364136, 30-35.jpeg"
    }
  ]
}
```

---

## 🏃 Quick-Start Development Guide

Follow these steps to execute the pipeline and run the dashboard locally:

### 1. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn folium scikit-learn flask --break-system-packages
```

### 2. Execute Data Preprocessing & Mathematical Calculations
Run the standalone data cleaning and calculation scripts:
```bash
python scripts/preprocess_mirpur_data.py
python scripts/calculate_mirpur_indices.py
```
*(This cleans the high-resolution 11k dataset and generates reports under `field_data/`)*.

### 3. Run the Unified Master Pipeline
Execute the master orchestration script from the root directory:
```bash
python main.py
```
*(This processes all 5 regions, runs calculations, fits ML regressors, exports JSON parameters to `ml_models/`, and generates Leaflet maps under `gis_maps/`)*.

### 4. Launch the Web Dashboard
Start the Flask web server:
```bash
python dashboard/run_dashboard.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to view the interactive glassmorphic GIS mapping dashboard.
