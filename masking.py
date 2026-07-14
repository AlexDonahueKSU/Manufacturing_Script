"""
Handles some basic logic around how we plan to mask, I know this 
likely is going to change but based on how I've inputted I'll 
get some basic masking handled.
"""
import hashlib

def mask_data(record):
    if record[4] == "Keep":
        keep_mask(record)
    elif record[4] == "Block":
        block_mask(record)
    elif record[4] == "Placeholder Mask":
        placeholder_mask(record)
    elif record[4] == "Generalize":
        generalize_mask(record)
    elif record[4] == "Hash Pseudonymize":
        hash_mask(record)

def keep_mask(record):
    record[5] = record[1]  

def block_mask(record):
    record[5] = "[BLOCKED]"

def placeholder_mask(record):
    record[5] = "[" + record[1].upper().replace(" ","_") + "]"

def generalize_mask(record):
    record[5] = "Placeholder generalized value"

def hash_mask(record):
    #Convert to bytes
    raw_value = str(record[2]).encode("utf-8")
    digest = hashlib.sha256(raw_value).hexdigest()

    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    value = int(digest[:8], 16)

    token = ""
    for _ in range(4):
        value, remainder = divmod(value, 36)
        token = alphabet[remainder] + token

    record[5] = f"[{record[1].split(' ', 1)[0].upper()}_{token}]"
