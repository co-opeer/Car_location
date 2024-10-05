import json


def normalize_coordinates(points, image_width, image_height):
    """Функція для нормалізації координат.

    Args:
        points (list): Список координат [x, y].
        image_width (int): Ширина зображення.
        image_height (int): Висота зображення.

    Returns:
        list: Список нормалізованих координат.
    """
    normalized_points = [(x / image_width, y / image_height) for x, y in points]
    return normalized_points


def process_json(file_path):
    """Функція для обробки JSON-файлу та виведення назв зон і їх нормалізованих координат.

    Args:
        file_path (str): Шлях до JSON-файлу.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    image_width = data["imageWidth"]
    image_height = data["imageHeight"]

    for shape in data["shapes"]:
        label = shape["label"]
        points = shape["points"]
        normalized_points = normalize_coordinates(points, image_width, image_height)

        print(f"{label} = [")
        for point in normalized_points:
            print(f"{point},")

        print("]")



process_json(r"C:\Users\PC\OneDrive\Робочий стіл\20240930_091340_2.json")