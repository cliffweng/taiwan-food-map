import json
import math
from pathlib import Path

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Taiwan Gourmet Map 台灣美食地圖",
    page_icon="🍜",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "restaurants.json"

CATEGORY_COLORS = {
    "Michelin 3 Stars": "#FFD700",
    "Michelin 2 Stars": "#C0C0C0",
    "Michelin 1 Star": "#CD7F32",
    "Bib Gourmand": "#E74C3C",
    "Selected": "#3498DB",
    "500碗 3 Bowls": "#8E44AD",
    "500碗 2 Bowls": "#E67E22",
    "500碗 1 Bowl": "#27AE60",
    "Asia's 50 Best Bars": "#1ABC9C",
    "World's 100 Best Coffee": "#795548",
    "Notable Coffee": "#A0522D",
}

CATEGORY_ICONS = {
    "Michelin 3 Stars": "star",
    "Michelin 2 Stars": "star",
    "Michelin 1 Star": "star",
    "Bib Gourmand": "cutlery",
    "Selected": "info-sign",
    "500碗 3 Bowls": "fire",
    "500碗 2 Bowls": "fire",
    "500碗 1 Bowl": "fire",
    "Asia's 50 Best Bars": "glass",
    "World's 100 Best Coffee": "leaf",
    "Notable Coffee": "leaf",
}

CATEGORY_EMOJIS = {
    "Michelin 3 Stars": "⭐⭐⭐",
    "Michelin 2 Stars": "⭐⭐",
    "Michelin 1 Star": "⭐",
    "Bib Gourmand": "🍽️",
    "Selected": "📍",
    "500碗 3 Bowls": "🍜🍜🍜",
    "500碗 2 Bowls": "🍜🍜",
    "500碗 1 Bowl": "🍜",
    "Asia's 50 Best Bars": "🍸",
    "World's 100 Best Coffee": "☕",
    "Notable Coffee": "☕",
}

SOURCE_LABELS = {
    "michelin": "Michelin Guide 米其林",
    "500bowl": "500碗 Award",
    "bar": "Asia's 50 Best Bars",
    "coffee": "Best Coffee ☕",
}

CITY_ORDER = [
    "Taipei", "New Taipei", "Keelung", "Hsinchu City", "Hsinchu County",
    "Taichung", "Changhua", "Tainan", "Kaohsiung", "Hualien/Yilan",
]


@st.cache_data
def load_data() -> pd.DataFrame:
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df = df[df["lat"].notna() & df["lon"].notna()]
    return df


def build_popup(row: pd.Series) -> str:
    emoji = CATEGORY_EMOJIS.get(row["category"], "")
    name = row["name"]
    name_zh = row.get("name_zh") or ""
    zh_part = f" <span style='color:#888;font-size:13px'>({name_zh})</span>" if name_zh and name_zh != name else ""
    address = row.get("address", "")
    cuisine = row.get("cuisine", "")
    price = row.get("price", "")
    desc = (row.get("description") or "")[:300]
    michelin_url = row.get("michelin_url", "")
    website = row.get("website", "")
    green = "🌿" if row.get("green_star") else ""

    links = ""
    if michelin_url:
        links += f'<a href="{michelin_url}" target="_blank">Michelin Guide</a>'
    if website:
        sep = " | " if links else ""
        links += f'{sep}<a href="{website}" target="_blank">Website</a>'

    return f"""
    <div style="font-family:sans-serif;max-width:300px">
      <h4 style="margin:0 0 2px">{emoji} {name} {green}</h4>
      {f'<p style="margin:0 0 4px;font-size:13px;color:#555">{name_zh}</p>' if name_zh and name_zh != name else ''}
      <p style="margin:2px 0;color:#777;font-size:12px">{row['category']}</p>
      <p style="margin:2px 0;font-size:12px">🍽 {cuisine} &nbsp; {price}</p>
      <p style="margin:2px 0;font-size:12px">📍 {address}</p>
      {'<hr style="margin:6px 0">' if desc else ''}
      <p style="margin:2px 0;font-size:11px;color:#333">{desc}</p>
      {'<hr style="margin:6px 0">' + links if links else ''}
    </div>
    """


def build_map(df: pd.DataFrame) -> folium.Map:
    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8,
        tiles="CartoDB positron",
    )

    # Group by category and add layer control
    feature_groups = {}
    for cat in df["category"].unique():
        fg = folium.FeatureGroup(name=cat, show=True)
        feature_groups[cat] = fg
        m.add_child(fg)

    for _, row in df.iterrows():
        color = CATEGORY_COLORS.get(row["category"], "#888888")
        icon_name = CATEGORY_ICONS.get(row["category"], "info-sign")
        popup_html = build_popup(row)

        name_zh = row.get("name_zh") or ""
        zh_tip = f" {name_zh}" if name_zh and name_zh != row["name"] else ""
        marker = folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"{CATEGORY_EMOJIS.get(row['category'], '')} {row['name']}{zh_tip}",
            icon=folium.Icon(color="white", icon_color=color, icon=icon_name, prefix="glyphicon"),
        )
        feature_groups[row["category"]].add_child(marker)

    folium.LayerControl(collapsed=False).add_to(m)
    return m


