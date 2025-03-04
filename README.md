# Проект по визуализации геоданных

## Установка

### Linix (Ubuntu)

Установка python на систему.

``` bash
sudo apt install python3-full
```

Активировать виртуальную среду из корневой папки проекта

``` bash
source ./bin/activate  
pip install --upgrade pip  
```

Необходимо установить библиотеки. Вы можете это сделать с помощью команды:

```bash
pip install flask folium pandas sqlalchemy psycopg2-binary geoalchemy2 geopandas
```

#### Пометка

_В случае возникновения ошибок при установке, прочитайте, что вывела команда. Там будет описана проблема и
дополнительные инструкции по её устранению (а именно, что ещё нужно установить и команда для выполнения)._

## Добавление данных из датасета CSV в БД

``` bash
\copy dataset(id, period, station_name, surveillance_zone_characteristics, adm_area, district, parameter, monthly_average, monthly_average_pdkss, longitude, latitude) FROM 'dataset.csv' DELIMITER ';' CSV HEADER;
```
