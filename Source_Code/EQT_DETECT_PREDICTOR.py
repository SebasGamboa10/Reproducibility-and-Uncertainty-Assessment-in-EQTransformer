import argparse
from os import path
import sys

from config.vars import *
from plotting.plots import s_p_time


def parse_args():
    parser = argparse.ArgumentParser()

    description = (
        '\tEQTransformer mseed predictor\n'
    )

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=Formatter_Class)

    required = parser.add_argument_group('required arguments')

    required.add_argument(
        '--base_dir',
        help='Path to the project root folder',
        required=True
    )

    required.add_argument(
        '--eqt_path',
        help='Path to EQTransformer code',
        required=True
    )

    eqt_params = parser.add_argument_group('EQTransformer arguments')

    eqt_params.add_argument(
        '--detection_threshold',
        default=0.85,
        help='Event detection threshold',
        type=float
    )
    

    eqt_params.add_argument(
        '--P_threshold',
        default=0.9, #Cons model
        #default=0.85, #Original model
        help='P picks detection threshold',
        type=float
    )

    eqt_params.add_argument(
        '--S_threshold',
        default=0.7, #Cons model
        #default=0.5, #Original model
        help='S picks detection threshold',
        type=float
    )

    eqt_params.add_argument(
        '--overlap',
        default=0.9,
        help='Moving window overlap',
        type=float
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    base_dir = args.base_dir
    sys.path.insert(0, args.eqt_path)

    from EQTransformer.utils.hdf5_maker import preprocessor

    preprocessor(
    preproc_dir=path.join(base_dir, EQT_FOLDER, "preproc"),
    mseed_dir=path.join(base_dir, EQT_FOLDER, EQT_WAVES_DIR),
    stations_json=path.join(base_dir, EQT_FOLDER, 'stations.json'),
    overlap=0.3,
    n_processor=16
)


    from EQTransformer.core.predictor import predictor

    predictor(
        input_dir           =path.join(base_dir, EQT_FOLDER, EQT_WAVES_DIR+"_processed_hdfs"),
        input_model         = path.join(args.eqt_path, 'ModelsAndSampleData/EqT_model2.h5'), #Original Model
        output_dir          = path.join(base_dir, EQT_FOLDER, EQT_DET_DIR),
        estimate_uncertainty=True, 
        output_probabilities=False,
        use_multiprocessing=False, #Esta opcion se mantiene desactivada (comentada)
        number_of_sampling=50,
        loss_weights=[0.02, 0.40, 0.58],  
        detection_threshold = args.detection_threshold,
        P_threshold         = args.P_threshold,
        S_threshold         = args.S_threshold, 
        #number_of_plots=100, #100
        #plot_mode='time'
        batch_size=500,
        number_of_cpus=4,
        keepPS=False,
        spLimit=60,
        gpuid               = 0,
        gpu_limit           = None
        )
         

    #fig = s_p_time(path.join(args.base_dir, EQT_FOLDER, EQT_DET_DIR), show=False)

    #fig.savefig(path.join(args.base_dir, EQT_FOLDER, 'S-P_times.pdf'), format='pdf')
