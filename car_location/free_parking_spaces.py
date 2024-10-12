from car_location.occupied_p_spaces import find_parking_zones
from zones.enum_parking_area.enum_parking_spaces import ParkingSpaces
from sklearn.cluster import DBSCAN
import numpy as np

def find_all_free_zones(occupied_zones):
    """
    Повертає список вільних паркомісць на основі зайнятих зон.

    Args:
        occupied_zones (list): Список зайнятих зон із `ParkingSpaces`.

    Returns:
        list: Список вільних зон із `ParkingSpaces`.
    """
    # Всі можливі зони (зміна: перетворення enum в ітерований список)
    all_zones = set(ParkingSpaces)

    # Видаляємо зайняті зони з повного списку
    free_zones = list(all_zones - set(occupied_zones))

    return free_zones


def get_free_parking_spaces(car_coordinates, image_size):
    occupied_zones = find_parking_zones(car_coordinates, image_size)

    # Отримуємо всі можливі зони з enum ParkingSpaces
    free_zones = find_all_free_zones(occupied_zones)

    # Створення одномірного списку координат зон
    flat_zones = [zone.value for zone in free_zones]

    # Перетворення в numpy array
    coords = np.array(flat_zones)

    # Переконаймося, що coords має правильну форму (n, 2)
    if len(coords.shape) != 2 or coords.shape[1] != 2:
        coords = coords.reshape(-1, 2)

    # Застосування DBSCAN для видалення подібних зон
    db = DBSCAN(eps=0.05, min_samples=1).fit(coords)

    # Отримання унікальних вільних зон
    unique_zones = []
    for zone, label in zip(flat_zones, db.labels_):
        if label != -1:  # Відкидаємо шуми (зони, що не входять до жодного кластера)
            unique_zones.append(zone)

    return unique_zones  # Повертаємо список вільних зон


def get_parking_occupancy(car_coordinates, image_size):

    # Отримуємо вільні зони
    free_zones = get_free_parking_spaces(car_coordinates, image_size)

    # Перетворюємо список вільних зон у формат, сумісний з plot_zones_with_centers
    free_zones_list = [zone for zone in free_zones]  # або можете залишити як є, якщо вже у правильному форматі

    return free_zones_list


