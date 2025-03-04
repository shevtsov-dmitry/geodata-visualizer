from flask import Flask, render_template
import folium
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

# Настройки подключения к базе данных
DB_USER = "postgres"
DB_PASS = "123123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "geodata"
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Запрос для получения данных из базы данных
def get_data(parameter):
    """Получает данные для заданного параметра, группируя точки по polygon_id."""
    query = """
    SELECT polygon_id, station_name, adm_area, district, parameter, monthly_average, monthly_average_pdkss,
           array_agg(latitude ORDER BY id) as latitudes,
           array_agg(longitude ORDER BY id) as longitudes
    FROM dataset
    WHERE parameter = %s
    GROUP BY polygon_id, station_name, adm_area, district, parameter, monthly_average, monthly_average_pdkss
    """
    return pd.read_sql(query, engine, params=(parameter,))

# Функция для создания карты с полигонами
def create_map():
    """Создает карту с полигонами для всех параметров, используя слои Folium."""
    m = folium.Map(location=[55.75, 37.61], zoom_start=10)  # Центр карты — Москва
    
    # Определяем параметры и цвета
    parameters = [
        {"name": "Взвешенные частицы РМ2.5 (суточные измерения)", "color": "blue", "label": "PM2.5"},
        {"name": "Взвешенные частицы РМ10", "color": "green", "label": "PM10"},
        {"name": "Метан", "color": "red", "label": "Метан"},
        {"name": "Оксид углерода", "color": "purple", "label": "Оксид углерода"}
    ]
    
    for param in parameters:
        # Создаем слой для каждого параметра
        show = param["name"] == "Взвешенные частицы РМ2.5 (суточные измерения)"  # PM2.5 виден по умолчанию
        layer = folium.FeatureGroup(name=param["label"], show=show)
        data = get_data(param["name"])
        
        for _, row in data.iterrows():
            points = list(zip(row["latitudes"], row["longitudes"]))
            popup_text = (
                f"Станция: {row['station_name']}<br>"
                f"Адм. округ: {row['adm_area']}<br>"
                f"Район: {row['district']}<br>"
                f"Параметр: {row['parameter']}<br>"
                f"Среднемесячное: {row['monthly_average']}<br>"
                f"ПДКсс: {row['monthly_average_pdkss']}"
            )
            folium.Polygon(
                locations=points,
                popup=folium.Popup(popup_text, max_width=300),
                color=param["color"],
                fill=True,
                fill_color=param["color"]
            ).add_to(layer)
        layer.add_to(m)
    
    # Добавляем контроллер слоев для переключения
    folium.LayerControl().add_to(m)
    return m._repr_html_()

# Главный маршрут
@app.route('/')
def index():
    """Отображает главную страницу с картой."""
    map_html = create_map()
    return render_template('index.html', map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)