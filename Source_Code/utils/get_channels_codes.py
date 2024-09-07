waves_dir = '/home/leo/extract_waveforms/sismo/'
years = range(2017, 2018)
days  = range(1, 367)


import json
from os import listdir, path


data = {}
for year in years:
    for day in days:
        print(year, day)
        folder = f'{waves_dir}{year}/{day:03d}/'

        if path.exists(folder):
            fnames = [f for f in listdir(folder)]
            for fname in fnames:
                if fname[:2] == 'i4':
                    station = fname.split('.')[1]
                    channel = fname.split('.')[2]

                    if channel[1] == 'H':
                        if station in data:
                            data[station].add(channel)
                        else:
                            data[station] = set([channel])

data_out = {}
for station in data.keys():
    data_out[station] = {}
    for channel in data[station]:
        if channel[2] in data_out[station]:
            data_out[station][channel] = channel
        else:
            data_out[station][channel[2]] = channel


with open('una_stations_channels.json', 'w') as f:
    json.dump(data_out, f, indent=4)
