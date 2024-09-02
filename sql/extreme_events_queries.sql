-- How have the frequency and intensity of extreme weather events (heatwaves, heavy rainfall, strong winds) changed over time?
-- Define thresholds for extreme events 
WITH extreme_events AS (
  SELECT 
    *,
    CASE 
        WHEN max_temp_day >= 95 AND max_temp_day != 9999.9 -- Temp 95 and over for 3 days
            AND 
            (
                LAG(max_temp_day, 1) OVER (ORDER BY year, mo, day) >= 95 
                AND 
                LAG(max_temp_day, 2) OVER (ORDER BY year, mo, day) >= 95
            )
            THEN TRUE 
            ELSE FALSE
        END AS heatwave_start,
        CASE
            WHEN prcp >= 3 AND prcp != 99.99 THEN 'Heavy Rainfall' -- Heavy rain = 3 or more inches of rain
            WHEN max_wind_speed >= 40 AND max_wind_speed != 999.9 THEN 'Strong Winds' -- 40 MPH or higher
            ELSE NULL 
        END AS event_type
  FROM {cleaned_data}
),

heatwave_events AS (
    SELECT
        *,
        LAG(heatwave_start) OVER (ORDER BY year, mo, day) AS prev_day_heatwave
    FROM extreme_events
),

final_events AS (
    SELECT
        *,
        CASE
            WHEN heatwave_start 
                AND (prev_day_heatwave IS NULL OR prev_day_heatwave = FALSE) 
                THEN 'Heatwave'
            ELSE event_type
        END AS final_event_type
    FROM heatwave_events
),

event_summary AS (
SELECT
  year,
  final_event_type AS event_type,
  COUNT(*) AS event_count,
  ROUND(AVG(CASE WHEN final_event_type = 'Heatwave' THEN max_temp_day ELSE NULL END), 2) AS avg_heatwave_intensity,
  ROUND(AVG(CASE WHEN final_event_type = 'Heavy Rainfall' THEN prcp ELSE NULL END), 2) AS avg_rainfall_intensity,
  ROUND(AVG(CASE WHEN final_event_type = 'Strong Winds' THEN max_wind_speed ELSE NULL END), 2) AS avg_wind_intensity 
FROM final_events
WHERE final_event_type IS NOT NULL
GROUP BY year, final_event_type
)

SELECT
  year,
  event_type,
  event_count,
  avg_heatwave_intensity,
  avg_rainfall_intensity,
  avg_wind_intensity
FROM event_summary
ORDER BY year, event_type;

-- Which regions have undergone the most significant shifts in the frequency or intensity of extreme weather events?

WITH extreme_events AS (
  SELECT 
    *,
    CASE 
        WHEN max_temp_day >= 95 AND max_temp_day != 9999.9 
            AND 
            (
                LAG(max_temp_day, 1) OVER (ORDER BY year, mo, day) >= 95 
                AND 
                LAG(max_temp_day, 2) OVER (ORDER BY year, mo, day) >= 95
            )
            THEN TRUE 
            ELSE FALSE
        END AS heatwave_start,
        CASE
            WHEN prcp >= 3 AND prcp != 99.99 THEN 'Heavy Rainfall' 
            WHEN max_wind_speed >= 40 AND max_wind_speed != 999.9 THEN 'Strong Winds' 
            ELSE NULL 
        END AS event_type
  FROM {cleaned_data}
),

heatwave_events AS (
    SELECT
        *,
        LAG(heatwave_start) OVER (PARTITION BY region ORDER BY year, mo, day) AS prev_day_heatwave
    FROM extreme_events
),

final_events AS (
    SELECT
        *,
        CASE
            WHEN heatwave_start 
                AND (prev_day_heatwave IS NULL OR prev_day_heatwave = FALSE) 
                THEN 'Heatwave' 
            ELSE event_type
        END AS final_event_type
    FROM heatwave_events
),

event_metrics AS (
  SELECT
    region,
    final_event_type AS event_type,
    COUNTIF(year BETWEEN 2004 AND 2013) AS event_count_recent,
    COUNTIF(year BETWEEN 1994 AND 2003) AS event_count_past,
    ROUND(AVG(CASE WHEN final_event_type = 'Heatwave' AND year BETWEEN 2004 AND 2013 THEN max_temp_day ELSE NULL END), 2) AS avg_heatwave_intensity_recent,
    ROUND(AVG(CASE WHEN final_event_type = 'Heatwave' AND year BETWEEN 1994 AND 2003 THEN max_temp_day ELSE NULL END), 2) AS avg_heatwave_intensity_past,
    ROUND(AVG(CASE WHEN final_event_type = 'Heavy Rainfall' AND year BETWEEN 2004 AND 2013 THEN prcp ELSE NULL END), 2) AS avg_rainfall_intensity_recent,
    ROUND(AVG(CASE WHEN final_event_type = 'Heavy Rainfall' AND year BETWEEN 1994 AND 2003 THEN prcp ELSE NULL END), 2) AS avg_rainfall_intensity_past,
    ROUND(AVG(CASE WHEN final_event_type = 'Strong Winds' AND year BETWEEN 2004 AND 2013 THEN max_wind_speed ELSE NULL END), 2) AS avg_wind_intensity_recent,
    ROUND(AVG(CASE WHEN final_event_type = 'Strong Winds' AND year BETWEEN 1994 AND 2003 THEN max_wind_speed ELSE NULL END), 2) AS avg_wind_intensity_past
  FROM final_events
  WHERE final_event_type IS NOT NULL
  GROUP BY region, final_event_type
),

change_metrics AS (
  SELECT
    region,
    event_type,
    (event_count_recent - event_count_past) AS count_change,
    CASE 
        WHEN event_type = 'Heatwave' THEN avg_heatwave_intensity_recent - avg_heatwave_intensity_past
        WHEN event_type = 'Heavy Rainfall' THEN avg_rainfall_intensity_recent - avg_rainfall_intensity_past
        WHEN event_type = 'Strong Winds' THEN avg_wind_intensity_recent - avg_wind_intensity_past
    END AS intensity_change
  FROM event_metrics
),

ranked_regions AS (
  SELECT
    region,
    event_type,
    ROW_NUMBER() OVER (PARTITION BY event_type ORDER BY ABS(count_change) DESC, ABS(intensity_change) DESC) AS count_change_rank,
    ROW_NUMBER() OVER (PARTITION BY event_type ORDER BY ABS(intensity_change) DESC, ABS(count_change) DESC) AS intensity_change_rank
  FROM change_metrics
)

SELECT 
  ranked_regions.region,
  ranked_regions.event_type,
  change_metrics.count_change,
  ROUND(change_metrics.intensity_change, 2) AS intensity_change
FROM ranked_regions
JOIN change_metrics 
ON ranked_regions.region = change_metrics.region 
AND ranked_regions.event_type = change_metrics.event_type
WHERE count_change_rank <= 5 OR intensity_change_rank <= 5
ORDER BY event_type, count_change_rank, intensity_change_rank;