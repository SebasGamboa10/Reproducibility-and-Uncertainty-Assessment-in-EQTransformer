
import argparse
import json
from os import getcwd, system as _
from pathlib import Path
from shutil import copy

from config.vars import *
from utils.catalog import cat_to_gmt
from utils.spatial import *
from utils.stations import sta2GMT



def parse_args():
    description = (
        '\tPlots map and cross-section with GMT\n'
    )

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=Formatter_Class)

    parser.add_argument('--output',
                        help='Path to output PDF file: /path/to/name')

    parser.add_argument('--stations_csv',
                        help='Path to stations csv file')

    required = parser.add_argument_group('Required arguments')

    required.add_argument('--catalog', required=True,
                          help='Path to catalog file')

    required.add_argument('--fmt', required=True,
                          help='collect,growclust,hypodd_in,hypoellipse,zmap')

    args = parser.parse_args()
    return args


class Conf(dict):
    def __init__(self, *args, **kwargs):
        super(Conf, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    if isinstance(v, dict):
                        v = Conf(v)
                    if isinstance(v, list):
                        self.__convert(v)
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                if isinstance(v, dict):
                    v = Conf(v)
                elif isinstance(v, list):
                    self.__convert(v)
                self[k] = v

    def __convert(self, v):
        for elem in range(0, len(v)):
            if isinstance(v[elem], dict):
                v[elem] = Conf(v[elem])
            elif isinstance(v[elem], list):
                self.__convert(v[elem])

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Conf, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Conf, self).__delitem__(key)
        del self.__dict__[key]


