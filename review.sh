#!/bin/bash -xe

PKG="$1"
MOCK_CONFIG="$2"
H=/travis/$PKG

dnf -q -y install fedora-review spectool
useradd -d ${H} -g mock review
cd /travis/$PKG
spectool -g ${PKG}.spec
rpmbuild -D"_sourcedir ${PWD}" -D"_srcrpmdir ${PWD}" -bs ${PKG}.spec

chown -R review:mock ${H}
if ! /travis/spinner.sh su - -c 'fedora-review -v --mock-config ${MOCK_CONFIG} -n ${PKG} --mock-options "--no-bootstrap-chroot --no-cleanup-after --no-clean --old-chroot" review'; then
  cat .cache/fedora-review.log
  find  review-${PKG} -name '*.log' -print -exec cat {} ;
  exit 1
fi
find review-${PKG} -name '*.log' -print -exec cat {} ;
cat review-${PKG}/licensecheck.txt
cat review-${PKG}/review.txt
