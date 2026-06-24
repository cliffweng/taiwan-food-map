# 🗺️ Taiwan Gourmet Map 台灣美食地圖

An interactive map of Taiwan's best food, bars, and coffee — compiled from four authoritative sources and hosted as a Streamlit web app. Also exports a Google My Maps–ready CSV.

**Live demo:** run locally with `streamlit run src/app.py`

![Taiwan Gourmet Map screenshot](https://raw.githubusercontent.com/placeholder/taiwan_food_map/main/docs/screenshot.png)

---

## Data Sources

| Source | Year | Entries |
|--------|------|---------|
| [Michelin Guide Taiwan](https://guide.michelin.com/tw/en) | 2025 | 436 |
| [500碗 Award](https://500times.udn.com/wtimes/story/123497/8874123) | 2025 (3rd edition) | 79 |
| [Asia's 50 Best Bars](https://www.theworlds50best.com/bars/asia/list/1-50) | 2025 | 10 |
| [World's 100 Best Coffee Shops](https://www.timeout.com/asia/news/worlds-100-best-coffee-shops-2026-14-asian-cafes-make-the-global-list-021926) | 2026 | 7 |
| **Total** | | **532** |

### Breakdown by category

| Category | Count | Description |
|----------|-------|-------------|
| ⭐⭐⭐ Michelin 3 Stars | 3 | Le Palais, Taïrroir, JL STUDIO |
| ⭐⭐ Michelin 2 Stars | 7 | Eika, Restaurant A, Yu Kapo, logy, Mudan, L'Atelier de Joël Robuchon, Molino de Urdániz |
| ⭐ Michelin 1 Star | 43 | Across Taipei, Taichung, Kaohsiung |
| 🍽️ Bib Gourmand | 143 | Good value picks across Taiwan |
| 📍 Michelin Selected | 240 | Recommended restaurants |
| 🍜🍜🍜 500碗 3 Bowls | 5 | Highest-rated street food |
| 🍜🍜 500碗 2 Bowls | 13 | Top street food picks |
| 🍜 500碗 1 Bowl | 61 | Curated 1-bowl winners across all regions |
| 🍸 Asia's 50 Best Bars | 10 | Vender #20, The Public House #40, Moonrock #42… |
| ☕ World's 100 Best Coffee | 4 | Coffee Sind #36, KEEP Coffee #46, Tomorrow Coffee #57… |
| ☕ Notable Coffee | 3 | Simple Kaffa (2016 World Barista Champion), VWI by CHADWANG |

**Coverage:** 20 cities/counties — Taipei, New Taipei, Keelung, Taoyuan, Hsinchu, Taichung, Changhua, Yunlin, Chiayi, Tainan, Kaohsiung, Pingtung, Yilan, Hualien, Taitung, Penghu, Matsu, and more.

---

## Features

- **Interactive folium map** with color-coded, icon-based markers for each category
- **Layer control** to toggle individual categories on/off
- **Sidebar filters**: source, category/rating, city, cuisine/name search
- **Stats bar** showing live counts per category
- **Restaurant list** (expandable table with all visible entries)
- **CSV download** of any filtered view
- **Google My Maps CSV** (`src/data/restaurants_mymaps.csv`) for import into My Maps

---

## Quick Start

```bash
# 1. Clone and enter the project
git clone <repo-url>
cd taiwan_food_map

# 2. Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Run the app
streamlit run src/app.py
# → opens at http://localhost:8501
```

---

## Google My Maps Import

1. Go to [mymaps.google.com](https://mymaps.google.com) → **Create a new map**
2. Click **Import** on a new layer
3. Upload `src/data/restaurants_mymaps.csv`
4. Set **Latitude** and **Longitude** columns for location
5. Set **Name** column for place titles
6. After import, use **Style by data column → Category** to color-code by source

---

## Deploy to Streamlit Cloud (free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Point to `src/app.py`
4. Deploy — no additional configuration needed

---

## Project Structure

```
taiwan_food_map/
├── src/
│   ├── app.py                    # Streamlit application
│   └── data/
│       ├── restaurants.json      # Full dataset (532 entries)
│       └── restaurants_mymaps.csv # Google My Maps import file
├── tests/
│   └── test_data.py              # Dataset validation tests
├── .streamlit/
│   └── config.toml               # Theme configuration
├── requirements.txt
├── CLAUDE.md
└── README.md
```

---

## Data Schema (`restaurants.json`)

Each entry contains:

```json
{
  "id": 1,
  "name": "Le Palais",
  "name_zh": "頤宮",
  "source": "michelin",
  "award": "3 Stars",
  "category": "Michelin 3 Stars",
  "rating_value": 3,
  "cuisine": "Cantonese",
  "city": "Taipei",
  "address": "17F, Palais de Chine Hotel, 3, Section 1, Chengde Road, Datong District, Taipei",
  "lat": 25.0491625,
  "lon": 121.5168892,
  "phone": "+886221819985",
  "michelin_url": "https://guide.michelin.com/...",
  "website": "https://...",
  "green_star": false,
  "price": "$$$",
  "description": "..."
}
```

`source` values: `michelin` · `500bowl` · `bar` · `coffee`

---

## Sources & Credits

- **Michelin data**: pulled from [ngshiheng/michelin-my-maps](https://github.com/ngshiheng/michelin-my-maps) (open dataset with coordinates)
- **500碗 2025**: [500輯 × 聯合報](https://500times.udn.com) — Taiwan's grassroots street food award (50 judges, no weighting)
- **Asia's 50 Best Bars 2025**: [theworlds50best.com](https://www.theworlds50best.com/bars/asia/list/1-50)
- **World's 100 Best Coffee Shops 2026**: [Kerry / Beverage Trade Network](https://www.kerry.com)
