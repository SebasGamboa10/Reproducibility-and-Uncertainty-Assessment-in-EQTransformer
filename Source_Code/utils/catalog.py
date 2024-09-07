# Python Standard Library
from os import listdir, path

# Other dependencies
from obspy import Catalog, UTCDateTime, read_events
from obspy.core.event.base import WaveformStreamID
from obspy.core.event.origin import Pick, Arrival, Origin
from obspy.core.event.event import Event
import pandas as pd

# Local files
from config.vars import *

def hypodd_in_to_df(filepath):
    converters = {
        'date'     : str,
        'time'     : str,
        'latitude' : float,
        'longitude': float,
        'depth'    : float,
        'magnitude': float,
    }

    df = pd.read_fwf(filepath, usecols=range(6), names=converters.keys(),
                     converters=converters)

    df['datetime'] = df['date'] + df['time']
    df['datetime'] = pd.to_datetime(df.datetime, format='%Y%m%d%H%M%S%f')
    df.drop(['date', 'time',], axis=1, inplace=True)
    return df


def growclust_to_df(filepath):
    fmt = {
        'year'      : {'converter': int,   'colspec': ( 1,   5)},
        'month'     : {'converter': int,   'colspec': ( 5,   8)},
        'day'       : {'converter': int,   'colspec': ( 8,   11)},
        'hour'      : {'converter': int,   'colspec': ( 11,  14)},
        'minutes'   : {'converter': int,   'colspec': ( 14,  17)},
        'seconds'   : {'converter': float, 'colspec': ( 17,  24)},
        'eID'       : {'converter': int,   'colspec': ( 24,  34)},
        'latitude'  : {'converter': float, 'colspec': ( 34,  44)},
        'longitude' : {'converter': float, 'colspec': ( 44,  55)},
        'depth'     : {'converter': float, 'colspec': ( 55,  63)},
        'magnitude' : {'converter': float, 'colspec': ( 63,  69)},
        'qID'       : {'converter': int,   'colspec': ( 69,  77)},
        'cID'       : {'converter': int,   'colspec': ( 77,  85)},
        'nbranch'   : {'converter': int,   'colspec': ( 85,  93)},
        'qnpair'    : {'converter': int,   'colspec': ( 93,  99)},
        'qndiffP'   : {'converter': int,   'colspec': ( 99, 105)},
        'qndiffS'   : {'converter': int,   'colspec': (105, 111)},
        'rmsP'      : {'converter': float, 'colspec': (111, 117)},
        'rmsS'      : {'converter': float, 'colspec': (117, 123)},
        'ez'        : {'converter': float, 'colspec': (123, 131)},
        'eh'        : {'converter': float, 'colspec': (131, 139)},
        'et'        : {'converter': float, 'colspec': (139, 147)},
        'latC'      : {'converter': float, 'colspec': (147, 159)},
        'lonC'      : {'converter': float, 'colspec': (159, 170)},
        'depC'      : {'converter': float, 'colspec': (170, 178)}
    }

    converters = {}
    _colspecs = []

    for key in fmt.keys():
        converters[key] = fmt[key]['converter']
        _colspecs.append(fmt[key]['colspec'])

    colspecs = []
    for colspec in _colspecs:
        colspecs.append((colspec[0] - 1, colspec[1] - 1))

    df = pd.read_fwf(filepath, names=converters.keys(), converters=converters,
                     colspecs=colspecs)

    date_cols = ['year', 'month', 'day', 'hour', 'minutes', 'seconds']
    df['datetime'] = pd.to_datetime(df[date_cols])
    df.drop(date_cols, axis=1, inplace=True)
    return df


def collect2df(filepath):
    fmt = {
        'year'     : {'converter': int,   'colspec'  : ( 1,  5)},
        'month'    : {'converter': int,   'colspec'  : ( 6,  8)},
        'day'      : {'converter': int,   'colspec'  : ( 8, 10)},
        'hour'     : {'converter': int,   'colspec'  : (11, 13)},
        'minutes'  : {'converter': int,   'colspec'  : (13, 15)},
        'seconds'  : {'converter': float, 'colspec'  : (16, 20)},
        'latitude' : {'converter': float, 'colspec'  : (23, 30)},
        'longitude': {'converter': float, 'colspec'  : (30, 38)},
        'depth'    : {'converter': float, 'colspec'  : (38, 43)},
        'n_sta'    : {'converter': int,   'colspec'  : (48, 51)},
        'rms'      : {'converter': float, 'colspec'  : (51, 55)},
        'magnitude': {'converter': float, 'colspec'  : (55, 59)}
    }

    converters = {}
    colspecs = []

    for key in fmt.keys():
        converters[key] = fmt[key]['converter']
        colspecs.append(fmt[key]['colspec'])


    df = pd.read_fwf(filepath, names=converters.keys(), converters=converters,
                     colspecs=colspecs)

    date_cols = ['year', 'month', 'day', 'hour', 'minutes', 'seconds']
    df['datetime'] = pd.to_datetime(df[date_cols])
    df.drop(date_cols, axis=1, inplace=True)
    return df


