import os
import sys
import argparse
from analysis.utils import init_bigquery
from analysis.temperature_analysis import perform_temperature_analysis
from analysis.precipitation_analysis import perform_precipitation_analysis
from analysis.extreme_events_analysis import perform_extreme_events_analysis

import warnings
warnings.filterwarnings('ignore', message='BigQuery Storage module not found, fetch data with the REST endpoint instead.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_set', help='Your cleaned data set')
    parser.add_argument('label', help='A label used in figure filenames and chart titles')
    parser.add_argument('-t', '--temperature', action='store_true', help='Perform temperature analysis')
    parser.add_argument('-p', '--precipitation', action='store_true', help='Perform precipitation analysis')
    parser.add_argument('-e', '--extreme', action='store_true', help='Perform extreme events analysis')
    parser.add_argument('-a', '--all', action='store_true', help='Perform all analyses')

    if not any(arg in sys.argv for arg in ['-t', '-p', '-e', '-a']):
        parser.print_help()
        sys.exit(1) 

    base_directory_vis = '../visualizations'
    subdirectories = ['extreme_events', 'temperature', 'precipitation']

    if not os.path.exists(base_directory_vis):
        os.makedirs(base_directory_vis)
        print(f'Created visualizations directory: {base_directory_vis}')

    for subdir in subdirectories:
        directory_path = os.path.join(base_directory_vis, subdir) 
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f'Created visualizations subdirectory: {directory_path}')

    cache_base_dir = '../cache'
    if not os.path.exists(cache_base_dir):
        os.makedirs(cache_base_dir)
        print(f'Created cache directory: {cache_base_dir}')

    for subdir in subdirectories:
        cache_subdir = os.path.join(cache_base_dir, subdir)
        if not os.path.exists(cache_subdir):
            os.makedirs(cache_subdir)
            print(f'Created cache subdirectory: {cache_subdir}')

    init_bigquery()
    args = parser.parse_args()

    cleaned_data = args.data_set
    label = args.label

    if args.temperature:
        perform_temperature_analysis(cleaned_data, label)

    if args.precipitation:
        perform_precipitation_analysis(cleaned_data, label)

    if args.extreme:
        perform_extreme_events_analysis(cleaned_data, label)

    if args.all:
        perform_temperature_analysis(cleaned_data, label)
        perform_precipitation_analysis(cleaned_data, label)
        perform_extreme_events_analysis(cleaned_data, label)