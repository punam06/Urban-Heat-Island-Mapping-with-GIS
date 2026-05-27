# 🌡️ Urban Heat Island Mapping & Predictive GIS Dashboard

Welcome to the **Urban Heat Island (UHI) Mapping & Analytics System**. This repository serves as a modular, high-end collaborative codebase designed for **Theory Project Group 4 (CSE 3-2)**.

The system focuses on a high-resolution micro-analysis of **Mirpur 12** as the baseline ground-truth deployment and scales dynamically to divisional boundaries across Bangladesh: **Entire Dhaka Metropolitan Area**, **Sylhet**, **Rajshahi**, and **Chittagong**. It fuses satellite remote sensing data (specifically Land Surface Temperature and vegetation canopy ratios) with ground-truth sensor parameters to visualize thermal anomalies and support sustainable urban planning.

---

## 🌐 Strategic Project Charter

### 🎯 Project Purpose & Objectives
Rapid urbanization across Bangladesh has replaced natural green canopies with heat-absorbing concrete pavements and high-density multi-story structures. The purpose of this project is to model and visualize this **Urban Heat Island (UHI) effect** to identify thermal hotspots, analyze their environmental causes, and predict temperatures based on vegetation coverage.
- **Identify Micro-Thermal Anomalies:** Locate localized heat zones (down to street/alley levels like the Mirpur 12 Bus Stand and Metro Station) that standard macro-climatic tools miss.
- **Model Vegetation Influence:** Calculate the exact mathematical inverse correlation between green cover indices (NDVI) and surface temperature.
- **Support Strategic Cooling:** Provide city planners with data-backed locations to deploy green roofs, parks, and water bodies to cool the city.

### 👥 Stakeholders & Beneficiaries (How They Benefit)
* **Municipal Corporations (e.g., DNCC, DSCC):**
  - *Benefit:* Obtain hyper-local thermal risk maps to optimize the layout of urban cooling zones and community parks.
* **Urban Planners & Architects:**
  - *Benefit:* Acquire concrete-to-vegetation data sheets to design heat-resilient building envelopes, green building guidelines, and low-heat pavements.
* **General Citizens & Residents:**
  - *Benefit:* View active regional thermal alerts to plan outdoor activities, reduce heatstroke risks, and locate nearby cooling zones.
* **Environmental Research Bodies & Academic Institutions:**
  - *Benefit:* Access a unified platform blending ground-truth coordinates with satellite LST outputs to study climate changes in rapidly growing cities.

### 📈 Expected Impacts
* **Mitigated Energy Consumption:** Pinpointing hotspots enables targeted tree planting, lowering surrounding temperatures by 2–4°C and cutting air conditioning power demands by up to 15%.
* **Optimized Public Health Planning:** Provides local hospitals and authorities with heat risk assessments, helping to lower heat-related illnesses among vulnerable demographics (like field workers and children).
* **Informed Policy Guidance:** Helps establish sustainable city laws, such as mandating minimum green space requirements for new construction projects.

---

## ⚔️ The Strategic Advantage: Over Google's Features

Standard GIS tools (like the Google Environmental Insights Explorer or Google Earth Engine Tree Canopy tool) provide valuable macro datasets. However, this system offers distinct advantages for developing regions:

| Feature Dimension | Google Environmental Insights | This UHI GIS Project |
| :--- | :--- | :--- |
| **Data Granularity** | Macro-level estimates (often broad grid scales). | **Hyper-local resolution** incorporating side-streets, DOHS parks, and bus stands. |
| **Ground-Truth Calibration** | Purely satellite-derived estimates without ground verification. | **Hybrid Data Fusion** combining Landsat/Sentinel LST with synthesized ground sensor coordinates. |
| **Update Frequency** | Refreshed annually or bi-annually in developing regions. | **Real-time API capabilities** allowing instant uploads of manual field sensor logs. |
| **Interactive Simulation** | Static viewing of green cover percentages. | **Interactive Regression Engine** allowing planners to simulate how expanding green canopy impacts localized heat. |
| **Local Customization** | Built on global standard presets, ignoring localized Bangladesh building materials. | **Context-specific parameters** (such as high-traffic metro hubs, local soil, and asphalt structures). |

