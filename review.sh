#!/bin/bash -xe

PKG="$1"
MOCK_CONFIG="$2"
EXIT_CODE=0
H=/travis/$PKG

dnf -q -y install fedora-review spectool sudo dnf-plugins-core
useradd -d ${H} -g mock review

cd /travis/$PKG
spectool -g ${PKG}.spec
dnf builddep -y ${PKG}.spec
rpmbuild -D"_sourcedir ${PWD}" -D"_srcrpmdir ${PWD}"  -D"_rpmdir ${PWD}" -ba ${PKG}.spec
mv -v */*.rpm .

chown -R review:mock ${H}
if ! sudo -u review fedora-review -v -p --mock-config ${MOCK_CONFIG} -n ${PKG} --mock-options "--no-bootstrap-chroot --no-cleanup-after --no-clean --old-chroot"; then
  EXIT_CODE=1
fi
cd review-${PKG}
set -e
find . -name '*.log' -print -exec cat {} +
cat licensecheck.txt
cat review.txt
exit ${EXIT_CODE}
