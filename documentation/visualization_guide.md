# 🎨 Visualization Role Guide — Spondon & Rushafi

**Role**: Dataset Plotting & GIS Visualization (Role 3)
**Assigned to**: Spondon, Rushafi
**Last updated**: 2026-06-03

---

## 🎯 Objective

Generate static and interactive visualizations that communicate Urban Heat Island (UHI) patterns in **Mirpur 12** (baseline) and the four divisional presets (**Dhaka All**, **Sylhet**, **Rajshahi**, **Chittagong**). Your output will let planners see *where* to plant trees, *which* surfaces drive heat retention, and *how* vegetation cools the city.

You are **not** re-running calculations — Punam and Nafiz have already produced the cleaned, calculated dataset. You are **building visuals** from it.

---

## 📂 What's Already Done (Read-Only Inputs for You)

| File | Purpose |
| :--- | :--- |
| [data/mirpur_unified_environmental_data_clean.csv](../data/mirpur_unified_environmental_data_clean.csv) | Master dataset: 11,627 rows × all columns (`LST_C`, `NDVI`, `Calculated_NDVI`, `SurfaceType`, `TrafficDensity`, weather) |
| [pipeline/plotting.py](../pipeline/plotting.py) | Existing plotting module — currently produces one scatter + one heatmap per region. **You will extend this.** |
| [output/graphs/](../output/graphs/) | Pre-existing scatter plots per region |
| [output/maps/](../output/maps/) | Pre-existing Folium Leaflet HTML heatmaps per region |
| [documentation/proposed_final_projection.png](proposed_final_projection.png) | Mockup of the final projection |

---

## ✅ Your Deliverables (Definition of Done)

### 1. Static Graphs (Matplotlib / Seaborn) → `output/graphs/`

| # | File | Type | What It Shows |
| :--- | :--- | :--- | :--- |
| 1 | `mirpur12_ndvi_vs_lst.png` | Scatter + regression line | NDVI (x) vs LST_C (y), color-coded by SurfaceType |
| 2 | `mirpur12_surface_type_boxplot.png` | Box/violin | LST distribution per SurfaceType (Asphalt, Concrete, Vegetation, Water Body, Bare Soil, Mixed) |
| 3 | `mirpur12_traffic_heat_bar.png` | Grouped bar | Mean LST by TrafficDensity × SurfaceType |
| 4 | `mirpur12_hourly_heat_profile.png` | Line | LST by `Observation_Hour` (diurnal curve), one line per SurfaceType |
| 5 | `mirpur12_temporal_trend.png` | Line | Monthly avg LST (`Observation_Month`) to show seasonal UHI |
| 6 | `divisional_comparison.png` | Grouped bar | Avg LST across the 5 regions (Mirpur-12, Dhaka, Sylhet, Rajshahi, Chittagong) |

### 2. Interactive GIS Maps (Folium) → `output/maps/`

| # | File | What It Shows |
| :--- | :--- | :--- |
| 1 | `mirpur12_heatmap.html` | **Already exists.** Verify it opens and legend renders. |
| 2 | `mirpur12_hotspots_cluster.html` | Folium map with marker clusters for top-10 hotspots and top-10 coolspots, color-coded |
| 3 | `mirpur12_surface_layer_map.html` | Folium map with circle markers colored by SurfaceType, with layer toggles |
| 4 | `divisional_overview_map.html` | Single map showing all 5 region centers + mini-heat bubbles |

### 3. Report Integration → `documentation/Report writting/`

- Embed the 6 static graphs + screenshots of maps into the final report.
- Each figure needs a **caption** (1–2 sentences) explaining the takeaway.
- Save captions in `documentation/Report writting/figure_captions.md`.

---

## 🛠️ Tools & Setup

```bash
# Install everything in one shot
pip install pandas numpy matplotlib seaborn folium plotly branca scikit-learn --break-system-packages
```

**Python entry point**: extend [pipeline/plotting.py](../pipeline/plotting.py). Don't write a one-off notebook — add functions so the next run of `python main.py` regenerates all your visuals reproducibly.

