import pandas as pd

def extract_json_hierarchy(df):
    """Dynamically extracts hierarchy structure based on non-empty columns and includes all relevant details."""
    result = {}

    # Get column headers
    headers = df.columns.tolist()

    # Detect hierarchy start and end
    start_idx = next((i for i, col in enumerate(headers) if pd.notna(col) and str(col).strip()), None)
    end_idx = headers.index("Source Occurs") if "Source Occurs" in headers else None

    if start_idx is None or end_idx is None or start_idx >= end_idx:
        print("⚠️ Could not determine hierarchy columns correctly.")
        return {}

    hierarchy_columns = headers[start_idx:end_idx]  # Get only hierarchy-related columns
    attribute_columns = headers[end_idx:]  # All columns after "Source Occurs" are attributes

    for _, row in df.iterrows():
        # Extract non-empty hierarchy levels dynamically
        levels = [str(row[col]).strip() for col in hierarchy_columns if str(row[col]).strip()]

        if not levels:
            continue  # Skip rows without valid hierarchy

        current_level = result

        for level in levels[:-1]:  # Traverse or create nested levels
            current_level = current_level.setdefault(level, {})

        last_level = levels[-1]
        attributes = {
            header: str(row[header]).strip().replace("\u2026", "...")  # Fix ellipsis issue
            for header in attribute_columns if pd.notna(row[header]) and str(row[header]).strip()
        }

        if last_level not in current_level:
            current_level[last_level] = {}

        current_level[last_level].update(attributes)  # Attach attributes at the last level

    # If there's a single root key like {"JSON": {...}}, unwrap it
    if len(result) == 1:
        return next(iter(result.values()))

    return result

def extract_edi_x12_hierarchy(df):
    """Extracts hierarchy for EDI-X12 format."""
    hierarchy = {}
    headers = df.columns.tolist()[10:]

    for _, row in df.iterrows():
        segment = row[0]  # First column contains segment (ISA, GS, ST, etc.)
        elements = {header: str(row[header]) if pd.notna(row[header]) else "" for header in headers}

        if segment:
            hierarchy[segment] = elements

    return hierarchy

def extract_edifact_hierarchy(df):
    """Extracts hierarchy for EDIFACT format."""
    hierarchy = {}
    headers = df.columns.tolist()[10:]

    for _, row in df.iterrows():
        segment = row[0]  # First column contains segment (UNB, UNH, UNT, etc.)
        elements = {header: str(row[header]) if pd.notna(row[header]) else "" for header in headers}

        if segment:
            hierarchy[segment] = elements

    return hierarchy

def extract_idoc_hierarchy(df):
    """Extracts hierarchy for IDOC format."""
    hierarchy = {}
    headers = df.columns.tolist()[10:]

    for _, row in df.iterrows():
        segment = row[0]  # First column contains segment (E1EDK01, E1EDP01, etc.)
        elements = {header: str(row[header]) if pd.notna(row[header]) else "" for header in headers}

        if segment:
            hierarchy[segment] = elements

    return hierarchy
