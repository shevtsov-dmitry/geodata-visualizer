CREATE TABLE dataset
(
    id                                BIGINT PRIMARY KEY,
    date                              TIMESTAMP,
    global_id                         BIGINT,
    station_name                      VARCHAR(255),
    latitude                          DOUBLE PRECISION,
    longitude                         DOUBLE PRECISION,
    surveillance_zone_characteristics VARCHAR(510),
    adm_area                          VARCHAR(510),
    district                          VARCHAR(510),
    location                          VARCHAR(510),
    parameter                         VARCHAR(255),
    monthly_average                   DOUBLE PRECISION,
    monthly_average_pdkss             DOUBLE PRECISION
);