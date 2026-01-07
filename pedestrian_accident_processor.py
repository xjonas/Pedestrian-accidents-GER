import pandas as pd
import os

# Config
INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"
YEARS = range(2019, 2024)

def process_data():
    all_data = []

    print("Looking for accident data")

    for year in YEARS:
        # Files are usually named something like Unfallorte2019_LinRef.csv
        found = False
        for f in os.listdir(INPUT_DIR):
            if str(year) in f and f.endswith(".csv"):
                print(f"Loading {f}")
                path = os.path.join(INPUT_DIR, f)
                
                # German CSVs use semicolon sep and comma for decimals
                # loading with decimal=',' saves us manual conversion work later
                df = pd.read_csv(path, sep=";", decimal=",", low_memory=False)
                
                # Filter: IstFuss == 1 means pedestrian involved
                pedestrians = df[df["IstFuss"] == 1].copy()
                
                # Keep relevant columns: Year, Longitude (X), Latitude (Y)
                subset = pedestrians[["UJAHR", "XGCSWGS84", "YGCSWGS84"]].copy()
                subset.columns = ["Year", "Longitude", "Latitude"]
                
                all_data.append(subset)
                found = True
                break
        
        if not found:
            print(f"No file for {year}, skipping.")

    if not all_data:
        print("Nothing processed. Check your input folder!")
        return

    # Combine all years
    final_df = pd.concat(all_data, ignore_index=True)
    
    # Save clean data
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_file = os.path.join(OUTPUT_DIR, "PedestrianAccidents_2019_2023.csv")
    final_df.to_csv(out_file, index=False)
    
    print(f"Success! Saved {len(final_df)} accidents to {out_file}")

if __name__ == "__main__":
    process_data()
