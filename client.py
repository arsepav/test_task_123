import sys
import json
import requests

BASE_URL = "http://localhost:8000"
API_KEY = "tmp-api-key"

HEADERS = {"X-API-Key": API_KEY, "Accept": "application/json"}


def get(path: str, params: dict | None = None) -> dict | list:
    r = requests.get(f"{BASE_URL}{path}", headers=HEADERS, params=params or {}, timeout=10)
    r.raise_for_status()
    return r.json()


def print_result(endpoint: str, title: str, params: dict | None = None):
    print("\n" + "=" * 60)
    print(title)
    print(json.dumps(get(endpoint, params), ensure_ascii=False, indent=2))
    print("=" * 60)


def main():
    try:
        print_result("/buildings", "GET /buildings — список зданий")

        print_result("/organizations/building/4", "GET /organizations/building/4 — организации в здании 4 (Кошки, Самарская обл.)")

        print_result("/organizations/activity/3", "GET /organizations/activity/3 — по деятельности (Мясная продукция)")

        print_result("/organizations/activity/1", "GET /organizations/activity/1 — по деятельности (Еда)")

        print_result("/organizations/nearby", "GET /organizations/nearby — в радиусе 5 км от Москвы", {"lat": 55.76, "lon": 37.61, "radius_km": 5})

        print_result("/organizations/nearby", "GET /organizations/nearby — прямоугольник (Самарская обл.)", {"lat_min": 54.0, "lat_max": 54.5, "lon_min": 50.0, "lon_max": 51.0})

        print_result("/organizations/5", "GET /organizations/5 — организация по ID (Гастроном)")

        print_result("/organizations/search/activity", "GET /organizations/search/activity — по виду деятельности с поддеревом (Еда)", {"activity_id": 1})

        print_result("/organizations/search/name", "GET /organizations/search/name?q=ООО", {"q": "ООО"})

        print_result("/organizations/search/name", "GET /organizations/search/name?q=Гастроном", {"q": "Гастроном"})

        print_result("/buildings", "GET /buildings — в прямоугольнике (Москва)", {"lat_min": 55.75, "lat_max": 55.77, "lon_min": 37.60, "lon_max": 37.62})

    except requests.HTTPError as e:
        print(f"HTTP error: {e.response.status_code}")
        print(e.response.text)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Request error: {e}")
        sys.exit(1)

    print("\nГотово.\n")


if __name__ == "__main__":
    main()
