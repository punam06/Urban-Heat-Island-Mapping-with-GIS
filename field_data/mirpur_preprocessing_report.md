# Mirpur Data Preprocessing Report

Generated from `data/mirpur_unified_environmental_data.csv`.

## Summary

- Original rows: `11700`
- Duplicate rows removed: `0`
- Rows after cleaning: `11627`
- Total rows removed: `73`

## Invalid Value Checks

- `Observation_Time` invalid rows found: `0`
- `Latitude` invalid rows found: `0`
- `Longitude` invalid rows found: `0`
- `max_temp_C` invalid rows found: `15`
- `min_temp_C` invalid rows found: `15`
- `mean_temp_C` invalid rows found: `15`
- `humidity_pct` invalid rows found: `15`
- `rainfall_mm` invalid rows found: `15`
- `wind_speed_kmh` invalid rows found: `15`
- `heat_index_C` invalid rows found: `73`
- `temperature_order` invalid rows found: `0`

## Output Files

- `data/mirpur_unified_environmental_data_clean.csv`: cleaned non-encoded data with preserved timestamps.
- `data/mirpur_ml_ready_data_clean.csv`: encoded ML-ready data with date/time features preserved.
- `data/mirpur_encoding_dictionary_clean.csv`: category-to-code dictionary for the cleaned ML file.

This preprocessing does not calculate NDVI, LST, NIR, Red, or satellite-derived values. Those remain for the calculation stage.
