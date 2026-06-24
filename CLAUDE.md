# Taiwan Food Map

Interactive gourmet map combining Michelin Guide Taiwan 2025 and 500碗 2025 award data.

## Stack
- Python 3.11+
- Streamlit (frontend + server)
- Folium (interactive maps via leaflet.js)
- Pandas (data)

## Commands
```bash
# Install deps
pip install -r requirements.txt

# Run locally
streamlit run src/app.py

# Deploy to Streamlit Cloud
# Push to GitHub, connect at share.streamlit.io
```

## Data
- `src/data/restaurants.json` — 454 restaurants (Michelin + 500碗)
- `src/data/restaurants_mymaps.csv` — Google My Maps import file

### Sources
- Michelin 2025: ngshiheng/michelin-my-maps (GitHub) — 436 Taiwan restaurants
  - 3 Stars: Le Palais, Taïrroir, JL STUDIO
  - 2 Stars: Eika, Restaurant A, Yu Kapo, logy, Mudan, L'Atelier de Joël Robuchon, Molino de Urdániz
  - 1 Star: 43 restaurants across Taipei, Taichung, Kaohsiung
  - Bib Gourmand: 143 restaurants
- 500碗 2025 (3rd edition): 18 top winners manually curated (3-bowl + 2-bowl)

## Google My Maps
Import `src/data/restaurants_mymaps.csv` at mymaps.google.com:
1. Create new map
2. Import CSV layer
3. Set latitude/longitude columns
4. Style by Category column