class NLLoc_Pha_Reader(object):
    def __init__(self, detections_file, stations_csv):
        self.detections_file = detections_file
        self.df = pd.read_csv(stations_csv)

    def get_channels(self, station_code):
        channels = self.df.loc[self.df.code == station_code]['channels'].values[0].split('_')
        return channels

    def get_channel_code(self, station_code, component):
        channels = self.get_channels(station_code)
        return [channel for channel in channels if channel[-1] == component][0]

    def parse_line(self, line):
        row          = line.split()

        station_code = row[0]
        network_code = row[1]
        phase        = row[4]
        ymd          = row[6]
        hm           = row[7]
        s            = float(row[8])
        year         = int(ymd[0:4])
        month        = int(ymd[4:6])
        day          = int(ymd[6:8])
        hour         = int(hm[0:2])
        minute       = int(hm[2:4])

        time = UTCDateTime(year, month, day, hour, minute, s)
        return station_code, network_code, time, phase

    def create_pick(self, station_code, network_code, time, phase, pick_id):

        if phase == 'P':
            channel_code = self.get_channel_code(station_code, 'Z')

        elif phase == 'S':
            if len(self.get_channels(station_code)) > 1:
                channel_code = self.get_channel_code(station_code, 'N')
            else:
                channel_code = self.get_channel_code(station_code, 'Z')

        waveform_id = WaveformStreamID(network_code=network_code,
                                       station_code=station_code,
                                       location_code='',
                                       channel_code=channel_code)

        pick = Pick(resource_id=str(pick_id), time=time,
                    waveform_id=waveform_id, phase_hint=phase,
                    evaluation_mode='automatic')

        arrival = Arrival(resource_id=str(pick_id), pick_id=str(pick_id),
                          phase=phase)

        return pick, arrival

    def get_catalog(self, latitude=8.337, longitude=-82.830, depth=36):

        with open(self.detections_file, 'r') as f:
            text = f.read()
        blocks = text.split('\n\n')

        catalog = Catalog()

        pick_id = 0

        for eventid, block in enumerate(blocks):
            lines = block.split('\n')

            picks, arrivals = [], []

            for line in lines:
                try:
                    station_code, network_code, time, phase = self.parse_line(line)
                except:
                    continue

                pick, arrival = self.create_pick(station_code, network_code, time,
                                            phase, pick_id)

                picks.append(pick)
                arrivals.append(arrival)
                pick_id += 1

            origin = Origin(
                arrivals=arrivals,
                latitude=latitude,
                longitude=longitude,
                depth=depth
            )

            event = Event(
                resource_id=str(eventid),
                picks=picks,
                origins=[origin]
            )

            catalog.events.append(event)
        return catalog


def nlloc_to_catalog(location_output_dir):
    print('\n\tReading NonLinLoc .hyp output files...')
    fnames = [
        f for f in listdir(location_output_dir)
        if (f.split('.')[-1] == 'hyp') and ('sum' not in f)
        and (f != 'last.hyp')
    ]

    catalog, eID = Catalog(), 0
    for fname in fnames:
        events = read_events(path.join(location_output_dir, fname))
        for event in events:
            event.resource_id.id = f'{eID:05d}'
            catalog.append(event)
            eID += 1
    return catalog


def zmap_to_df(filepath):
    catalog = read_events(filepath, format='ZMAP')

    columns = 'datetime|latitude|longitude|depth|magnitude'.split('|')
    datetime, latitude, longitude, depth, magnitude = [], [], [], [], []
    for event in catalog:
        datetime.append(event.origins[0].time.datetime)
        latitude.append(event.origins[0].latitude)
        longitude.append(event.origins[0].longitude)
        depth.append(event.origins[0].depth/1000)
        magnitude.append(event.magnitudes[0].mag)

    df = pd.DataFrame(list(zip(datetime, latitude, longitude, depth,
                               magnitude)), columns=columns)

    df.index = pd.to_datetime(df.datetime)
    return df


