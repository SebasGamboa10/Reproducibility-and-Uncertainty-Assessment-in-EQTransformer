# Python Standard Library
import argparse
from datetime import datetime, timedelta
from os import system, path, makedirs

# Other dependencies
import pandas as pd

# Local files
from config.vars import *


def parse_args():
    description = (
        '\tTransfer files from OVSICORI servers\n'
    )

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=Formatter_Class)

    parser.add_argument(
        '--waves_in_dir',
        help='Path to continuous raw waveforms (with IP)',
        required=True
    )

    parser.add_argument(
        '--base_dir',
        help='Path to folder of the OKSP project',
        required=True
    )

    parser.add_argument(
        '--startdate',
        help='Y-j',
        required=True
    )

    parser.add_argument(
        '--enddate',
        help='Y-j, not inclusive',
        required=True
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    df = pd.read_csv(STA_FILEPATH.format(base_dir=args.base_dir))

    start = datetime.strptime(args.startdate, '%Y-%j')
    end   = datetime.strptime(args.enddate,   '%Y-%j')

    in_paths = []
    for day in range(int((end - start).days)):
        tt = (start + timedelta(day)).timetuple()
        year = tt.tm_year
        yday = tt.tm_yday

        year_path = path.join(args.base_dir, CONT_FOLDER, str(year))
        yday_path = path.join(year_path, f'{yday}')

        for folder in [year_path, yday_path]:
            if not path.exists(folder): makedirs(folder)

        for i, row in df.iterrows():
            station  = row.code
            channels = row.channels.split('_')

            for channel in channels:
                filepath = DB_MSEED_PATH_FMT.format(
                    waves_in_dir = args.waves_in_dir,
                    year         = year,
                    julday       = yday,
                    station      = station,
                    channel      = channel
                )

                system(f'scp {filepath} {yday_path}/.')
