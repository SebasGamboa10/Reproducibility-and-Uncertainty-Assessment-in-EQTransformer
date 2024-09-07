"""

TODO:
    Export stations csv file to different formats:
        * WAST
        * STATION0.HYP

"""
import argparse
import math
from os import system, path
from pathlib import Path
import sys

from obspy import read_inventory
import pandas as pd

sys.path.insert(0, Path(path.realpath(__file__)).parent.parent)
from config.vars import *


INVENTORY_CSV_COLUMNS = 'code,longitude,latitude,elevation,channels'
PLOTS_DIR = 'plots/'
NETWORK = 'OV'


# STATION0.HYP stations format in Fortran: seisan.pdf p.100
# 2x,a4,i2,f5.3,a1,i3,f5.3,a1,i4,f6.2,5f5.2,9f6.2
STATION0_FMT = (
    '{station}'
    '{latitude_degrees:2d}{latitude_minutes:05.2f}{hemisphere_equator}'
    '{longitude_degrees:3d}{longitude_minutes:05.2f}{hemisphere_greenwich}'
    '{elevation:4d}'
)


def export_csv(inventory, output_dir):
    with open(output_dir+'stations.csv', 'w') as f:
        f.write(INVENTORY_CSV_COLUMNS)
        f.write('\n')

        for network in inventory:
            for station in network:
                channels = []
                for channel in station:
                    if channel.code[:2] == 'HH':
                        channels.append(channel.code)

                line = (
                    f'{station.code},{station._longitude},{station._latitude},'
                    f'{station._elevation},{"_".join(channels)}'
                )
                f.write(line)
                f.write('\n')
    return


def plot_area(stations_csv, margin, output_dir):

    sta = pd.read_csv(stations_csv)

    sta[['longitude', 'latitude', 'code']].to_csv(
        output_dir+'stations.gmt', sep=' ', index=False, header=False
    )

    xmin = sta.longitude.min() - margin
    ymin = sta.latitude.min() - margin
    xmax = sta.longitude.max() + margin
    ymax = sta.latitude.max() + margin

    print(ymin, ymax, xmin, xmax)

    lat_mean = (ymin + ymax) / 2

    map_path = output_dir + 'map.ps'

    aspect_ratio = (xmax - xmin) / (ymax - ymin)
    system(f'gmtset PS_MEDIA            = 12cx{12/aspect_ratio}c')
    system(f'gmtset MAP_FRAME_TYPE      = plain')
    system(f'gmtset PS_PAGE_ORIENTATION = portrait')
    system(f'gmtset FONT_ANNOT_PRIMARY  = 7p,Helvetica,black')
    system((
        f'pscoast -JM{lat_mean}/10 -R{xmin}/{xmax}/{ymin}/{ymax} -Xc -Yc '
        f'-Ba1f1/a1f1wSnE -G245/245/245 -S220/240/255 -K -Di -W0.4 > {map_path}'
    ))

    # system((
    #     f'psxy {output_dir}stations.gmt -R -J -St.15 -W0.5 '
    #     f'-Gblue -O >> {map_path}'))
    system((
        f'pstext {output_dir}stations.gmt -R -J '
        f'-O >> {map_path}'))

    system(f'psconvert {map_path} -Tg')
    system(f'open {map_path.replace("ps", "png")}')
    system(f'rm {map_path}')


def sta2GrowClust(df, output_dir):
    df = df[['code', 'latitude', 'longitude', 'elevation']]
    df.to_csv(output_dir+'stlist_GrowClust_fmt2.txt', sep=' ', index=False,
               header=False)
    return


def sta2PhaseLink(df, output_dir):
    df['network'] = NETWORK
    df = df[['network', 'code', 'latitude', 'longitude']]
    df.to_csv(output_dir+'stlist_PhaseLink.txt', sep=' ', index=False,
              header=False)
    return


def sta2NLLoc(df, output_dir):
    with open(path.join(output_dir, NLL_STA_FILENAME), 'w') as f:
        f.write('# ')

        f.write(
            NLL_STA_FMT.format(
                station='station',
                latitude='latitude',
                longitude='longitude',
                depth='depth',
                elevation='elevation')
        )
        f.write('\n')

        for i, row in df.iterrows():
            f.write(
                NLL_STA_FMT.format(
                    station='  ' +row.code,
                    latitude=row.latitude,
                    longitude=row.longitude,
                    depth=0.0,
                    elevation=row.elevation/1000
                )
            )
            f.write('\n')
    return


def sta2NLLocEQ(df, output_dir):
    with open(path.join(output_dir, NLL_EQSTA_FILENAME), 'w') as f:
        f.write('# ')

        f.write(
            NLL_EQSTA_FMT.format(
                station='station',
                phase='phase',
                errorType='errorType',
                error='error',
                errorReportType='errorReportType',
                errorReport='errorReport',
                probActive='probActive'
            )
        )

        f.write('\n')

        for i, row in df.iterrows():
            f.write(
                NLL_EQSTA_FMT.format(
                    station=row.code,
                    phase='P',
                    errorType='GAU',
                    error='0.1',
                    errorReportType='GAU',
                    errorReport='0.1',
                    probActive=''
                )
            )

            f.write('\n')
    return


def ddeg2degdmin(ddeg):
    d, deg = math.modf(ddeg)
    dmin = 60 * d
    return int(deg), dmin


def sta2STATION0(df):
    for i, row in df.iterrows():
        if len(row.code) == 3:
            station = '  ' + row.code + ' '
        elif len(row.code) == 4:
            station = '  ' + row.code
        elif len(row.code) == 5:
            station = ' ' + row.code

        if row.latitude < 0:
            hemisphere_equator = 'S'
        else:
            hemisphere_equator = 'N'

        latitude_degrees, latitude_minutes = ddeg2degdmin(abs(row.latitude))

        if row.longitude < 0:
            hemisphere_greenwich = 'W'
        else:
            hemisphere_greenwich = 'E'

        longitude_degrees, longitude_minutes = ddeg2degdmin(abs(row.longitude))

        line = STATION0_FMT.format(
            station=station,
            latitude_degrees=latitude_degrees,
            latitude_minutes=latitude_minutes,
            hemisphere_equator=hemisphere_equator,
            longitude_degrees=longitude_degrees,
            longitude_minutes=longitude_minutes,
            hemisphere_greenwich=hemisphere_greenwich,
            elevation=int(row.elevation)
        )

        if row.elevation < 0:
            line[0] = '-'

        print(line)

    return


def get_channels(df, station_code):
    channels = df.loc[df.code == station_code]['channels'].values[0].split('_')
    return channels


def sta2GMT(df, filepath_out):
    df = df[['longitude', 'latitude', 'code']]
    df.to_csv(filepath_out, sep=' ', index=False, header=False)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', help='csv2nlloc/csv2sta0/csv2eqt')
    parser.add_argument('--stations_csv', help='Path to inventory')
    parser.add_argument('--output_dir', help='Output directory path')

    args = parser.parse_args()

    df = pd.read_csv(args.stations_csv)

    if args.mode == 'csv2nlloc':
        sta2NLLoc(df, args.output_dir)
        sta2NLLocEQ(df, args.output_dir)

    if args.mode == 'csv2sta0':
        sta2STATION0(df)

