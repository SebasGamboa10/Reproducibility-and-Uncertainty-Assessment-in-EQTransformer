# Python Standard Library
from datetime import datetime, timedelta
from glob import glob

# Other dependencies
from obspy import read, Stream

from config.vars import *
from utils.stations import get_channels


PATH_FMT = (
    '{waves_in_dir}{year}/{julday:03d}/'
    'i4.{station}.{channel}.{year}{julday:03d}_0+'
)


def load(waves_in_dir, starttime, endtime, stations, channels=['*']):
    if waves_in_dir[-1] != '/':
        waves_in_dir += '/'

    start_dt = starttime.datetime
    end_dt   = endtime.datetime

    st = Stream()

    for day in range(int((end_dt - start_dt).days + 1)):
        tt = (start_dt + timedelta(day)).timetuple()
        year   = tt.tm_year
        julday = tt.tm_yday

        for station in stations:
            for channel in channels:
                filepath = PATH_FMT.format(
                            waves_in_dir = waves_in_dir,
                            station      = station,
                            channel      = channel,
                            year         = year,
                            julday       = julday
                )
                if len(glob(filepath)) > 0:
                    st += read(filepath, starttime=starttime, endtime=endtime)
                else:
                    print('{}.{} not found'.format(station, channel))

    return st


def catalog_to_waves(catalog, df, waves_in_dir, output_dir):
    print('\n\tExtracting waveforms')
    start = min(event.origins[0].time for event in catalog).datetime
    #print(start)
    end   = max(event.origins[0].time for event in catalog).datetime
    #print(end)

    days = list(range(int((end - start).days + 1)))
    for day in days:
        print(f'\n\tDay {day+1} of {len(days)}')

        date_fmt = '{year}-{month:02d}-{day:02d}'

        # Start date to filter catalog
        tt_start = (start + timedelta(day)).timetuple()
        #print(tt_start)
        date_start_str = date_fmt.format(year=tt_start.tm_year,
                                         month=tt_start.tm_mon,
                                         day=tt_start.tm_mday)


        # End date to filter catalog
        tt_end = (end + timedelta(day+1)).timetuple()
        #print(tt_end)
        date_end_str = date_fmt.format(year=tt_end.tm_year,
                                       month=tt_end.tm_mon,
                                       day=tt_end.tm_mday)

        subcatalog = catalog.filter(f'time >= {date_start_str}',
                                    f'time <  {date_end_str}')

        print('\n\tLoading waveforms...')
        stations = set()
        for event in subcatalog:
            for pick in event.picks:
                stations.add(pick.waveform_id.station_code)

        year   = tt_start.tm_year
        julday = tt_end.tm_yday-1

        st = Stream()
        for station in stations:
            channels = get_channels(df, station)
            #print(station)
            #print(channels)
            for channel in channels:
                filepath = DB_MSEED_PATH_FMT.format(
                            waves_in_dir = waves_in_dir,
                            station      = station,
                            channel      = channel,
                            year         = year,
                            julday       = julday
                )
                #print(filepath)
                
                if len(glob(filepath)) > 0:
                    st1 = read(filepath)
                    #ESTE CAMBIO SE HACE PARA SOLUCIONAR PROBLEMA CON INFORMACION DEL ENCABEZADO DE LOS NODOS SISMOLOGICOS.
                    if st1[0].stats.network == "SS":
                        st1[0].stats.network = "OV"
                    if st1[0].stats.station == "17019":
                        st1[0].stats.station = "AVIA"
                    if st1[0].stats.station == "16458":
                        st1[0].stats.station = "CARI"
                    if st1[0].stats.station == "15147":
                        st1[0].stats.station = "FIZU"
                    if st1[0].stats.station == "14442":
                        st1[0].stats.station = "JPAC"
                    if st1[0].stats.station == "15655":
                        st1[0].stats.station = "PATR"
                    if st1[0].stats.station == "16529":
                        st1[0].stats.station = "TUNEL"
                    if st1[0].stats.channel == "DP1":
                        st1[0].stats.channel = "HHE"
                    if st1[0].stats.channel == "DP2":
                        st1[0].stats.channel = "HHN"
                    if st1[0].stats.channel == "DPZ":
                        st1[0].stats.channel = "HHZ"
                    st += st1
                else:
                    print('\t{}.{} not found'.format(station, channel))

        #print(st)


        print('\n\tWriting waveforms...')
        for i, event in enumerate(subcatalog):
            st_ev = Stream()
            for station in stations:
                #print(station)
                picks = [pick for pick in event.picks
                         if pick.waveform_id.station_code == station]

                if len(picks) > 0:
                    starttime = min(pick.time for pick in picks) - WAV_LEFT_MARGIN
                    endtime   = max(pick.time for pick in picks) + WAV_RIGHT_MARGIN
                    print(picks)
                    print(st)
                    st_ev += st.select(station=station).slice(starttime, endtime)
                    #print(st_ev)

            filepath = path.join(output_dir, f'{event.resource_id.id}.mseed')
            if st_ev:
                #print(filepath)
                st_ev.write(filepath, format='MSEED')
            else:
                print("------------")
                print(filepath)
                print("------------")
    return
