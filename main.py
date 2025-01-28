import folium

# Шаг 1: Создать объект карты
mymap = folium.Map(location=[37.7749, -122.4194], zoom_start=13)  # Отцентрован в Сан-Франциско

# Шаг 2: Добавить векторную форму (Многоугольник)
folium.Polygon(
    locations=[
        [37.7749, -122.4194],  # Точка 1: Сан-Франциско
        [37.7849, -122.4294],  # Точка 2
        [37.7649, -122.4094]   # Точка 3
    ],
    color='blue',
    fill=True,
    fill_color='cyan',
    fill_opacity=0.5,
    tooltip='Пример многоугольника'
).add_to(mymap)

# Шаг 3: Сохранить карту как файл HTML
mymap.save("map_with_polygon.html")

print("Карта сохранена как map_with_polygon.html!")
