# City Weather Checker

A small weather app (plain JavaScript, HTML and CSS) and a page that shows how it works.

- `app/` is the original app. It asks OpenWeatherMap for a city's current weather, changes the page background to match the conditions, shows the matching icon, and converts sunrise and sunset to the city's own time.
- `index.html` runs the app beside a walk-through of its code.
- The API key is not in this repository. A scheduled job (`.github/workflows/refresh.yml`) asks the weather service for a fixed list of cities and saves the answers in `data/`; the public page replays those.
