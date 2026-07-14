"""
 Goal on this module is to import both the policy table and raw_records and store all necessary information in the 
 records_table list.

 The Policy Table csv contains most of the information on what to do with our records, here how I'm storing the list
 0 - Field
 1 - Sensitivity Label
 2 - Protection Action

 raw_records csv will contain only the the record ID, field and raw record. Field is important for matching the 
 policy table information

 Finally I will cross reference the fields in policy_table and store all necessary information in records_table
 0 - Record ID
 1 - Field
 2 - Raw Value
 3 - Sensitivity Label
 4 - Protection Action
 5 - Protection Value
"""

import csv

def return_records():
    
    policy_table = []
    records_table = []
    
    def get_policy_table(file_path):
        with open(file_path, newline="", encoding="utf-8-sig", errors="replace") as file:
            reader = csv.reader(file)
            # Skip first 2 lines to avoid headers
            next(reader, None)
            next(reader, None)
            
            for row in reader:
                if len(row) >= 2:
                    policy_table.append([row[0], row[2], row[4]])
    
    
    def get_raw_records(file_path):
       with open(file_path, newline="", encoding="utf-8-sig", errors="replace") as file:
            reader = csv.reader(file)
            # Skip first 2 lines to avoid headers
            next(reader, None)
            next(reader, None)
            
            for row in reader:
                if len(row) >= 2:
                    records_table.append([row[0], row[1], row[2], "0", "0", "0"])
    
    file_path = "./policy_table.csv"
    get_policy_table(file_path)
    file_path = "./raw_records.csv"
    get_raw_records(file_path)

    # Adds the proper values from policy table to records_table
    for policy in policy_table:
        for record in records_table:
            if (policy[0] == record[1]):
                record[3] = policy[1]
                record[4] = policy[2]
    return records_table

    
