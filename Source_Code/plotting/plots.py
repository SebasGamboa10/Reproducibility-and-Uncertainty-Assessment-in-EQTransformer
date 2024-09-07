# Python Standard Library
from os import path, listdir
from datetime import datetime
import pickle
import sys
from pathlib import Path

# Other dependencies
import matplotlib.dates as md

# Other dependencies
import matplotlib.pyplot as plt
import pandas as pd

# Local files
# sys.path.insert(0, Path(path.realpath(__file__)).parent.parent)
from utils.catalog import NLLoc_Pha_Reader,  collect2df


DATA_FNAME    = 'data.pkl'
EQT_DET_FNAME = 'X_prediction_results.csv'
EQT_DET_COLS  = ['event_start_time', 'event_end_time',
                 'p_arrival_time', 's_arrival_time']


def get_S_P_data_nlloc(detections_file, stations_csv):
    catalog = NLLoc_Pha_Reader(detections_file, stations_csv).get_catalog()

    df = pd.read_csv(stations_csv)

    data = {}
    for station in df.code.tolist():
        data[station] = []

    for event in catalog:
        for station in df.code.tolist():
            picks = [
                pick for pick in event.picks
                if pick.waveform_id.station_code == station
            ]

            if len(picks) == 2:
                for pick in picks:
                    if pick.phase_hint == 'P':
                        p = pick.time
                    elif pick.phase_hint == 'S':
                        s = pick.time
                data[station].append(s-p)

    with open(path.join(output_dir, DATA_FNAME), 'wb') as f:
        pickle.dump(data, f)
    return


def s_p_time(detections_dir, title='', show=True):
    data = {}
    for folder in listdir(detections_dir):
        station = folder.split('_')[0]

        filepath = path.join(detections_dir, folder, EQT_DET_FNAME)

        if not path.isfile(filepath):
            continue

        df = pd.read_csv(filepath, usecols=EQT_DET_COLS).dropna()

        df.s_arrival_time = pd.to_datetime(df.s_arrival_time)
        df.p_arrival_time = pd.to_datetime(df.p_arrival_time)

        df['s_p'] = (df.s_arrival_time - df.p_arrival_time).dt.total_seconds()

        if len(df) > 1:
            data[station] = {'array': df.s_p.values, 'mean': df.s_p.values.mean()}

    stations = sorted(data, key=lambda x: (data[x]['mean']))

    sorted_data = []
    for i, station in enumerate(stations):
        sorted_data.append(data[station]['array'])

    for station in sorted(stations):
        print(station +','+str(len(data[station]['array'])))
    labels = [station + f' ({len(data[station]["array"])})' for station in stations]
    fig = plt.figure(figsize=(6, 6))
    fig.subplots_adjust(left=.1, bottom=.19, right=.98, top=.92, wspace=.2,
                        hspace=.2)

    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.set_ylim(0, 35)
    ax.set_ylabel('S-P [s]')
    ax.boxplot(sorted_data, showfliers=False)
    ax.set_xticklabels(labels, rotation='vertical')
    if show:
        plt.show()
    return fig


def xy_vs_time(df):
    fig = plt.figure(figsize=(4, 6))
    fig.subplots_adjust(left=.18, bottom=.04, right=.85, top=.98, wspace=.2,
                        hspace=.2)

    ax1 = fig.add_subplot(211)
    # ax1.set_xlabel()
    ax1.set_ylabel('Latitude []')
    ax1.scatter(df.index, df.latitude)

    ax2 = fig.add_subplot(212)
    ax2.set_ylabel('Longitude []')
    # ax2.set_ylabel()
    ax2.scatter(df.index, df.longitude)
    plt.show()
    return


def magnitude_timeseries(df):
    fig = plt.figure(figsize=(6, 6))
    fig.subplots_adjust(left=.18, bottom=.04, right=.85, top=.98, wspace=.2,
                        hspace=.2)

    ax = fig.add_subplot(111)
    ax.scatter(df.index, df.magnitude, c='r', s=10, alpha=.7)
    ax.vlines(df.index, 0, df.magnitude, color='r', linewidth=.3, alpha=.7)
    ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
    ax.set_xlabel('2019')
    ax.set_ylabel('Magnitude')
    plt.show()
    return fig


if __name__ == '__main__':
    out_path = '/Volumes/leo_1/SISMOLOGIA/ARMUELLES_OV/S-P_comparison'

    fig = s_p_time('/Volumes/leo_1/SISMOLOGIA/ARMUELLES_OV/RESULTS',
                   title='OVSICORI picks', show=False)
    fig.savefig(path.join(out_path, 'OV.png'), format='png', dpi=300)

    fig = s_p_time('/Volumes/leo_1/SISMOLOGIA/ARMUELLES_OV/PS/DETECTION',
                   title='EQT picks', show=False)
    fig.savefig(path.join(out_path, 'EQT.png'), format='png', dpi=300)
