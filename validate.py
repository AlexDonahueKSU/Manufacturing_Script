import input
import csv
"""
This file handles a few different validations to ensure that our data 
functions as we intend.
"""
records = input.return_records()
def validate_records():
    if (validate_30_records() 
        and contains_15_records()
        and check_duplicate()
        and missing_policy_rules()
        and check_pseudonym_consistency()
        and sensitive_value_check()
    ):
        print("VALIDATION PASSED") 
    else:
        print("VALIDATION FAILED")

def validate_30_records():
    counter = 0
    currentRecord = 0
    for record in records:
        if int(record[0]) != int(currentRecord):
            currentRecord = record[0]
            counter = counter + 1
    print("Records validated: " + str(counter))

    if (int(counter) == 30):
        return True
    else:
        return False

def contains_15_records():
    counter = 0
    currentRecord = 1
    for record in records:
        counter = counter + 1   
        if int(record[0]) != int(currentRecord):
            currentRecord = int(record[0])
            if counter != 16:
                print("Error in number of fields")
                return False
            counter = 1
    print("Fields per record: " + str(counter))
    return True

def check_duplicate():
    duplicate_set = set()
    currentRecord = 1
    for record in records:
        if int(record[0]) != currentRecord:
                    currentRecord = record[0]
                    duplicate_set.clear()

        if record[1] not in duplicate_set:
            duplicate_set.add(record[1])
        else:
            print("There is a duplicate in record: " + str(currentRecord))
            return False
        
    print("No duplcates in records")
    return True

def missing_policy_rules():
    missing_rules = 0
    for record in records:
        if (
            record[4] != "Keep"
            and record[4] != "Block"
            and record[4] != "Placeholder Mask"
            and record[4] != "Generalize"
            and record[4] != "Hash Pseudonymize"
            ):
              missing_rules = missing_rules + 1
    print("Missing policy rules " + str(missing_rules))
    if missing_rules != 0:
        return False
    return True

def check_pseudonym_consistency():
    try:
        with open("protected_records.csv", newline="", encoding="utf-8") as f:
            protected_rows = list(csv.DictReader(f))
    except FileNotFoundError:
        print("Could not find protected_records.csv; run main.py first.")
        return False

    try:
        with open("pseudonym_mapping.csv", newline="", encoding="utf-8") as f:
            mapping_rows = {
                (row["Raw Value"], row["Field Type"]): row["Protected Value"]
                for row in csv.DictReader(f)
            }
    except FileNotFoundError:
        print("Could not find pseudonym_mapping.csv; run main.py first.")
        return False

    mismatches = []

    for row in protected_rows:
        if row.get("Protection Action") == "Hash Pseudonymize":
            key = (row.get("Raw Value", ""), row.get("Field", ""))
            expected = mapping_rows.get(key)
            actual = row.get("Protected Record", "")

            if expected is None:
                mismatches.append(
                    f"Missing mapping for field '{row.get('Field')}' with raw value '{row.get('Raw Value')}'."
                )
            elif actual != expected:
                mismatches.append(
                    f"Mismatch for field '{row.get('Field')}' with raw value '{row.get('Raw Value')}': expected {expected}, got {actual}."
                )
    total_Mismatches = 0
    if mismatches:
        for mismatch in mismatches:
            total_Mismatches = total_Mismatches + 1
            print("Pseudonym consistency errors: " + str(total_Mismatches))
        return False

    print("Pseudonym consistency errors: " + str(total_Mismatches))
    return True

def sensitive_value_check():
    try:
        with open("protected_records.csv", newline="", encoding="utf-8") as f:
            protected_rows = list(csv.DictReader(f))
    except FileNotFoundError:
        print("Could not find protected_records.csv; run main.py first.")
        return False

    leakage_counter = 0

    for row in protected_rows:
        field = row.get("Field", "")
        protected_value = row.get("Protected Record", "")
        raw_value = row.get("Raw Value", "")

        if field == "Operator Name" and protected_value != "" and protected_value.lower() != "[operator_name]":
            leakage_counter += 1

        if field == "Customer/Order Information" and protected_value != "" and protected_value.lower() != "[blocked]":
            leakage_counter += 1

        if field in {"Supplier ID", "Batch ID", "Machine ID"}:
            if raw_value and protected_value and raw_value in protected_value:
                leakage_counter += 1

    if leakage_counter > 0:
        print("Sensitive-value leakage errors: " + str(leakage_counter))
        return False

    print("Sensitive-value leakage errors: 0")
    return True


if __name__ == "__main__":
    validate_records()
