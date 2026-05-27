# 🏗️ Project Architecture & Workflow Guide

Welcome to the Urban Heat Island (UHI) Mapping Project! This document serves as the master architectural blueprint for our entire software ecosystem. It explains exactly how our system is engineered, how data flows from spatial satellites down to the web client, and most importantly, defines the rigid, highly-detailed responsibilities for each of the four subgroups. 

---

## 🎯 1. Project Purpose, Inputs & Outputs

**The Purpose:** 
Cities are rapidly heating up because concrete infrastructure absorbs solar radiation, while natural green canopies and water bodies act as cooling sinks. The core objective of this project is to develop a dynamic, web-based environmental dashboard that provides high-resolution micro-analysis of neighborhoods (starting with Mirpur 12). By analyzing this data, urban planners can mathematically predict how planting trees (increasing NDVI) will directly lower localized surface temperatures, aiding in sustainable, climate-resilient city planning.

* **📥 Primary Inputs (Data Sources):** 
  * Satellite rasters (Landsat 8/9 and Sentinel-2) detailing Land Surface Temperature (LST) and Normalized Difference Vegetation Index (NDVI) bands.
  * Our synthesized, high-fidelity ground-verification database (`mirpur12_ground_data.csv`), which includes exact GPS coordinates, estimated temperature ranges, environmental surface types (Concrete, Asphalt, Vegetation), and linked real-world photographic evidence.
* **💻 Processing Engine (The Backend):** 
  * A Python-powered Flask server utilizing the Pandas library to parse environmental data and the Scikit-Learn library to execute a Linear Regression algorithm. This mathematically determines the inverse correlation between green cover and heat retention.
* **📤 The Output (User Interface):** 
  * A highly interactive, glassmorphic web application built with Leaflet.js and Chart.js. The dashboard renders thermal hotspots dynamically over map tiles, allowing stakeholders to visually inspect heat disparities block-by-block and review statistical predictions in real time.

---

## 👥 2. Subgroup Responsibilities & Technical Workflows

To ensure our project scales properly without causing Git merge conflicts, the workload is strictly partitioned among four subgroups. Each group has distinct files to edit, specific API behaviors to manage, and strict deliverables to meet.

### 🌍 Subgroup A: GIS & Remote Sensing (The Spatial Engineers)

**Primary Directive & Workflow:** 
Subgroup A acts as the foundational data provider for the entire architectural stack. Your primary responsibility is to harvest raw satellite imagery from platforms like USGS Earth Explorer and Google Earth Engine. You must focus on extracting the Thermal Infrared Sensor (TIRS) bands to calculate Land Surface Temperature (LST) and the Near-Infrared (NIR)/Red bands to compute the Normalized Difference Vegetation Index (NDVI). Without your accurate spatial data, the backend algorithms have no baseline to run predictions on.

**File Access & Modifications:**
You will operate exclusively within the `data/geojson/` directory. Your main target file is `placeholders.js`. Currently, this file contains empty, dummy bounding boxes representing Mirpur 12 and other divisional areas. Your job is to replace these dummy JSON blocks with highly accurate, multi-layered GeoJSON structures that represent actual thermal gradients. You will not touch the Python backend or the frontend CSS; your strict boundary is spatial data formulation.

**Technical Execution & Code Changes:**
You will run heavy geoprocessing tasks using QGIS or Python's Rasterio library on your local machines. Once you have calculated the heat maps, you must vectorize these raster files into GeoJSON polygons. You will then open `placeholders.js` and paste your massive array of coordinates into the `REGION_PRESETS` object. You must ensure that each polygon feature has an `intensity` property (ranging from 0.0 to 1.0) so the frontend Leaflet engine knows exactly how dark to shade the red and green overlays. 

**Database & API Intersections:**
While you do not write the Flask API, you control the data that the API ultimately serves. You must communicate constantly with Subgroup C (Frontend) to ensure that the coordinate bounds you generate match the base tile limits they are using in Leaflet. If your GeoJSON structure is malformed, the API endpoint will crash when it attempts to serialize the spatial data, resulting in a blank map on the dashboard.