def parse_shadow_pick(line, to_obspy=True, pick_id=None):
    line_fmt = {
        'station' : {'i': ( 0,  5), 'type': str},
        'network' : {'i': ( 5,  7), 'type': str},
        'channel' : {'i': ( 9, 12), 'type': str},
        'p_phase' : {'i': (13, 15), 'type': str},
        'year'    : {'i': (17, 21), 'type': int},
        'month'   : {'i': (21, 23), 'type': int},
        'day'     : {'i': (23, 25), 'type': int},
        'hour'    : {'i': (25, 27), 'type': int},
        'minute'  : {'i': (27, 29), 'type': int},
        'P_second': {'i': (29, 34), 'type': str},
        'S_second': {'i': (41, 46), 'type': str},
        's_phase' : {'i': (46, 48), 'type': str},
        'Sweight' : {'i': (49, 50), 'type': int}
    }
    data = {}
    for key, value in line_fmt.items():
        data[key] = value['type'](line[value['i'][0]:value['i'][1]])

    data['station'] = data['station'].strip()

    if data['p_phase'] == 'IP':
        data['second'] = float(data['P_second'])
        data['phase'] = 'P'
    elif data['s_phase'] == 'ES':
        data['second'] = float(data['S_second'])
        data['phase'] = 'S'

    if to_obspy:
        second, microsecond = divmod(data['second'], 1)
        second = int(second)
        microsecond = int(microsecond * 10**6)

        time = UTCDateTime(year=data['year'], month=data['month'], day=data['day'],
                           hour=data['hour'], minute=data['minute'], second=second,
                           microsecond=microsecond)

        waveform_id = WaveformStreamID(network_code=data['network'],
                                       station_code=data['station'],
                                       location_code='',
                                       channel_code=data['channel'])

        pick = Pick(resource_id=str(pick_id), time=time, waveform_id=waveform_id,
                    phase_hint=data['phase'], evaluation_mode='automatic')

        arrival = Arrival(resource_id=str(pick_id), pick_id=str(pick_id),
                          phase=data['phase'])

        return pick, arrival
    else:
        return data


def shadow_to_nlloc_pha(cat_filepath_in, cat_filepath_out):
    f_in  = open(cat_filepath_in)
    f_out = open(cat_filepath_out, 'w')

    header_idx = 0
    for i, line in enumerate(f_in):
        if i == header_idx:
            print(line)

        elif line[0] != ' ':
            data = parse_shadow_pick(line, to_obspy=False)

            f_out.write(NLL_PHA_FMT.format(
                station       = data['station'],
                network       = data['network'],
                component     = '?',
                P_phase_onset = '?',
                phase         = data['phase'],
                first_motion  = '?',
                year          = data['year'],
                month         = data['month'],
                day           = data['day'],
                hour          = data['hour'],
                minute        = data['minute'],
                second        = data['second'],
                err           = 'GAU',
                pick_error    = 0.1,
                err_mag       = -1,
                coda_dur      = -1,
                amplitude     = -1
            ))
            f_out.write('\n')

        elif line[0] == ' ':
            eventid = line.split()[0]
            header_idx = i + 1
            f_out.write('\n')
    return


def hypoellipse_to_df(filepath):
    converters = {
        'date': str,
        'hourmin': str,
        'seconds': str,
        'latitude_degrees': int,
        'hemisphere_equator': str,
        'latitude_minutes': float,
        'longitude_degrees': int,
        'hemisphere_greenwich': str,
        'longitude_minutes': float,
        'depth': float,
        'magnitude': float,
        'n_stations': int,
        'gap': int,
        'D1': float,
        'rms': float,
        'AZ1': int,
        'DIP1': int,
        'SE1': float,
        'AZ2': int,
        'DIP2': int,
        'SE2': float,
        'SE3': float,
    }

    df = pd.read_fwf(filepath, names=converters.keys(), converters=converters,
                    skiprows=[0, 1])

    df['datetime'] = df.date + df.hourmin + df.seconds
    df['datetime'] = pd.to_datetime(df.datetime, format='%Y%m%d%H%M%S.%f')

    df['latitude'] = df.latitude_degrees + df.latitude_minutes/60
    df.loc[df.hemisphere_equator == 'S', 'latitude'] *= -1

    df['longitude'] = df.longitude_degrees + df.longitude_minutes/60
    df.loc[df.hemisphere_greenwich == 'W', 'longitude'] *= -1

    useless_columns = ['date', 'hourmin', 'seconds', 'latitude_degrees',
                       'latitude_minutes', 'longitude_degrees',
                       'longitude_minutes', 'hemisphere_equator',
                       'hemisphere_greenwich']
    df.drop(useless_columns, axis=1, inplace=True)
    return df


def _df_to_gmt(df, filepath_out):
    df['depth'] = -1 * df.depth
    df = df[['longitude', 'latitude', 'depth']]
    df.to_csv(filepath_out, sep=' ', header=False, index=False)
    return


def cat_to_gmt(filepath_in, filepath_out, fmt):
    functions = {
        'growclust'  : growclust_to_df,
        'hypodd_in'  : hypodd_in_to_df,
        'hypoellipse': hypoellipse_to_df,
        'zmap'       : zmap_to_df
    }

    df = functions[fmt](filepath_in)

    _df_to_gmt(df, filepath_out)

    return


if __name__ == '__main__':
    print(growclust_to_df('/Volumes/leo_1/SISMOLOGIA/ARMUELLES_OV/PS/RELOCATION/OUT/out.growclust_cat')); exit()

