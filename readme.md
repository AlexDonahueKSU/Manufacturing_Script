# Project Objective
This project focuses on label-aware masking for privacy-preserving LLM/RAG manufacturing workflows. Essentially we study how we can use sensitivity-label-based masking to reduce manufacturing information leakage while preserving the usefulness of the information. 

## Dataset description
The dataset we use for this project involves 30 different records of 15 different manufacturing related pieces of data. The data types are diverse and encompass many different challenges as to replicate the challenges of real world masking.

## Five Protection Actions
1. Keep - Self explanatory, these are examples of data that do not need changed.
2. Block - Data that are completely masked with a [BLOCKED] output.
3. Placeholder Mask - Data types that are replaced with their associated field type. For example, QL-2026-014 becomes [QUALITY_LOG_ID]
4. Generalize - Data types that are generalized to a specific value range instead of a precise value. For example, 5.70% becomes 5-10%
5. Hash Pseudonymize - Data types that are changed to a field related prefix, and a 4 digit suffix. For example, Supplier-E21 becomes [SUPPLIER_QC9B]

## Privacy and Utility Evaluation
Specific evaluations for each different field type can be seen in the policy_table.csv file. Speaking broadly, type of masking is as follows.

1. Keep - High utility, low privacy
2. Block - low utility, high privacy
3. Placeholder Mask - Medium utility, high privacy
4. Generalize - high utility, medium privacy
5. Hash Pseudonymize - high utility, high privacy

I'll explain how I reached each metric here. In terms of keeping data, it goes without saying that you are getting the full use of the information, but doing nothing to retain privacy. Blocking is the opposite, you get no utility but it's impossible to leak any useful information. Placeholder Masks give you some idea of the information you are dealing with while not leaking any sensitive data, but in cases where more detailed information is needed, this may not be sufficient. Generalization is quite useful when you don't want to leak precise values but ranges are acceptable. They give some degree of utility while never leaking the precise values being used. Finally, Hash Pseudonymize is the most effective overall, as it provides information that can be tracked back to the original piece of data, while being quite effective for privacy as the values are meaningless to potential attackers.

## Input Files
1. policy_table.csv
2. raw_records.csv

## Output Files
1. protected_records.csv
2. pseudonym_mapping.csv
3. blocked_fields_log.csv
4. audit_evidence.csv

## How to Run
1. Open a terminal in the project folder.
2. Run the following command:
   python main.py
3. Program should then create protected_records.csv, blocked_fields_log.csv and pseudonym_mapping.csv
4. Afterwards, python validate.py can be ran to ensure that our expected output is reached.

## Limitations/Future Work
While our work can provide benefit to LLM privacy preservation in theory, these concepts have yet to be applied to real world manufacturing datasets. Our masking is limited to our strict dataset, which does not cover the full breadth of potential manufacturing privacy concerns. Real world testing and collaboration with companies should be the next step.
