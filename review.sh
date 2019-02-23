#!/bin/bash -xe

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
sudo -u review fedora-review -v --mock-config ${MOCK_CONFIG} -n ${PKG} --mock-options "--no-bootstrap-chroot --no-cleanup-after --no-clean --old-chroot" || EXIT_CODE=1
find "review-${PKG}" -name '*.log' -print -exec cat {} ; || true
cat review-${PKG}/licensecheck.txt || true
cat review-${PKG}/review.txt || true
exit ${EXIT_CODE}
