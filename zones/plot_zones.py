import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image


# 2. Функція для побудови графіка з зображенням та зонами
def plot_image_with_zones(image_path, zones_enum):
    """Функція для відображення зображення та зон з enum.

    Args:
        image_path (str): Шлях до зображення.
        zones_enum (Enum): Enum з назвами зон та їх нормалізованими координатами.
    """
    # Відкриваємо зображення за допомогою PIL
    image = Image.open(image_path)
    plt.figure(figsize=(10, 8))

    # Відображення зображення
    plt.imshow(image)

    # Обхід зон з enum та їх малювання на зображенні
    for zone in zones_enum:
        points = zone.value
        # Масштабування координат до розмірів зображення
        image_width, image_height = image.size
        scaled_points = [(x * image_width, y * image_height) for x, y in points]

        # Малюємо полігон на зображенні
        polygon = Polygon(scaled_points, closed=True, fill=None, edgecolor='r', linewidth=2, label=zone.name)
        plt.gca().add_patch(polygon)

        # Додаємо підписи зон
        plt.text(scaled_points[0][0], scaled_points[0][1], zone.name, fontsize=12, color='red')

    return plt


# Нова функція для відображення зон та центрів

# Нова функція для відображення зон та центрів
def plot_zones_with_centers(image_path, zones_enum, df=None):
    # Відкриваємо зображення за допомогою PIL
    image = Image.open(image_path)
    # Отримуємо розміри зображення
    image_width, image_height = image.size
    plt = plot_image_with_zones(image_path, zones_enum)

    if df is not None:
        # Додаємо центри до зображення як червоні зірочки
        for index, row in df.iterrows():
            center_x = row['center_x']
            center_y = row['center_y']
            plt.scatter(center_x, center_y, color='red', marker='*', s=100)  # Зірочка для центру

    plt.axis('off')  # Прибираємо осі

    plt.show()  # Відображення зображення
