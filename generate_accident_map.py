import pandas as pd
import folium
from folium.plugins import HeatMap
import os

def make_map():
    data_path = "data/output/PedestrianAccidents_2019_2023.csv"
    
    if not os.path.exists(data_path):
        print("Data file not found. Run the processor script first.")
        return

    print("Loading data for map...")
    df = pd.read_csv(data_path)
    
    # Drop rows without coordinates just in case
    df = df.dropna(subset=["Latitude", "Longitude"])

    # Center map on average location of accidents
    center_lat = df["Latitude"].mean()
    center_lon = df["Longitude"].mean()
    
    print(f"Center: {center_lat:.4f}, {center_lon:.4f}")

    # Create base map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    # Add heatmap layer
    points = df[["Latitude", "Longitude"]].values.tolist()
    HeatMap(points, radius=15, blur=10).add_to(m)

    out_file = "data/output/hotspots.html"
    m.save(out_file)
    print(f"Map saved to {out_file}")

if __name__ == "__main__":
    make_map()
