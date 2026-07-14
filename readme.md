# Manufacturing Script

This project reads data from a CSV file, analyzes the information, and writes the results to a new CSV file.

## Files
- main.py: runs the main logic
- input.py: reads the input CSV files
- output.py: writes the output CSV files
- masking.py: Handles logic around how to mask each individual data piece

## How to Run
1. Open a terminal in the project folder.
2. Run the following command:
   python main.py
3. Program should then create protected_records.csv, blocked_fields_log.csv and pseudonym_mapping.csv

## What It Does
The script:
- loads data from policy_table and raw_records
- processes the information
- creates output files with the results


