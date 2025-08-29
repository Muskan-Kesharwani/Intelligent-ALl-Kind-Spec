import os
import json
import pandas as pd
from extractor import extract_json_hierarchy, extract_edi_x12_hierarchy, extract_edifact_hierarchy, extract_idoc_hierarchy
from detector import detect_format

# Get the current script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to config.json
CONFIG_PATH = os.path.join(BASE_DIR, "..", "config", "config.json")

# Load Config
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

# Read paths from config
INPUT_PATH = config["input_path"]
OUTPUT_PATH = config["output_path"]

print(f"📂 Input Path: {INPUT_PATH}")
print(f"📂 Output Path: {OUTPUT_PATH}")

def process_excel():
    """Reads Excel file and generates JSON based on format detection."""
    xls = pd.ExcelFile(INPUT_PATH)
    df = xls.parse(sheet_name=2, skiprows=13, dtype=str,engine="openpyxl")  # Sheet 3, starting from row 12
    df.fillna("", inplace=True)

    detected_format = detect_format(df, INPUT_PATH)

    # Select the correct extractor function
    extractors = {
        "JSON": extract_json_hierarchy,
        "EDI-X12": extract_edi_x12_hierarchy,
        "EDIFACT": extract_edifact_hierarchy,
        "IDOC": extract_idoc_hierarchy,
    }

    hierarchy = extractors[detected_format](df)

    # Save output
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    output_file = os.path.join(OUTPUT_PATH, f"{detected_format}_structure.json")

    with open(output_file, "w") as f:
     json.dump({"format": detected_format, **hierarchy}, f, indent=4)

    print(f"✅ Processed and saved: {output_file}")

if __name__ == "__main__":
    process_excel()
