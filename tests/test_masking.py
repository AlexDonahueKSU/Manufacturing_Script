import masking


def test_block_mask():
    record = ["1", "Customer/Order Information", "Order 123", "Sensitive", "Block", ""]

    masking.mask_data(record)

    assert record[5] == "[BLOCKED]"


def test_placeholder_mask():
    record = ["1", "Operator Name", "Jane Doe", "Sensitive", "Placeholder Mask", ""]

    masking.mask_data(record)

    assert record[5] == "[OPERATOR_NAME]"


def test_hash_mask_does_not_expose_raw_value():
    raw_value = "Supplier-E21"
    record = ["1", "Supplier ID", raw_value, "Sensitive", "Hash Pseudonymize", ""]

    masking.mask_data(record)

    assert record[5].startswith("[SUPPLIER_")
    assert raw_value not in record[5]


def test_generalize_percentage():
    record = ["1", "Defect Rate", "5.70%", "Sensitive", "Generalize", ""]

    masking.mask_data(record)

    assert record[5] == "5-10%"
