from math import sqrt

from zones.enum_parking_area.enum_centre_of_polygons import ParkingCenters
from zones.enum_parking_area.enum_parking_spaces import ParkingSpaces

def point_in_polygon(point, polygon):
    """Перевіряє, чи точка знаходиться в межах полігону."""
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def calculate_distance(point1, point2):
    """Обчислює відстань між двома точками у декартовій системі координат."""
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def find_parking_zones(car_coordinates, image_size):
    """Повертає список зон, в яких знаходяться автомобілі, враховуючи мінімальну відстань до центру зони."""
    occupied_zones = []

    # Нормалізація координат автомобілів
    width, height = image_size
    normalized_car_coordinates = [(x / width, y / height) for x, y in car_coordinates]

    for car in normalized_car_coordinates:
        closest_zone = None
        min_distance = float('inf')

        for zone in ParkingSpaces:
            if point_in_polygon(car, zone.value):
                # Визначаємо центр поточного полігону
                zone_center = ParkingCenters[zone.name].value

                # Обчислюємо відстань між автомобілем та центром полігону
                distance = calculate_distance(car, zone_center)

                # Якщо поточна відстань менша, зберігаємо цю зону як найближчу
                if distance < min_distance:
                    min_distance = distance
                    closest_zone = zone

        if closest_zone:
            occupied_zones.append(closest_zone)

    return list(set(occupied_zones))  # повертаємо унікальні зони