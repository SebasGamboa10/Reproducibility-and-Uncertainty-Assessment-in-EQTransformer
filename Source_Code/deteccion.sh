#!/bin/bash
##source miniconda_path/miniconda3/etc/profile.d/conda.sh
##source /home/ovsicori/miniconda3/etc/profile.d/conda.sh
conda activate eq_env
python3 "mydir/EQT_DETECT_PREDICTOR.py" --base_dir=directorio_origen --eqt_path=directorio_eqt > "directorio_origen/LOGS/det_logs/det_experiment.txt"  2>&1
