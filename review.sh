#!/bin/bash -xe

spin()
{
  spinner="/|\\-/|\\-"
  while :
  do
    for i in `seq 0 7`
    do
      echo -n "${spinner:$i:1}"
      echo -en "\010"
      sleep 1
    done
  done
}

PKG="$1"
MOCK_CONFIG="$2"
EXIT_CODE=0
H=/travis/$PKG

dnf -q -y install fedora-review spectool sudo
useradd -d ${H} -g mock review
cd /travis/$PKG
spectool -g ${PKG}.spec
rpmbuild -D"_sourcedir ${PWD}" -D"_srcrpmdir ${PWD}" -bs ${PKG}.spec

chown -R review:mock ${H}
set +x
spin &
set -x
SPIN_PID=$!
trap "kill -9 $SPIN_PID" $(seq 0 15)
if ! sudo -u review fedora-review -v --mock-config ${MOCK_CONFIG} -n ${PKG} --mock-options "--no-bootstrap-chroot --no-cleanup-after --no-clean --old-chroot"; then
  EXIT_CODE=1
fi
kill -9 $SPIN_PID
cd review-${PKG}
find . -name '*.log' -print -exec cat {} + || true
cat licensecheck.txt || true
cat review.txt || true
exit ${EXIT_CODE}
