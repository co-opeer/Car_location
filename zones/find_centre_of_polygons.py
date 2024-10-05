# Обчислення центру полігону
from zones.enum_parking_area.enum_parking_spaces import ParkingSpaces


def calculate_polygon_center(polygon):
    x_coords = [point[0] for point in polygon]
    y_coords = [point[1] for point in polygon]
    center_x = sum(x_coords) / len(polygon)
    center_y = sum(y_coords) / len(polygon)
    return center_x, center_y

# Створення нового enum з центрами зон
centers_enum_code = "class ParkingCenters(Enum):\n"
for zone in ParkingSpaces:
    center = calculate_polygon_center(zone.value)
    centers_enum_code += f"    {zone.name} = ({center[0]:.6f}, {center[1]:.6f})\n"

# Вивід коду
print(centers_enum_code)