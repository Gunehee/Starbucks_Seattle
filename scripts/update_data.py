"""
update_data.py
--------------
Fetches the latest Starbucks locations CSV from chrismeller/StarbucksLocations,
filters to Seattle-only stores, then replaces the FEATURES array in map.html.
Runs automatically via GitHub Actions on a daily schedule.
"""

import json
import re
import sys
import requests
import pandas as pd

# ── Configuration ─────────────────────────────────────────────────────────────
CSV_URL = (
    "https://raw.githubusercontent.com/chrismeller/StarbucksLocations"
    "/master/locations.csv"
)

# Keywords in store names used to identify drive-thru locations
DRIVE_THRU_KEYWORDS = ["drive", "drive-thru", "drive thru", "dt"]

# File paths (relative to repository root, where Actions runs)
MAP_HTML_PATH = "map.html"
GEOJSON_PATH  = "assets/Starbucks_Seattle.geojson"


# ── Fetch & filter data ───────────────────────────────────────────────────────
def fetch_seattle(url: str) -> pd.DataFrame:
    print(f"Fetching: {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    from io import StringIO
    df = pd.read_csv(StringIO(resp.text))

    print(f"  Total rows: {len(df)}")
    print(f"  Columns: {list(df.columns)}")

    # Normalize column names (strip whitespace, lowercase, replace spaces)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("/", "_")

    # Filter to Seattle, WA, US only
    mask = (
        df["city"].str.strip().str.lower()           == "seattle"
    ) & (
        df["state_province"].str.strip().str.upper() == "WA"
    ) & (
        df["country"].str.strip().str.upper()        == "US"
    )
    seattle = df[mask].copy()
    print(f"  Seattle rows: {len(seattle)}")

    # Drop rows with missing coordinates
    seattle = seattle.dropna(subset=["longitude", "latitude"])
    print(f"  Seattle rows (with coords): {len(seattle)}")
    return seattle


# ── Determine service type ────────────────────────────────────────────────────
def service_type(row: pd.Series) -> str:
    """
    Infers service type from store name and ownership_type column:
      - If store name contains a drive-thru keyword, classify as 'both'
        (drive-thru stores almost always have in-store service too)
      - Otherwise, classify as 'inStore'
    """
    name_lower = str(row.get("store_name", "")).lower()
    has_dt = any(kw in name_lower for kw in DRIVE_THRU_KEYWORDS)

    ot = str(row.get("ownership_type", "")).lower()
    has_ot_dt = "drive" in ot

    if has_dt or has_ot_dt:
        return "both"
    return "inStore"


# ── Build FEATURES array ──────────────────────────────────────────────────────
def build_features(df: pd.DataFrame) -> list:
    features = []

    # Count duplicate store names so we can disambiguate them
    name_counts: dict = {}
    name_seen:   dict = {}
    for _, row in df.iterrows():
        n = str(row.get("store_name", "Unknown")).strip()
        name_counts[n] = name_counts.get(n, 0) + 1

    for idx, (_, row) in enumerate(df.iterrows()):
        raw_name = str(row.get("store_name", "Unknown")).strip()
        addr     = str(row.get("street_address", "")).strip()
        city_str = str(row.get("city", "Seattle")).strip()
        state    = str(row.get("state_province", "WA")).strip()
        postcode = str(row.get("postcode", "")).strip()
        phone    = str(row.get("phone_number", "")).strip()
        lat      = float(row["latitude"])
        lng      = float(row["longitude"])

        # Disambiguate duplicate store names by appending street address
        if name_counts[raw_name] > 1:
            seen = name_seen.get(raw_name, 0)
            name_seen[raw_name] = seen + 1
            display_name = f"{raw_name} ({addr})" if addr else f"{raw_name} #{seen+1}"
        else:
            display_name = raw_name

        # Offset duplicate coordinates slightly so both markers are clickable
        existing = [f for f in features if
                    abs(f["coords"][1] - lat) < 0.0001 and
                    abs(f["coords"][0] - lng) < 0.0001]
        if existing:
            lat += 0.0003 * len(existing)

        # Build description string compatible with map.html's parseDesc()
        zip5 = postcode[:5] if len(postcode) >= 5 else postcode
        desc_parts = [addr, f"{city_str}, {state} {zip5}".strip()]
        if phone and phone != "nan":
            desc_parts.append(phone)

        features.append({
            "id":          idx,
            "displayName": display_name,
            "description": "<br>".join(p for p in desc_parts if p and p != "nan"),
            "serviceType": service_type(row),
            "coords":      [round(lng, 6), round(lat, 6)],
        })

    return features


# ── Patch map.html ────────────────────────────────────────────────────────────
def patch_map_html(features: list, path: str):
    with open(path, encoding="utf-8") as f:
        html = f.read()

    new_js = json.dumps(features, ensure_ascii=False, separators=(",", ":"))

    # Replace the existing const FEATURES = [...]; block
    pattern = r"(const FEATURES\s*=\s*)\[[\s\S]*?\];"
    replacement = rf"\g<1>{new_js};"
    new_html, n = re.subn(pattern, replacement, html, count=1)

    if n == 0:
        print("ERROR: Could not find FEATURES pattern in map.html. Check file structure.")
        sys.exit(1)

    # Update the store count badge
    count = len(features)
    new_html = re.sub(
        r'id="store-count-badge">[^<]+<',
        f'id="store-count-badge">{count} stores<',
        new_html
    )
    # Update the About section description
    new_html = re.sub(
        r'\d+ Starbucks locations across Seattle',
        f'{count} Starbucks locations across Seattle',
        new_html
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"  map.html updated → {count} features")


# ── Save GeoJSON backup ───────────────────────────────────────────────────────
def save_geojson(features: list, path: str):
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": f["coords"],
                },
                "properties": {
                    "name":        f["displayName"],
                    "description": f["description"],
                    "serviceType": f["serviceType"],
                },
            }
            for f in features
        ],
    }
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(geojson, fp, ensure_ascii=False, indent=2)
    print(f"  GeoJSON saved → {path} ({len(features)} features)")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = fetch_seattle(CSV_URL)

    if len(df) == 0:
        print("No Seattle stores found. Skipping update.")
        sys.exit(0)

    features = build_features(df)
    print(f"\nBuilt {len(features)} features")

    patch_map_html(features, MAP_HTML_PATH)
    save_geojson(features,   GEOJSON_PATH)

    print("\n✓ Update complete")
