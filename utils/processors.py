"""Processing functions for different report types"""

import re

import pandas as pd

# Mailing list segments
MAILING_LISTS = {
    "PNW": {"WA", "OR", "WY", "ID", "MT"},
    "CA": {"CA"},
    "GG": {"NM", "NV", "UT", "CO", "AZ", "LA", "TX", "AR", "OK"},
}

# All allowed states (union of all mailing lists)
ALLOWED_STATES = set().union(*MAILING_LISTS.values())


def process_contacts(df, segment_by_region=False):
    """Process contacts dataframe with validation and formatting

    Args:
        df: pandas DataFrame with contact data
        segment_by_region: If True, returns dict of {region: df}. If False, returns single df with all regions

    Returns:
        If segment_by_region=False: Processed pandas DataFrame with cleaned contact data
        If segment_by_region=True: Dict of {region_name: dataframe} for each mailing list segment
    """
    # Delete all columns that contain "ID" in their name
    columns_to_delete = [col for col in df.columns if "ID" in col]
    df = df.drop(columns=columns_to_delete, errors="ignore")

    # Combine Phone and Mobile into single Phone column
    if "Phone" in df.columns and "Mobile" in df.columns:
        df["Phone"] = df["Phone"].fillna(df["Mobile"])
        df = df.drop(columns=["Mobile"])
    elif "Mobile" in df.columns:
        df = df.rename(columns={"Mobile": "Phone"})

    # Parse Business Address column
    if "Business Address" in df.columns:
        address_parts = df["Business Address"].str.split(" / ")

        def get_second_to_last(parts):
            if not isinstance(parts, list) or len(parts) < 2:
                return None
            return parts[-2].strip()

        city_state_zip = address_parts.apply(get_second_to_last)

        parsed = city_state_zip.str.rsplit(n=2, expand=True)

        if parsed.shape[1] == 3:

            def validate_city(val):
                if pd.isna(val) or not isinstance(val, str):
                    return None
                val = val.strip()
                if len(val) > 2 and not any(char.isdigit() for char in val):
                    return val
                return None

            def validate_state(val):
                if pd.isna(val) or not isinstance(val, str):
                    return None
                val = val.strip()
                if len(val) == 2 and val.isalpha():
                    return val
                return None

            def validate_zip(val):
                if pd.isna(val) or not isinstance(val, str):
                    return None
                val = val.strip()
                if re.match(r"^\d{5}", val):
                    return val
                return None

            df["City"] = parsed[0].apply(validate_city)
            df["State"] = parsed[1].apply(validate_state)
            df["Zip"] = parsed[2].apply(validate_zip)

        df = df.drop(columns=["Business Address"])

    # Filter to only include allowed states
    if "State" in df.columns:
        df = df[df["State"].isin(ALLOWED_STATES)]

    # Return segmented by region or as single dataframe
    if segment_by_region and "State" in df.columns:
        segments = {}
        for region_name, states in MAILING_LISTS.items():
            region_df = df[df["State"].isin(states)].copy()
            if len(region_df) > 0:  # Only include regions with contacts
                segments[region_name] = region_df
        return segments

    return df


def process_visits(df):
    """Process visits dataframe by removing unnecessary columns

    Args:
        df: pandas DataFrame with visit data

    Returns:
        Processed pandas DataFrame with cleaned visit data
    """
    columns_to_delete = [
        "ID",
        "Status",
        "Scheduled End Date/Time",
        "Organizer Details_Organizer",
        "Visit Type Code",
        "Visit Type",
        "Sales Organization Details_Sales Organization",
        "Distribution Channel Code",
        "Distribution Channel",
        "Division Code",
        "Division",
        "Location",
        "Technical ID",
    ]
    df = df.drop(columns=columns_to_delete, errors="ignore")
    return df
