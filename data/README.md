# Data Structure Guide

This project needs two different kinds of temperature data:

1. **Point-based environmental/GIS data** for heat maps, NDVI regression, and the current Python pipeline.
2. **Historical daily temperature data** for background climate trend analysis or future model features.

`data/mirpur_historical_temperatures.csv` is valid as a historical weather table, but it is **not enough by itself** for the current UHI pipeline because it has no GPS coordinates, surface type, NDVI, or traffic/field observations.

## 1. Current Pipeline Input

Main file currently used by `main.py`:

```text
data/environmental/mirpur12_ground_data.csv
```

Required columns:

| Column | Data type | Required | Example | Notes |
| --- | --- | --- | --- | --- |
| `LocationName` | string | yes | `Mirpur-12 Metrorail station` | Human-readable site name. |
| `Latitude` | float | yes | `23.826606` | Decimal degrees. |
| `Longitude` | float | yes | `90.364136` | Decimal degrees. |
| `Temperature` | float | yes | `32.5` | Measured or estimated surface/air temperature in Celsius. |
| `SurfaceType` | category/string | yes | `Concrete` | Use consistent labels. |
| `NDVI` | float | yes | `0.10` | Range should normally be `-1.0` to `1.0`; vegetation usually higher than `0.3`. |
| `TrafficDensity` | category/string | yes | `High` | Recommended values: `Low`, `Medium`, `High`. |
| `Time` | string | yes | `Afternoon` | Keep consistent, or use ISO datetime if exact time is available. |
| `EstimatedTemp` | string | optional | `30-35` | Useful for field notes/image labels. |
| `Image` | string | optional | `site_photo.jpeg` | Filename in `frontend/images/`. |
| `LocationID` | integer | optional | `1` | Helpful unique ID; generated regional data already uses this. |
| `NIR` | float | optional | `0.122` | Near-infrared reflectance. If absent, the code synthesizes it from `NDVI`. |
| `Red` | float | optional | `0.100` | Red-band reflectance. If absent, the code synthesizes it from `NDVI`. |

Use template:

```text
data/templates/ground_observations_template.csv
```

## 2. Historical Temperature Data

Your file:

```text
data/mirpur_historical_temperatures.csv
```

Current shape:

| Column | Data type | Required | Example | Notes |
| --- | --- | --- | --- | --- |
| `date` | datetime/string | yes | `2024-04-01 18:00:00` | Parse with `pd.to_datetime`. |
| `max_temp_C` | float | yes | `36.2` | Daily maximum Celsius. |
| `min_temp_C` | float | yes | `25.1` | Daily minimum Celsius. |
| `mean_temp_C` | float | yes | `30.4` | Daily average Celsius. |

This format is okay for weather trend analysis. For stronger modeling, optional useful columns are `humidity_pct`, `rainfall_mm`, `wind_speed_kmh`, `heat_index_C`, and `source`.

Use template:

```text
data/templates/historical_temperatures_template.csv
```

## 3. Satellite / Remote-Sensing Data

For the remote sensing part of the project, collect a separate satellite table before fusing it with ground data.

| Column | Data type | Required | Example | Notes |
| --- | --- | --- | --- | --- |
| `SceneID` | string | yes | `LC09_20240415_DHAKA` | Satellite image/scene identifier. |
| `AcquiredDate` | date/datetime | yes | `2024-04-15` | Date image was captured. |
| `Latitude` | float | yes | `23.826606` | Pixel/sample latitude or matched ground point latitude. |
| `Longitude` | float | yes | `90.364136` | Pixel/sample longitude or matched ground point longitude. |
| `Red` | float | yes | `0.100` | Red-band reflectance. |
| `NIR` | float | yes | `0.122` | Near-infrared reflectance. |
| `NDVI` | float | yes | `0.100` | `(NIR - Red) / (NIR + Red)`. |
| `LST_C` | float | yes | `34.7` | Land Surface Temperature in Celsius. |
| `CloudCoverPct` | float | optional | `4.5` | Prefer low-cloud scenes. |
| `Satellite` | string | optional | `Landsat 9` | Landsat/Sentinel/source name. |

Use template:

```text
data/templates/satellite_observations_template.csv
```

## Recommended Data For Final Project

Minimum:

- `ground_observations`: GPS-tagged temperature measurements with surface type and NDVI.
- `historical_temperatures`: daily max/min/mean temperature history.
- `satellite_observations`: NDVI and LST from satellite scenes.

Better:

- Add field survey notes: shade level, road width, traffic density, water body nearby, building density.
- Add weather context: humidity, rainfall, wind speed, date/time of observation.
- Add image filenames for each field point, so the dashboard can show evidence for each hotspot.

