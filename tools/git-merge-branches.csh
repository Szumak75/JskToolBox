#!/usr/bin/env csh

# Merge all branches from master
#
# Usage: git-merge-branches.csh

set MASTER = 'master'
set BRANCHES = ('systemtool_devel' 'configtool_devel' 'devices_devel' 'libs_devel' 'logstool_devel' 'netaddresstool_devel' 'raise_devel' 'stringtool_devel' 'datetool_devel' 'basetool_devel' 'tktool_devel' 'edmctool_devel' )

echo ${MASTER}
echo ${BRANCHES}

foreach i (${BRANCHES})
    echo "\033[31m----[\033[39mMerge \033[32m${i}\033[39m branch from \033[32m${MASTER}\033[39m\033[31m]----\033[39m"
    git switch ${i}
    git pull
    git merge ${MASTER}
    git push
    git switch ${MASTER}
end