def plot_catalog(filepath, fmt, output, df_stations=None):

    # Get configuration settings
    script_path = path.dirname(path.realpath(__file__))

    params_filepath = path.join(getcwd(), 'map_section.json')

    if not path.exists(params_filepath):
       copy(path.join(script_path, 'map_section.json'), params_filepath)

    with open(params_filepath) as json_file:
        c = Conf(json.load(json_file))

    data_path = path.join(Path(script_path).parent, 'data', 'Plot')

    c.topo.grd = path.join(data_path, c.topo.grd)
    c.topo.cpt = path.join(data_path, c.topo.cpt)
    c.subduction.grd = path.join(data_path, c.subduction.grd)
    c.subduction.asc = path.join(data_path, c.subduction.asc)

    if df_stations is not None:
        sta2GMT(df_stations, c.tmp.stations)

    # Export catalog
    cat_to_gmt(filepath, c.tmp.catalog, fmt)

    x, y, z = np.loadtxt(c.tmp.catalog, delimiter=' ', usecols=(0, 1, 2), unpack=True)

    centroid_x = np.median(x)
    centroid_y = np.median(y)
    max_depth  = z.max()


    # Profile
    x1, x2, y1, y2 = get_profile_extremes(centroid_x, centroid_y, c.profile.azimuth,
                                          c.profile.x_range, c.profile.y_range)

    x1 += c.profile.shift_x
    x2 += c.profile.shift_x
    y1 += c.profile.shift_y
    y2 += c.profile.shift_y

    with open(c.tmp.extremes, 'w') as f:
        f.write(f'{x1} {y1} X\n')
        f.write(f'{x2} {y2} X\'\n')


    # Project locations
    distance = project_points(x1, x2, y1, y2, x, y)
    np.savetxt(c.tmp.proj_location, np.transpose([deg2km(distance), z, z]), fmt='%f')


    # Project topography
    _((
        f"project -C{x1}/{y1} -E{x2}/{y2} -G{c.topo.dist} -Q | "
        f"awk '{{ print $1,$2,$3 }}' > {c.tmp.track}")
     )
    _((
        f"grdtrack {c.tmp.track} -G{c.topo.grd} -T | awk -v v={c.topo.exageration} "
        f"'{{ print $3,$4*v/1000 }}' > {c.tmp.topo_track}")
    )

    d, z = np.loadtxt(c.tmp.topo_track, usecols=(0, 1), unpack=True)

    max_distance = d.max()
    zmin         = z.min()
    zmax         = 5*c.topo.exageration
    z_range      = zmax + abs(zmin)

    with open(c.tmp.topo_label, 'w') as f:
        f.write(f'{0} {zmax/2} Topography\ vertical\ exageration:\ {c.topo.exageration}')


    # Project subduction
    x, y, cellsize, zz = read_ascDEM(c.subduction.asc)
    x = -(360 - x)
    distance, elevation, _xy = cross_section(x, y, zz, x1, x2, y1, y2,
                                             c.profile.dist, cellsize)
    np.savetxt(c.tmp.subduction_track,
               np.transpose([deg2km(distance), elevation]), fmt='%f')

    max_depth = c.max_depth

    # Map boundaries
    xmin = centroid_x - c.map.x_range/2 + c.map.shift_x
    xmax = centroid_x + c.map.x_range/2 + c.map.shift_x
    ymin = centroid_y - c.map.y_range/2 + c.map.shift_y
    ymax = centroid_y + c.map.y_range/2 + c.map.shift_y

    # Heights
    map_height       = c.map.y_range * c.map.width / c.map.x_range
    topo_prof_height = z_range * c.map.width / max_distance
    profile_height   = abs(max_depth) * c.map.width / max_distance

    # Figure size
    media_width  = c.map.width
    media_height = map_height + topo_prof_height + profile_height

    # Y positions
    map_Yc     = (topo_prof_height + profile_height)/2
    topo_Yc    = map_Yc - (map_height/2 + topo_prof_height/2)
    profile_Yc = -(map_height + topo_prof_height)/2

    # Depth scale position
    depth_scale_x = c.map.width + 1.2
    depth_scale_y = map_height/2

    # Update figure size
    media_width  = media_width  + 5*c.layout.margin
    media_height = media_height + 2*c.layout.margin

    # Ticks separation (map)
    xticks_delta = c.map.x_range/c.map.n_ticks
    yticks_delta = c.map.y_range/c.map.n_ticks

    map_region   = f'-R{xmin}/{xmax}/{ymin}/{ymax}'
    map_proj     = f'-JX{c.map.width}d/{map_height}d'
    map_position = f'-Xc -Yc{map_Yc}'
    map_boundary = f'-B{xticks_delta}/{yticks_delta}wsNE'

    topo_region   = f'-Rm0/{max_distance}/{zmin}/{zmax}'
    topo_proj     = f'-JX{c.map.width}/{topo_prof_height}'
    topo_position = f'-Xc -Yc{topo_Yc}'

    profile_region   = f'-Rm0/{max_distance}/{max_depth}/5'
    profile_proj     = f'-JX{c.map.width}/{profile_height}'
    profile_position = f'-Xc -Yc{profile_Yc}'
    profile_boundary = (
        f'-Ba{c.profile.y_ticks_delta}f{c.profile.y_ticks_delta/2}:"X-X\' '
        f'[km]":/{c.profile.y_ticks_delta}f{c.profile.y_ticks_delta/2}:"[km]":WSe'
    )

    n_events = sum(1 for line in open(c.tmp.catalog))

    out = output+'.ps'

    ###########################################################################

    _(f'gmtset PS_MEDIA            = {media_width}cx{media_height}c')
    _(f'gmtset MAP_FRAME_TYPE      = plain')
    _(f'gmtset PS_PAGE_ORIENTATION = portrait')
    _(f'gmtset FONT_ANNOT_PRIMARY  = 8')
    _(f'gmtset FONT_LABEL          = 9')

    ###########################################################################

    _(f'makecpt -T{max_depth}/1/1 -C{c.subduction.cpt} -M > {c.tmp.depth_cpt}')

    ################################################################################

    _(f'psbasemap -K {map_region} {map_proj} {map_position} {map_boundary} > {out}')

    # Topography
    _(f'grdgradient {c.topo.grd} -G{c.tmp.hillshade} -A{c.topo.azimuth} -N{c.topo.gradient_max}')
    # _(f'grdimage -O -K {c.topo.grd} -R -J -C{c.topo.cpt} -I{c.tmp.hillshade} -t{c.topo.transparency} >> {out}')
    _(f'grdimage -O -K {c.topo.grd} -R -J -C{c.topo.cpt} -t{c.topo.transparency} >> {out}')
    _(f'pscoast -O -K -R -J -W.7 -N1 -Dh >> {out}')
    _(f'psscale -O -K -Dx{-2}/{depth_scale_y}/{map_height}/0.2 -B1000 -C{c.topo.cpt} >> {out}')

    # Subduction
    _(f'grdimage -O -K -R -J {c.subduction.grd} -C{c.tmp.depth_cpt} -Q -t{c.subduction.transparency} >> {out}')
    _(f'grdcontour -O -K -R -J {c.subduction.grd} -C10 -A >> {out}')
    _(f'psscale -O -K -Dx{depth_scale_x}/{depth_scale_y}/{map_height}/0.2 '
      f' -Bxa+l"Depth [km]" -C{c.tmp.depth_cpt} >> {out}')

    # Locations
    _(f'psxy -O -K -R -J {c.tmp.catalog} -Sc{c.events.circle_size}'
      f' -W{c.events.linewidth} -C{c.tmp.depth_cpt} >> {out}')

    #Profile
    _(f'psxy -O -K -R -J {c.tmp.extremes} -W0.5 >> {out}')
    _(f'pstext -O -K -R -J {c.tmp.extremes} -F+f10 -Gwhite >> {out}')

    # Stations
    if df_stations:
        _(f'psxy -O -K {c.tmp.stations} -R -J -St{c.stations.size} -G{c.stations.color} -W.7 >> {out}')

    ###########################################################################

    _(f'psxy -O -K {topo_region} {topo_proj} {topo_position} {c.tmp.topo_track} -W1 >> {out}')
    _(f'pstext -O -K -R -J {c.tmp.topo_label} -F+f8+jLB -Gwhite >> {out}')

    ###########################################################################

    _(f'psxy -O -K {profile_region} {profile_proj} {profile_position} '
      f'{c.tmp.subduction_track} -W1 {profile_boundary} >> {out}')
    _(f'psxy -O -R -J {c.tmp.proj_location} -Sc{c.events.circle_size}'
      f' -C{c.tmp.depth_cpt} -W{c.events.linewidth}  >> {out}')

    _('rm tmp*')
    _(f'psconvert {out} -Tf')
    _(f'rm {out}')


if __name__ == '__main__':
    args = parse_args()

    if args.stations_csv:
        df_stations = pd.read_csv(args.stations_csv)
    else:
        df_stations = None

    plot_catalog(args.catalog, args.fmt, args.output, df_stations=df_stations)
