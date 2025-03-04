# Проект по визуализации геоданных

## Установка

### Linix (Ubuntu)

## Настройка базы данных

Установить PostgreSQL

```bash
sudo apt install postgresql
```

#### примечание

_На Ubuntu необходимо редактировать файл конфигурации postgresql для того, чтобы были права подключения к БД._
_Для этого откройте файл /var/lib/postgres/data/pg_hba.conf от имени администратора и редактируйте ipv4 и ipv6 заменив метод на "trust"._

![image](readme/guide_postgres_hba.png)

Подключиться к бд

```bash
sudo -u postgres psql
```

Изменить пароль (ради примера будет 123123)

```SQL
ALTER USER postgres PASSWORD '123123';
```

Создать базу данных

```SQL
CREATE DATABASE geodata
WITH
OWNER postgres
ENCODING 'UTF8'
LC_COLLATE = 'ru_RU.UTF-8'
LC_CTYPE = 'ru_RU.UTF-8'
TEMPLATE template0;
```

Подключиться к базе данных

```SQL
\c geodata
```

Создать таблицу данных

```SQL
CREATE TABLE dataset (
    id SERIAL PRIMARY KEY, 
    polygon_id INTEGER,
    period VARCHAR(10),
    station_name VARCHAR(255), 
    surveillance_zone_characteristics TEXT, 
    adm_area VARCHAR(255),   
    district VARCHAR(255),  
    parameter VARCHAR(255), 
    monthly_average DECIMAL,
    monthly_average_pdkss DECIMAL,
    longitude DECIMAL,
    latitude DECIMAL 
);
```

## Добавление данных из файла CSV в БД

Клонировать репозиторий

```bash
git clone https://github.com/shevtsov-dmitry/geodata-visualizer
```

Переместить датасет из папки проекта в корневую папку PostgresSQL

```bash
sudo cp datasets/data.csv /var/lib/postgres/
```

Добавить датасет в базу данных

```bash
\copy dataset(polygon_id, period, station_name, surveillance_zone_characteristics, adm_area, district, parameter, monthly_average, monthly_average_pdkss, longitude, latitude) FROM '~/data.csv' DELIMITER ';' CSV HEADER;
```

#### примечание

_**CSV HEADER** используется для игнорирования первой строки в CSV файле, в случае, когда в нём первая строка - это названия колонок в датасете._

## Установка python

```bash
sudo apt install python3-full
```

Активировать виртуальную среду из корневой папки проекта

```bash
source ./bin/activate
pip install --upgrade pip
```

Необходимо установить библиотеки. Вы можете это сделать с помощью команды:

```bash
pip install flask folium pandas sqlalchemy psycopg2-binary geoalchemy2 geopandas gunicorn
```

#### примечание

_В случае возникновения ошибок при установке, прочитайте, что вывела команда. Там будет описана проблема и
дополнительные инструкции по её устранению (а именно, что ещё нужно установить и команда для выполнения)._

## Запуск приложения

Из корневой папки необходимо выполнить команду 

```bash
gunicorn -w 4 -b 127.0.0.1:8000 main:app
```

#### примечание

_Все команды связанные с python выполняются исключительно из виртуальной среды. Для запуска необходимо выполнять команду ```source bin/activate``` из корневой папки проекта._

## Деплой на хостинг (Опционально)

Подключение к удалённому серверу

```bash
ssh [username]@[host_ip_address]
```

Обновление ПО

```bash
apt update && apt upgrade
```

Перезагрузка (опционально)

```bash
systemctl reboot
```

Установить nginx

```bash
apt-get install nginx
```

#### примечание

_**website-domain** это плейсхолдер, который необходимо заменить на домен сайта._

Здесь будет прописана конфигурация веб-сервера.

```bash
nano /etc/nginx/sites-available/website-domain
```

Описание: Конфигурация Nginx:

- Настраивает сервер для прослушивания порта 80 (HTTP).
- Определяет доменное имя.
- Проксирует входящие HTTP-запросы на локальный сервер http://127.0.0.1:8000.
- Передает заголовки клиента для корректного функционирования обратного прокси.

```nginx
server {
    listen 80;
    server_name website-domain.com www.website-domain.com; 

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Поставить флаг на веб-сайт о том, что он обязан быть включённым

```bash
ln -s /etc/nginx/sites-available/website-domain /etc/nginx/sites-enabled/
```

Проверить конфигурационные файлы Nginx на наличие синтаксических ошибок, затем перезагрузить для применения конфигурации

```bash
nginx -t
systemctl reload nginx
```

Запускает Certbot для автоматической выдачи SSL-сертификата через Let's Encrypt и настраивает конфигурацию Nginx для использования HTTPS.

```bash
apt-get install certbot python3-certbot-nginx
certbot --nginx -d website-domain.com
```