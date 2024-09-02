# Analyzing Global Weather Patterns and Trends (1929-Present)

**Overview:**

This study explores weather patterns and trends worldwide by utilizing the NOAA Global Summary of the Day (GSOD) dataset on BigQuery. Through the use of SQL for data retrieval and manipulation along with Python for analysis and visualization this research reveals findings on temperature variations, precipitation trends and the prevalence of extreme weather occurrences. With an additional analysis of the USA on a state level.

**Table of Contents:**

* [Key Questions Addressed](#key-questions-addressed)
    * [Global Temperature Trends](#global-temperature-trends)
    * [Global Precipitation Analysis](#global-precipitation-analysis)
    * [Global Extreme Weather Events](#global-extreme-weather-events)
    * [Deep Dive into the United States](#deep-dive-into-the-united-states)
* [Data and Tools](#data-and-tools) 
    * [Data](#data)
    * [Methods](#methods)
* [Project Structure](#project-structure)
* [How to Run the Project](#how-to-run-the-project)
    * [Prerequisites](#prerequisites)
    * [Running the Analysis](#running-the-analysis)
* [Key Visualizations](#key-visualizations)
    * [Temperature Trends](#temperature-trends)
    * [Precipitation Patterns](#precipitation-patterns)
    * [Extreme Weather Events](#extreme-weather-events)
* [Conclusion](#conclusion)
* [Challenges and Methodologies](#challenges-and-methodologies)
* [Recommendations and Future Work](#recommendations-and-future-work--todo)

## Key Questions Addressed:

### Global Temperature Trends:

* What are the average, highest, and lowest temperatures recorded globally in the past decade (2014-2023)?
* How have global average temperatures evolved over time (1929-present)?
* Which 5 stations worldwide have experienced the most significant temperature increases in the past decade?

### Global Precipitation Analysis:

* What is the global average precipitation in the past 5 years (2019-2023) compared to the previous 5 years (2014-2018)?
* How has global precipitation varied by season over the past 20 years?

### Global Extreme Weather Events:

* How have the frequency and intensity of extreme weather events (heatwaves, heavy rainfall, strong winds) changed over time?
* Which regions have undergone the most significant shifts in the frequency or intensity of extreme weather events between 1994-2003 and 2004-2013?

### Deep Dive into the United States:

* Replicate the global analysis for the United States, focusing on temperature, precipitation, and extreme weather event trends.

## Data and Tools

### Data:

* NOAA Global Summary of the Day (GSOD) dataset on BigQuery

### Methods:

* **SQL:** Data extraction, cleaning, transformation, and aggregation using BigQuery.
* **Python:** Data analysis, visualization, and statistical modeling using `matplotlib`, `seaborn`, `pandas`, and `scipy`.

## Project Structure:

* **/python:**
    * `main.py`: Main script to execute the analysis.
    * **/analysis:**
        * `temperature_analysis.py`
        * `precipitation_analysis.py`
        * `extreme_events_analysis.py`
        * `utils.py`: Helper functions for data fetching and visualization.
* **/sql:**
    * `create_view.sql`: Creates cleaned views of the raw data for USA and Global datasets
    * `temperature_queries.sql`
    * `precipitation_queries.sql`
    * `extreme_events_queries.sql`
* **/visualizations:** Generated charts and maps will be saved here
* `README.md`: This project overview

## How to Run the Project:

### Prerequisites:

* **Google Cloud SDK:** Install and initialize the Google Cloud SDK (`gcloud init`).
* **Authentication:** Authenticate to your BigQuery project (`gcloud auth application-default login`).
* **BigQuery Project:** 
    * Set up a Google Cloud project with BigQuery enabled.
    * Once your project is created, set it as the current project using the following command, replacing `[YOUR_PROJECT_ID]` with your actual project ID:

    ```bash
    gcloud config set project [YOUR_PROJECT_ID]
    ```

### Running the Analysis:

1.  **Set up environment:** Create and activate a virtual environment. Install required packages: `pip install -r requirements.txt`
2.  **Prepare the data:**
  * Run the SQL queries in `create_view.sql` within the BigQuery console to create the cleaned data views.
3.  **Run the analysis:** Execute `main.py` from the command line, providing the necessary arguments:

  ```bash
  py main.py data_set label [-t] [-p] [-e] [-a]
  ```

  * `data_set`: The name of the cleaned data view (e.g., `gsod_analysis.cleaned_data_usa` or `gsod_analysis.cleaned_data_global`)
  * `label`: A label for the output (e.g., 'USA' or 'Global')
  * `-t`: Perform temperature analysis
  * `-p`: Perform precipitation analysis
  * `-e`: Perform extreme events analysis
  * `-a`: Perform all analyses

**Example Usage:**

```bash
py main.py gsod_analysis.cleaned_data_global "Global" -a
````

## Key Visualizations:

The project generates a variety of visualizations to illustrate the findings. Here are some examples showcasing both global and US trends:

* ### Temperature Trends:

    * **Global Average Yearly Temperature Trend:** Illustrates the gradual increase in global average temperatures over time.
    [![Average Yearly Temperature Trend (World)](/visualizations/temperature/global_avg_yearly_temp_trend.png)](/visualizations/temperature/global_avg_yearly_temp_trend.png)

    * **USA Average Yearly Temperature Trend:** Demonstrates how US temperatures have converged with the global average, highlighting regional variations in climate change.
    [![Average Yearly Temperature Trend (USA)](/visualizations/temperature/usa_avg_yearly_temp_trend.png)](/visualizations/temperature/usa_avg_yearly_temp_trend.png)

* ### Precipitation Patterns:

    * **Global Seasonal Precipitation:** Visualizes the consistent seasonal patterns in global precipitation, with no major shifts observed over time.
    [![Seasonal Precipitation (World)](/visualizations/precipitation/global_seasonal_precipitation_small_multiples.png)](/visualizations/precipitation/global_seasonal_precipitation_small_multiples.png)

* ### Extreme Weather Events:

    * **Trend of Global Extreme Weather Event Counts:** Showcases the increasing frequency of extreme weather events globally, emphasizing the urgency of addressing climate change.
    [![Trend of Extreme Weather Event Counts](/visualizations/extreme_events/global_extreme_event_counts_trend.png)](/visualizations/extreme_events/global_extreme_event_counts_trend.png)

    * **Change in Extreme Event Intensity (Global vs. USA):** Compares the trends in intensity of extreme weather events between the globe and the USA, highlighting regional differences.

    [![Change in Global Extreme Event Intensity](/visualizations/extreme_events/global_extreme_event_intensity_change_faceted.png)](/visualizations/extreme_events/global_extreme_event_intensity_change_faceted.png)

    [![Change in USA Extreme Event Intensity](/visualizations/extreme_events/usa_extreme_event_intensity_change_faceted.png)](/visualizations/extreme_events/usa_extreme_event_intensity_change_faceted.png)

## Conclusion:

This analysis of global weather patterns from 1929 to the present reveals several key trends:

* **Global Precipitation Trends:** The average amount of precipitation worldwide each year seems to have leveled off recently, with no major increases or decreases overall or in any particular season. There was a small drop of 0.01 inches over the last 5 years compared to the 5 years before that. However, if we look at the big picture, the total amount of precipitation each year around the globe has been steadily going up since 2000.

* **US Precipitation Trends:** In the US, there's been a slight increase in the average yearly rainfall for Spring, Summer, and Winter.  Over the past 5 years, the average hasn't changed compared to the 5 years before that. Just like the global trend, the US has also experienced a noticeable increase in total yearly precipitation since 2000.

* **Global Warming Trend:** The average temperature around the world is slowly but steadily rising, without any unusual changes from season to season. 

* **USA Temperature Convergence:** While the US saw a drop in temperatures, it's now in a similar range (50-60°F) to the global average. No major seasonal temperature swings were observed in the US either.

* **Extreme Weather Events Escalating:** The number of all types of extreme weather events is on the rise both globally and in the USA. However, the increase is happening a bit slower in the USA. Heatwaves are the most common extreme event in the USA, while strong winds are more frequent globally. 

* **Intensity Divergence:** Interestingly, while the intensity of extreme weather events has been decreasing globally, with a particular decrease noted in strong winds within the USA, the overall intensity has actually been increasing within the USA.

### Challenges and Methodologies:

* **Data Quality and Completeness:** The visuals hint that the data recorded before 1970 may be less reliable due to limitations in data collection and recording practices at that time. Even though invalid entries were filtered out based on NOAA GSOD guidelines, the accuracy and completeness of older records might still be affected. This highlights the importance of either checking the findings against other data sources or focusing the analysis on data from 1970 onwards. This will help ensure any conclusions drawn about long-term trends are accurate.

* **Data Aggregation and Visualization:** Analyzing data from thousands of weather stations worldwide posed challenges due to the sheer volume of data and the need to create easily understandable visuals. To improve clarity and efficiency, the data was grouped by country (or state, when focusing on the USA). Visualizations were created to present this complex information in a clear and concise manner.

* **Defining Extreme Weather Events:** To pinpoint extreme weather events, established criteria were used to set thresholds for temperature, precipitation, and wind speed. While a heatwave is often defined as three or more consecutive days at or above 90 degrees, a more conservative threshold of 95 degrees was chosen to ensure accuracy. Heavy rain was classified as 3 inches or more in a single day, and strong winds as those exceeding 40 MPH.

* **Python for Automation and Flexibility:** Python helped streamline everything, making it easy to run SQL queries, handle the data, and create those visuals. This means the analysis can be easily adapted to focus on different regions or time periods, even zooming in on a specific state within the US if desired.

### Recommendations and Future Work / TODO:

* **Cross-Validate with Additional Datasets:** Incorporate data from other sources to verify and strengthen the findings of this analysis.
* **Deeper Regional Analysis:** Dig even deeper into the data, examining weather patterns and trends at the state, county, or even city level. Spotting local anomolies or patterns as compared to a large scale, potentially discovering areas with concerning patterns.
* **Investigate Underlying Causes:** Explore potential factors driving the observed trends, such as greenhouse gas emissions, deforestation, or natural climate cycles.
* **Predict Future Trends:** Utilize advanced statistical modeling or machine learning techniques to forecast future weather patterns and their potential impacts.
* **Dig Deeper into Rainfall:** Take a closer look at rainfall patterns, including droughts, unusual events, and how things differ from one region to another. Create visuals to highlight areas with strange or worrisome rainfall trends.
* **Connect the Dots:** Bring together all the charts and graphs from the analysis to see if any patterns emerge. For instance, we might notice that a year with less rainfall also saw higher temperatures and more heatwaves.

This project gives us a good look at what's happening with the weather around the world, showing us both worrying changes and areas where we need to do more research. By using the approaches outlined here and tackling the problems we've identified, future studies can build on this work and help us better understand our changing climate so we can find ways to deal with it.
