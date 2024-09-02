import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from . import utils

def plot_avg_precipitation(df, label):
    plt.figure(figsize=(10, 6))
    plt.bar(['Recent (2019-2023)', 'Historical (2014-2018)'], df[['avg_percipitation_recent', 'avg_percipitation_historical']].values[0])
    plt.ylabel('Average Precipitation')
    
    plt.title(f'Average Precipitation ({label}, 5 Year Recent vs. Historical)')

    for i, v in enumerate(df[['avg_percipitation_recent', 'avg_percipitation_historical']].values[0]):
        plt.text(i, v, str(v), ha='center', va='bottom')

    plt.savefig(f'../visualizations/precipitation/{label.lower()}_avg_precipitation.png')
    #plt.show()

def plot_seasonal_precipitation_small_multiples(df, label):
    palette = {
        "Spring": "#0072B2",  # Dark blue 
        "Summer": "#D55E00",  # Orange
        "Autumn": "#009E73",  # Green 
        "Winter": "#56B4E9",  # Light blue
    }

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)
    axes = axes.flatten()

    for i, season in enumerate(df['season'].unique()):
        season_data = df[df['season'] == season]
        ax = axes[i]

        ax.plot(
            season_data['year'],
            season_data['avg_precipitation'],
            linewidth=2,
            color=palette[season],
        )

        sns.regplot(
            x='year', 
            y='avg_precipitation', 
            data=season_data, 
            ax=ax, 
            color=palette[season], 
            scatter_kws={'s': 0} 
        )

        ax.set_title(season)
        ax.set_xlabel('Year' if i in [2, 3] else '')
        ax.set_ylabel('Avg. Precipitation' if i in [0, 2] else '')

        # Make the x axis labels fit
        margin = (df['year'].max() - df['year'].min()) * 0.02 
        ax.set_xlim(df['year'].min() - margin, df['year'].max() + margin) 

        xticks = np.arange(df['year'].min(), df['year'].max() + 1, 2)
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, rotation=45)

    fig.suptitle(f'Precipitation Variation by Season ({label}, 2004-2023)', fontsize=14)
    plt.tight_layout()

    plt.savefig(f'../visualizations/precipitation/{label.lower()}_seasonal_precipitation_small_multiples.png')

def plot_yearly_avg_precipitation(df, label):
    plt.figure(figsize=(10, 6))

    plt.plot(df['year'], df['avg_precipitation'], color='blue', linewidth=2)

    plt.xlabel('Year')
    plt.xticks(np.arange(df['year'].min(), df['year'].max() + 1, 2), rotation=45)

    # Make the x axis labels fit
    margin = (df['year'].max() - df['year'].min()) * 0.02
    plt.xlim(df['year'].min() - margin, df['year'].max() + margin) 
    plt.ylabel('Average Precipitation')
    plt.title(f'Yearly Average Precipitation ({label})')
    plt.grid(True)

    plt.savefig(f'../visualizations/precipitation/{label.lower()}_yearly_avg_precipitation.png')

def plot_yearly_total_precipitation(df, label):
    plt.figure(figsize=(10, 6))

    plt.bar(df['year'], df['total_precipitation'], color='#0072B2')

    plt.xlabel('Year')
    plt.ylabel('Total Precipitation')
    plt.title(f'Yearly Total Precipitation ({label})')
    plt.xticks(np.arange(df['year'].min(), df['year'].max() + 1, 2), rotation=45)
    
    # Make the x axis labels fit
    margin = (df['year'].max() - df['year'].min()) * 0.02
    plt.xlim(df['year'].min() - margin, df['year'].max() + margin) 
    plt.grid(axis='y')

    plt.savefig(f'../visualizations/precipitation/{label.lower()}_yearly_total_precipitation.png')

def perform_precipitation_analysis(cleaned_data, label):
    cache_dir = '../cache/precipitation'

    with open('../sql/precipitation_queries.sql', 'r') as f:
        queries = [query.strip() for query in f.read().split(';') if query.strip()]

    formatted_queries = [query.format(cleaned_data=cleaned_data) for query in queries if query.strip()]

    dataframes = []
    for i, query in enumerate(formatted_queries):
        cache_file = os.path.join(cache_dir, f'df_2_{i+1}_{label}.csv') 

        if os.path.exists(cache_file):
            print(f'Loading {cache_file} from cache...')
            df = pd.read_csv(cache_file)
        else:
            print(f'Fetching data from BigQuery and saving to {cache_file}...')
            df = utils.fetch_data_from_bigquery(query)
            df.to_csv(cache_file, index=False)

        dataframes.append(df)

    df_2_1, df_2_2, df_2_3, df_2_4 = dataframes 

    plot_avg_precipitation(df_2_1, label)

    plot_seasonal_precipitation_small_multiples(df_2_2, label)

    plot_yearly_avg_precipitation(df_2_3, label)

    plot_yearly_total_precipitation(df_2_4, label)