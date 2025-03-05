# Pedestrian-accidents-GER

## Background  
This project analyzes and visualizes pedestrian accident data in Germany from 2019 to 2023 since the official website can't process multiple years. It uses official accident datasets and generates an interactive map highlighting accident hotspots.
The accident data is sourced from the official German accident atlas:  
👉 [https://unfallatlas.statistikportal.de](https://unfallatlas.statistikportal.de)

---

## Workflow  

### 1. **Data Processing**  
**`pedestrian_accident_processor.py`**  
- Loads raw accident data (`Unfallorte*.csv`) from the **data/input/** folder.
- Cleans, filters, and merges yearly datasets.
- Focuses on pedestrian accidents and compiles them into a single file:  
  → **`data/output/PedestrianAccidents_2019_2023.csv`**

### 2. **Map Generation**  
**`generate_accident_map.py`**  
- Takes the processed pedestrian accident data.
- Visualizes accident hotspots on an interactive map.
- Generates an HTML map output:  
  → **`data/output/hotspots_map.html`**

---

## Project Structure
```
Pedestrian-accidents-GER/
├── accident_processing.log
├── data/
│   ├── input/
│   │   └── Unfallorte2019-2023_LinRef.csv
│   ├── output/
│       ├── PedestrianAccidents_2019_2023.csv
│       └── hotspots_map.html
├── generate_accident_map.py
├── pedestrian_accident_processor.py
└── requirements.txt
```

---

## Modularity
This project is fully modular and can easily be adapted to analyze **any type of accident data** provided in the **Unfallatlas**.  
By adjusting the filter conditions in `pedestrian_accident_processor.py`, you can switch the focus from pedestrian accidents to:
- Bicycle accidents
- Car accidents
- Motorcycle accidents  
...or any other category available in the dataset.

Simply place the desired CSV files from the Unfallatlas in the **data/input/** folder, modify the filter logic, and re-run the pipeline.

---

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---
