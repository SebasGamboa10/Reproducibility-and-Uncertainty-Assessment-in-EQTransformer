from argparse import ArgumentDefaultsHelpFormatter, RawTextHelpFormatter
from os import path
from pathlib import Path


class Formatter_Class(ArgumentDefaultsHelpFormatter, RawTextHelpFormatter): pass


################################################################################
#                             OVSICORI database
################################################################################

DB_MSEED_PATH_FMT = ('{waves_in_dir}/{year}/{julday}/'
                     'i4.{station}.{channel}.{year}{julday}_0+'
)

################################################################################
#                                  Stations
################################################################################

STA_FILEPATH  = '{base_dir}/stations.csv'

STA_INVENTORY = path.join(Path(path.realpath(__file__)).parent.parent,
                         'data', 'inventory.xml')

################################################################################
#                             Project continuous waves
################################################################################

CONT_FOLDER = 'CONT_WAVES'

################################################################################
#                               EQTransformer
################################################################################

EQT_FOLDER     = 'DETECTION'

EQT_WAVES_DIR  = 'WAVES'

EQT_DET_DIR    = 'RESULTS'

EQT_FNAME_FMT  = ('{network}.{station}.{location}.{channel}'
                 '__{ys}{ms:02d}{ds:02d}T{Hs:02d}{Ms:02d}{Ss:02d}Z'
                 '__{ye:02d}{me:02d}{de:02d}T{He:02d}{Me:02d}{Se:02d}Z.mseed')

EQT_JSON_FNAME = 'stations.json'

EQT_DET_FNAME  = 'X_prediction_results.csv'

EQT_DET_COLS   = ['network', 'station',
                  'station_lat', 'station_lon', 'station_elv',
                  'p_arrival_time', 'p_probability',
                  's_arrival_time', 's_probability']

################################################################################
#                               HypoInverse
################################################################################


################################################################################
#                               PhaseLink
################################################################################

PL_FOLDER       = 'EVENTS_ASSOCIATION'

PL_DATA_PATH    = path.join(Path(path.realpath(__file__)).parent.parent,
                            'data', 'PhaseLink')

PL_STA_FNAME    = 'stlist.txt'
PL_STA_FILE_FMT = '{network:2} {station:5} {latitude:9.4f} {longitude:10.4f}'

PL_DET_FNAME    = 'picks.txt'
PL_DET_FILE_FMT = '{network:2} {station:5} {phase:1} {time} {prob:4.2f}'

################################################################################
#                               NonLinLoc
################################################################################

NLL_FOLDER              = 'LOCATION'

NLL_DATA_PATH           = path.join(Path(path.realpath(__file__)).parent.parent,
                                   'data', 'NonLinLoc')

NLL_IN_FOLDER           = '0_IN'
NLL_MODEL_FOLDER        = '1_MODEL'
NLL_TIME_FOLDER         = '2_TIME'
NLL_SYNTH_FOLDER        = '3_SYNTH'
NLL_LOC_FOLDER          = '4_LOC'

NLL_IN_FILE_NAME        = 'nlloc.in'
NLL_IN_FILE             = path.join(NLL_IN_FOLDER, NLL_IN_FILE_NAME)

NLL_LOCFILES_STATEMENT  = ('LOCFILES {obs_filepath} {obs_type} '
                           '{time_folder_path}/layer '
                           '{loc_folder_path}/{root_name}')

NLL_IN_RANKS_FOLDER     = 'RANKS'
NLL_RANK_OBS_FILE       = '{rank:03d}_obs.txt'
NLL_RANK_IN_FILE        = '{rank:03d}.in'
NLL_FILE_RANK_HYPOELL   = ('{base_dir}/'
                          f'{NLL_FOLDER}/{NLL_LOC_FOLDER}/'
                          '{root_name}_{rank:03d}.sum.grid0.loc.hypo_ell')


NLL_VEL2GRID_CMD        = 'Vel2Grid'
NLL_GRID2TIME_CMD       = 'Grid2Time'
NLL_NLLOC_CMD           = 'NLLoc'

NLL_HYPO_ELL_OUT_SUFFIX = '.sum.hypo_ell'

NLL_STA_FILENAME        = 'stations.in'
NLL_STA_FMT             = (
    'GTSRCE {station:7} LATLON {latitude:8} {longitude:8} '
    '{depth:5} {elevation:9}'
)

NLL_EQSTA_FILENAME      = 'eqsta.in'
NLL_EQSTA_FMT           = (
    'EQSTA {station:7} {phase:5} {errorType:9} {error:5} '
    '{errorReportType:15} {errorReport:11} {probActive:10}'
)

NLL_PHA_FMT             = (
    '{station:6} {network:4} {component:4} {P_phase_onset:1} {phase:6} '
    '{first_motion:1} {year:04d}{month:02d}{day:02d} {hour:02d}{minute:02d} '
    '{second:7.4f} {err:3} {pick_error:9.2e} {err_mag:9.2e} {coda_dur:9.2e} '
    '{amplitude:9.2e}'
)

################################################################################
#                                Catalog
################################################################################

CAT_PATH     = '{base_dir}/catalog.pkl'
CAT_MAG_PATH = '{base_dir}/catalog_mag.pkl'

################################################################################
#                                 Waves
################################################################################

WAV_FOLDER       = 'WAVES'
WAV_LEFT_MARGIN  = 20 # Before minimum pick time
WAV_RIGHT_MARGIN = 60 # After maximum pick time

################################################################################
#                               GrowClust
################################################################################

GC_FOLDER       = 'RELOCATION'
GC_DATA_PATH    = path.join(Path(path.realpath(__file__)).parent.parent,
                            'data', 'GrowClust')
GC_IN           = 'IN'
GC_STA_FNAME    = 'stlist.txt'
GC_STA_FILE_FMT = '{station:5} {latitude:9.4f} {longitude:10.4f} {elevation:4d}'

GC_EVLIST_FNAME = 'evlist.txt'
GC_EVLIST_FMT   = ('{eID} {yr} {mon} {day} {hr} {mi} {sec} '
                  '{lat} {lon} {dep} {rms} {eh} {ez} {mag}')

GC_OUT_FNAME    = 'xcordata.txt'
GC_DT_HEAD_FMT  = '# {i:>9d} {j:>9d} 0.0'
GC_DT_PHAS_FMT  = '{station:<7s} {pick2_corr:7.3f} {cc:6.4f} {phase}'
