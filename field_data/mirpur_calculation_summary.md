# Mirpur Calculation Summary

Generated from `data/mirpur_unified_environmental_data_clean.csv`.

## Output

- `data/mirpur_calculated_environmental_indices.csv`
- `data/mirpur_calculation_summary.json`

## Calculated Columns

- `Red`: estimated red-band reflectance from surface type and weather context.
- `NIR`: estimated near-infrared reflectance from surface type and weather context.
- `NDVI`: `(NIR - Red) / (NIR + Red)`.
- `Calculated_NDVI`: verification copy recalculated from `NIR` and `Red`.
- `LST_C`: estimated land surface temperature in Celsius.
- `Temperature`: alias of `LST_C` for the existing pipeline, plotting, and ML modules.

These are calculation-stage estimates from ground/weather data. Replace `Red`, `NIR`, and `LST_C` with true satellite-derived values when Landsat/Sentinel bands are available.

## Dataset Summary

- Rows: `11627`
- Average LST: `30.857` C
- Average NDVI: `0.00137`
- NDVI range: `-0.29591` to `0.68874`

## Hotspot

- Location: `Mirpur-10 Roundabout`
- LST: `43.991` C
- Coordinate: `23.81, 90.37`

## Coolspot

- Location: `National Botanical Garden`
- LST: `10.0` C
- Coordinate: `23.82, 90.35`
