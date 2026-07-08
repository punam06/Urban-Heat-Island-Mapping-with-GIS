<div align="center">
  <h1>🌡️ Urban Heat Island (UHI) Mapping & Predictive GIS Analytics System</h1>
  <p><strong>A modular, high-end spatial analytics platform for micro and macro urban temperature forecasting.</strong></p>
  
  [![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen.svg)](https://your-live-url-here.com)
  [![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
  [![Flask](https://img.shields.io/badge/Flask-Backend-black.svg)](https://flask.palletsprojects.com/)
  [![Leaflet](https://img.shields.io/badge/Leaflet-GIS-lightgreen.svg)](https://leafletjs.com/)
</div>

---

## 📖 About The Project

As cities grow, they become significantly warmer than their rural surroundings—a phenomenon known as the **Urban Heat Island (UHI) effect**. This poses severe health risks and increases energy consumption. 

We built the **Urban Heat Island Mapping & Analytics System** to provide actionable, hyper-local intelligence for urban planners and climate researchers. Focused initially on **Mirpur 12** as our ground-truth baseline, the system dynamically scales to entire divisions in Bangladesh (Dhaka, Sylhet, Rajshahi, Chittagong). It fuses remote sensing satellite data with ground-truth sensors to process thermal anomalies, predict future temperatures using machine learning, and recommend sustainable urban interventions like tree plantation and green roofs.

### ✨ Key Features

- **Hyper-local Micro-Analysis**: Maps 20+ baseline ground-truth coordinates using field sensors and satellite data.
- **Predictive ML Modeling**: Forecasts 1, 3, and 5-year regional temperatures using Linear Regression and Hybrid ML models.
- **Heat Risk Index (HRI)**: Calculates composite heat risk scores based on Land Surface Temperature (LST) and Normalized Difference Vegetation Index (NDVI).
- **Climate Resilience Scoring**: Ranks regions from 0-100 based on their ability to withstand heat anomalies.
- **Green Infrastructure Simulation**: Simulates the cooling impact of +10%, +20%, and +30% vegetation increases.
- **Automated Report Generation**: Exports comprehensive JSON/PDF environmental intelligence reports.
- **Interactive Glassmorphic Dashboard**: A stunning Leaflet-powered GIS frontend for visualizing hotspots and metrics in real time.

---

## 🚀 Live Demo

**Check out the live interactive dashboard here:** 
👉 **[Urban Heat Island Analytics Dashboard](https://your-live-url-here.com)** 

*(Please update the placeholder URL with your actual deployment link)*

---

## 🛠️ How We Built It (Tech Stack)

Our architecture is split into a robust Python data pipeline and an interactive web dashboard.

* **Data Processing & Analytics:** Python, Pandas, NumPy, Statsmodels
* **Machine Learning:** Scikit-Learn
* **Geospatial Mapping:** Folium, Leaflet.js
* **Backend API:** Flask
* **Frontend Visualization:** HTML5, Custom CSS (Glassmorphism), Chart.js, Plotly

---

## 📂 Project Architecture

```text
Urban-Heat-Island-Mapping-with-GIS/
├── main.py                             # Master entry-point running the entire pipeline
├── dashboard/                          # Flask Web Server Runner
├── backend/                            # REST API serving analytics and ML predictions
├── frontend/                           # Interactive Glassmorphic Analytics Layout
├── pipeline/                           # Python Data Logic (Preprocessing, ML, GIS, Reports)
├── field_data/                         # Ground-truth datasets & CSV databases
├── satellite_data/                     # Remote sensing preset configurations
├── gis_maps/                           # Generated spatial layers & heatmaps
├── ml_models/                          # Serialized AI model accuracies and parameters
└── documentation/                      # Academic reports and architectural workflows
```

---

## 🌐 API Ecosystem & Endpoints

Our backend exposes a rich set of REST APIs for decision support systems:

* **`/api/heat-data`** - Core spatial data pipeline contract.
* **`/api/heat-risk`** - Composite HRI scoring and risk level categorization.
* **`/api/predict-temperature`** - ML-driven regional temperature forecasting.
* **`/api/recommendations`** - Green-infrastructure intervention plans.
* **`/api/climate-score`** - 0-100 resilience scoring based on environmental factors.
* **`/api/alerts`** - Heatwave threshold monitoring.
* **`/api/simulate-green-growth`** - Models hypothetical vegetation increases.

---

## 🏃 Quick Start / Local Setup

Follow these steps to run the pipeline and dashboard locally:

### 1. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn folium scikit-learn flask plotly statsmodels --break-system-packages
```

### 2. Preprocess Data & Calculate Indices
Run the data prep scripts:
```bash
python scripts/preprocess_mirpur_data.py
python scripts/calculate_mirpur_indices.py
```

### 3. Run the Master Pipeline
Execute the master orchestration script:
```bash
python main.py
```

### 4. Generate Ground Verification Images
```bash
python scripts/generate_ground_verification_images.py
```

### 5. Launch the Web Dashboard
Start the Flask web server:
```bash
python dashboard/run_dashboard.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to view the interactive dashboard.

---

## 🏆 Accomplishments & What's Next

- **Fusion of Micro and Macro Data**: We successfully combined high-resolution ground-truth sensor data with large-scale satellite LST readings.
- **Actionable Insights**: Rather than just displaying heatmaps, our Environmental Decision Support System (EDSS) provides concrete policy recommendations like tree planting priorities.
- **Future Integration**: We plan to integrate shapefile analytics via Geopandas, live SMS heatwave alerts via Twilio, and more complex hybrid forecasting models.

---
<div align="center">
  <p>Built for a sustainable and climate-resilient future. 🌍</p>
</div>
