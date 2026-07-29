"""
Handles some basic logic around how we plan to mask, I know this 
likely is going to change but based on how I've inputted I'll 
get some basic masking handled.
"""
import hashlib
import re
import math

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
    field = record[1].lower()
    if field == "defect severity":
        severity = record[2].lower()
        if "minor" in severity or "cosmetic" in severity:
            record[5] = "[LOW_SEVERITY]"
        elif "major" in severity or "critical" in severity:
            record[5] = "[HIGH_SEVERITY]"
    else:
        record[5] = "[" + record[1].upper().replace(" ","_") + "]"

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

def generalize_mask(record):

    field = record[1].strip().lower()
    value = str(record[2])

    if "rate" in field and "%" in value:
        record[5] = generalize_percentage(value)
    elif any(term in field for term in ["parameter", "temperature", "pressure", "force", "torque", "speed"]):
        record[5] = generalize_measurement(value)
    elif "note" in field or "action" in field:
        record[5] = generalize_text(value)
    elif "metadata" in field:
        record[5] = "Industrial camera image"
    else:
        record[5] = "Generalized value"


# Generalize mask helper functions
def generalize_percentage(value):
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", value)
    if not m:
        return "Generalized percentage"
    n = float(m.group(1))
    upper = math.ceil(n / 5.0) * 5
    return f"{max(5, upper - 5)}-{upper}%"


def generalize_measurement(value):
    #Regex for finding measurement values
    measurement = re.search(r"(\d+(?:\.\d+)?)\s*([A-Za-z°%/]+)", value)
    
    if not measurement:
        print(value)
        print(measurement)
        return "Generalized measurement"

    n = float(measurement.group(1))
    unit = measurement.group(2)

    if n < 100:
        step = 5
    elif n < 1000:
        step = 50
    else:
        step = 100

    lower = int(math.floor(n / step) * step)
    upper = int(math.ceil(n / step) * step)

    return f"{lower}-{upper} {unit}"


def generalize_text(value):
    val = value.lower()
    if "lubrication" in val:
        return error_observed_handler("lubrication")
    if "coolant" in val:
        return error_observed_handler("coolant")
    if "weld" in val:
        return error_observed_handler("weld")
    if "spindle" in val:
        return error_observed_handler("spindle")
    if "viscosity" in val:
        return error_observed_handler("batch viscosity")
    if "pressure" in val:
        return error_observed_handler("pressure")
    if "conveyor" in val:
        return error_observed_handler("conveyer")
    if "wear" in val:
        return "Mechanical wear observed"
    if "corrosion" in val:
        return "Corrosion observed"
    if "calibrat" in val:
        return error_observed_handler("calibration")
    if "rail" in val:
        return error_observed_handler("rail")
    if "die" in val:
        return error_observed_handler("die")
    if "replace" in val or "recalibrate" in val:
        return "Maintenance action required"
    return "Generalized operational issue"

def error_observed_handler(value):
    return value.capitalize() + " error observed"
