# Python Standard Library
from math import log10, sqrt

# Other dependencies
import numpy as np
from obspy.core.event.base import QuantityError
from obspy.core.event.magnitude import Amplitude, Magnitude, StationMagnitude
from obspy.core.event.base import WaveformStreamID
from obspy.geodetics import gps2dist_azimuth
from scipy.stats import t

# Local files


def local_magnitude(disp, dist):
    return log10(disp) + 2.56*log10(dist) - 1.67


def get_mag_errors(mag, confidence_level=0.95):
    t_bounds = t.interval(confidence_level, len(mag) - 1)

    interval = [
        mag.mean() + critval * mag.std() / sqrt(len(mag))
        for critval in t_bounds
    ]

    mag_errors = QuantityError(
        uncertainty       = np.abs(mag - mag.mean()).sum() / len(mag),
        lower_uncertainty = interval[0],
        upper_uncertainty = interval[1],
        confidence_level  = confidence_level
    )
    return mag_errors


def compute_magnitude(event, st, inventory, pre_filt=(0.5, 1, 40, 50),
                     magnitude_type='ML'):

    origin_id       = event.origins[0].resource_id
    station_count   = 0
    evaluation_mode = 'automatic'
    mag             = []

    stations = set(tr.stats.station for tr in st)
    for station in stations:
        station_latitude  = inventory.select(station=station)[0][0].latitude
        station_longitude = inventory.select(station=station)[0][0].longitude

        dist = gps2dist_azimuth(station_latitude, station_longitude,
                                event.origins[0].latitude,
                                event.origins[0].longitude)[0] / 1000.

        for tr in st.select(station=station):
            #print(station_latitude)
            #print(station_longitude)
            print(tr)
            #response = _get_response(inventory)
            #print(response)
            tr.remove_response(inventory=inventory, pre_filt=pre_filt,
                               output='DISP')
            print("resp removida")
            print(tr)
            waveform_id = WaveformStreamID(seed_string=tr.get_id())

            disp = abs(tr.max()*1e6)

            #SE INCLUYE ESTA LINEA POR ERROR MATEMATICO LOG10(0)
            if disp == 0:
                continue

            sta_mag = local_magnitude(disp, dist)

            mag.append(sta_mag)

            event.amplitudes.append(Amplitude(
                generic_amplitude = disp/1e6,
                type              = 'AML',
                category          = 'other',
                unit              = 'm',
                waveform_id       = waveform_id,
                magnitude_hint    = magnitude_type,
                evaluation_mode   = evaluation_mode
            ))

            event.station_magnitudes.append(StationMagnitude(
                origin_id              = origin_id,
                station_magnitude_type = magnitude_type,
                mag                    = sta_mag,
                waveform_id            = waveform_id
            ))

        station_count += 1

    mag = np.array(mag)

    event.magnitudes.append(Magnitude(
        mag             = round(mag.mean(), 3),
        mag_errors      = get_mag_errors(mag),
        magnitude_type  = magnitude_type,
        origin_id       = origin_id,
        station_count   = station_count,
        evaluation_mode = evaluation_mode
    ))

    print(f'\n\tOrigin time: {event.origins[0].time}',
          f'Ml {round(event.magnitudes[0].mag, 2)}')
    return event
