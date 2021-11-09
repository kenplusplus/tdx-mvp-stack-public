#!/usr/bin/bash

set -ex

CURR_DIR=$(dirname "$(readlink -f "$0")")
RPMBUILD_DIR=$CURR_DIR/rpmbuild
SPEC=$CURR_DIR/tdx-guest-kernel.spec

mkdir -p $RPMBUILD_DIR/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
cp $CURR_DIR/*.config $RPMBUILD_DIR/SOURCES/
cp $CURR_DIR/patches* $RPMBUILD_DIR/SOURCES/

sudo -E dnf builddep -y $SPEC
rpmbuild --define "_topdir $RPMBUILD_DIR" --undefine=_disable_source_fetch -v -ba $SPEC
