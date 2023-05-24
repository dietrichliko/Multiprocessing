# Multiprocessing with CMSSW, python2.7 and lamda functions

* lambda functions cannot be pickled, so cloudpickle is required. For python2.7
version 1.3.0 is used
* concurrent.futures has been backported and is already included in the CMSSW SW stack

## Quickstart

Create CMSSW area

    cmsrel CMSSW_10_6_26
    cd CMSSW_10_6_26/src
    
    git clone https://github.com/dietrichliko/Multiprocessing.git
    cmsenv

Install cloudpickle

    ./install_cloudpickle.sh
    cmsenv

Filling histograms in subprocesses

    ./mp_fill.py