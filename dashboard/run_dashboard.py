import os
import sys

# Ensure the backend directory is in the system path to run the app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from app import app

if __name__ == "__main__":
    print("=" * 65)
    print("🚀  URBAN HEAT ISLAND GIS ANALYTICS DASHBOARD - LAUNCHING SERVER  🚀")
    print("=" * 65)
    print(" -> Running on local address: http://127.0.0.1:5000")
    print(" -> Serving pre-calculated datasets from 'field_data/'")
    print(" -> Serving ML regression indices from 'ml_models/'")
    print(" -> Serving geospatial maps from 'gis_maps/'")
    print("-" * 65)
    app.run(debug=True, port=5000)