**Reusable functions already in the codebase**:
- `generate_visualizations(df, meta, graphs_dir, maps_dir)` in [pipeline/plotting.py](../pipeline/plotting.py) — currently produces one scatter + one heatmap per region. **Extend it** to call your new helpers.
- `summarize_calculated_indices(df)` in [pipeline/calculation.py](../pipeline/calculation.py) — gives you `peak_hotspot`, `peak_coolspot`, averages. Use these for annotations.

---

## 📐 Step-by-Step Workflow

### Step 1 — Load the data (don't recompute)
```python
import pandas as pd
df = pd.read_csv("data/mirpur_unified_environmental_data_clean.csv")
print(df.columns.tolist())  # Confirm LST_C, NDVI, Calculated_NDVI exist
```

### Step 2 — Build each static graph as a function
Pattern each graph as a standalone function in `pipeline/plotting.py`:
```python
def plot_ndvi_vs_lst(df, out_path):
    """Scatter of NDVI vs LST_C with regression line, colored by SurfaceType."""
    # ...use seaborn.lmplot or matplotlib scatter...
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
```
Then call them from `generate_visualizations()`.

### Step 3 — Build each Folium map
Use `folium.Map(location=[23.8248, 90.3621], zoom_start=14)` for Mirpur 12. Add:
- `folium.HeatMap(data=df[['Latitude','Longitude','LST_C']].values.tolist(), ...)`
- `folium.Marker(...)` for hotspots/coolspots with `folium.Popup(...)`
- `folium.LayerControl()` so users can toggle layers
- `branca.colormap.LinearColormap` for the LST legend

### Step 4 — Annotate findings
For each graph, write the takeaway in `figure_captions.md`. Example:
> **Figure 2**: Concrete and asphalt surfaces in Mirpur 12 show median LST of 35.2°C and 36.8°C respectively — 6°C hotter than vegetated zones (median 29.4°C). This confirms vegetation's cooling effect.

### Step 5 — Verify
```bash
python main.py
```
All 6 graphs + 4 maps should regenerate without errors.

---

## 📊 Key Insights to Surface (Look For These)

Based on the completed calculation phase, your visuals should make these obvious:

1. **Mirpur 12 baseline**: avg LST ≈ 30.86°C; peak hotspot **Mirpur-10 Roundabout** at 43.99°C; peak coolspot **National Botanical Garden** at 10.0°C.
2. **Vegetation cools ~3°C per 0.1 NDVI** (linear regression slope ≈ −15.16 × NDVI).
3. **Traffic adds heat**: High > Medium > Low traffic density by ~1–2°C at constant surface.
4. **Diurnal pattern**: peak heat 12:00–15:00, coolest before dawn.
5. **Divisional ranking** ( hottest → coolest ): Rajshahi > Dhaka > Chittagong > Sylhet.

---

## ⚠️ Guardrails

- **Do not** modify [pipeline/calculation.py](../pipeline/calculation.py) — that's Punam/Nafiz's lane.
- **Do not** delete or overwrite existing files in `output/` without checking with the team.
- **Do** use the cleaned CSV (`*_clean.csv`), not the raw one.
- **Do** commit new visuals with a clear message: `Add NDVI vs LST scatter for Mirpur 12`.
- **Do** keep figures under 500KB each (use `dpi=200`, not 600).

---

## 🗓️ Timeline

| Date | Milestone |
| :--- | :--- |
| 2026-06-04 | Step 1 complete — data loaded, columns confirmed |
| 2026-06-06 | Static graphs 1–3 delivered |
| 2026-06-07 | Static graphs 4–6 delivered |
| 2026-06-08 | Folium maps 2–4 delivered |
| 2026-06-09 | Captions + report integration |
| 2026-06-10 | Final review with team |

---

## 🤝 Hand-offs

- **From**: Punam, Nafiz (calculation complete — CSV is ready, don't recompute).
- **To**: Ajwad, Sabbir (ML) — they need your visualizations to interpret model outputs; share early drafts.
- **To**: Sayed, Nusair (preprocessing) — if you spot data quality issues in the visuals, loop them in.

---

## ❓ Questions?

Ping the group chat. If a calculation looks wrong, **do not** edit `calculation.py` — file an issue with a screenshot and tag Punam/Nafiz.
