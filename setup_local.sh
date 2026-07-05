#!/bin/bash
# k4simdelphes_install is now under delphes/
INSTALL_DIR="/ceph/salshamaily/haa4K_FCCee/delphes/k4simdelphes_install"
export PKG_CONFIG_PATH=${PKG_CONFIG_PATH:-}
export XLOCALEDIR=${XLOCALEDIR:-}
source /cvmfs/sw.hsf.org/key4hep/releases/2024-10-03/x86_64-almalinux9-gcc14.2.0-opt/key4hep-stack/2024-10-08-k6xtr3/setup.sh
export PATH="$INSTALL_DIR/bin:$PATH"
export LD_LIBRARY_PATH="$INSTALL_DIR/lib:$INSTALL_DIR/lib64:$LD_LIBRARY_PATH"
if [ -n "${PS1:-}" ]; then
    echo "Local k4SimDelphes: $(which DelphesPythia8_EDM4HEP 2>/dev/null || echo 'NOT FOUND')"
fi
