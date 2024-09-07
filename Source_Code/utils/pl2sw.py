station = 'BRU2'
station_label = station + ' HHZ PA'

in_picks_file = '/Users/leonardovanderlaat/Desktop/PN_TEST/continuous_picks/OV_MODEL/picks4PhaseLink.csv'

import pandas as pd

df = pd.read_csv(in_picks_file, sep=' ', names=['network', 'station', 'phase',
                                             'datetime', 'prob'])

df.prob = df.prob.round(1).apply(str)

df = df[df.station == station]

df['label'] = df.phase + ' ' + df.prob


df.datetime = pd.to_datetime(df.datetime)

df['station_label'] = station_label

df = df[['datetime', 'station_label', 'label']]

out_picks_file = in_picks_file[:-4] + '_' + station + '_swarm.csv'
df.to_csv(out_picks_file, header=False, index=False)
