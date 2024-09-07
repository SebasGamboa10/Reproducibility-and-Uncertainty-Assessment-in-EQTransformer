apt-get update
yes | apt install vim
yes | apt-get install git
yes | conda install -c anaconda scipy 
yes | conda install -c conda-forge obspy 
yes | conda install -c conda-forge geopy
yes | conda install -c numba numba
yes | conda install -c anaconda pandas 

# git clone https://github.com/NVIDIA/apex
# cd apex
# pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./

git clone https://github.com/lvanderlaat/PhaseLink-1.0.git
