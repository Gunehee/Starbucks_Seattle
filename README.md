<div align="center">

# ☕ Starbucks in Seattle
### Interactive Location Finder

**A geospatial web application mapping all 102 Starbucks locations across Seattle, WA.**  
Filter by service type, search by address, and get directions — all from a single file with no API key.

<br>

<!-- ── DEMO BUTTONS ── -->
<a href="https://htmlpreview.github.io/?https://github.com/Gunehee/Starbucks_Seattle/blob/main/index.html">
  <img src="https://img.shields.io/badge/📄%20View%20Project%20Page-1A6335?style=for-the-badge&logoColor=white" alt="Project Page" height="44">
</a>
&nbsp;&nbsp;
<br><br>
</div>

---

## Overview

Seattle is home to more Starbucks locations per capita than any other U.S. city — the birthplace of the brand. With over 100 locations across the city and an estimated 2,000+ employees, Starbucks is deeply embedded in Seattle's daily life and urban landscape.

This project visualizes those locations through an interactive web map built with Leaflet.js, allowing users to explore stores by service type, search by neighborhood or address, and access store-specific details including hours of operation and phone numbers.

> **[→ Open the interactive map](https://htmlpreview.github.io/?https://github.com/Gunehee/Starbucks_Seattle/blob/main/map.html)** to explore all 102 locations now.

---

## Features

| Feature | Description |
|---|---|
| **Service Type Filtering** | Toggle between All Stores, In-Store Only, Drive-Thru Only, and In-Store & Drive-Thru |
| **Real-Time Search** | Instantly filter the map and store list by name or address as you type |
| **Alphabetical Store List** | Scrollable sidebar listing all visible locations — click any to fly the map there |
| **Store Detail Panel** | Slide-in panel with address, phone, hours, and service type for each store |
| **Fly-To Animation** | Map smoothly pans and zooms to any selected store |
| **Google Maps Integration** | One-click "Get Directions" button in every store detail view |
| **Dynamic Store Count** | Badge updates in real time with the active filter and search state |
| **Zero-Dependency Deploy** | No API key, no server — open `map.html` directly in any modern browser |

---

## Dataset

**Source:** [Starbucks Locations Worldwide 2021 — Kaggle](https://www.kaggle.com/datasets/kukuroo3/starbucks-locations-worldwide-2021-version?resource=download)

The source dataset contains worldwide Starbucks locations as of 2021. Cleaning steps applied:

1. **Filter** — Isolated rows where `city = Seattle` and `country_code = US`
2. **Clean** — Removed 5 irrelevant columns; dropped rows with null coordinate values
3. **Normalize** — Converted ZIP+4 codes (e.g., `981162812`) to standard 5-digit ZIP (e.g., `98116`)
4. **Segment** — Exported four GeoJSON files split by service type for layer filtering

**Final dataset: 102 store locations across Seattle**

| File | Description | Count |
|---|---|---|
| `Starbucks_Seattle.geojson` | All store locations | 102 |
| `in_store.geojson` | In-store service only | 85 |
| `drive_thru.geojson` | Drive-thru service only | 2 |
| `both.geojson` | Both in-store and drive-thru | 15 |

---

## Tech Stack

| Technology | Role |
|---|---|
| [Leaflet.js v1.9.4](https://leafletjs.com/) | Interactive map rendering |
| [CartoDB Voyager](https://carto.com/basemaps/) | Base map tile layer (no API key) |
| GeoJSON | Store location and attribute data, embedded inline |
| Vanilla JavaScript (ES6+) | Filtering, search, and all interactivity |
| CSS3 | Layout, animations, and Starbucks-themed design |
| [Google Maps URLs](https://developers.google.com/maps/documentation/urls/get-started) | Directions deep link (no key required) |

All dependencies load via CDN. No build tools, no framework, no API key required.

---

## Repository Structure

```
Starbucks_Seattle/
├── index.html                    # Portfolio landing page
├── map.html                      # Interactive map application  ← main demo
├── README.md
├── Starbucks_Cleaned.csv         # Cleaned source dataset
├── Starbucks_Seattle.geojson     # All 102 store locations
├── in_store.geojson
├── drive_thru.geojson
└── both.geojson
```

`map.html` is the standalone interactive map — all CSS, JS, and GeoJSON data are embedded inline. `index.html` is the portfolio overview page.

---

## Running Locally

```bash
git clone https://github.com/Gunehee/Starbucks_Seattle.git
cd Starbucks_Seattle
open map.html        # launch the interactive map directly
open index.html      # open the portfolio landing page
```

No install steps. No local server required.

---

## Team

Developed a **Digital Geographies** at the **University of Washington**.

| Contributor | Responsibilities |
|---|---|
| **Gunhee** | Geocoder, sidebar panel, project rebuild and deployment |
| **Haochen** | Layer toggle logic, GeoJSON data loading |
| **Sophia L.** | Map frame, interactive feature implementation |
| **Sophia S.** | Data collection, cleaning, and GeoJSON export |

---

## References

**Data**
- Kukuroo3. (2021). *Starbucks Locations Worldwide 2021 Version*. Kaggle. https://www.kaggle.com/datasets/kukuroo3/starbucks-locations-worldwide-2021-version

**Libraries**
- Agafonkin, V. (2010). *Leaflet.js* (v1.9.4). https://leafletjs.com/
- CARTO. (n.d.). *Voyager Basemap Tiles*. https://carto.com/basemaps/

**Context & Background**
- Starbucks. (n.d.). *Our Heritage*. https://www.starbucks.com/about-us/our-heritage/
- Seattle Metropolitan. (2015, August). *Every Single Starbucks in Seattle, Ranked*. https://www.seattlemet.com/eat-and-drink/2015/08/every-single-starbucks-in-seattle-ranked
- The Commons Cafe. (n.d.). *Starbucks Dominates the Coffee Market in Seattle*. https://www.thecommonscafe.com/starbucks-dominates-the-coffee-market-in-seattle/
- Starbucks Melody. (2018, November). *Your Seattle Starbucks Checklist*. http://www.starbucksmelody.com/2018/11/24/starbucks-checklist/
- Choose Washington State. (n.d.). *Starbucks: A Legendary Washington State Business Since 1971*. http://choosewashingtonstate.com/success-stories/starbucks/
- Condé Nast Traveler. (n.d.). *Starbucks Reserve Roastery, Seattle*. https://www.cntraveler.com/bars/seattle/starbucks-reserve-roastery

---
