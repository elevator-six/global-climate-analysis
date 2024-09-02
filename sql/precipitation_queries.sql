-- What is the average precipitation in the past 5 years (2019-2023)?
-- Comparison with Historical Average (previous 5 years)
WITH recent_precipitation AS (
    SELECT
        ROUND(AVG(prcp), 2) AS avg_percipitation_recent
    FROM
        {cleaned_data}
    WHERE
        year BETWEEN 2019 AND 2023
        AND prcp != 99.99  -- Exclude invalid data
),

historical_precipitation AS (
    SELECT
        ROUND(AVG(prcp), 2) AS avg_percipitation_historical
    FROM
        {cleaned_data}
    WHERE
        year BETWEEN 2014 AND 2018
        AND prcp != 99.99  -- Exclude invalid data
)

SELECT 
    avg_percipitation_recent,
    avg_percipitation_historical,
    avg_percipitation_recent - avg_percipitation_historical AS precipitation_difference
FROM 
    recent_precipitation
CROSS JOIN
    historical_precipitation;

-- Analyze how precipitation has varied by season over the past 20 years.
WITH seasonal_data AS (
    SELECT
        year,
        CASE 
            WHEN mo IN (3, 4, 5) THEN 'Spring'
            WHEN mo IN (6, 7, 8) THEN 'Summer'
            WHEN mo IN (9, 10, 11) THEN 'Autumn'
            WHEN mo IN (12, 1, 2) THEN 'Winter'
        END AS season,
        ROUND(AVG(prcp), 2) AS avg_precipitation
    FROM
        {cleaned_data}
    WHERE
        year BETWEEN 2004 AND 2023
        AND prcp != 99.99  -- Exclude invalid data
    GROUP BY
        year, season
)

SELECT
    year,
    season,
    avg_precipitation
FROM
    seasonal_data
ORDER BY
    year, 
    CASE season
        WHEN 'Spring' THEN 1
        WHEN 'Summer' THEN 2
        WHEN 'Autumn' THEN 3
        WHEN 'Winter' THEN 4
    END;

-- Non-seasonal

SELECT
    year,
    ROUND(AVG(prcp), 2) AS avg_precipitation
FROM
    {cleaned_data}
WHERE
    prcp != 99.99  -- Exclude invalid data
GROUP BY year
ORDER BY year ASC;

-- Total Precipitation by Year
SELECT
    year,
    ROUND(SUM(prcp), 2) AS total_precipitation
FROM
    {cleaned_data}
WHERE
    prcp != 99.99  -- Exclude invalid data
GROUP BY year
ORDER BY year ASC;