**Deliverables & Final Output:**
By the end of Phase 3, you must deliver fully functional, multi-layered GeoJSON representations for the Entire Dhaka Metropolitan Area, Sylhet, Rajshahi, and Chittagong. These must be cleanly nested within the `data/geojson/` directory. You will also supply Subgroup D with a high-level summary of your processing methodology so they can accurately draft Chapter 3 of the final academic report.

### ⚙️ Subgroup B: Backend & Analytics (The Server & Logic Engineers)

**Primary Directive & Workflow:** 
Subgroup B is the absolute brain of this software. You are responsible for engineering the server infrastructure that bridges the static data files (CSVs and GeoJSONs) with the live web application. Your workflow involves setting up a local web server, reading raw data files from the file system, cleaning that data in memory using Pandas, and running statistical machine-learning operations (Linear Regression) to dynamically calculate the relationship between temperature and vegetation. 

**File Access & Modifications:**
You have total dominion over the `backend/` directory. Your primary files are `app.py` (the Flask server router) and `models/analytics.py` (the statistical calculation engine). You must also manage `requirements.txt` to ensure all pip dependencies (like `flask`, `pandas`, `numpy`, and `scikit-learn`) are properly documented for the team. You are strictly forbidden from altering the frontend UI files, as your job is solely to deliver clean data to the web interface.

**Technical Execution & Code Changes:**
Inside `app.py`, you will write the routing logic using the `@app.route('/api/heat-data')` decorator. Your code must intercept HTTP GET requests, read the `region` parameter from the URL, and load the corresponding data. Inside `analytics.py`, you will write Python functions that take the raw CSV rows (containing Temperature and NDVI columns), feed them into a linear regression model, and extract the Alpha (Intercept), Beta (Slope), $R^2$ Score, and Root Mean Squared Error (RMSE). You must wrap all these calculations into a unified Python dictionary.

**API Endpoints & Database Connection:**
You are the creators of the RESTful API. You do not use a traditional SQL database; instead, you treat the `data/` directory (CSVs and JSONs) as a flat-file database. Your main endpoint, `/api/heat-data?region=<region_id>`, must be bulletproof. It must serialize the Pandas dataframe and the regression metrics into a strict JSON payload (as defined in the README Data Contract). If the frontend sends a bad region ID, your API must gracefully handle the error and return a 404 response rather than crashing the Python server.

**Deliverables & Final Output:**
You must deliver a highly stable, lightning-fast Flask server capable of processing mathematical regressions in under 100 milliseconds. Your API must correctly output the equations required for the frontend to update the "Live Regression Engine" widget. Finally, you will provide Subgroup D with a complete breakdown of the mathematical formulas you used so they can include them in the technical thesis.

### 🎨 Subgroup C: Frontend & Map UI (The Client-Side Developers)

**Primary Directive & Workflow:** 
Subgroup C is responsible for the entire user experience (UX) and visual aesthetic of the project. You must take the raw, invisible JSON data supplied by Subgroup B's API and transform it into a beautiful, interactive, and responsive web dashboard. Your workflow involves designing modern UI elements, managing asynchronous JavaScript data fetching (AJAX), and configuring complex third-party visualization libraries like Leaflet.js for mapping and Chart.js for statistical plotting.

**File Access & Modifications:**
You control the entire `frontend/` directory. You will work heavily inside `index.html` to build the structural skeleton of the dashboard. You will write advanced styling rules in `css/styles.css` to achieve the requested "premium glassmorphic" aesthetic, utilizing neon accents, smooth gradients, and micro-animations. Your most critical file is `js/app.js`, where all the dynamic client-side logic lives. You should not touch the Python backend or the raw data files.