---

## 🛠️ Technological Stack & Tools Used

To support easy cross-collaboration, the project integrates modern tools across the entire stack:
* **Frontend UI / Visualization:** HTML5, CSS3 (Glassmorphism & Neon Aesthetics), Bootstrap, **Leaflet.js** (GIS interactive map overlays), and **Chart.js** (Surface telemetry comparison charts).
* **Backend Processing:** **Python Flask** (routing architecture, local development server, and API dispatching).
* **Data Processing & Analytics:** **Pandas** (CSV database parsing), **NumPy** (matrix operations), and **Scikit-Learn** (Linear Regression engine).
* **Spatial/Satellite Assets:** Google Earth Engine (GEE), QGIS, USGS Earth Explorer (Landsat 8/9 thermal bands, Sentinel-2 optical bands).

---

## 🗺️ System Architecture & Workflow

**For a full, easy-to-understand breakdown of the project architecture, inputs/outputs, and detailed subgroup responsibilities, please read the [Project Architecture Guide](documentation/project_architecture.md).**

Understanding the data flow is key to smooth subgroup integration. The system routes spatial and environmental telemetry through three main stages:

```mermaid
graph TD
    A1[Satellite Telemetry: Landsat 8/9 & Sentinel-2] -->|Subgroup A: LST & NDVI Bands| B(GIS Processing: QGIS & GEE)
    A2[Ground Verification: 20-Point CSV] -->|Subgroup D: Coordinates & Sensor Readings| C(Flask API Gateway)
    B -->|GeoJSON Layers & Raster Outlines| C
    C -->|Subgroup B: Predictive Regression Script| D(Analytics & Performance metrics: R2, RMSE)
    D -->|Unified JSON Payloads| E(Sleek Leaflet.js & Chart.js Web Dashboard)
    E -->|Subgroup C: User Interaction Controls| F[Dynamic Dynamic FlyTo, Maps & Charts Re-rendering]
```

---

## 👥 Granular Subgroup Collaboration Blueprint

To prevent merge conflicts and define clear engineering boundaries, the work is divided into four highly-focused subgroups. Follow the instructions below for your specific team:

### 📡 Subgroup A: GIS & Remote Sensing Leads
* **Core Mandate:** Satellite data acquisition, thermal infrared processing, calculating NDVI, and exporting regional vector boundaries.
* **Granular Technical Role:**
  1. Download Landsat 8/9 thermal bands and calculate **Land Surface Temperature (LST)**.
  2. Compute the **Normalized Difference Vegetation Index (NDVI)**:
     $$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}$$
  3. Export boundary maps as optimized GeoJSON structures.
* **Workspace Boundaries & Deliverables:**
  - `data/geojson/placeholders.js`: Replace the dummy bounding vectors inside `REGION_PRESETS[region].geojson` with your processed GeoJSON layers.
  - Coordinate with **Subgroup C** to align map bounds (`bounds` property in the presets object) so overlays render correctly on top of the base tiles.

---

### 🧠 Subgroup B: Backend & Analytics Leads
* **Core Mandate:** Server-side environment setup, API endpoint routing, data fusion, and lightweight statistical predictive modeling.
* **Granular Technical Role:**
  1. Develop Python Flask routes to parse ground telemetry CSVs and spatial GeoJSON layers.
  2. Implement the core **Lightweight Predictive Regression Engine** to analyze the inverse relationship between green cover (NDVI) and heat retention:
     $$\text{Predicted Temperature} = \alpha - (\beta \times \text{NDVI})$$
  3. Compute error metrics: Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Coefficient of Determination ($R^2$ Score) to check fit quality.
* **Workspace Boundaries & Deliverables:**
  - `backend/app.py`: Maintain and extend endpoints. Ensure `/api/heat-data?region=<id>` responds instantly with the formatted JSON schema (see Data Contract).
  - `backend/models/analytics.py`: Refine the modeling calculations, optimize regression logic, or plug in advanced ML models (Random Forest, XGBoost) if implementing advanced features.

