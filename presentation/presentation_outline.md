# 📊 UHI GIS Mapping & Predictive ML Analytics Presentation Outline

This document provides the PowerPoint slide outline and Viva rehearsal questions for Group 4.

---

## 📈 PowerPoint Slide Layout

### **Slide 1: Title Page**
* **Title:** Development of a Scalable GIS Mapping and Predictive Analysis Framework for Urban Heat Island (UHI) Monitoring
* **Sub-Title:** A Micro-Analysis of Mirpur 12 with Regional Extension across Bangladesh
* **Details:** Course: Environmental Science (CSE 3-2), Group 4, BUP
* **Members:** Sayed, Nusair, Punam, Nafiz, Spondon, Rushafi, Ajwad, Sabbir

### **Slide 2: Project Purpose & Core Problems**
* **Urban Challenges:** Concrete replacements of vegetation canopy trap solar radiation, elevating city core temperatures by 3–6°C.
* **Problem Statement:** Macro weather stations fail to capture street-level hotspots or micro-climate variations.
* **Our Solution:** A hybrid pipeline fusing remote sensing Landsat parameters with ground sensor verification, evaluated via ML models.

### **Slide 3: System Architecture & Data Flow**
* **Ingestion Layer:** Ingests ground observations (`field_data/`) and regional coordinate boundaries.
* **Calculation Engine:** Computes NDVI (vegetation canopy ratio) and LST (land surface temperature).
* **Plotting & Mapping:** Generates Seaborn regressions and interactive Leaflet.js HTML heatmaps.
* **AI/Predictive Layer:** Fits Linear, Decision Tree, and Random Forest regressions.
* **Web UI:** Interactive glassmorphic dashboard loading data dynamically.

### **Slide 4: Chapter 3 & 4 Results: Mirpur 12 Baseline**
* **Findings:** Ingested 20 coordinate inspection sites. 
* **Hotspots vs. Coolspots:**
  - *Hottest:* Mirpur-12 Metrorail Station (Concrete, high traffic) - **32.5°C**
  - *Coolest:* Mirpur-12 Kids Park (Vegetation Canopy) - **26.5°C**
* **Key Proof:** Concrete corridors demonstrate up to 6°C higher surface heat than shaded park regions.

### **Slide 5: Predictive Modeling & Mathematical Results**
* **Vectorized Formulations:**
  - NDVI Formula: $\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}$
  - Linear Model: $\text{Temperature} = 32.41 - (6.95 \times \text{NDVI})$
* **Model Fits (R² Scores):**
  - Linear Regression: **0.8592** (Strong negative correlation!)
  - Decision Tree: **0.9023**
  - Random Forest: **0.8954**

### **Slide 6: Regional Scaling ( Dhaka, Sylhet, Rajshahi, Chittagong )**
* **Dhaka Met Area:** Intense heat retention due to high concrete/low canopy.
* **Sylhet Division:** Milder temperatures driven by green tea gardens and evapotranspiration.
* **Rajshahi Division:** Dry heating peaks due to bare soil and summer heatwaves.
* **Chittagong Division:** Coastal cooling breezes offset industrial harbor heat belts.

### **Slide 7: Conclusion & Policy Recommendations**
* **Deliverables Done:** Fully operational GIS heatmap suite, predictive regressors, and Flask dashboard.
* **Recommendations:** Deploy shaded green roofs and reflective pavements directly at key transit hotspots (e.g. Mirpur 12 Metrorail Station).

---

## 🎙️ Viva / Interview Preparation Q&A

1. **Q: What is the Urban Heat Island (UHI) effect?**
   * *A:* It is a phenomenon where urban areas experience significantly higher surface and air temperatures than adjacent rural surroundings, caused by heat absorption in building concrete and asphalt pavements, heat emissions from traffic, and lack of cooling green canopy.

2. **Q: How does the NDVI formula gauge vegetation?**
   * *A:* NDVI compares Near-Infrared (NIR) light (heavily reflected by green leaves) and Red light (absorbed by plant chlorophyll). The values range between -1.0 and +1.0. Dense vegetation has high NDVI (typically > 0.5), while concrete features low NDVI (< 0.15).

3. **Q: What is the difference between Air Temperature and Land Surface Temperature (LST)?**
   * *A:* Air temperature measures atmospheric heat 1.5–2 meters above the ground. LST measures the skin temperature of the Earth's surface (e.g., concrete pavement temperature), which is directly affected by sunlight and surface material thermal properties, often making it much hotter than air temperature.

4. **Q: Why are multiple ML regression models implemented?**
   * *A:* Linear Regression captures the baseline rate of temperature drop per unit increase of green canopy (the slope $\beta$). Decision Trees and Random Forests analyze nonlinear patterns, like localized shading and microclimate humidity thresholds.
