"""
Download the Customer Support on Twitter dataset from Kaggle.

This script:
1. Downloads the dataset using kagglehub
2. Finds the CSV file
3. Copies it into data/raw/
4. Prints basic information about the dataset
"""

from pathlib import Path
import shutil
import pandas as pd
import kagglehub


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

DATASET_HANDLE = "thoughtvector/customer-support-on-twitter"


# --------------------------------------------------
# Download dataset
# --------------------------------------------------

def download_dataset():
    print("=" * 60)
    print("Downloading Customer Support on Twitter dataset")
    print("=" * 60)

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    dataset_path = kagglehub.dataset_download(DATASET_HANDLE)

    print(f"\nKaggle dataset downloaded to:")
    print(dataset_path)

    return Path(dataset_path)


# --------------------------------------------------
# Find CSV files
# --------------------------------------------------

def find_csv_files(dataset_path: Path):

    csv_files = list(dataset_path.rglob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            "No CSV files were found in the downloaded Kaggle dataset."
        )

    print("\nCSV files found:")

    for file in csv_files:
        print(f" - {file}")

    return csv_files


# --------------------------------------------------
# Copy dataset to project
# --------------------------------------------------

def copy_dataset(csv_files):

    print("\nCopying dataset into data/raw/")

    copied_files = []

    for csv_file in csv_files:

        destination = RAW_DIR / csv_file.name

        shutil.copy2(csv_file, destination)

        copied_files.append(destination)

        print(f"Copied: {destination}")

    return copied_files


# --------------------------------------------------
# Inspect dataset
# --------------------------------------------------

def inspect_dataset(file_path: Path):

    print("\n" + "=" * 60)
    print("DATASET INSPECTION")
    print("=" * 60)

    df = pd.read_csv(file_path)

    print("\nFile:")
    print(file_path.name)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    for column in df.columns:
        print(f" - {column}")

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nFirst 5 rows:")
    print(df.head())

    return df


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    dataset_path = download_dataset()

    csv_files = find_csv_files(dataset_path)

    copied_files = copy_dataset(csv_files)

    print("\n" + "=" * 60)
    print("DOWNLOAD COMPLETE")
    print("=" * 60)

    for file in copied_files:
        print(f"\nInspecting: {file.name}")

        try:
            inspect_dataset(file)

        except Exception as error:
            print(f"Could not inspect {file.name}: {error}")


if __name__ == "__main__":
    main()