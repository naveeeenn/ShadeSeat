# ShadeSeat: Sun-Side Seat Advisor

A small Python tool that tells you **which side of a bus or car to sit on (left or right)** to stay out of the sun.

Enter your start location, destination, departure time and trip duration. ShadeSeat works out which direction you're travelling, checks where the sun will be along the way, and recommends the shaded side.

## How it works

1. **Geocoding:** converts the start and destination names into latitude and longitude using `geopy` (OpenStreetMap Nominatim).
2. **Travel bearing:** calculates the direction of travel in degrees (0° = North, 90° = East).
3. **Solar position:** uses `pysolar` to find the sun's azimuth (compass direction) and altitude (height above the horizon) at points along the trip.
4. **Comparison:** compares the sun's direction with the travel direction.
   - Sun on the **right** of the vehicle: sit on the **left**.
   - Sun on the **left** of the vehicle: sit on the **right**.
   - Sun straight ahead or behind: seat side makes little difference (`ANY`).
   - Sun below the horizon: `NIGHT`.
5. **Verdict:** the trip is sampled at four points, and the side that is shaded for most of them is recommended.

## Installation

Requires Python 3.8 or newer.

```bash
git clone https://github.com/naveeeenn/ShadeSeat.git
cd ShadeSeat
python -m pip install -r requirements.txt
```

## Usage

```bash
python shadeseat.py
```

Example session:

```
Start location: Delhi, India
Destination: Bhadra, Rajasthan
Departure time today (HH:MM, 24-hour): 13:00
Trip duration in hours: 5

Travel direction: 284 degrees

13:00 -> RIGHT
14:39 -> RIGHT
16:18 -> RIGHT
18:00 -> RIGHT

Verdict: sit on the RIGHT side for most of the trip.
```

The vehicle is heading west-northwest in the afternoon, so the sun is on the left. Sitting on the right keeps you in shade.

## Tech stack

- Python 3
- [geopy](https://github.com/geopy/geopy) for geocoding
- [pysolar](https://github.com/pingswept/pysolar) for solar position calculations

## Limitations

- Uses a **straight line** between the two places, not the actual road, so winding routes are approximate.
- Samples the journey at **four points**, not continuously.
- Ignores weather, tall buildings, trees and the vehicle's own roof.
- Times are assumed to be in **IST (UTC+5:30)** for the departure date of today.
- Needs an internet connection for place lookup.

## Future improvements

- Use a routing API (such as OSRM) to follow the real road path.
- Sample the route more densely for long trips.
- Add a simple web interface using Flask or Streamlit.
- Support trains and flights.
- Allow choosing a date and time zone.

## License

Released under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**Naveen**
B.Tech EE, NSUT
linkedin.com/in/naveeeenn/ | naveen.ug25@nsut.ac.in
