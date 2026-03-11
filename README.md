# ☕ Starbucks in Seattle — Interactive Location Finder

> An interactive web map of all 102 Starbucks locations in Seattle, WA.  
> Filter by service type, search by name or address, and get directions to any store.

🔗 **[Live Demo → https://Gunehee.github.io/Starbucks_Seattle/](https://Gunehee.github.io/Starbucks_Seattle/)**

![Main View](img/ss1.png)
![Store Detail](img/ss2.png)

---

## Project Structure

```
Starbucks_Seattle/
├── index.html                  # ✅ Single-file app (HTML + CSS + JS, all inline)
├── README.md
├── Starbucks_Cleaned.csv       # Original cleaned dataset (source of truth)
├── Starbucks_Seattle.geojson   # All 102 stores
├── in_store.geojson            # In-store only locations
├── drive_thru.geojson          # Drive-thru only locations
└── both.geojson                # Stores with both services
```

> **Note:** The `scripts/` and `img/` folders have been removed.  
> All CSS and JavaScript are now embedded directly in `index.html`.  
> All GeoJSON data is also inlined — no server or file fetching required.

---

## Features

- **4 service-type filters** — All Stores / In-Store / Drive-Thru / In-Store & Drive-Thru
- **Live search** — Filter by store name or address in real time
- **Store list panel** — All visible stores listed alphabetically with scroll
- **Store detail panel** — Address, phone number, and hours on click
- **Google Maps integration** — "Get Directions" button on every store
- **Fly-to animation** — Map smoothly zooms to selected store
- **Store count badge** — Updates dynamically with active filter
- **Fully offline capable** — No API key, no server needed; open `index.html` directly in any browser

---

## Dataset

**Source:** [Starbucks Locations Worldwide (Kaggle)](https://www.kaggle.com/datasets/kukuroo3/starbucks-locations-worldwide-2021-version?resource=download)

The original dataset contained worldwide Starbucks locations (2021). We cleaned and filtered it to Seattle only:

- Removed unnecessary columns, keeping name, coordinates, address, phone, and hours
- Removed rows with missing or null values
- Filtered to `city = Seattle`, `country = US`
- Split into four GeoJSON files by service type for layer filtering

---

## Resources

- [Seattle \| Starbucks Reserve Roastery](https://www.youtube.com/watch?v=s6AgzclRCJE)
- [Your Seattle Starbucks Checklist](http://www.starbucksmelody.com/2018/11/24/starbucks-checklist/)
- [Starbucks Dominates Seattle's Coffee Market](https://www.thecommonscafe.com/starbucks-dominates-the-coffee-market-in-seattle/)
- [Starbucks: A Legendary Washington State Business Since 1971](http://choosewashingtonstate.com/success-stories/starbucks/)

---
