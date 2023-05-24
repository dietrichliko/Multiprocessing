#!/bin/bash

# Check if in CMSSW
if [ -z "$CMSSW_BASE" ]; then
  echo "You must use this package inside a CMSSW environment"
  exit 1
fi

# Check if it is already installed
scram tool info py2-cloudpickle > /dev/null 2> /dev/null
if [ $? -eq 0 ]; then
  echo "--> py2-cloudpickle already installed"
  exit 1
fi

installpath="${CMSSW_BASE}/install/py2-cloudpickle"
if [ -d "${installpath}" ]; then
  echo "--> Install path ${installpath} exists, please remove and try again if you want to reinstall"
  exit 1
fi

pip install --prefix=${installpath} cloudpickle==1.3.0

toolfile="${installpath}/py2-cloudpickle.xml"
cat <<EOF > "$toolfile"
<tool name="py2-cloudpickle" version="1.3.0">
  <info url="https://github.com/cloudpipe/cloudpickle"/>
  <client>
    <environment name="PY2_CLOUDPICKLE_BASE" default="${installpath}"/>
    <runtime name="LD_LIBRARY_PATH"     value="\$PY2_CLOUDPICKLE_BASE/lib" type="path"/>
    <runtime name="PYTHONPATH"          value="\$PY2_CLOUDPICKLE_BASE/lib/python2.7/site-packages" type="path"/>
  </client>
</tool>
EOF

mkdir -p "${CMSSW_BASE}/external/${SCRAM_ARCH}"
scram setup "$toolfile"