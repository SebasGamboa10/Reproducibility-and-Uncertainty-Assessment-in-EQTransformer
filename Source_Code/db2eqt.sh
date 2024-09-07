#!/bin/bash
##source /home/ovsicori/miniconda3/etc/profile.d/conda.sh
conda activate eq_env
python "mydir/DB2EQT.py" --base_dir=directorio_origen --startdate=ano-dia --enddate=ano-conuno > "directorio_origen/LOGS/db2eqt_logs/db2eqt_experiment.txt"
