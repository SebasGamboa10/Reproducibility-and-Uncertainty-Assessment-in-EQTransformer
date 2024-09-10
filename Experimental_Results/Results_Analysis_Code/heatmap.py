import pandas as pd
import plotly.graph_objs as go
from obspy.core import UTCDateTime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np

#Add the compared experiments paths (heatmaps for each method)
archivo_csv_list = [
    '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST12/2023-49/DETECTION/RESULTS/CPMI_outputs/X_prediction_results.csv',
    '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST12/2023-49/DETECTION/RESULTS/HDC3_outputs/X_prediction_results.csv',
    '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST12/2023-49/DETECTION/RESULTS/RIFO_outputs/X_prediction_results.csv',
    '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST12/2023-49/DETECTION/RESULTS/VPTE_outputs/X_prediction_results.csv',
    '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST12/2023-49/DETECTION/RESULTS/VPLC_outputs/X_prediction_results.csv'
]

archivo2_csv_list = [
    '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST13/2023-49/DETECTION/RESULTS/CPMI_outputs/X_prediction_results.csv',
    '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST13/2023-49/DETECTION/RESULTS/HDC3_outputs/X_prediction_results.csv',
    '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST13/2023-49/DETECTION/RESULTS/RIFO_outputs/X_prediction_results.csv',
    '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST13/2023-49/DETECTION/RESULTS/VPTE_outputs/X_prediction_results.csv',
    '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST13/2023-49/DETECTION/RESULTS/VPLC_outputs/X_prediction_results.csv'
]

heatmap_data = []

for archivo_csv, archivo2_csv in zip(archivo_csv_list, archivo2_csv_list):
    df = pd.read_csv(archivo_csv)
    df2 = pd.read_csv(archivo2_csv)

    df['event_start_time'] = pd.to_datetime(df['event_start_time'])
    df = df.sort_values(by='event_start_time')
    df2['event_start_time'] = pd.to_datetime(df2['event_start_time'])
    df2 = df2.sort_values(by='event_start_time')

    df_hourly = df.resample('H', on='event_start_time').size().reset_index(name='event_count')
    df2_hourly = df2.resample('H', on='event_start_time').size().reset_index(name='event_count')

    merged_df = pd.merge(df_hourly, df2_hourly, on='event_start_time', how='outer', suffixes=('_exp1', '_exp2')).fillna(0)
    merged_df['event_diff'] = merged_df['event_count_exp1'] - merged_df['event_count_exp2']
    merged_df['event_diff'] = abs(merged_df['event_diff'])

    heatmap_data.append(merged_df['event_diff'].tolist())

heatmap_data = np.array(heatmap_data)

fig = go.Figure(data=go.Heatmap(
    z=heatmap_data,
    x=merged_df['event_start_time'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
    y=['CPMI','HDC3','RIFO','VPTE','VPLC'],
    colorscale='PuBu',
    texttemplate="%{z}",
    textfont={"size":20},
    cbar_kws={'label': 'colorbar title'}
))

fig.update_layout(
    #title='Heatmap',
    xaxis_title='Time',
    yaxis_title='Stations',
    template='plotly_white'
)

fig.write_image('/work/sgamboa/Dropout_TEST/NEW_TEST/1.Results/V100_Predictor/CPMI/Ev_dif.png')
