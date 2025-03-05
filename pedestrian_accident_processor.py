"""
Pedestrian Accident Data Processor

This script processes German traffic accident data from 2019-2023, filtering for
pedestrian-involved accidents and extracting their geographic coordinates.

"""

import pandas as pd
from pathlib import Path
import logging
from typing import List, Optional
import datetime


class AccidentDataProcessor:
    """
    Processes accident data from CSV files, focusing on pedestrian accidents.
    Extracts year, coordinates, and creates a unified dataset.
    """

    def __init__(self, input_dir: str = "data/input", output_dir: str = "data/output"):
        """
        Initialize the processor with input and output directories.

        Args:
            input_dir: Directory containing the accident CSV files
            output_dir: Directory for storing the processed output
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.years_to_process = list(range(2019, 2024))  # 2019-2023

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("accident_processing.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_input_files(self) -> List[Path]:
        """
        Find all relevant accident data files in the input directory.

        Returns:
            List of Path objects for accident data files from 2019-2023
        """
        all_files = list(self.input_dir.glob("Unfallorte*_LinRef.csv"))

        # Filter for the years we want
        year_files = []
        for year in self.years_to_process:
            matching_files = [f for f in all_files if str(year) in f.name]
            if matching_files:
                year_files.append(matching_files[0])
            else:
                self.logger.warning(f"No accident data file found for year {year}")

        return year_files

    def process_file(self, file_path: Path) -> Optional[pd.DataFrame]:
        """
        Process a single accident data CSV file, extracting pedestrian accidents.

        Args:
            file_path: Path to the CSV file

        Returns:
            DataFrame containing filtered pedestrian accident data, or None if processing failed
        """
        try:
            # Extract year from filename
            year = None
            for y in self.years_to_process:
                if str(y) in file_path.name:
                    year = y
                    break

            if not year:
                self.logger.error(f"Could not determine year for file: {file_path}")
                return None

            self.logger.info(f"Processing data for year {year} from {file_path}")

            # Read the CSV file
            df = pd.read_csv(file_path, delimiter=';', low_memory=False)

            # Filter for pedestrian accidents (IstFuss == 1)
            pedestrian_accidents = df[df['IstFuss'] == 1].copy()

            # Select only the columns we need
            filtered_df = pedestrian_accidents[['UJAHR', 'XGCSWGS84', 'YGCSWGS84']]

            # Log statistics
            self.logger.info(f"Year {year}: {len(filtered_df)} pedestrian accidents found")

            return filtered_df

        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            return None

    def process_all_files(self) -> pd.DataFrame:
        """
        Process all accident data files and combine into a single DataFrame.

        Returns:
            Combined DataFrame with all pedestrian accident data
        """
        input_files = self.get_input_files()
        self.logger.info(f"Found {len(input_files)} input files to process")

        # Process each file and collect results
        dataframes = []
        for file_path in input_files:
            df = self.process_file(file_path)
            if df is not None and not df.empty:
                dataframes.append(df)

        # Combine all dataframes
        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)
            self.logger.info(f"Combined data contains {len(combined_df)} pedestrian accidents")
            return combined_df
        else:
            self.logger.warning("No valid data was processed")
            return pd.DataFrame(columns=['UJAHR', 'XGCSWGS84', 'YGCSWGS84'])


    def save_output(self, df: pd.DataFrame, filename: str = "PedestrianAccidents_2019_2023.csv") -> str:
        """
        Save the processed DataFrame to CSV.

        Args:
            df: DataFrame to save
            filename: Output filename

        Returns:
            Path to the saved file
        """
        output_path = self.output_dir / filename
        df.to_csv(output_path, index=False)
        self.logger.info(f"Saved output to {output_path}")
        return str(output_path)

    def run(self) -> str:
        """
        Run the complete processing pipeline.

        Returns:
            Path to the output file
        """
        self.logger.info("Starting pedestrian accident data processing")
        start_time = datetime.datetime.now()

        # Process all files
        combined_df = self.process_all_files()

        # Save to output file
        output_path = self.save_output(combined_df)

        # Log completion
        processing_time = (datetime.datetime.now() - start_time).total_seconds()
        self.logger.info(f"Processing completed in {processing_time:.2f} seconds")
        self.logger.info(f"Extracted {len(combined_df)} pedestrian accidents across {len(self.years_to_process)} years")

        return output_path


if __name__ == "__main__":
    processor = AccidentDataProcessor()
    output_file = processor.run()
    print(f"Processing complete. Output saved to: {output_file}")