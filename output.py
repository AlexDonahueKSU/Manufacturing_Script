import csv

"""
Outputs the 3 different files that we designated for the project.
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
            writer.writerow([record[0], record[1], record[2], "Sensitive Customer Information"])

def output_audit_evidence(records):
    rule_map = {
        "Keep": "R1",
        "Generalize": "R2",
        "Hash Pseudonymize": "R3",
        "Placeholder Mask": "R4",
        "Block": "R5",
    }

    release_map = {
        "Keep": "Released",
        "Generalize": "Released",
        "Hash Pseudonymize": "Released",
        "Placeholder Mask": "Released",
        "Block": "Blocked",
    }

    reason_map = {
        "Keep": "Analytically necessary, lower-risk value retained",
        "Generalize": "Sensitive value generalized to reduce disclosure risk",
        "Hash Pseudonymize": "Supplier, batch, and machine identifiers pseudonymized",
        "Placeholder Mask": "Personal identifier masked with a placeholder",
        "Block": "Customer and order information blocked from release",
    }

    rows = []
    for record in records:
        action = record[4]
        rows.append({
            "Record ID": record[0],
            "Field": record[1],
            "Sensitivity Label": record[3],
            "Protection Action": action,
            "Policy Rule ID": rule_map.get(action, "N/A"),
            "Protected Value": record[5],
            "Release Decision": release_map.get(action, "N/A"),
            "Reason": reason_map.get(action, "N/A"),
        })

    with open("audit_evidence.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "Record ID",
                "Field",
                "Sensitivity Label",
                "Protection Action",
                "Policy Rule ID",
                "Protected Value",
                "Release Decision",
                "Reason",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