**Technical Execution & Code Changes:**
Inside `app.js`, you will write `async/await` fetch functions that ping Subgroup B's `/api/heat-data` endpoint. Once the data arrives, you must write JavaScript to dynamically update the DOM (e.g., changing the text of the "Average Temp" widget). For the map, you will utilize the Leaflet `L.circleMarker` API to plot the CSV coordinates, binding custom HTML popups that display the location's name, temperature, and dynamically loaded images via `<img src="images/...">`. You will also write the logic to dynamically re-render the Chart.js canvases when the user switches regions.

**API Integration & Asset Management:**
You are the exclusive consumers of the backend API. You must ensure your JavaScript gracefully handles API loading states and errors (e.g., showing a notification if the Python server is offline). Furthermore, you are responsible for managing the `frontend/images/` directory. You must ensure that the image paths returned by the CSV/API accurately resolve to the physical image files on the web server, otherwise users will see broken image links in their map popups.

**Deliverables & Final Output:**
Your final deliverable is a stunning, bug-free, zero-lag interactive dashboard. The UI must be fully responsive, scaling perfectly on both large desktop monitors and smaller laptops. You must successfully implement smooth map animations (using `map.flyTo()`) when transitioning between Mirpur 12, Dhaka, and Sylhet. You will work with Subgroup D to capture high-resolution screenshots of your finished dashboard for the final project presentation.

### 📝 Subgroup D: Project Managers & Technical Writers (The Directors)

**Primary Directive & Workflow:** 
Subgroup D serves as the architectural glue that holds the entire project together. Your job is dual-purposed: you are the central database architects who synthesize the ground-truth testing data, and you are the technical writers responsible for all academic documentation. Your workflow involves overseeing the 12-day agile sprint, ensuring all other subgroups meet their deadlines, validating that the API contracts are honored, and translating complex Python/GIS jargon into professional thesis chapters.

**File Access & Modifications:**
You have the most cross-functional access. You manage the physical flat-file database located at `data/environmental/mirpur12_ground_data.csv`. You are also in charge of the `documentation/` folder (including this `project_architecture.md` file) and the `Report writting/ESL Group 4 Report.md` academic thesis. You must also routinely audit the `README.md` file to ensure the onboarding instructions remain accurate as the codebase evolves.

**Technical Execution & Code Changes:**
While you do not write Python or JavaScript, you write the critical data schemas. You must carefully expand the CSV files to include exact GPS coordinates (Latitude/Longitude), environmental profiles (Concrete vs Vegetation), and precise string mappings for image filenames. If you make a typo in the CSV (e.g., writing "Bup.jpeg" instead of "BUP.jpeg"), you will break Subgroup C's image rendering. Your data entry must be flawless and mathematically sound so Subgroup B's regression algorithms output realistic numbers.

**Collaboration & Database Generation:**
Because physical field surveys were skipped due to time constraints, you are responsible for synthetically generating the "ground verification" database. You must carefully curate data points that reflect reality (e.g., ensuring a busy bus depot has a higher temperature and lower NDVI than a lakeside park). You must also coordinate daily stand-up meetings to ensure Subgroup A's GeoJSON bounds align with your CSV coordinates, and that Subgroup B is returning the exact JSON structure Subgroup C expects.

**Deliverables & Final Output:**
You will deliver a flawlessly formatted, highly detailed academic thesis (the `ESL Group 4 Report.md`) ready for submission. You will author comprehensive Regional Geographic Summaries explaining the climate dynamics of different cities. Finally, you will design the final PowerPoint presentation, compile the backup demonstration video, and lead the team through a simulated Viva rehearsal to ensure everyone can defend the project architecture to the professors.

---

## 🗺️ 3. System Architecture & Workflow Diagrams

Here is how the data flows from the satellite/surveyors all the way to the user's screen.

