CREATE TABLE dataset (
    id SERIAL PRIMARY KEY, -- ID из CSV файла, либо автогенирирующееся
    period VARCHAR(10),      -- Период (например, 'янв.22', 'май.22')
    station_name VARCHAR(255), -- Название станции
    surveillance_zone_characteristics TEXT, -- Характеристики зоны наблюдения
    adm_area VARCHAR(255),   -- Административный округ
    district VARCHAR(255),    -- Район
    parameter VARCHAR(255),   -- Параметр (например, 'Взвешенные частицы РМ2.5')
    monthly_average DECIMAL,  -- Среднемесячное значение
    monthly_average_pdkss DECIMAL, -- Среднемесячное значение в долях ПДКсс
    longitude DECIMAL,        -- Долгота
    latitude DECIMAL         -- Широта
);
