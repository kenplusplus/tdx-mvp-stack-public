#!/usr/bin/bash

set -ex

DOWNSTREAM_GIT_URI="https://github.com/tianocore/edk2-staging.git"
DOWNSTREAM_TAG="2021-ww43.5"
CURR_DIR=$(dirname "$(readlink -f "$0")")
RPMBUILD_DIR=$CURR_DIR/rpmbuild
SPEC=$CURR_DIR/tdvf.spec

mkdir -p $RPMBUILD_DIR/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

pushd $CURR_DIR
if [[ ! -f $RPMBUILD_DIR/SOURCES/edk2.tar.gz ]]; then
  if [[ ! $(command -v git) ]]; then
      echo "error: git is not installed"
      exit 1
  fi
  git clone --single-branch --depth 1 --branch ${DOWNSTREAM_TAG} ${DOWNSTREAM_GIT_URI}
  pushd edk2-staging
  git submodule init
  git submodule sync
  git submodule update
  rm -rf .git/
  popd
  tar czf edk2.tar.gz edk2-staging/

  mv edk2.tar.gz $RPMBUILD_DIR/SOURCES/
  rm -rf edk2-staging
fi
popd

sudo -E dnf builddep -y $SPEC
rpmbuild --define "_topdir $RPMBUILD_DIR" --undefine=_disable_source_fetch -v -ba $SPEC
