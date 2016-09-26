Name:           exodusii
Version:        6.02
Release:        4%{?dist}
Summary:        Library to store and retrieve transient finite element data
License:        BSD
Url:            http://sourceforge.net/projects/exodusii/
#last version of the orinal source, got merge into https://github.com/gsjaardema/seacas
# but has different API
Source0:         http://distfiles.gentoo.org/distfiles/exodus-%{version}.tar.gz
Source1:        http://prod.sandia.gov/techlib/access-control.cgi/1992/922137.pdf
Source2:        http://fossies.org/linux/Trilinos-trilinos-release/packages/seacas/doc/exodusII.pdf
Patch1:         sovers.diff
Patch2:         exodus-6.02-testresults.patch

BuildRequires:  tcsh
BuildRequires:  gcc-gfortran
BuildRequires:  cmake
BuildRequires:  netcdf-devel

%description
EXODUS II is a model developed to store and retrieve data for finite element
analyses. It is used for pre-processing (problem definition), post-processing
(results visualization), as well as code to code data transfer. An EXODUS II
data file is a random access, machine independent, binary file that is written
and read via C, C++, or Fortran library routines which comprise the
Application Programming Interface (API).

%package devel
Summary:    Development headers and libraries for exodusII
Requires:   %{name} = %{version}-%{release}

%description devel
EXODUS II is a model developed to store and retrieve data for finite element
analyses. It is used for pre-processing (problem definition), post-processing
(results visualization), as well as code to code data transfer. An EXODUS II
data file is a random access, machine independent, binary file that is written
and read via C, C++, or Fortran library routines which comprise the
Application Programming Interface (API).

This package contains development headers and libraries for exodusII.

%package doc
Summary:    PDF documentation for exodusII
BuildArch:  noarch

%description doc
EXODUS II is a model developed to store and retrieve data for finite element
analyses. It is used for pre-processing (problem definition), post-processing
(results visualization), as well as code to code data transfer. An EXODUS II
data file is a random access, machine independent, binary file that is written
and read via C, C++, or Fortran library routines which comprise the
Application Programming Interface (API).

This package contains pdf documentation for exodusII.

%prep
%setup -n exodus-%{version} -q
%patch -P 1 -p1
%patch -P 2 -p1
#avoid over-linking
#zlib is actually not a direct dep of exodus, but hdf5
sed -i '/FATAL_ERROR.*ZLib/s/^/#/' exodus/CMakeLists.txt

%build
cd exodus
mkdir %{_target_platform}
pushd %{_target_platform}
export LDFLAGS="${LDFLAGS} -Wl,--as-needed"
%{cmake} -DBUILD_SHARED=ON -DHDF5HL_LIBRARY="" -DHDF5_LIBRARY="" -DCMAKE_DISABLE_FIND_PACKAGE_ZLIB=ON -DZLIB_LIBRARY="" ..
%make_build

%install
%make_install -C exodus/%{_target_platform}
[[ %{_lib} = lib ]] || mv %{buildroot}/%{_prefix}/{lib,%{_lib}}
ln -s libexoIIv2c-%version.so "%buildroot/%_libdir/libexoIIv2c.so"
ln -s libexoIIv2for-%version.so "%buildroot/%_libdir/libexoIIv2for.so"
mkdir -p %{buildroot}/%{_docdir}/%{name}
cp -p %{S:1} %{S:2} %{buildroot}/%{_docdir}/%{name}

%check
make -C exodus/%{_target_platform}  check f_check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files devel
%{_includedir}/*
%{_libdir}/libexoIIv2c.so
%{_libdir}/libexoIIv2for.so

%files
%license exodus/COPYRIGHT
%{_libdir}/libexoIIv2c-*.so
%{_libdir}/libexoIIv2for-*.so

%files doc
%{_docdir}/%{name}

%changelog
* Mon Sep 26 2016 Christoph Junghans <junghans@votca.org> - 6.02-4
- Fixed another overlinking issue by --as-needed

* Fri Sep 09 2016 Christoph Junghans <junghans@votca.org> - 6.02-3
- Fixed testsuite
- Avoid over-linking
- Minor changes from review (bug #1336552)

* Sat Sep 03 2016 Christoph Junghans <junghans@votca.org> - 6.02-2
- Minor changes from review (bug #1336552)
- Added doc package

* Thu Sep 01 2016 Christoph Junghans <junghans@votca.org> - 6.02-1
- First release.
