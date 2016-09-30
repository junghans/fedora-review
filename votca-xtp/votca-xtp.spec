%global _rcname rc1
%global _rc _%%_rcname

Name:           votca-xtp
Version:        1.4
Release:        0.1%{?_rcname}%{?dist}
Summary:        VOTCA excitation and charge properties module
License:        ASL 2.0
URL:            http://www.votca.org
Source0:        https://github.com/votca/xtp/archive/v%{version}%{?_rc}.tar.gz#/%{name}-%{version}%{?_rc}.tar.gz
Source1:        https://github.com/votca/xtp/releases/download/v%{version}%{?_rc}/votca-xtp-manual-%{version}%{?_rc}.pdf

BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  votca-csg-devel = %{version}

Requires:   %{name}-common = %{version}-%{release}
Requires:   %{name}-libs%{_isa} = %{version}-%{release}

%description
Versatile Object-oriented Toolkit for Coarse-graining Applications (VOTCA) is
a package intended to reduce the amount of routine work when doing systematic
coarse-graining of various systems. The core is written in C++.

This package contains the excitation and charge properties module of VOTCA
package.

%package libs
Summary:        Libraries for VOTCA excitation and charge properties module

%description libs
Versatile Object-oriented Toolkit for Coarse-graining Applications (VOTCA) is
a package intended to reduce the amount of routine work when doing systematic
coarse-graining of various systems. The core is written in C++.

This package contains libraries for the excitation and charge properties 
module of VOTCA package.

%package devel
Summary:        Development headers and libraries for VOTCA XTP
Requires:       %{name}-libs%{_isa} = %{version}-%{release}
Requires:       votca-csg-devel%{_isa} = %{version}

%description devel
Versatile Object-oriented Toolkit for Coarse-graining Applications (VOTCA) is
a package intended to reduce the amount of routine work when doing systematic
coarse-graining of various systems. The core is written in C++.

This package contains development headers and libraries for the excitation and
charge properties module.

%package common
Summary:        Architecture independent data files for VOTCA XTP
BuildArch:      noarch

%description common
Versatile Object-oriented Toolkit for Coarse-graining Applications (VOTCA) is
a package intended to reduce the amount of routine work when doing systematic
coarse-graining of various systems. The core is written in C++.

This package contains architecture independent data files for VOTCA XTP.

%package doc
Summary:        Architecture independent doc files for VOTCA XTP
BuildArch:      noarch

%description doc
Versatile Object-oriented Toolkit for Coarse-graining Applications (VOTCA) is
a package intended to reduce the amount of routine work when doing systematic
coarse-graining of various systems. The core is written in C++.

This package contains architecture independent documentation for VOTCA XTP.

%prep
%setup -qn xtp-%{version}%{?_rc}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
#save some memory
%{cmake} .. -DLIB=%{_lib} -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE="-DNDEBUG -O1"
%define _smp_mflags -j1
%make_build

%install
%make_install -C%{_target_platform}
sed -i '1s@env @@' %{buildroot}/%{_bindir}/xtp_{basisset,update,update_exciton,testsuite}

mkdir -p %{buildroot}%{_docdir}/%{name}
cp %{S:1} %{buildroot}%{_docdir}/%{name}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%{_bindir}/xtp_*

%files doc
%doc CHANGELOG.md NOTICE README LICENSE.md
%license LICENSE.md
%{_docdir}/%{name}

%files common
%license LICENSE.md
%{_datadir}/votca/*

%files libs
%license LICENSE.md
%{_libdir}/libvotca_xtp.so.*

%files devel
%{_includedir}/votca/xtp/
%{_libdir}/libvotca_xtp.so
%{_libdir}/pkgconfig/libvotca_xtp.pc

%changelog
* Wed Sep 28 2016 Christoph Junghans <junghans@votca.org> - 1.4-0.1rc1
- Imported 1.4_rc1

