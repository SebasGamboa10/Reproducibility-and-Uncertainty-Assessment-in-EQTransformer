# Hacer objeto
# Other dependencies
import pandas as pd


def sta2df(filepath):
    """
    Details of STATION0.HYP file format in page 100 of SeisAn PDF manual,
    section 6.1
    columns = {
        'elevation_sign': (0, 1),
        'station_4_char': (2, 6),
        'station_5_char': (1, 6),
        'latitude_degrees': (6, 8),
        'latitude_minutes': (8, 13),
        'hemisphere_equator': (13, 14),
        'longitude_degrees': (14, 17),
        'longitude_minutes': (17, 22),
        'hemisphere_greenwich': (22, 23),
        'elevation': (23, 27),
        'P_delay': (27, 33)
    }


    Parameters
    ----------
    filepath : str
        Path to STATION0.HYP file

    Returns
    -------

    """
    f = open(filepath, 'r')

    stations = []
    for line in f:
        try:
            station = {}

            if line[1] == ' ':
                station['code'] = line[2:6]
                if station['code'][-1] == ' ':
                    station['code'] = station['code'][:-1]
            else:
                station['code'] = line[1:6]

            latitude_degrees = int(line[6:8])
            latitude_minutes = line[8:13]
            if latitude_minutes[2] == '.':
                latitude_minutes = float(latitude_minutes)
            else:
                latitude_minutes = float(
                    latitude_minutes[:2]+'.'+latitude_minutes[2:]
                )
            station['latitude'] = latitude_degrees + latitude_minutes/60
            hemisphere_equator = line[13]
            if hemisphere_equator == 'S':
                station['latitude'] *= -1

            longitude_degrees = int(line[14:17])
            longitude_minutes = line[17:22]
            if longitude_minutes[2] == '.':
                longitude_minutes = float(longitude_minutes)
            else:
                longitude_minutes = float(
                    longitude_minutes[:2]+'.'+longitude_minutes[2:]
                )
            station['longitude'] = longitude_degrees + longitude_minutes/60
            hemisphere_greenwich = line[22]
            if hemisphere_greenwich == 'W':
                station['longitude'] *= -1

            elevation_sign = line[0]
            station['elevation'] = int(line[23:27])
            if elevation_sign == '-':
                station['elevation'] *= -1
        except:
            continue
        stations.append(station)

    df = pd.DataFrame.from_dict(stations)
    return df


def write4GrowClust(df, outpath):
    df = df[['code', 'latitude', 'longitude', 'elevation']]
    df.to_csv(outpath, sep=' ', index=False, header=False)


def write4PhaseLink(df, output_dir, station_network):
    df['network'] = ''
    for i, row in df.iterrows():
        if row.code in list(station_network.keys()):
            df.at[i, 'network'] = station_network[row.code]
        # else:
    df = df[['network', 'code', 'latitude', 'longitude']]
    df.to_csv(output_dir+'stlist.PL.txt', sep=' ', index=False, header=False)


def write4GMT(df, output_dir):
    df = df[['longitude', 'latitude', 'code']]
    df.to_csv(output_dir+'stlist.GMT.txt', sep=' ', index=False, header=False)
