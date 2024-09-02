import numpy as np
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy.stats import linregress

from . import utils

def plot_temp_extremes_by_region(df, label):
    df_sorted = df.sort_values('avg_temp', ascending=False)

    plt.figure(figsize=(10, 6))

    cmap = cm.get_cmap('RdYlBu_r') 
    norm = plt.Normalize(df_sorted['avg_temp'].min(), df_sorted['avg_temp'].max())

    sc = plt.scatter(
        df_sorted['lowest_temp'],
        df_sorted['highest_temp'],
        c=df_sorted['avg_temp'], 
        cmap=cmap,
        norm=norm,
        alpha=0.7
    )

    cbar = plt.colorbar(sc)
    cbar.set_label('Average Temperature (°F)')

    plt.xlabel('Minimum Temperature (°F)')
    plt.ylabel('Maximum Temperature (°F)')
    plt.title(f'Temperature Extremes by Region ({label}, 2014-2023)')

    plt.tight_layout()
    plt.savefig(f'../visualizations/temperature/{label.lower()}_temp_extremes.png', dpi=300)
    #plt.show()

def plot_avg_temp_by_season(df, label):
    palette = {
        "Spring": "#0072B2",  # Dark blue 
        "Summer": "#D55E00",  # Orange 
        "Autumn": "#009E73",  # Green 
        "Winter": "#56B4E9",  # Light blue 
    }

    plt.figure(figsize=(10, 6))
    sns.lineplot(
        x='year',
        y='avg_temp',
        hue='season',
        data=df,
        palette=palette,
        markers=False,
        linewidth=2.5,
    )

    plt.grid(True, linewidth=0.5, alpha=0.7)

    plt.title(f'Average Temperature by Season Over Time ({label})')
    plt.xlabel('Year')
    plt.ylabel('Average Temperature (°F)')
    plt.legend(title='Season')
    plt.xticks(np.arange(df['year'].min(), df['year'].max() + 1, 2), rotation=45) 
    plt.yticks(range(int(df['avg_temp'].min()), int(df['avg_temp'].max()) + 1, 2))

    # Make the x axis labels fit
    margin = (df['year'].max() - df['year'].min()) * 0.02
    plt.xlim(df['year'].min() - margin, df['year'].max() + margin) 
    plt.tight_layout()

    plt.savefig(f'../visualizations/temperature/{label.lower()}_avg_temp_by_season_over_time.png')

def plot_avg_temp_by_season_small_multiples(df, label):
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

        sns.lineplot(
            x='year',
            y='avg_temp',
            data=season_data,
            ax=ax,
            color=palette[season],
            linewidth=2.5,
        )

        # Linear regression for the season
        slope, intercept, _, _, _ = linregress(season_data['year'], season_data['avg_temp'])
        trend_line = slope * season_data['year'] + intercept

        # Plot the trend line
        ax.plot(season_data['year'], trend_line, color='black', label='Trend Line')

        ax.set_title(season)
        ax.set_xlabel('Year' if i in [2, 3] else '') 
        ax.set_ylabel('Avg. Temp (°F)' if i in [0, 2] else '') 

        ax.grid(True, linewidth=0.5, alpha=0.7)

        margin = (df['year'].max() - df['year'].min()) * 0.02 
        ax.set_xlim(df['year'].min() - margin, df['year'].max() + margin) 
        ax.set_xticks(np.arange(df['year'].min(), df['year'].max() + 1, 4))
        ax.set_xticklabels(np.arange(df['year'].min(), df['year'].max() + 1, 4), rotation=45)

        ax.set_yticks(range(int(df['avg_temp'].min()) - 1, int(df['avg_temp'].max()) + 2, 3))
        ax.legend()

    fig.suptitle(f'Average Temperature by Season Over Time ({label})', fontsize=14)
    plt.tight_layout()

    plt.savefig(f'../visualizations/temperature/{label.lower()}_avg_temp_by_season_small_multiples.png')

def plot_avg_yearly_temp_trend(df, label):
    # Anomaly Detection
    mean_temp = df['avg_temp'].mean()
    std_dev = df['avg_temp'].std()
    threshold = 2 * std_dev
    df['anomaly'] = (df['avg_temp'] - mean_temp).abs() > threshold

    # Regression Analysis
    slope, intercept, r_value, p_value, std_err = linregress(df['year'], df['avg_temp'])
    trend_line = slope * df['year'] + intercept

    plt.figure(figsize=(10, 6))
    sns.lineplot(
        x='year',
        y='avg_temp',
        data=df,
        color='blue',
        label='Yearly Average',
        linewidth=2,
    )

    # Plot anomalies
    plt.scatter(
        df[df['anomaly']]['year'], 
        df[df['anomaly']]['avg_temp'], 
        color='orange',
        marker='o', 
        label='Anomaly'
    )

    plt.plot(df['year'], trend_line, color='black', label='Trend Line')

    plt.title(f'Average Yearly Temperature Trend ({label})')
    plt.xlabel('Year')
    plt.ylabel('Average Temperature (°F)')
    plt.xticks(np.arange(df['year'].min(), df['year'].max() + 1, 2), rotation=45) 
    plt.yticks(range(int(df['avg_temp'].min()), int(df['avg_temp'].max()) + 1, 2))

    # Make the x axis labels fit
    margin = (df['year'].max() - df['year'].min()) * 0.02 
    plt.xlim(df['year'].min() - margin, df['year'].max() + margin) 
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'../visualizations/temperature/{label.lower()}_avg_yearly_temp_trend.png')

def perform_temperature_analysis(cleaned_data, label):
    cache_dir = '../cache/temperature'
    queries_file = '../sql/temperature_queries.sql'

    df_1_1, df_1_2, df_1_3, df_1_4 = utils.load_data_and_cache(cache_dir, queries_file, cleaned_data, label)

    plot_temp_extremes_by_region(df_1_1, label)

    plot_avg_temp_by_season(df_1_2, label)
    plot_avg_temp_by_season_small_multiples(df_1_2, label)

    plot_avg_yearly_temp_trend(df_1_3, label)

    print(df_1_4)
