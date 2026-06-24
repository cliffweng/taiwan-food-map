"""Basic sanity checks for the restaurant dataset."""
import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "src" / "data" / "restaurants.json"


def load():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def test_file_exists():
    assert DATA_PATH.exists(), "restaurants.json missing"


def test_minimum_count():
    data = load()
    assert len(data) >= 50, f"Expected 50+ restaurants, got {len(data)}"


def test_all_have_required_fields():
    required = {"name", "source", "category", "lat", "lon"}
    data = load()
    for r in data:
        missing = required - set(r.keys())
        assert not missing, f"{r.get('name')} missing fields: {missing}"


def test_michelin_stars_present():
    data = load()
    cats = {r["category"] for r in data}
    for expected in ["Michelin 3 Stars", "Michelin 2 Stars", "Michelin 1 Star"]:
        assert expected in cats, f"Missing category: {expected}"


def test_500bowl_present():
    data = load()
    bowls = [r for r in data if r["source"] == "500bowl"]
    assert len(bowls) >= 5, f"Expected 500碗 entries, got {len(bowls)}"


def test_coordinates_in_taiwan():
    data = load()
    for r in data:
        if r["lat"] is not None and r["lon"] is not None:
            assert 21.5 <= r["lat"] <= 26.5, f"{r['name']} lat {r['lat']} out of range"
            assert 119.0 <= r["lon"] <= 122.5, f"{r['name']} lon {r['lon']} out of range"


def test_three_star_count():
    data = load()
    three_star = [r for r in data if r["category"] == "Michelin 3 Stars"]
    assert len(three_star) == 3, f"Expected 3 three-star restaurants, got {len(three_star)}"
