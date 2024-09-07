# Python Standard Library
import argparse
from os import path

# Other dependencies
import pandas as pd

CODE_PATH, _ = path.split(path.abspath(__file__))
IASP_FILE    = CODE_PATH + '/data/IASP91.csv'

NLLOC_VELMOD_FILENAME = 'velmod_IASP91.in'
NLLOC_VELMOD_FMT = 'LAYER   depth    Vp_top    Vp_grad  Vs_top    Vs_grad   p_top  p_grad'

def to_nlloc(df, output_dir):
    df['var']     = 'LAYER'
    df['Vp_grad'] = 0.0
    df['Vs_grad'] = 0.0
    df['p_top']   = 2.7
    df['p_grad']  = 0.0

    df.vpvs = df.vp/df.vs

    columns = [
        'var', 'depth', 'vp', 'Vp_grad', 'vs', 'Vs_grad', 'p_top', 'p_grad'
    ]

    df = df[columns]

    lines = df.to_string(index=False, header=False, index_names=False,
                         justify='left')

    with open(output_dir + NLLOC_VELMOD_FILENAME, 'w') as f:
        f.write('# ')
        f.write(NLLOC_VELMOD_FMT)
        f.write('\n')
        for line in lines.split('\n'):
            f.write(line[1:])
            f.write('\n')

    # with open('output.dat') as ofile:
    #      fmt = '%.0f %02.0f %4.1f %3.0f %4.0f %4.1f %4.0f %4.1f %4.0f'
    #      np.savetxt(ofile, df.values, fmt=fmt)
    return


def to_growclust(df, output_dir):
    fmt = '{depth:4d} {vp:7.4f} {vs:7.4f}'

    with (open(path.join(output_dir, 'vzmodel_IASP.txt'), 'w')) as f:
        for i, row in df.iterrows():
            f.write(
                fmt.format(
                    depth = int(row.depth),
                    vp    = row.vp,
                    vs    = row.vs
                )
            )
            f.write('\n')
    return



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--max_depth', type=int, default=7000,
                        help='Maximum depth [km]')

    parser.add_argument('-m', '--mode', help='growclust/nlloc')

    parser.add_argument('-o', '--output_dir', help='Path to output directory',
                       default='')

    args = parser.parse_args()

    df = pd.read_csv(IASP_FILE, names=['depth', 'radius', 'vp', 'vs'])
    df = df[df.depth <= args.max_depth]

    if args.mode == 'nlloc':
        to_nlloc(df, args.output_dir)
    elif args.mode == 'growclust':
        to_growclust(df, args.output_dir)


