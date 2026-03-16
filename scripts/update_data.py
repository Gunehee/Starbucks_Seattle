"""
update_data.py
--------------
매일 chrismeller/StarbucksLocations 에서 최신 CSV를 받아
Seattle 매장만 필터링 → map.html 의 FEATURES 배열을 교체합니다.
"""

import json
import re
import sys
import requests
import pandas as pd

# ── 설정 ──────────────────────────────────────────────────────────────────────
CSV_URL = (
    "https://raw.githubusercontent.com/chrismeller/StarbucksLocations"
    "/master/locations.csv"
)

# 드라이브스루 포함 매장으로 판별할 키워드 (매장명 기준)
DRIVE_THRU_KEYWORDS = ["drive", "drive-thru", "drive thru", "dt"]

# map.html 경로 (Actions 실행 시 저장소 루트 기준)
MAP_HTML_PATH = "map.html"
GEOJSON_PATH  = "assets/Starbucks_Seattle.geojson"


# ── 데이터 가져오기 ────────────────────────────────────────────────────────────
def fetch_seattle(url: str) -> pd.DataFrame:
    print(f"Fetching: {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    from io import StringIO
    df = pd.read_csv(StringIO(resp.text))

    print(f"  Total rows: {len(df)}")
    print(f"  Columns: {list(df.columns)}")

    # 컬럼명 정규화 (공백·대소문자 허용)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("/", "_")

    # Seattle, WA, US 필터
    mask = (
        df["city"].str.strip().str.lower()             == "seattle"
    ) & (
        df["state_province"].str.strip().str.upper()   == "WA"
    ) & (
        df["country"].str.strip().str.upper()          == "US"
    )
    seattle = df[mask].copy()
    print(f"  Seattle rows: {len(seattle)}")

    # 좌표 없는 행 제거
    seattle = seattle.dropna(subset=["longitude", "latitude"])
    print(f"  Seattle rows (with coords): {len(seattle)}")
    return seattle


# ── 서비스 타입 판별 ───────────────────────────────────────────────────────────
def service_type(row: pd.Series) -> str:
    """
    chrismeller CSV 는 ownership_type 컬럼으로 구분:
      - 'Licensed' / 'Company Owned' 등
    매장명에 드라이브스루 키워드가 있으면 우선 적용.
    """
    name_lower = str(row.get("store_name", "")).lower()
    has_dt = any(kw in name_lower for kw in DRIVE_THRU_KEYWORDS)

    # ownership_type 에 Drive 언급이 있으면 driveThru 또는 both
    ot = str(row.get("ownership_type", "")).lower()
    has_ot_dt = "drive" in ot

    if has_dt or has_ot_dt:
        return "both"   # 드라이브스루가 있으면 보통 인스토어도 있음
    return "inStore"


# ── FEATURES 배열 생성 ─────────────────────────────────────────────────────────
def build_features(df: pd.DataFrame) -> list:
    features = []

    # 이름 중복 처리 (주소 뒤에 괄호로 구분)
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

        # 중복 이름 구분
        if name_counts[raw_name] > 1:
            seen = name_seen.get(raw_name, 0)
            name_seen[raw_name] = seen + 1
            display_name = f"{raw_name} ({addr})" if addr else f"{raw_name} #{seen+1}"
        else:
            display_name = raw_name

        # 좌표 중복 → 미세하게 offset (같은 위치 두 번째 이후)
        coord_key = (round(lat, 6), round(lng, 6))
        # (간단 구현: features 안에서 이미 있는지 확인)
        existing = [f for f in features if
                    abs(f["coords"][1] - lat) < 0.0001 and
                    abs(f["coords"][0] - lng) < 0.0001]
        if existing:
            lat += 0.0003 * len(existing)

        # description 포맷 (기존 map.html parseDesc 와 호환)
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


# ── map.html FEATURES 교체 ────────────────────────────────────────────────────
def patch_map_html(features: list, path: str):
    with open(path, encoding="utf-8") as f:
        html = f.read()

    new_js = json.dumps(features, ensure_ascii=False, separators=(",", ":"))

    # const FEATURES = [...]; 패턴을 교체
    pattern = r"(const FEATURES\s*=\s*)\[[\s\S]*?\];"
    replacement = rf"\g<1>{new_js};"
    new_html, n = re.subn(pattern, replacement, html, count=1)

    if n == 0:
        print("ERROR: FEATURES 패턴을 찾지 못했습니다. map.html 구조를 확인하세요.")
        sys.exit(1)

    # 스토어 개수 뱃지도 업데이트
    count = len(features)
    new_html = re.sub(
        r'id="store-count-badge">[^<]+<',
        f'id="store-count-badge">{count} stores<',
        new_html
    )
    # About 섹션 문구도 업데이트
    new_html = re.sub(
        r'\d+ Starbucks locations across Seattle',
        f'{count} Starbucks locations across Seattle',
        new_html
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"  map.html updated → {count} features")


# ── GeoJSON 저장 (assets/ 백업용) ─────────────────────────────────────────────
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


# ── 메인 ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = fetch_seattle(CSV_URL)

    if len(df) == 0:
        print("Seattle 매장이 0개입니다. 업데이트를 건너뜁니다.")
        sys.exit(0)

    features = build_features(df)
    print(f"\nBuilt {len(features)} features")

    patch_map_html(features, MAP_HTML_PATH)
    save_geojson(features,   GEOJSON_PATH)

    print("\n✓ 업데이트 완료")
