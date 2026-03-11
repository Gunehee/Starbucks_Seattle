# Starbucks in Seattle — Interactive Location Finder

**A geospatial web application mapping all 102 Starbucks locations across Seattle, WA.**  
Filter by service type, search by store name or address, and navigate directly to any location.

🔗 **Live Demo: [https://gunehee.github.io/Starbucks_Seattle/](https://gunehee.github.io/Starbucks_Seattle/)**

---

## Overview

Seattle is home to more Starbucks locations per capita than any other U.S. city — the birthplace of the brand. With over 100 locations across the city and an estimated 2,000+ employees, Starbucks is deeply embedded in Seattle's daily life and urban landscape.

This project visualizes those locations through an interactive web map built with Leaflet.js, allowing users to explore stores by service type, search by neighborhood or address, and access store-specific details including hours of operation and phone numbers.

---

## Features

- **Service type filtering** — Toggle between All Stores, In-Store Only, Drive-Thru Only, and In-Store & Drive-Thru
- **Real-time search** — Instantly filter the map and store list by name or address as you type
- **Alphabetical store list** — Scrollable sidebar listing all currently visible locations
- **Store detail panel** — Slide-in panel displaying address, phone number, and hours of operation for each selected store
- **Fly-to animation** — Map smoothly pans and zooms to any selected location
- **Google Maps integration** — One-click directions from any store detail view
- **Dynamic store count** — Badge updates in real time to reflect the active filter and search state
- **Zero-dependency deployment** — No API key, no server required; runs directly from a single HTML file

---

## Dataset

**Source:** [Starbucks Locations Worldwide 2021 — Kaggle](https://www.kaggle.com/datasets/kukuroo3/starbucks-locations-worldwide-2021-version?resource=download)

The source dataset contains Starbucks locations worldwide as of 2021. The following cleaning steps were applied to produce the project dataset:

- Filtered to `city = Seattle` and `country_code = US`
- Removed columns not relevant to the map: brand, ownership type, timezone, and phone country code
- Removed rows with null or malformed coordinate values
- Normalized ZIP codes from ZIP+4 format (e.g., `981162812`) to standard 5-digit ZIP (e.g., `98116`)
- Exported as four GeoJSON files segmented by service type for use in layer filtering

**Final dataset:** 102 store locations across Seattle

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
| [CartoDB Voyager](https://carto.com/basemaps/) | Base map tile layer |
| GeoJSON | Store location and attribute data |
| Vanilla JavaScript (ES6+) | Application logic and interactivity |
| CSS3 | Layout, animations, and theming |
| [Google Maps Directions](https://developers.google.com/maps/documentation/urls/get-started) | External directions link (no key required) |

All dependencies are loaded via CDN. No build tools, no framework, no API key.

---

## Repository Structure

```
Starbucks_Seattle/
├── index.html                    # Complete single-file application
├── README.md                     # Project documentation
├── Starbucks_Cleaned.csv         # Cleaned source dataset
├── Starbucks_Seattle.geojson     # All 102 store locations
├── in_store.geojson              # In-store only
├── drive_thru.geojson            # Drive-thru only
└── both.geojson                  # In-store & drive-thru
```

All HTML, CSS, and JavaScript are contained within `index.html`. All GeoJSON data is embedded inline — no external file requests are made at runtime.

---

## Team

This project was developed as a group assignment for **GEOG 495: Digital Geographies** at the **University of Washington**.

| Contributor | Responsibilities |
|---|---|
| **Gunhee** | Geocoder, sidebar panel, project rebuild and deployment |
| **Haochen** | Layer toggle logic, GeoJSON data loading |
| **Sophia L.** | Map frame, interactive feature implementation |
| **Sophia S.** | Data collection, cleaning, and GeoJSON export |

---

## Acknowledgements

Special thanks to **Professor Bo Zhao** and **Teaching Assistant Steven Bao** at the University of Washington for their guidance, feedback, and support throughout this project.

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

*GEOG 495 — Digital Geographies · University of Washington · Seattle, WA*
