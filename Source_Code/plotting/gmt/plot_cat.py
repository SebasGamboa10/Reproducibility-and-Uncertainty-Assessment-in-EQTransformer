from os import system
cat_filepath = '../../PhaseNet_DB/pn_db.event.cat'
ymin, ymax, xmin, xmax = 7.574341, 10.2829, -84.6239, -82.133
output = '../../PhaseNet_DB/events_map'

MARGIN = 1.6
WIDTH = 15
height = WIDTH/(xmax-xmin)*(ymax-ymin)

MAP_WIDTH = WIDTH-MARGIN


PS_MEDIA   = f'{WIDTH}cx{height}c'
region     = f'-R{xmin}/{xmax}/{ymin}/{ymax}'
projection = f'-JM{(ymin+ymax)/2}/{MAP_WIDTH}'
boundary   = '-B2/2WSne'
position   = f'"-Xc -Yc"'
TMP_XY     = 'tmp_xy'


system((
        f'./plot_cat.sh {PS_MEDIA} {output} {region} '
        f'{projection} {boundary} {position} {cat_filepath}'
))
