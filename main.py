from flask import Flask, render_template, Response
import folium
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

# Подключение к базе данных PostgreSQL
DB_USER = "postgres"
DB_PASS = "123123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "geodata"
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Функция для получения данных из базы
def get_data(parameter):
    query = f"""
    SELECT latitude, longitude, station_name, monthly_average
    FROM dataset
    WHERE parameter = %s
    """
    df = pd.read_sql(query, engine, params=(parameter,))
    return df

# Функция для создания карты
def create_map(data, color):
    # Создаем карту, центрируем на средней точке координат (например, Москва)
    m = folium.Map(location=[55.75, 37.61], zoom_start=10)

    # Добавляем маркеры на карту
    for index, row in data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['station_name']}: {row['monthly_average']}",
            icon=folium.Icon(color=color)
        ).add_to(m)

    # Возвращаем HTML-код карты
    return m._repr_html_()

# Главная страница
@app.route('/')
def index():
    # Изначально отображаем карту с параметром "Оксид углерода" как пример
    data = get_data("Оксид углерода")
    map_html = create_map(data, "blue")
    return render_template('index.html', map_html=map_html)

# Обработка запросов для обновления карты
@app.route('/<group>')
def load_map(group):
    # Определяем параметр и цвет в зависимости от группы
    if group == "blue":
        parameter = "Частицы РМ2.5"
        color = "blue"
    elif group == "red":
        parameter = "Метан"
        color = "red"
    else:
        parameter = "Оксид углерода"
        color = "blue"

    # Получаем данные и генерируем карту
    data = get_data(parameter)
    map_html = create_map(data, color)
    return Response(map_html, mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=True)