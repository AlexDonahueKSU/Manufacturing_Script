import csv

"""
Outputting based on the criteria given to me via email. Will update as
we refine what that criteria is.
"""

def output_protected_records(records):
    with open("protected_records.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        writer.writerow(["Record ID", "Field", "Raw Value", "Sensitivity Label", "Protection Action", "Protected Record"])
        
        for record in records:
            writer.writerow([record[0], record[1], record[2], record[3], record[4], record[5]])

def output_pseudonym_records(records):
    with open("pseudonym_mapping.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        writer.writerow(["Raw Value", "Field Type", "Protected Value"])
        
        for record in records:
            writer.writerow([record[0], record[1], record[2]])

def output_blocked_records(records):
    with open("blocked_fields_log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        writer.writerow(["Record ID", "Field", "Raw Value", "Reason"])
        
        for record in records:
            writer.writerow([record[0], record[1], record[2], "Placeholder reason"])
