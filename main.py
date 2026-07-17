import input
import output
import masking
"""
    0 - Record ID
    1 - Field
    2 - Raw Value
    3 - Sensitivity Label
    4 - Protection Action
    5 - Protection Value
"""
def main() -> None:
    
    records = input.return_records()

    pseudonym_mapping = []
    seen_values = set()
    mapped_values = set()

    for record in records:
        masking.mask_data(record)
        original_value = record[2]
        
        if original_value in seen_values and record[4] == "Hash Pseudonymize":
            if original_value not in mapped_values:
                pseudonym_mapping.append([original_value, record[1], record[5]])
                mapped_values.add(original_value)
        else:
            seen_values.add(original_value)
    
    blocked_mapping = []
    for record in records:
        if (record[4] == "Block"):
            blocked_mapping.append([record[0], record[1], record[2]])
            masking.mask_data(record)

    output.output_protected_records(records)
    output.output_pseudonym_records(pseudonym_mapping)
    output.output_blocked_records(blocked_mapping)
if __name__ == "__main__":
    main()
