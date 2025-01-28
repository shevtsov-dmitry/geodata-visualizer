from flask import Flask, render_template
import folium
import pandas as pd

app = Flask(__name__)

# Шаг 1: Функция для динамической генерации карты на основе выбранной группы
def generate_map(selected_group):
    # Загрузка файла CSV
    df = pd.read_csv("polygon_data.csv")

    # Создание базовой карты
    mymap = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

    # Фильтрация данных для выбранной группы
    group_data = df[df["group"] == selected_group]

    # Извлечение координат
    coords = group_data[["latitude", "longitude"]].values.tolist()

    # Добавление полигона
    folium.Polygon(
        locations=coords,
        color="blue" if selected_group == "blue" else "red",
        fill=True,
        fill_color="cyan" if selected_group == "blue" else "pink",
        fill_opacity=0.5,
        tooltip=f"{selected_group.capitalize()} Полигон"
    ).add_to(mymap)

    # Возвращение HTML-представления карты
    return mymap._repr_html_()

@app.route("/")
def home():
    # По умолчанию отображаем "синюю" карту
    map_html = generate_map("blue")
    return render_template("index.html", map_html=map_html)

# Маршрут для динамического обновления карты в зависимости от выбранной группы
@app.route("/<group>")
def update_map(group):
    return generate_map(group)

if __name__ == "__main__":
    app.run(debug=True)