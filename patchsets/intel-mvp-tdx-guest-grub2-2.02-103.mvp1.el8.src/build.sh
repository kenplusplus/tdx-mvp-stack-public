#!/usr/bin/bash

set -ex


UPSTREAM_GIT_URI="https://github.com/rhboot/grub2.git"
UPSTREAM_BRANCH="rhel-8.4"
CURR_DIR=$(dirname "$(readlink -f "$0")")
RPMBUILD_DIR=$CURR_DIR/rpmbuild
SPEC=$CURR_DIR/tdx-guest-grub2.spec

mkdir -p $RPMBUILD_DIR/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
pushd $CURR_DIR
if [[ ! -f $RPMBUILD_DIR/SOURCES/grub-2.02.tar.gz ]]; then
  if [[ ! $(command -v git) ]]; then
      echo "error: git is not installed"
      exit 1
  fi
  git clone --single-branch --depth 1 --branch ${UPSTREAM_BRANCH} ${UPSTREAM_GIT_URI}
  mv grub2 grub-2.02
  tar --exclude=.git -czf $RPMBUILD_DIR/SOURCES/grub-2.02.tar.gz grub-2.02
  rm -rf grub-2.02
fi
popd

cp $CURR_DIR/grub.macros $RPMBUILD_DIR/SOURCES/
cp $CURR_DIR/patch* $RPMBUILD_DIR/SOURCES/

sudo -E dnf builddep --define "_topdir $RPMBUILD_DIR" -y $SPEC
rpmbuild --define "_topdir $RPMBUILD_DIR" --undefine=_disable_source_fetch -v -ba $SPEC