---

### 🎨 Subgroup C: Frontend & Map UI Leads
* **Core Mandate:** HTML5/CSS3 dashboard development, Leaflet.js interactive mapping integration, Chart.js statistics binding, and responsive glassmorphic styling.
* **Granular Technical Role:**
  1. Style the dashboard using modern web aesthetics (radial neon gradients, glassmorphism, responsive CSS grid grids).
  2. Wire up **Leaflet.js** to hard-center on Mirpur 12 and handle zoom levels.
  3. Bind Chart.js canvases to draw comparative analysis plots (Concrete vs. Vegetation surfaces).
  4. Write the dynamic client event listeners that fetch data on dropdown change and update the page via `map.flyTo()` and chart re-rendering.
* **Workspace Boundaries & Deliverables:**
  - `frontend/index.html`: Maintain structural layouts, SEO titles, and statistical HUD labels.
  - `frontend/css/styles.css`: Centralize design systems, cards, and micro-animations.
  - `frontend/js/app.js`: Manage AJAX fetch calls, map leaflet layer bindings, and Chart.js updates.

---

### ✍️ Subgroup D: Project Managers & Technical Writers (Your Group)
* **Core Mandate:** Baseline data synthesis, daily roadmap progress tracking, code freezing, report editing, and viva preparation.
* **Granular Technical Role:**
  1. Coordinate with all subgroups to ensure milestones are met according to the 12-day schedule.
  2. Manage and expand the **synthesized ground-truth verification database**.
  3. Author final report chapters (methodology, spatial analysis results) and format the presentation slides.
* **Workspace Boundaries & Deliverables:**
  - `data/environmental/mirpur12_ground_data.csv`: Update or expand the 20-point CSV dataset with actual physical parameters or expanded survey locations.
  - Keep project documentations stable and lead team viva simulation rehearsals.

---

## 📊 Shared Data Contract (API Schema)

To keep backend (Subgroup B) and frontend (Subgroup C) teams aligned, all data exchanged via `/api/heat-data?region=<region_id>` must adhere strictly to this schema:

```json
{
  "region": "mirpur12",
  "name": "Mirpur 12",
  "description": "Hyper-local baseline micro-analysis...",
  "analytics": {
    "alpha_intercept": 37.8331,
    "beta_slope": 13.3629,
    "avg_temp": 33.43,
    "r2_score": 0.9498,
    "rmse": 0.661,
    "mae": 0.5963,
    "peak_hotspot": {
      "name": "Ceramic Factory Area",
      "temp": 38.1,
      "lat": 23.8205,
      "lng": 90.3685
    },
    "peak_coolspot": {
      "name": "DOHS Lake Side Walkway",
      "temp": 28.5,
      "lat": 23.827,
      "lng": 90.363
    }
  },
  "records": [
    {
      "LocationID": 1,
      "LocationName": "Mirpur 12 Metro Station",
      "Latitude": 23.8248,
      "Longitude": 90.3621,
      "Temperature": 37.2,
      "SurfaceType": "Concrete",
      "NDVI": 0.08,
      "TrafficDensity": "High",
      "Time": "Afternoon"
    }
  ]
}
```

---

## 🏃 Quick-Start Development Guide

Follow these steps to spin up the codebase locally:

### 1. Set Up Your Environment
Ensure Python 3 is installed, then install the required lightweight data-science dependencies:
```bash
pip install flask pandas numpy scikit-learn --break-system-packages
```
*(Use `--break-system-packages` if developing on modern macOS with externally-managed Python environments, or activate a virtual environment).*

### 2. Launch the Development Server
From the root of the project directory, run:
```bash
python backend/app.py
```

### 3. Open the Dashboard
Navigate to:
```text
http://127.0.0.1:5000/
```
The interface will boot up instantly, default-centered over **Mirpur 12**, displaying real-time mapping layers, statistical charts, and regression metrics.