```mermaid
graph TD
    %% Define Styles
    classDef data fill:#2b3a42,stroke:#4a90e2,stroke-width:2px,color:#fff;
    classDef backend fill:#1a252c,stroke:#e67e22,stroke-width:2px,color:#fff;
    classDef frontend fill:#2c3e50,stroke:#2ecc71,stroke-width:2px,color:#fff;

    %% Data Layer
    subgraph Data Sources (Subgroups A & D)
        A[Satellite GeoJSON Layers<br>(Subgroup A)]:::data
        B[Ground CSV Database & Images<br>(Subgroup D)]:::data
    end

    %% Backend Layer
    subgraph Python Backend API (Subgroup B)
        C[Pandas Data Parser]:::backend
        D[Scikit-Learn Regression Engine]:::backend
        E[Flask REST API Server]:::backend
        C --> D
        D --> E
    end

    %% Frontend Layer
    subgraph Client Web Dashboard (Subgroup C)
        F[Leaflet.js GIS Map Engine]:::frontend
        G[Chart.js Statistical Canvases]:::frontend
        H[Glassmorphic HTML/CSS UI]:::frontend
    end

    %% Flow Connections
    A -.->|Injects Map Boundaries| F
    B -->|Provides Telemetry| C
    E ==>|Serves Unified JSON Schema| F
    E ==>|Serves Regression Variables| G
    F --- H
    G --- H
```

### 🔄 The Step-by-Step API Workflow:
1. **The Request:** A user clicks "Sylhet" on the dashboard dropdown. Subgroup C's JavaScript sends an asynchronous `GET` request to `http://127.0.0.1:5000/api/heat-data?region=sylhet`.
2. **The Database Read:** Subgroup B's Flask server intercepts the request, maps "sylhet" to the correct CSV flat-file, and loads it into a Pandas DataFrame.
3. **The Analytics Crunch:** The server passes the DataFrame to `analytics.py`, which runs the regression algorithms to compute the precise environmental correlations.
4. **The JSON Delivery:** The Flask server bundles the statistical metrics, the individual coordinate rows, and image paths into a single JSON response and sends it back to the client.
5. **The Visual Render:** Subgroup C's JavaScript parses the JSON, updates the Chart.js graphs, and triggers Leaflet.js to plot the thermal hotspots and bind the HTML image popups to the map markers.

---

## 📂 4. Project Structure & File Architecture

This is how our code is physically organized inside the repository. This strict modularity guarantees that Subgroups will not interfere with each other's files during parallel development.

```text
Urban-Heat-Island-Mapping-with-GIS/
│
├── README.md                           # Master instructions, stack overview, and setup guide
│
├── documentation/                      # 📝 SUBGROUP D'S WORKSPACE (Technical Writing)
│   ├── project_architecture.md         # THIS FILE: The master workflow and responsibility guide
│   └── regional_summaries_report.md    # The theoretical breakdown of regional thermal profiles
│
├── Report writting/                    # 📝 SUBGROUP D'S WORKSPACE (Academic Deliverables)
│   └── ESL Group 4 Report.md           # The final, formatted 6-chapter thesis document
│
├── data/                               # 🌍 SUBGROUP A & D'S WORKSPACE (The Database)
│   ├── environmental/
│   │   └── mirpur12_ground_data.csv    # The core flat-file database of temps, coords, and images
│   └── geojson/
│       └── placeholders.js             # The spatial bounding boxes provided by Subgroup A
│
├── backend/                            # ⚙️ SUBGROUP B'S WORKSPACE (The API Server)
│   ├── app.py                          # The Flask routing application and primary server file
│   ├── requirements.txt                # Dependency list for pip (flask, pandas, scikit-learn)
│   └── models/
│       └── analytics.py                # The mathematical regression engine and data parser
│
└── frontend/                           # 🎨 SUBGROUP C'S WORKSPACE (The Client UI)
    ├── index.html                      # The structural DOM and widget layout
    ├── css/
    │   └── styles.css                  # The glassmorphic, responsive styling definitions
    ├── js/
    │   └── app.js                      # The AJAX controllers, Leaflet maps, and Chart.js logic
    └── images/
        ├── BUP.jpeg                    # The physical image assets directly referenced by the CSV
        └── Alubdi...jpeg               # Additional ground-truth photographic evidence
```
