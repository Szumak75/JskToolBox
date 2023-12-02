#!/bin/csh

set MASTER = 'master'
set BRANCHES = ('configtool_devel' 'devices_devel' 'libs_devel' 'logstool_devel' 'netaddresstool_devel' 'raise_devel' 'stringtool_devel')

echo ${MASTER}
echo ${BRANCHES}

foreach i (${BRANCHES})
    echo "----[Merge ${i} branch from ${MASTER}]----"
    git switch ${i}
    git pull
    git merge ${MASTER}
    git push
    git switch ${MASTER}
end
