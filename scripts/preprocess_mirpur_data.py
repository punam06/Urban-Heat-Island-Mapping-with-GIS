from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "field_data"

RAW_FILE = DATA_DIR / "mirpur_unified_environmental_data.csv"
CLEAN_FILE = DATA_DIR / "mirpur_unified_environmental_data_clean.csv"
ML_READY_FILE = DATA_DIR / "mirpur_ml_ready_data_clean.csv"
ENCODING_FILE = DATA_DIR / "mirpur_encoding_dictionary_clean.csv"
REPORT_FILE = DATA_DIR / "mirpur_preprocessing_report.md"

CORE_NUMERIC_COLUMNS = [
    "Latitude",
    "Longitude",
    "max_temp_C",
    "min_temp_C",
    "mean_temp_C",
    "humidity_pct",
    "rainfall_mm",
    "wind_speed_kmh",
    "heat_index_C",
]

VALUE_RANGES = {
    "Latitude": (23.0, 24.0),
    "Longitude": (90.0, 91.0),
    "max_temp_C": (-10.0, 60.0),
    "min_temp_C": (-10.0, 45.0),
    "mean_temp_C": (-10.0, 50.0),
    "humidity_pct": (0.0, 100.0),
    "rainfall_mm": (0.0, 500.0),
    "wind_speed_kmh": (0.0, 250.0),
    "heat_index_C": (-10.0, 70.0),
}

CATEGORICAL_COLUMNS = ["LocationName", "SurfaceType", "TrafficDensity"]


def normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    for column in CATEGORICAL_COLUMNS + ["source"]:
        if column in df.columns:
            df[column] = df[column].astype(str).str.strip()
    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    observed_at = pd.to_datetime(df["Observation_Time"], errors="coerce")
    epoch = pd.Timestamp("1970-01-01")
    df["Observation_Time"] = observed_at.dt.strftime("%Y-%m-%d %H:%M:%S")
    df["Observation_Date"] = observed_at.dt.strftime("%Y-%m-%d")
    df["Observation_Timestamp"] = (
        (observed_at - epoch) // pd.Timedelta(seconds=1)
    ).astype("int64")
    df["Observation_Hour"] = observed_at.dt.hour
    df["Observation_Minute"] = observed_at.dt.minute
    df["Observation_Month"] = observed_at.dt.month
    df["Observation_Year"] = observed_at.dt.year
    return df


def build_validity_mask(df: pd.DataFrame) -> tuple[pd.Series, dict[str, int]]:
    mask = pd.Series(True, index=df.index)
    invalid_counts = {}

    parsed_time = pd.to_datetime(df["Observation_Time"], errors="coerce")
    time_invalid = parsed_time.isna()
    invalid_counts["Observation_Time"] = int(time_invalid.sum())
    mask &= ~time_invalid

    for column, (minimum, maximum) in VALUE_RANGES.items():
        invalid = df[column].isna() | (df[column] < minimum) | (df[column] > maximum)
        invalid_counts[column] = int(invalid.sum())
        mask &= ~invalid

    temp_order_invalid = (
        (df["min_temp_C"] > df["mean_temp_C"])
        | (df["mean_temp_C"] > df["max_temp_C"])
    )
    invalid_counts["temperature_order"] = int(temp_order_invalid.sum())
    mask &= ~temp_order_invalid

    return mask, invalid_counts


def encode_categories(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ml_df = df.copy()
    dictionary_rows = []

    for column in CATEGORICAL_COLUMNS:
        categories = sorted(ml_df[column].dropna().unique())
        mapping = {category: code for code, category in enumerate(categories)}
        ml_df[column] = ml_df[column].map(mapping).astype("int64")

        for category, code in mapping.items():
            dictionary_rows.append(
                {
                    "Column_Name": column,
                    "String_Category": category,
                    "Numerical_Code": code,
                }
            )

    encoding_df = pd.DataFrame(dictionary_rows)
    return ml_df, encoding_df


def write_report(
    original_rows: int,
    duplicate_rows_removed: int,
    invalid_counts: dict[str, int],
    cleaned_rows: int,
) -> None:
    dropped_rows = original_rows - cleaned_rows
    lines = [
        "# Mirpur Data Preprocessing Report",
        "",
        "Generated from `data/mirpur_unified_environmental_data.csv`.",
        "",
        "## Summary",
        "",
        f"- Original rows: `{original_rows}`",
        f"- Duplicate rows removed: `{duplicate_rows_removed}`",
        f"- Rows after cleaning: `{cleaned_rows}`",
        f"- Total rows removed: `{dropped_rows}`",
        "",
        "## Invalid Value Checks",
        "",
    ]

    for column, count in invalid_counts.items():
        lines.append(f"- `{column}` invalid rows found: `{count}`")

    lines.extend(
        [
            "",
            "## Output Files",
            "",
            "- `data/mirpur_unified_environmental_data_clean.csv`: cleaned non-encoded data with preserved timestamps.",
            "- `data/mirpur_ml_ready_data_clean.csv`: encoded ML-ready data with date/time features preserved.",
            "- `data/mirpur_encoding_dictionary_clean.csv`: category-to-code dictionary for the cleaned ML file.",
            "",
            "This preprocessing does not calculate NDVI, LST, NIR, Red, or satellite-derived values. Those remain for the calculation stage.",
        ]
    )

    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    df = pd.read_csv(RAW_FILE)
    original_rows = len(df)

    df = normalize_text_columns(df)

    for column in CORE_NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    duplicate_rows = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    valid_mask, invalid_counts = build_validity_mask(df)
    clean_df = df.loc[valid_mask].copy()
    clean_df = add_time_features(clean_df)

    clean_df = clean_df.sort_values(
        ["LocationID", "Observation_Time"], kind="stable"
    ).reset_index(drop=True)

    ml_df, encoding_df = encode_categories(clean_df)
    ml_drop_columns = ["source", "Observation_Time", "Observation_Date"]
    ml_df = ml_df.drop(columns=[c for c in ml_drop_columns if c in ml_df.columns])

    clean_df.to_csv(CLEAN_FILE, index=False)
    ml_df.to_csv(ML_READY_FILE, index=False)
    encoding_df.to_csv(ENCODING_FILE, index=False)
    write_report(original_rows, duplicate_rows, invalid_counts, len(clean_df))

    print(f"Wrote {CLEAN_FILE} ({len(clean_df)} rows)")
    print(f"Wrote {ML_READY_FILE} ({len(ml_df)} rows)")
    print(f"Wrote {ENCODING_FILE} ({len(encoding_df)} mappings)")
    print(f"Wrote {REPORT_FILE}")


if __name__ == "__main__":
    main()
