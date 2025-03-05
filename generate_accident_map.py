import os
import pandas as pd
import folium
from folium.plugins import HeatMap

def load_data(filepath):
    """
    Custom loader:
      - Reads the first line to parse the header (which is a quoted, comma-separated string).
      - Loads the remainder of the file using a comma as the delimiter.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        header_line = f.readline().strip()
    # Remove surrounding quotes if present
    if header_line.startswith("'") and header_line.endswith("'"):
        header_line = header_line[1:-1]
    # Split header by comma to get column names
    column_names = [col.strip() for col in header_line.split(',')]
    print("Parsed header:", column_names)

    # Read the rest of the CSV using comma as delimiter.
    df = pd.read_csv(
        filepath,
        sep=',',
        decimal=',',
        skiprows=1,
        names=column_names,
        quotechar='"'
    )
    print("CSV loaded with custom header using comma delimiter.")
    return df

def process_data(df):
    """
    Process the coordinate columns:
      - Convert columns to numeric.
      - These columns are expected to represent longitude and latitude.
      - Replace any commas in the numeric strings with dots and then convert.
      - Drop rows with missing values.
      - Rename the columns to 'Longitude' and 'Latitude' for clarity.
    """
    # Show raw data for debugging
    print("Raw data head before conversion:\n", df.head())

    for col in ['XGCSWGS84', 'YGCSWGS84']:
        # Force the column to string, replace commas with dots, and convert to numeric.
        df[col] = df[col].astype(str).str.replace(',', '.')
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with missing coordinate values
    df = df.dropna(subset=['XGCSWGS84', 'YGCSWGS84'])

    # Debug: show data after conversion
    print("Data head after conversion:\n", df.head())

    # Rename columns for clarity
    df = df.rename(columns={'XGCSWGS84': 'Longitude', 'YGCSWGS84': 'Latitude'})
    return df

def create_heatmap(df, output_html):
    """
    Create an interactive heat map using Folium:
      - The map is centered on the average coordinates.
      - A heat layer visualizes the accident hotspots.
    """
    lat_mean = df['Latitude'].mean()
    lon_mean = df['Longitude'].mean()
    print("Computed mean latitude:", lat_mean)
    print("Computed mean longitude:", lon_mean)

    if pd.isna(lat_mean) or pd.isna(lon_mean):
        raise ValueError("The computed map center contains NaNs. Check coordinate conversion.")

    heat_data = df[['Latitude', 'Longitude']].values.tolist()
    accident_map = folium.Map(location=[lat_mean, lon_mean], zoom_start=12)
    HeatMap(heat_data, radius=10).add_to(accident_map)
    accident_map.save(output_html)
    print(f"Heatmap saved to: {output_html}")

def main():
    # CSV file is in data/output, and the script is at the same level as the data folder.
    csv_filepath = os.path.join("data", "output", "PedestrianAccidents_2019_2023.csv")

    if not os.path.exists(csv_filepath):
        raise FileNotFoundError(f"CSV file not found: {csv_filepath}")

    df = load_data(csv_filepath)
    df = process_data(df)

    if df.empty:
        raise ValueError("No valid data rows after processing. Check the CSV file format and conversion logic.")

    output_html = os.path.join("data", "output", "hotspots_map.html")
    create_heatmap(df, output_html)

if __name__ == '__main__':
    main()
