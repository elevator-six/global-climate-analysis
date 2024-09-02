-- What are the average, highest, and lowest temperatures recorded in the past decade (2014-2023)?
SELECT
    region,
    ROUND(AVG(temp), 2) AS avg_temp,
    ROUND(MAX(temp), 2) AS highest_temp,
    ROUND(MIN(temp), 2) AS lowest_temp
FROM
    {cleaned_data} 
WHERE
    year BETWEEN 2014 AND 2023
    AND region IS NOT NULL
GROUP BY
    region;

-- How have average temperatures changed over the entire dataset period (1929-present)?
-- Seasonal --
WITH seasonal_temp_data AS (
    SELECT
        year,
        CASE 
            WHEN mo IN (3, 4, 5) THEN 'Spring'
            WHEN mo IN (6, 7, 8) THEN 'Summer'
            WHEN mo IN (9, 10, 11) THEN 'Autumn'
            WHEN mo IN (12, 1, 2) THEN 'Winter'
        END AS season,
        ROUND(AVG(temp), 2) AS avg_temp
    FROM
        {cleaned_data} 
    WHERE
        year BETWEEN 1929 AND 2024
    GROUP BY
        year,
        season
)

SELECT
    year,
    season,
    avg_temp
FROM
    seasonal_temp_data 
ORDER BY
    year, 
    CASE season
        WHEN 'Spring' THEN 1
        WHEN 'Summer' THEN 2
        WHEN 'Autumn' THEN 3
        WHEN 'Winter' THEN 4
    END;

-- Yearly --
SELECT 
    year, 
    ROUND(AVG(temp), 2) AS avg_temp
FROM 
    {cleaned_data} 
WHERE 
    year BETWEEN 1929 AND 2024
GROUP BY 
    year
ORDER BY
    year; 

-- Identify the top 5 stations that have experienced the most significant temperature increases in the past decade.
WITH decade_temp_data AS (
    SELECT
        region AS region,
        ROUND(AVG(IF(year = 2014, temp, NULL)), 2) AS avg_temp_2014,
        ROUND(AVG(IF(year = 2023, temp, NULL)), 2) AS avg_temp_2023
    FROM
        {cleaned_data} 
    WHERE
        year IN (2014, 2023)
    GROUP BY
        region
)

SELECT
    region,
    avg_temp_2014,
    avg_temp_2023,
    (avg_temp_2023 - avg_temp_2014) AS temp_increase
FROM
    decade_temp_data 
ORDER BY
    temp_increase DESC
LIMIT 5;