def main():
    st.title("🗺️ Taiwan Gourmet Map 台灣美食地圖")
    st.caption(
        "Data sources: [Michelin Guide Taiwan 2025](https://guide.michelin.com/tw/en) · "
        "[500碗 2025](https://500times.udn.com/wtimes/story/123497/8874123) · "
        "[Asia's 50 Best Bars 2025](https://www.theworlds50best.com/bars/asia/list/1-50) · "
        "[World's 100 Best Coffee Shops 2026](https://www.timeout.com/asia/news/worlds-100-best-coffee-shops-2026-14-asian-cafes-make-the-global-list-021926)"
    )

    df = load_data()

    # ── Sidebar filters ──────────────────────────────────────────────────
    with st.sidebar:
        st.header("🔍 Filters")

        source_options = ["All"] + [SOURCE_LABELS[s] for s in ["michelin", "500bowl"]]
        selected_source = st.selectbox("Source", source_options)

        all_categories = sorted(df["category"].unique())
        selected_categories = st.multiselect(
            "Category / Rating",
            options=all_categories,
            default=all_categories,
        )

        cities_in_data = sorted(df["city"].dropna().unique())
        selected_cities = st.multiselect(
            "City",
            options=cities_in_data,
            default=cities_in_data,
        )

        cuisine_search = st.text_input("Search cuisine or name", "")

        st.markdown("---")
        st.markdown("### 🗂 Legend")
        for cat, emoji in CATEGORY_EMOJIS.items():
            color = CATEGORY_COLORS.get(cat, "#888")
            st.markdown(
                f'<span style="color:{color};font-size:18px">●</span> {emoji} {cat}',
                unsafe_allow_html=True,
            )

    # ── Apply filters ─────────────────────────────────────────────────────
    filtered = df.copy()

    if selected_source != "All":
        source_key = next(k for k, v in SOURCE_LABELS.items() if v == selected_source)
        filtered = filtered[filtered["source"] == source_key]

    if selected_categories:
        filtered = filtered[filtered["category"].isin(selected_categories)]

    if selected_cities:
        filtered = filtered[filtered["city"].isin(selected_cities)]

    if cuisine_search:
        mask = (
            filtered["name"].str.contains(cuisine_search, case=False, na=False)
            | filtered["cuisine"].str.contains(cuisine_search, case=False, na=False)
        )
        filtered = filtered[mask]

    # ── Stats row ────────────────────────────────────────────────────────
    total = len(filtered)
    stars3 = len(filtered[filtered["category"] == "Michelin 3 Stars"])
    stars2 = len(filtered[filtered["category"] == "Michelin 2 Stars"])
    stars1 = len(filtered[filtered["category"] == "Michelin 1 Star"])
    bib = len(filtered[filtered["category"] == "Bib Gourmand"])
    bowls = len(filtered[filtered["source"] == "500bowl"])
    bars_count = len(filtered[filtered["source"] == "bar"])
    coffee_count = len(filtered[filtered["source"] == "coffee"])

    cols = st.columns(8)
    cols[0].metric("Total", total)
    cols[1].metric("⭐⭐⭐", stars3)
    cols[2].metric("⭐⭐", stars2)
    cols[3].metric("⭐", stars1)
    cols[4].metric("🍽️ Bib", bib)
    cols[5].metric("🍜 500碗", bowls)
    cols[6].metric("🍸 Bars", bars_count)
    cols[7].metric("☕ Coffee", coffee_count)

    if filtered.empty:
        st.warning("No restaurants match the current filters.")
        return

    # ── Map ──────────────────────────────────────────────────────────────
    st.subheader("Interactive Map")
    m = build_map(filtered)
    st_folium(m, width="100%", height=580, returned_objects=[])

    # ── Table ────────────────────────────────────────────────────────────
    with st.expander(f"📋 Restaurant List ({total})", expanded=False):
        display_cols = ["name", "name_zh", "category", "cuisine", "city", "address", "price", "michelin_url", "website"]
        display_cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(
            filtered[display_cols].rename(columns={
                "name": "Name",
                "name_zh": "中文名",
                "category": "Category",
                "cuisine": "Cuisine",
                "city": "City",
                "address": "Address",
                "price": "Price",
                "michelin_url": "Michelin",
                "website": "Website",
            }),
            use_container_width=True,
            hide_index=True,
        )

    # ── Download ─────────────────────────────────────────────────────────
    csv_bytes = filtered.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Download filtered data (CSV)",
        data=csv_bytes,
        file_name="taiwan_gourmet_filtered.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
