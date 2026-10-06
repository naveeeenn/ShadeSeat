"""
ShadeSeat: Sun-Side Seat Advisor
Tells you which side (LEFT or RIGHT) to sit on in a bus or car
to avoid direct sunlight, based on route direction and the sun's position.
"""

import math
import warnings
from datetime import datetime, timedelta, timezone

from geopy.exc import GeocoderServiceError, GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim
from pysolar.solar import get_altitude, get_azimuth

# pysolar prints a harmless leap-second warning; hide it for clean output
warnings.filterwarnings("ignore")

IST = timezone(timedelta(hours=5, minutes=30))
SAMPLE_POINTS = [0, 0.33, 0.66, 1]  # fractions of the journey to check


def bearing(lat1, lon1, lat2, lon2):
    """Direction of travel in degrees (0 = North, 90 = East)."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    x = math.sin(dl) * math.cos(p2)
    y = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


def seat_side(lat, lon, travel_dir, when):
    """Return 'LEFT', 'RIGHT', 'ANY' or 'NIGHT' for a point and time."""
    if get_altitude(lat, lon, when) <= 0:
        return "NIGHT"
    sun_az = get_azimuth(lat, lon, when)
    diff = (sun_az - travel_dir) % 360  # sun angle relative to travel direction
    if diff < 20 or diff > 340 or abs(diff - 180) < 20:
        return "ANY"  # sun is straight ahead or behind
    return "LEFT" if diff < 180 else "RIGHT"  # sun on right -> sit left


def find_place(geo, name):
    """Look up a place name and return its location, or None."""
    try:
        return geo.geocode(name)
    except (GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError):
        print("Could not reach the location service. Check your internet and retry.")
        return None


def main():
    geo = Nominatim(user_agent="shadeseat", timeout=10)

    start = find_place(geo, input("Start location: "))
    end = find_place(geo, input("Destination: "))
    if not start or not end:
        print("Could not find one of the locations. Try adding the city and country.")
        return

    try:
        dep = input("Departure time today (HH:MM, 24-hour): ")
        hours = float(input("Trip duration in hours: "))
        h, m = map(int, dep.split(":"))
        depart = datetime.now(IST).replace(hour=h, minute=m, second=0, microsecond=0)
    except ValueError:
        print("Invalid input. Use HH:MM for time and a number for duration.")
        return

    direction = bearing(start.latitude, start.longitude, end.latitude, end.longitude)
    print(f"\nTravel direction: {direction:.0f} degrees\n")

    results = []
    for frac in SAMPLE_POINTS:
        lat = start.latitude + frac * (end.latitude - start.latitude)
        lon = start.longitude + frac * (end.longitude - start.longitude)
        when = depart + timedelta(hours=hours * frac)
        side = seat_side(lat, lon, direction, when)
        results.append(side)
        print(f"{when.strftime('%H:%M')} -> {side}")

    left, right = results.count("LEFT"), results.count("RIGHT")
    if left == right == 0:
        print("\nVerdict: sit anywhere.")
    else:
        best = "LEFT" if left >= right else "RIGHT"
        print(f"\nVerdict: sit on the {best} side for most of the trip.")


if __name__ == "__main__":
    main()
