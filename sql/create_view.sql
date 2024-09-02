CREATE VIEW cleaned_data_global AS 
SELECT
    CAST(gsod.year AS INT64) AS year,
    CAST(gsod.mo AS INT64) AS mo,
    CAST(gsod.da AS INT64) AS day,
    gsod.temp,
    gsod.prcp,
    SAFE_CAST(gsod.mxpsd AS FLOAT64) AS max_wind_speed,
    gsod.max AS max_temp_day,
    stations.country AS region
FROM
    `bigquery-public-data.noaa_gsod.gsod*` AS gsod
JOIN 
    `bigquery-public-data.noaa_gsod.stations` AS stations
ON 
    gsod.stn = stations.usaf
WHERE
    _TABLE_SUFFIX BETWEEN '1929' AND '2023'
    AND gsod.stn != '999999' -- https://www.ncei.noaa.gov/data/global-summary-of-the-day/doc/readme.txt
    AND CAST(temp AS STRING) NOT LIKE '999.9' 
    AND CAST(max AS STRING) NOT LIKE '9999.9' 
    AND CAST(min AS STRING) NOT LIKE '9999.9'
    AND (flag_min IS NULL OR flag_min = '') 
    AND (flag_max IS NULL OR flag_max = '');

CREATE VIEW cleaned_data_usa AS 
SELECT
    CAST(gsod.year AS INT64) AS year,
    CAST(gsod.mo AS INT64) AS mo,
    CAST(gsod.da AS INT64) AS day,
    gsod.temp,
    gsod.prcp,
    SAFE_CAST(gsod.mxpsd AS FLOAT64) AS max_wind_speed,
    gsod.max AS max_temp_day,
    stations.state AS region
FROM
    `bigquery-public-data.noaa_gsod.gsod*` AS gsod
JOIN 
    `bigquery-public-data.noaa_gsod.stations` AS stations
ON 
    gsod.stn = stations.usaf
WHERE
    _TABLE_SUFFIX BETWEEN '1929' AND '2023'
    AND stations.country = 'US'
    AND gsod.stn != '999999' -- https://www.ncei.noaa.gov/data/global-summary-of-the-day/doc/readme.txt
    AND CAST(temp AS STRING) NOT LIKE '999.9' 
    AND CAST(max AS STRING) NOT LIKE '9999.9' 
    AND CAST(min AS STRING) NOT LIKE '9999.9'
    AND (flag_min IS NULL OR flag_min = '') 
    AND (flag_max IS NULL OR flag_max = '');