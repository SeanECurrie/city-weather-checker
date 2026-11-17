"""Fetch current weather for a fixed list of cities and save each raw answer to data/.
The key comes from the OWM_KEY environment variable and is never written anywhere."""
import json, os, sys, time, urllib.parse, urllib.request

CITIES = ["Chicago", "New York", "Los Angeles", "Seattle", "Miami", "Denver", "Phoenix", "Anchorage",
          "Honolulu", "Toronto", "Vancouver", "Mexico City", "Lima", "Sao Paulo", "Buenos Aires",
          "London", "Paris", "Berlin", "Oslo", "Reykjavik", "Moscow", "Cairo", "Lagos", "Nairobi",
          "Cape Town", "Dubai", "Mumbai", "Delhi", "Bangkok", "Singapore", "Hong Kong", "Tokyo",
          "Seoul", "Beijing", "Sydney", "Auckland"]

key = os.environ["OWM_KEY"]
out = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(out, exist_ok=True)
index = []
for city in CITIES:
    url = ("https://api.openweathermap.org/data/2.5/weather?q=" + urllib.parse.quote(city)
           + "&appid=" + key + "&units=imperial")
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            d = json.load(r)
    except Exception as e:  # keep the previous file for this city
        print("skip", city, type(e).__name__, file=sys.stderr)
        continue
    if str(d.get("cod")) != "200" or not d.get("weather"):
        print("skip", city, d.get("cod"), file=sys.stderr)
        continue
    slug = city.lower().replace(" ", "-")
    with open(os.path.join(out, slug + ".json"), "w") as f:
        json.dump(d, f, indent=1)
    index.append({"city": city, "slug": slug, "main": d["weather"][0]["main"], "dt": d["dt"]})
    time.sleep(0.2)
if len(index) < len(CITIES) // 2:
    sys.exit("too few cities answered; leaving the old index in place")
with open(os.path.join(out, "index.json"), "w") as f:
    json.dump({"refreshed": int(time.time()), "cities": index}, f, indent=1)
print("saved", len(index), "cities")
