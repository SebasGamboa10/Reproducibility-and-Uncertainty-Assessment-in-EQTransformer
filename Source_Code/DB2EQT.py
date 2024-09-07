# Python Standard Library
import argparse
from datetime import datetime, timedelta
import json
from os import path, makedirs, symlink, listdir
import warnings

# Other dependencies
from obspy import read
import pandas as pd

# Local files
from config.vars import *


DATE_FMT = '%Y-%j'

def get_args():
    parser = argparse.ArgumentParser()

    description = (
        '\tCreate symlinks for MSEED files for the requested stations and time span\n'
        '\tOutput under --output_dir:\n'
        '\t\toutput_dir\n'
        '\t\t├── stations.json\n'
        '\t\t└── DETECTION\n'
    )
    parser = argparse.ArgumentParser(
        description     = description,
        formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument(
        '--waves_in_dir',
        help='Path to continuous raw waveforms, (only if in OVSICORI server)',
    )

    required = parser.add_argument_group('required arguments')

    required.add_argument(
        '--base_dir',
        help='Path to folder of the OKSP project',
        required=True
    )

    required.add_argument(
        '--startdate',
        help='Y-j',
        required=True
    )

    required.add_argument(
        '--enddate',
        help='Y-j, not inclusive',
        required=True
    )

    args = parser.parse_args()

    return args

def set_tree(stations, waves_out_dir):
    if not path.exists(waves_out_dir):
        makedirs(waves_out_dir)

    for station in stations:
        if not path.exists(path.join(waves_out_dir, station)):
            makedirs(path.join(waves_out_dir, station))
    return


def create_symlinks(waves_in_dir, startdate, enddate, df, waves_out_dir):

    stations = df.code.tolist()

    set_tree(stations, waves_out_dir)

    startdate = datetime.strptime(startdate, DATE_FMT)
    enddate   = datetime.strptime(enddate,   DATE_FMT)

    for station in stations:
        channels = df[df.code == station].channels.values[0].split('_')
        for channel in channels:
            for day in range(int((enddate - startdate).days)):
                tt = (startdate + timedelta(day)).timetuple()

                in_filepath = DB_MSEED_PATH_FMT.format(
                    waves_in_dir = waves_in_dir,
                    year         = tt.tm_year,
                    julday       = tt.tm_yday,
                    station      = station,
                    channel      = channel
                )

                if path.isfile(in_filepath):
                    st = read(in_filepath, headonly=True)

                    starttime = min(tr.stats.starttime for tr in st)
                    endtime   = max(tr.stats.endtime + tr.stats.delta for tr in st)

                    out_filename = EQT_FNAME_FMT.format(
                        network  = st[0].stats.network,
                        station  = st[0].stats.station,
                        location = st[0].stats.location,
                        channel  = st[0].stats.channel,

                        ys = starttime.year,
                        ms = starttime.month,
                        ds = starttime.day,
                        Hs = starttime.hour,
                        Ms = starttime.minute,
                        Ss = starttime.second,

                        ye = endtime.year,
                        me = endtime.month,
                        de = endtime.day,
                        He = endtime.hour,
                        Me = endtime.minute,
                        Se = endtime.second
                    )

                    out_filepath = path.join(waves_out_dir, station, out_filename)
                    if not path.isfile(out_filepath):
                        print(out_filename)
                        symlink(in_filepath, out_filepath)
    return


def create_json(base_dir, df, waves_out_dir):

    data = {}
    for station in listdir(waves_out_dir):

        network, channels = set(), set()
        fnames = [f for f in listdir(path.join(waves_out_dir, station))]

        if len(fnames) == 0:
            continue

        for fname in fnames:
            network.add(fname.split('.')[0])
            channels.add(fname.split('.')[3].split('_')[0])

        latitude  = df[df.code == station].latitude.values[0]
        longitude = df[df.code == station].longitude.values[0]
        elevation = df[df.code == station].elevation.values[0]

        if len(network) > 1:
            warnings.warn('Several networks for station {}: {}'.format(station,
                                                                      network))
        network = list(network)[0]

        data[station] = {
            'network' : network,
            'channels': list(channels),
            'coords'  : [latitude, longitude, elevation]
        }

    with open(path.join(base_dir, EQT_FOLDER, EQT_JSON_FNAME), 'w') as f:
        json.dump(data, f, indent=4)

    return


if __name__ == '__main__':
    args = get_args()

    df = pd.read_csv(STA_FILEPATH.format(base_dir=args.base_dir))

    if not args.waves_in_dir:
        args.waves_in_dir = path.join(args.base_dir, CONT_FOLDER)

    waves_out_dir = path.join(args.base_dir, EQT_FOLDER, EQT_WAVES_DIR)

    create_symlinks(args.waves_in_dir, args.startdate, args.enddate,
                    df, waves_out_dir)

    create_json(args.base_dir, df, waves_out_dir)
