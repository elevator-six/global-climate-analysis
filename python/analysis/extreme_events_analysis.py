import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from . import utils

def plot_event_trends_log_scale(df, label):
    plt.figure(figsize=(10, 6))

    color_map = {
        'Heatwave': '#D55E00',  # Orange
        'Strong Winds': '#009E73',  # Green
        'Heavy Rainfall': '#0072B2',  # Dark blue
    }

    sns.lineplot(data=df, x='year', y='event_count', hue='event_type', palette=color_map)

    plt.title(f'Trend of Extreme Weather Event Counts Over Time ({label} , Logarithmic Scale)')
    plt.xlabel('Year')
    plt.ylabel('Event Count (Log Scale)')
    plt.yscale('log')  # Set y-axis to logarithmic scale
    plt.xticks(np.arange(df['year'].min(), df['year'].max() + 1, 2), rotation=45) 

    # Make the x axis labels fit
    margin = (df['year'].max() - df['year'].min()) * 0.02 
    plt.xlim(df['year'].min() - margin, df['year'].max() + margin) 
    plt.legend(title='Event Type')

    plt.savefig(f'../visualizations/extreme_events/{label.lower()}_extreme_event_counts_trend_log_scale.png')
    # plt.show()

def plot_event_trends(df, label):
    plt.figure(figsize=(10, 6))

    color_map = {
        'Heatwave': '#D55E00',  # Orange
        'Strong Winds': '#009E73',  # Green
        'Heavy Rainfall': '#0072B2',  # Dark blue
    }

    sns.lineplot(data=df, x='year', y='event_count', hue='event_type', palette=color_map)

    plt.title(f'Trend of Extreme Weather Event Counts Over Time ({label})')
    plt.xlabel('Year')
    plt.ylabel('Event Count')
    plt.xticks(np.arange(df['year'].min(), df['year'].max() + 1, 2), rotation=45) 

    # Make the x axis labels fit
    margin = (df['year'].max() - df['year'].min()) * 0.02
    plt.xlim(df['year'].min() - margin, df['year'].max() + margin) 
    plt.legend(title='Event Type')

    plt.savefig(f'../visualizations/extreme_events/{label.lower()}_extreme_event_counts_trend.png')
    # plt.show()

def visualize_extreme_event_shifts(df, data_label):
    df_count_change = df.pivot(index='region', columns='event_type', values='count_change')

    # Sort by absolute change in count (descending)
    df_count_change['abs_total_change'] = df_count_change.abs().sum(axis=1)
    df_count_change_sorted = df_count_change.sort_values('abs_total_change', ascending=False)
    df_count_change_sorted.drop(columns=['abs_total_change'], inplace=True)

    # FacetGrid for count change, log scale, and better spacing
    g = sns.FacetGrid(df_count_change_sorted.reset_index().melt(id_vars='region'), 
                      col='event_type', sharey=False, height=5, aspect=1.2)
    g.map(sns.barplot, 'region', 'value', order=df_count_change_sorted.index)
    g.set_titles(col_template='{col_name}') 
    g.set_axis_labels('Region', 'Change in Count (Log Scale)')
    g.set(yscale='symlog') 
    for ax in g.axes.flat:
        for xtick_label in ax.get_xticklabels():
            xtick_label.set_rotation(45)

    plt.subplots_adjust(top=0.9) 
    g.figure.suptitle(f'Change in Extreme Event Counts by Region and Type ({data_label}, 2004-2013 vs 1994-2003)')
    plt.savefig(f'../visualizations/extreme_events/{data_label.lower()}_extreme_event_count_change_faceted.png')

    df_intensity_change = df.pivot(index='region', columns='event_type', values='intensity_change')

    # Sort by absolute change in intensity (descending)
    df_intensity_change['abs_total_change'] = df_intensity_change.abs().sum(axis=1)
    df_intensity_change_sorted = df_intensity_change.sort_values('abs_total_change', ascending=False)
    df_intensity_change_sorted.drop(columns=['abs_total_change'], inplace=True)

    # FacetGrid for intensity change
    g = sns.FacetGrid(df_intensity_change_sorted.reset_index().melt(id_vars='region'), 
                      col='event_type', sharey=False, height=5, aspect=1.2)
    g.map(sns.barplot, 'region', 'value', order=df_intensity_change_sorted.index)
    g.set_titles(col_template='{col_name}')
    g.set_axis_labels('Region', 'Change in Intensity')
    for ax in g.axes.flat:
        for xtick_label in ax.get_xticklabels():
            xtick_label.set_rotation(45)

    plt.subplots_adjust(top=0.9)
    g.figure.suptitle(f'Change in Average Extreme Event Intensity by Region and Type ({data_label}, 2004-2013 vs 1994-2003)')
    plt.savefig(f'../visualizations/extreme_events/{data_label.lower()}_extreme_event_intensity_change_faceted.png')

def perform_extreme_events_analysis(cleaned_data, label):
    cache_dir = '../cache/extreme_events'
    queries_file = '../sql/extreme_events_queries.sql'

    df_3_1, df_3_2 = utils.load_data_and_cache(cache_dir, queries_file, cleaned_data, label)

    plot_event_trends(df_3_1, label)
    plot_event_trends_log_scale(df_3_1, label)
    visualize_extreme_event_shifts(df_3_2, label)