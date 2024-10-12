import cv2
import pandas as pd
from ultralytics import YOLO

def load_model(model_path):
    """Завантажує модель YOLO з вказаного шляху.

    Args:
        model_path (str): Шлях до моделі YOLO.

    Returns:
        model: Завантажена модель.
    """
    model = YOLO(model_path)
    return model


def get_bounding_boxes(image_path, model):
    """Отримує координати рамок для об'єктів на зображенні за допомогою моделі YOLO.

    Args:
        image_path (str): Шлях до зображення.
        model: Модель YOLO.

    Returns:
        list: Список координат рамок у форматі [[x_min, y_min, x_max, y_max], ...].
    """
    # Зчитування зображення
    img = cv2.imread(image_path)

    # Виконання предиктів
    results = model(img)

    bounding_boxes = []

    # Отримуємо bounding boxes з результатів
    for bbox in results[0].boxes:
        x_min, y_min, x_max, y_max = [float(coord) for coord in bbox.xyxy[0].numpy()]
        label = model.names[int(bbox.cls[0])]  # Отримуємо назву класу об'єкта

        # Фільтруємо лише автомобілі
        if label == "car":
            bounding_boxes.append([x_min, y_min, x_max, y_max])

    return bounding_boxes




# Функція для знаходження центрів рамок
def get_box_centers(bounding_boxes):
    """Функція для знаходження центрів рамок за координатами.

    Args:
        bounding_boxes (list): Список координат рамок у форматі [[x_min, y_min, x_max, y_max], ...].

    Returns:
        list: Список центрів рамок у форматі [(center_x, center_y), ...].
    """
    centers = []
    for box in bounding_boxes:
        x_min, y_min, x_max, y_max = box
        center_x = (x_min + x_max) / 2
        center_y = (y_min + y_max) / 2
        centers.append((center_x, center_y))
    return centers


def get_car_centres(image_path):
    model = YOLO('yolov8s.pt')
    bounding_boxes = get_bounding_boxes(image_path, model)
    box_centers = get_box_centers(bounding_boxes)
    # Збереження в DataFrame для подальшої обробки
    df = pd.DataFrame(box_centers, columns=["center_x", "center_y"])
    return df





