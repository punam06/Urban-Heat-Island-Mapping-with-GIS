import os
import matplotlib.pyplot as plt
import seaborn as sns

def generate_visualizations(df, meta, graphs_dir, maps_dir):
    """
    Generates Matplotlib comparative scatter plots and an interactive Leaflet.js
    HTML heatmap overlay centered over the selected region.
    """
    region = meta["region"]
    region_name = meta["name"]
    
    # 1. Generate Matplotlib Comparative Plot
    plt.figure(figsize=(8, 5))
    sns.set_theme(style="darkgrid")
    
    # Custom neon aesthetics
    scatter = sns.scatterplot(
        data=df, 
        x="NDVI", 
        y="Temperature", 
        hue="SurfaceType",
        palette={"Concrete": "#e74c3c", "Asphalt": "#f39c12", "Vegetation": "#2ecc71", "Bare Soil": "#9b59b6", "Water Body": "#3498db", "Mixed": "#7f8c8d"},
        s=100,
        alpha=0.8
    )
    
    # Linear trendline
    sns.regplot(
        data=df, 
        x="NDVI", 
        y="Temperature", 
        scatter=False, 
        color="#3498db", 
        line_kws={"linestyle": "--", "linewidth": 2}
    )
    
    plt.title(f"Thermal Disparity: Temperature vs. NDVI ({region_name})", fontsize=12, fontweight="bold")
    plt.xlabel("Normalized Difference Vegetation Index (NDVI)", fontsize=10)
    plt.ylabel("Temperature (°C)", fontsize=10)
    plt.legend(title="Surface Type")
    plt.tight_layout()
    
    graph_filename = f"{region}_concrete_vs_veg_scatter.png"
    graph_path = os.path.join(graphs_dir, graph_filename)
    plt.savefig(graph_path, dpi=150)
    plt.close()
    
    # 2. Generate Interactive Leaflet.js HTML Map
    # We will generate a self-contained premium HTML file using a beautiful template
    lat_center = float(df["Latitude"].mean())
    lng_center = float(df["Longitude"].mean())
    
    # Build JavaScript markers array
    markers_js = ""
    for idx, row in df.iterrows():
        name = row["LocationName"].replace("'", "\\'")
        temp = row["Temperature"]
        surface = row["SurfaceType"]
        ndvi = row["NDVI"]
        lat = row["Latitude"]
        lng = row["Longitude"]
        traffic = row.get("TrafficDensity", "N/A")
        
        # Select color matching the surface profile
        color_map = {
            "Concrete": "#e74c3c",
            "Asphalt": "#f39c12",
            "Vegetation": "#2ecc71",
            "Bare Soil": "#9b59b6",
            "Water Body": "#3498db",
            "Mixed": "#7f8c8d"
        }
        color = color_map.get(surface, "#7f8c8d")
        
        markers_js += f"""
        L.circle([{lat}, {lng}], {{
            color: '{color}',
            fillColor: '{color}',
            fillOpacity: 0.65,
            radius: 80
        }}).addTo(map).bindPopup(`
            <div style="font-family: 'Outfit', sans-serif; min-width: 180px;">
                <h4 style="margin: 0 0 5px 0; color: #2c3e50; border-bottom: 2px solid #ecf0f1; padding-bottom: 3px;">${name}</h4>
                <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
                    <tr><td><b>Temperature:</b></td><td style="color: {color};"><b>{temp}°C</b></td></tr>
                    <tr><td><b>Surface Type:</b></td><td>{surface}</td></tr>
                    <tr><td><b>NDVI Index:</b></td><td>{ndvi}</td></tr>
                    <tr><td><b>Traffic Density:</b></td><td>{traffic}</td></tr>
                </table>
            </div>
        `);
        """

    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>UHI GIS Hotspot Overlay - {region_name}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body, html {{ margin: 0; padding: 0; height: 100%; font-family: 'Outfit', sans-serif; background-color: #0f172a; color: #f8fafc; overflow: hidden; }}
        #header {{
            position: absolute; top: 15px; left: 15px; z-index: 1000;
            background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(10px);
            padding: 15px 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);
            max-width: 320px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }}
        #header h2 {{ margin: 0 0 5px 0; font-size: 18px; font-weight: 700; color: #38bdf8; }}
        #header p {{ margin: 0; font-size: 12px; color: #94a3b8; line-height: 1.4; }}
        #legend {{
            position: absolute; bottom: 25px; right: 25px; z-index: 1000;
            background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(10px);
            padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 10px 25px rgba(0,0,0,0.5); font-size: 12px;
        }}
        .legend-title {{ font-weight: 600; margin-bottom: 8px; color: #38bdf8; text-transform: uppercase; font-size: 10px; letter-spacing: 1px; }}
        .legend-item {{ display: flex; align-items: center; margin-bottom: 5px; }}
        .legend-color {{ width: 14px; height: 14px; border-radius: 30%; margin-right: 8px; }}
        #map {{ width: 100%; height: 100%; }}
        .leaflet-bar a {{ background-color: rgba(15, 23, 42, 0.9) !important; color: #f8fafc !important; border: 1px solid rgba(255,255,255,0.1) !important; }}
    </style>
</head>
<body>

    <div id="header">
        <h2>🌡️ UHI Overlay: {region_name}</h2>
        <p>{meta["description"]}</p>
    </div>

    <div id="legend">
        <div class="legend-title">Surface Profile & Heat</div>
        <div class="legend-item"><div class="legend-color" style="background: #e74c3c;"></div>Concrete (High Heat)</div>
        <div class="legend-item"><div class="legend-color" style="background: #f39c12;"></div>Asphalt (Medium-High)</div>
        <div class="legend-item"><div class="legend-color" style="background: #9b59b6;"></div>Bare Soil (Medium)</div>
        <div class="legend-item"><div class="legend-color" style="background: #2ecc71;"></div>Vegetation (Cool Zone)</div>
        <div class="legend-item"><div class="legend-color" style="background: #3498db;"></div>Water Body (Cool Sink)</div>
        <div class="legend-item"><div class="legend-color" style="background: #7f8c8d;"></div>Mixed/Other</div>
    </div>

    <div id="map"></div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        // Initialize Leaflet Map centered over regional center
        const map = L.map('map', {{
            zoomControl: true,
            maxZoom: 18,
            minZoom: 10
        }}).setView([{lat_center}, {lng_center}], 14);

        // Standard CartoDB Dark Matter tile layer for neon aesthetic
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        }}).addTo(map);

        // Inject computed regional hotspot circle layers
        {markers_js}

    </script>
</body>
</html>
"""
    
    map_filename = f"{region}_heatmap.html"
    map_path = os.path.join(maps_dir, map_filename)
    with open(map_path, "w", encoding="utf-8") as f:
        f.write(html_template)
        
    return graph_path, map_path

def plot_macro_temporal_evolution(df, graphs_dir):
    """
    Section 1: Macro-Temporal Microclimate Evolution.
    Plots Heat Index Matrix and Wind Speed Distribution.
    """
    import pandas as pd
    if 'Year_Month' not in df.columns:
        if 'Observation_Time' in df.columns:
            dt_col = pd.to_datetime(df['Observation_Time'])
            df['Year_Month'] = dt_col.dt.strftime('%Y-%m')
            
    evolution_data = df.groupby(['Location_Label', 'Year_Month']).agg({
        'heat_index_C': 'mean',
        'wind_speed_kmh': 'mean'
    }).reset_index()

    # Determine sorting based on a simplified logic or average heat
    loc_avg_heat = evolution_data.groupby('Location_Label')['heat_index_C'].mean().sort_values().index.tolist()
    
    pivot_heat = evolution_data.pivot(index='Location_Label', columns='Year_Month', values='heat_index_C').reindex(loc_avg_heat)
    pivot_wind = evolution_data.pivot(index='Location_Label', columns='Year_Month', values='wind_speed_kmh').reindex(loc_avg_heat)

    fig, axes = plt.subplots(2, 1, figsize=(24, 14), sharex=True)
    sns.set_theme(style="white")

    sns.heatmap(pivot_heat, cmap="YlOrRd", cbar_kws={'label': 'Mean Heat Index (°C)', 'orientation': 'horizontal', 'pad': 0.05}, ax=axes[0], xticklabels=True)
    axes[0].set_title("A. Macro-Temporal Microclimate Evolution: Heat Index Across Mirpur (2020 - 2026)", fontsize=16, fontweight='bold', pad=15)
    axes[0].set_ylabel("Urban Morphology Configuration", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("")

    sns.heatmap(pivot_wind, cmap="YlGnBu", cbar_kws={'label': 'Mean Wind Speed (km/h)', 'orientation': 'horizontal', 'pad': 0.05}, ax=axes[1], xticklabels=True)
    axes[1].set_title("B. Convective Cooling Dynamics: Wind Speed Distribution Over Time", fontsize=16, fontweight='bold', pad=15)
    axes[1].set_ylabel("Urban Morphology Configuration", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Timeline Evolution (Year - Month Grouped Cycles)", fontsize=12, fontweight='bold')

    for ax in axes:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=9)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10, fontweight='bold')

    plt.tight_layout()
    graph_path = os.path.join(graphs_dir, "macro_temporal_evolution.png")
    plt.savefig(graph_path, dpi=150)
    plt.close()
    return graph_path

def plot_longitudinal_thermal_profile(df, graphs_dir):
    """
    Section 2: Deep-Dive Longitudinal Thermal Profiling
    """
    import pandas as pd
    if 'Year' not in df.columns:
        dt_col = pd.to_datetime(df['Observation_Time'])
        df['Year'] = dt_col.dt.year
        df['Month_Name'] = dt_col.dt.strftime('%b')
        
    loc_avg_heat = df.groupby('Location_Label')['heat_index_C'].mean().sort_values().index.tolist()
    
    fig, axes = plt.subplots(len(loc_avg_heat), 1, figsize=(14, 20), sharex=True)
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for i, idx_label in enumerate(loc_avg_heat):
        loc_df = df[df['Location_Label'] == idx_label]
        matrix = loc_df.pivot_table(index='Month_Name', columns='Year', values='heat_index_C', aggfunc='mean').reindex(month_order)
        sns.heatmap(matrix, cmap="YlOrRd", annot=True, fmt=".1f", linewidths=0.4, 
                    cbar_kws={'label': 'Heat Index (°C)'} if i == len(loc_avg_heat)-1 else None, ax=axes[i])
        axes[i].set_title(f"Thermal Profile: {idx_label.replace(chr(10), ' ')}", fontsize=12, fontweight='bold', loc='left')
        axes[i].set_ylabel("Months", fontsize=10)
        axes[i].set_xlabel("")

    axes[-1].set_xlabel("Year Progression Baseline (2020 - 2026)", fontsize=12, fontweight='bold', labelpad=10)
    plt.suptitle("Mirpur Climate Vulnerability Study: Year-over-Year Progression of Heat Index", fontsize=16, fontweight='bold', y=1.01)
    plt.tight_layout()
    
    graph_path = os.path.join(graphs_dir, "longitudinal_thermal_profile.png")
    plt.savefig(graph_path, dpi=150)
    plt.close()
    return graph_path

def plot_thermal_divergence(df, graphs_dir):
    """
    Section 3: Quantification of Absolute Thermal Divergence
    """
    import pandas as pd
    if 'Year' not in df.columns:
        df['Year'] = pd.to_datetime(df['Observation_Time']).dt.year
    df['Profile'] = df['SurfaceType'] + " (" + df['TrafficDensity'] + " Traffic)"
    
    annual_means = df.groupby(['Profile', 'Year'])['heat_index_C'].mean().reset_index()
    pivot_means = annual_means.pivot(index='Profile', columns='Year', values='heat_index_C')
    
    # Safely get net change, fallback if 2020/2025 are missing
    y_min = pivot_means.columns.min()
    y_max = pivot_means.columns.max()
    pivot_means['Net_Change_C'] = pivot_means[y_max] - pivot_means[y_min]
    pivot_means = pivot_means.reset_index().sort_values(by='Net_Change_C', ascending=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))
    sns.set_theme(style="whitegrid")

    sns.lineplot(data=annual_means, x='Year', y='heat_index_C', hue='Profile', marker='o', linewidth=2.5, markersize=8, palette="YlOrRd_r", ax=ax1)
    ax1.set_title(r"Annual Heat Index Progression Profile", fontsize=13, fontweight='bold')
    ax1.set_ylabel("Mean Heat Index (°C)", fontsize=11)
    ax1.set_xlabel("Year", fontsize=11)
    
    sns.barplot(data=pivot_means, x='Net_Change_C', y='Profile', hue='Profile', palette="Reds", legend=False, ax=ax2)
    ax2.set_title(fr"Net Temperature Increase ($\Delta$T) from {y_min} to {y_max}", fontsize=13, fontweight='bold')
    ax2.set_xlabel("Absolute Increase in Heat Index (°C)", fontsize=11)
    ax2.set_ylabel("")

    for container in ax2.containers:
        ax2.bar_label(container, fmt=' +%.2f °C', padding=5, fontweight='bold')

    plt.suptitle("Overall Thermal Change Analysis in Mirpur, Dhaka", fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    graph_path = os.path.join(graphs_dir, "thermal_divergence.png")
    plt.savefig(graph_path, dpi=150)
    plt.close()
    return graph_path

def plot_hazard_days(danger_counts, graphs_dir):
    """
    Section 4: Public Health Vulnerability Framework
    Plots the frequency of extreme heat days.
    """
    plt.figure(figsize=(14, 6))
    sns.set_theme(style="ticks")

    sns.barplot(data=danger_counts, x='Year', y='Dangerous_Days_Count', hue='Profile', palette="flare", edgecolor="black")

    plt.title(fr"Climatic Risk Exposure: Frequency of Extreme Heat Days Per Year", fontsize=14, fontweight='bold', pad=15)
    plt.ylabel("Number of Hazardous Days / Year", fontsize=11, fontweight='bold')
    plt.xlabel("Yearly Timeline", fontsize=11, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title="Monitoring Footprints", frameon=True)

    for container in plt.gca().containers:
        plt.gca().bar_label(container, fmt='%d', label_type='edge', padding=3, fontsize=9)

    plt.tight_layout()
    
    graph_path = os.path.join(graphs_dir, "hazard_days_exposure.png")
    plt.savefig(graph_path, dpi=150)
    plt.close()
    return graph_path

def plot_wind_cooling_mechanics(df, maps_dir):
    """
    Section 5: Interactive Mechanical Verification via OLS Regression
    Saves an interactive Plotly HTML chart.
    """
    import plotly.express as px
    import os
    
    fig = px.scatter(
        df,
        x="wind_speed_kmh",
        y="heat_index_C",
        color="SurfaceType",
        trendline="ols",
        title="Convective Cooling Mechanics: Microclimate Heat Index vs. Wind Speed Attenuation",
        labels={
            "wind_speed_kmh": "Anemometer Wind Speed Reading (km/h)",
            "heat_index_C": "Resulting Heat Index (°C)",
            "SurfaceType": "Surface Cover Category"
        },
        opacity=0.4
    )
    fig.update_layout(width=1000, height=600, template="plotly_white")
    
    map_filename = "mirpur_wind_cooling_scatter.html"
    map_path = os.path.join(maps_dir, map_filename)
    fig.write_html(map_path)
    return map_path

def plot_ml_hybrid_projections(metrics_df, timeline_df, graphs_dir):
    """
    Section 6: Advanced Hybrid Machine Learning Pipeline & Projections visualization.
    """
    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(16, 11))

    # Panel A: R2 Metric Comparison
    ax1 = plt.subplot(2, 2, 1)
    sns.barplot(data=metrics_df.sort_values(by='R2', ascending=False), x='R2', y='Model', palette='viridis', ax=ax1, hue='Model', legend=False)
    ax1.set_title("Model Variance Explanation Capability ($R^2$ Score)", fontsize=12, fontweight='bold')
    ax1.set_xlabel("R² Coefficient (Higher is Better)")
    ax1.set_ylabel("")
    for c in ax1.containers: ax1.bar_label(c, fmt=' %.3f', padding=3, fontweight='bold')

    # Panel B: RMSE Metric Comparison
    ax2 = plt.subplot(2, 2, 2)
    sns.barplot(data=metrics_df.sort_values(by='RMSE'), x='RMSE', y='Model', palette='flare', ax=ax2, hue='Model', legend=False)
    ax2.set_title("Absolute Error Distribution Magnitude (RMSE)", fontsize=12, fontweight='bold')
    ax2.set_xlabel("RMSE Bounds in °C (Lower is Better)")
    ax2.set_ylabel("")
    for c in ax2.containers: ax2.bar_label(c, fmt=' %.2f °C', padding=3, fontweight='bold')

    # Panel C: Decadal Projection Forecast
    ax3 = plt.subplot(2, 1, 2)
    hist_line = timeline_df[timeline_df['Model'] == 'Observed Baseline']
    ax3.plot(hist_line['Year'], hist_line['Heat_Index'], marker='o', color='black', linewidth=3.5, label='Observed Historical Data', zorder=5)

    last_obs_yr = hist_line['Year'].max()
    last_obs_val = hist_line[hist_line['Year'] == last_obs_yr]['Heat_Index'].values[0]
    models_list = timeline_df[timeline_df['Model'] != 'Observed Baseline']['Model'].unique()
    colors = sns.color_palette("Set1", len(models_list))

    for m_name, col in zip(models_list, colors):
        m_slice = timeline_df[timeline_df['Model'] == m_name].sort_values('Year')
        extended_years = [last_obs_yr] + list(m_slice['Year'])
        extended_vals = [last_obs_val] + list(m_slice['Heat_Index'])
        ax3.plot(extended_years, extended_vals, linestyle='--', marker='X', linewidth=2.2, color=col, label=f"Forecast: {m_name}")

    ax3.set_title("Multi-Model Horizon Heat Projections Pipeline (2020 - 2030 Timeline)", fontsize=13, fontweight='bold')
    ax3.set_xlabel("Chronological Multi-Year Trackers", fontsize=11, fontweight='bold')
    ax3.set_ylabel("Mean Regional Heat Index (°C)", fontsize=11, fontweight='bold')
    
    # Create ticks properly
    years = sorted(list(timeline_df['Year'].unique()))
    ax3.set_xticks(range(min(years), max(years) + 1))
    ax3.legend(loc='upper left', frameon=True)

    plt.suptitle("Redoing Machine Learning Framework: Robust Model Comparison & Multi-Architecture Projections", fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    graph_path = os.path.join(graphs_dir, "multi_model_ml_comparison.png")
    plt.savefig(graph_path, dpi=150)
    plt.close()
    return graph_path
