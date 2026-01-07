# Pedestrian Accidents Germany (2019-2023)

This project visualizes where pedestrian accidents happen in Germany. 

The official 'Unfallatlas' website only lets you look at one year at a time, so this tool combines data from 2019-2023 to show the bigger picture.

## Data Source
The raw data comes from the German Statistical Office: 
**Reference:** https://unfallatlas.statistikportal.de

We use the "Unfallorte" CSV files (with LinRef).

## How to use
1. Download the CSV files for the years you want (2019-2023) and put them in `data/input/`.
2. Run the processor to clean and merge the data:
   ```bash
   python pedestrian_accident_processor.py
   ```
   This creates a clean file `data/output/PedestrianAccidents_2019_2023.csv`.
   
3. Generate the heatmap:
   ```bash
   python generate_accident_map.py
   ```
   Open `data/output/hotspots.html` in your browser to see the result.

## Requirements
- pandas
- folium
