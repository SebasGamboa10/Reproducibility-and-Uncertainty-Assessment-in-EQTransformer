# Python standard Library
from datetime import datetime, timedelta
from os import path
import sys
from pathlib import Path

# Other dependencies
import matplotlib.dates as md
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib_venn import venn2
import numpy as np
import pandas as pd
from scipy.stats import linregress

# # Local files
from utils.catalog import OV_sum2df, collect2df, zmap_to_df



def pd_datetime2str(datetime):
    return str(datetime).replace(' ', 'T')+'Z'


def compare(df1, df2, outpath, dt):
    # 0: 1 not in 2
    # 1: 1 in 2
    # 2: 2 not in 1

    df2['t1'] = df2.datetime - pd.Timedelta(dt, unit='s')
    df2['t2'] = df2.datetime + pd.Timedelta(dt, unit='s')

    out = open(outpath, 'w')
    out.write('time,latitude,longitude,depth,magnitude_ov,magnitude_ok,cat\n')

    for i, event in df1.iterrows():
        line = (f'{pd_datetime2str(i)},{event.latitude},{event.longitude},'
                f'{event.depth},{event.magnitude}')
        out.write(line); print(line)

        coincidence = df2[(i >= df2.t1) & (i <= df2.t2)]

        if len(coincidence) == 0:
            out.write(',nan,0\n')
        else:
            out.write(f',{coincidence.iloc[0].magnitude},1\n')

    for i, event in df2.iterrows():

        coincidence = df1[(df1.index >= event.t1) & (df1.index <= event.t2)]
        if len(coincidence) == 0:
            line = (f'{pd_datetime2str(i)},{event.latitude},{event.longitude},'
                    f'{event.depth},nan,{event.magnitude},2\n')
            out.write(line); print(line)

    return


def plot_comparison(filepath, sets, set_labels, starttime, endtime, show=True):
    s = 10
    # colors = ['red', 'purple', 'blue']
    colors = ['cyan', 'yellow', 'magenta']

    df = pd.read_csv(filepath)

    df.index = pd.to_datetime(df.time)


    fig = plt.figure(figsize=(6, 3))
    fig.subplots_adjust(left=.1, bottom=.15, right=.98, top=.98, wspace=.0,
                        hspace=.2)
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])

    ax1 = fig.add_subplot(gs[:, 0])
    # ax1.set_xlim(starttime, endtime)
    max_mag = max(df.magnitude_ov.max(), df.magnitude_ok.max())
    for time in [starttime, endtime]:
        ax1.vlines(x=time, ymin=-.5, ymax=max_mag, color='k',
                   linestyle='--', linewidth=0.5)

    ax1.set_xlabel('2019')
    ax1.set_ylabel('Magnitude')
    ax1.set_facecolor((.7, .7, .7))

    subsets = np.array([sets[0], sets[1], 0])
    magnitudes = ['magnitude_ov', 'magnitude_ov', 'magnitude_ok']
    for i, c, magnitude in zip([0, 1, 2], colors, magnitudes):
        df_sel = df[df.cat == i]
        if i == 1:
            n_shared = len(df_sel)
            subsets -= n_shared
        # if i == 2:
        #     df_sel.magnitude = -0.5
        ax1.scatter(df_sel.index, df_sel[magnitude], c=c, s=s, alpha=.7)
        ax1.vlines(df_sel.index, 0, df_sel[magnitude], color=c, linewidth=.3,
                   alpha=.7)
    ax1.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
    subsets = np.abs(subsets)

    ax2 = fig.add_subplot(gs[:, 1])

    v = venn2(
        subsets=subsets, set_labels=set_labels,
        set_colors=[colors[0], colors[2]], alpha=1, ax=ax2
    )

    if show:
        plt.show()
    return fig


def magnitude_comparison(filepath):
    df = pd.read_csv(filepath)
    df = df[df.cat == 1]

    slope, intercept, r_value, p_value, std_err = linregress(
        df.magnitude_ov, df.magnitude_ok)


    fig = plt.figure(figsize=(4, 4))
    fig.subplots_adjust(left=.13, bottom=.12, right=.95, top=.91, wspace=.2,
                        hspace=.2)

    ax = fig.add_subplot(111)
    ax.set_title(r'$R^2$ = {}, N = {}'.format(str(round(r_value**2, 2)), len(df)))
    ax.set_xlabel('Magnitude OVSICORI')
    ax.set_ylabel('Magnitude OKSP')
    ax.axis('equal')
    ax.scatter(df.magnitude_ov, df.magnitude_ok, c= 'r', s=10)

    xlim = ax.get_xlim()
    ax.plot([0, xlim[1]], [intercept, intercept+slope*xlim[1]], c='k', zorder=1,
           linewidth=1)

    plt.show()
    return fig



if __name__ == '__main__':

    file_OV_big = '/Volumes/leo_1/SISMOLOGIA/ARMUELLES_OV/PS/ov_sum.cat'
    file_eqt    = '/Volumes/leo_1/SISMOLOGIA/ARMUELLES_OV/EQT_assoc/catalog_summary.zmap'

    latmin, latmax, lonmin, lonmax = 7.021, 11.114, -85.295, -81.453

    starttime = datetime(2019, 6, 26)
    endtime   = datetime(2019, 7,  4)

    dt = 10

    ###########################################################################

    df_ov = OV_sum2df(file_OV_big)

    df_ov = df_ov[
        (df_ov.latitude >= latmin) & (df_ov.latitude <= latmax) &
        (df_ov.longitude >= lonmin) & (df_ov.longitude <= latmax)
    ]

    df_ov.index = df_ov.datetime

    df_ov = df_ov[df_ov.index >= starttime]
    df_ov = df_ov[df_ov.index <= endtime]

    df_eqt = zmap_to_df(file_eqt)
    # print(df_eqt.latitude.min(), df_eqt.latitude.max(),
    #       df_eqt.longitude.min(), df_eqt.longitude.max()); exit()

    # db2TOMODD ~/locate/una pn_db 2019-177 2019-185 7.021 11.114 -85.295 -81.453 -9 3



    df_eqt.index = df_eqt.datetime
    df_eqt = df_eqt[df_eqt.index >= starttime]
    df_eqt = df_eqt[df_eqt.index <= endtime]

    df_eqt = df_eqt[
        (df_eqt.latitude >= latmin) & (df_eqt.latitude <= latmax) &
        (df_eqt.longitude >= lonmin) & (df_eqt.longitude <= latmax)
    ]

    ############################################################################

    outpath = 'tmp_compare'

    compare(df_ov, df_eqt, outpath, dt)
    fig = magnitude_comparison(outpath)
    fig = plot_comparison(outpath, [len(df_ov), len(df_eqt)], ['OV', 'EQT'],
                          starttime, endtime, show=True)


