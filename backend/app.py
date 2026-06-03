from flask import Flask, jsonify, request, send_from_directory
import os
import json
import pandas as pd
import numpy as np

app = Flask(__name__, static_folder="../frontend", static_url_path="")

# Root path of the codebase workspace
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REGIONAL_DESCRIPTIONS = {
    "mirpur12": "Hyper-local baseline micro-analysis mapping 20 ground sensor coordinates.",
    "dhaka_all": "Dense urban environment with wide surface heat dispersion.",
    "sylhet": "High green canopy ratios and tea estate borders leading to low average heat retention.",
    "rajshahi": "High dry summer temperatures and heavy pavement-retained heat profiles.",
    "chittagong": "Coastal cooling winds offset by heavy industrial concrete hubs."
}

# Serve the satellite_data folder statically to the frontend
@app.route("/satellite_data/<path:filename>")
def serve_satellite_data(filename):
    return send_from_directory(os.path.join(BASE_DIR, "satellite_data"), filename)

# Serve the field_data folder statically if needed
@app.route("/field_data/<path:filename>")
def serve_field_data(filename):
    return send_from_directory(os.path.join(BASE_DIR, "field_data"), filename)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/heat-data")
def get_heat_data():
    region = request.args.get("region", "mirpur12")
    
    csv_filename = f"{region}_data_calculated.csv"
    csv_path = os.path.join(BASE_DIR, "field_data", csv_filename)
    
    json_filename = f"{region}_reg_metrics.json"
    json_path = os.path.join(BASE_DIR, "ml_models", json_filename)
    
    if not os.path.exists(csv_path) or not os.path.exists(json_path):
        return jsonify({"error": f"Data or metrics not pre-computed for region: {region}. Run main.py first."}), 400
        
    try:
        # Load records from calculated CSV
        df = pd.read_csv(csv_path)
        # Convert NaN values to None for clean JSON serialization
        df = df.replace({np.nan: None})
        records = df.to_dict(orient="records")
        
        # Load pre-trained metrics JSON
        with open(json_path, "r", encoding="utf-8") as f:
            analytics = json.load(f)
            
        return jsonify({
            "region": region,
            "name": analytics.get("region_name", region.capitalize()),
            "description": REGIONAL_DESCRIPTIONS.get(region, "Thermal GIS mapping layer."),
            "analytics": analytics,
            "records": records
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
