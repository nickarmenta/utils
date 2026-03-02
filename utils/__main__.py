"""CLI entry point for report processing"""

import argparse
import os
import zipfile

import pandas as pd
from dotenv import load_dotenv

from .processors import process_contacts, process_visits

load_dotenv()

BASE_DIRECTORY = os.getenv("BASE_DIRECTORY")


def visits():
    print("Running visits...")
    with zipfile.ZipFile(f"{BASE_DIRECTORY}\\Visit.zip", "r") as zip_ref:
        zip_ref.extractall()

    filename = None
    # Remove the file that starts with "Visit_Notes_"
    for file in os.listdir(BASE_DIRECTORY):
        if file.startswith("Visit_Notes_"):
            os.remove(file)
        elif file.startswith("Visit_2") and file.endswith(".xlsx"):
            filename = file

    assert filename

    # Read the Excel file
    df = pd.read_excel(filename)

    # Process using shared logic
    df = process_visits(df)

    # Save the modified file
    df.to_excel(filename, index=False)
    print(f"Headers removed from {filename}")


def contacts(segment=False):
    print("Running contacts...")

    filename = None
    # Find the file that starts with "Contact_" and ends with ".xlsx"
    for file in os.listdir(BASE_DIRECTORY):
        if file.startswith("Contact_") and file.endswith(".xlsx"):
            filename = file
            break

    assert filename, "No Contact file found"

    # Read the Excel file
    df = pd.read_excel(f"{BASE_DIRECTORY}\\{filename}")

    # Process using shared logic
    result = process_contacts(df, segment_by_region=segment)

    if segment:
        # Save separate files for each region
        print(f"Processing complete! Segmented into {len(result)} mailing lists")
        for region_name, region_df in result.items():
            output_filename = filename.replace("Contact_", f"Contact_{region_name}_")
            output_path = f"{BASE_DIRECTORY}\\{output_filename}"
            region_df.to_excel(output_path, index=False)
            print(f"  {region_name}: {len(region_df)} contacts -> {output_filename}")
    else:
        # Save single file
        output_filename = filename.replace("Contact_", "Contact_Processed_")
        result.to_excel(f"{BASE_DIRECTORY}\\{output_filename}", index=False)
        print(f"Processing complete!")
        print(f"Output saved to: {output_filename}")
        print(f"\nProcessed {len(result)} contacts")
        print("\n--- Preview of first 5 contacts ---")
        print(result.head().to_string())


def main():
    parser = argparse.ArgumentParser(description="Process spreadsheets.")
    parser.add_argument("report", type=str, help="Type of report to run")
    parser.add_argument(
        "--segment",
        "-s",
        action="store_true",
        help="Segment contacts into separate mailing lists (PNW, CA, GG)",
    )
    args = parser.parse_args()

    if args.report == "visits":
        visits()
    elif args.report == "contacts":
        contacts(segment=args.segment)
    else:
        print(f"Unknown report type: {args.report}")


if __name__ == "__main__":
    main()
