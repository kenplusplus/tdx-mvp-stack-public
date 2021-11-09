#!/usr/bin/bash

CURR_DIR=$(dirname "$(readlink -f "$0")")
HOST_REPO=$CURR_DIR/"tdx-repository"
GUEST_REPO=$CURR_DIR/"tdx-guest-repository"

mkdir -p $HOST_REPO $GUEST_REPO

for rpmsrc in intel-mvp-tdx-* ; do
  if [[ ! -f $rpmsrc/DONE ]]; then
    echo "build $rpmsrc ..."
    if $rpmsrc/build.sh; then
      touch $rpmsrc/DONE
    else
      echo "build error $rpmsrc"
      exit 1
    fi
  else
    echo "build skipped $rpmsrc ..."
  fi

  if [[ $rpmsrc == *"tdx-guest"* ]]; then
    cp -rv $rpmsrc/rpmbuild/RPMS/* $GUEST_REPO/
  else
    cp -rv $rpmsrc/rpmbuild/RPMS/* $HOST_REPO/
  fi
done

mv -vf $HOST_REPO/x86_64/*qemu-guest-agent* $GUEST_REPO/x86_64/