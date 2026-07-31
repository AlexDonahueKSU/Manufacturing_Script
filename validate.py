import input

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
    
if __name__ == "__main__":
    validate_records()
