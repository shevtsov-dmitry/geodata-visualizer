from flask import Flask, render_template
import folium
import pandas as pd
from sqlalchemy import create_engine
import geopandas as gpd

app = Flask(__name__)

# Подключение к базе данных
engine = create_engine('postgresql://user:password@localhost/geodata')

def generate_map(parameter, display_type='markers'):
    """
    Генерирует карту на основе выбранного параметра и типа отображения.

    Args:
        parameter (str): Загрязняющее вещество (например, 'Оксид углерода').
        display_type (str): Тип отображения ('markers' или 'polygons').
    """
    # Запрос данных из базы данных
    query = f"""
    SELECT station_name, latitude, longitude, parameter, monthly_average, ST_AsText(geom) as geom
    FROM air_quality
    WHERE parameter = '{parameter}'
    """
    gdf = gpd.read_postgis(query, engine, geom_col='geom')

    # Создание базовой карты
    mymap = folium.Map(location=[55.7558, 37.6173], zoom_start=10,
                       tiles='OpenStreetMap')

    # Добавление слоя спутниковой карты
    folium.TileLayer('Esri.WorldImagery', name='Спутник').add_to(mymap)

    if display_type == 'markers':
        # Добавление маркеров
        for idx, row in gdf.iterrows():
            color = 'blue' if row['monthly_average'] < 0.5 else 'red'
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['station_name']}: {row['monthly_average']}",
                icon=folium.Icon(color=color)
            ).add_to(mymap)
    elif display_type == 'polygons':
        # Пример создания полигонов (упрощенно, на основе координат)
        coords = gdf[['latitude', 'longitude']].values.tolist()
        if coords:
            folium.Polygon(
                locations=coords,
                color='blue',
                fill=True,
                fill_color='cyan',
                fill_opacity=0.5,
                tooltip=f"{parameter}"
            ).add_to(mymap)

    # Добавление управления слоями
    folium.LayerControl().add_to(mymap)

    return mymap._repr_html_()

@app.route('/')
def home():
    # Получить список уникальных параметров
    query = "SELECT DISTINCT parameter FROM air_quality"
    parameters = pd.read_sql(query, engine)['parameter'].tolist()

    # По умолчанию отображаем карту с первым параметром
    default_parameter = parameters[0] if parameters else 'Оксид углерода'
    map_html = generate_map(default_parameter, 'markers')

    return render_template('index.html', map_html=map_html, parameters=parameters)

@app.route('/map/<parameter>/<display_type>')
def update_map(parameter, display_type):
    map_html = generate_map(parameter, display_type)
    return map_html

if __name__ == '__main__':
    app.run(debug=True)