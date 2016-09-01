Name:           exodusii
Version:        6.02
Release:        1%{?dist}
Summary:        Library to store and retrieve transient finite element data
License:        BSD
Url:            http://sourceforge.net/projects/exodusii/
#last version of the orinal source, got merge into https://github.com/gsjaardema/seacas
# but has different API
Source:         http://distfiles.gentoo.org/distfiles/exodus-%{version}.tar.gz
Patch1:         sovers.diff

BuildRequires:  gcc-c++
BuildRequires:  tcsh
BuildRequires:  gcc-gfortran
BuildRequires:  cmake
BuildRequires:  netcdf-devel
BuildRequires:  zlib-devel

%description
EXODUS II is a model developed to store and retrieve data for finite element
analyses. It is used for pre-processing (problem definition), post-processing
(results visualization), as well as code to code data transfer. An EXODUS II
data file is a random access, machine independent, binary file that is written
and read via C, C++, or Fortran library routines which comprise the
Application Programming Interface (API).

%package devel
Summary:    Development headers and libraries for exodusII

%description devel
EXODUS II is a model developed to store and retrieve data for finite element
analyses. It is used for pre-processing (problem definition), post-processing
(results visualization), as well as code to code data transfer. An EXODUS II
data file is a random access, machine independent, binary file that is written
and read via C, C++, or Fortran library routines which comprise the
Application Programming Interface (API).

This package contains development headers and libraries for exodusII.

%prep
%setup -n exodus-%{version} -q
%patch -P 1 -p1

%build
cd exodus
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake} -DBUILD_SHARED=ON ..
%make_build

%install
%make_install -C exodus/%{_target_platform}
[[ %{_lib} = lib ]] || mv %{buildroot}/%{_prefix}/{lib,%{_lib}}
ln -s libexoIIv2c-%version.so "%buildroot/%_libdir/libexoIIv2c.so"
ln -s libexoIIv2for-%version.so "%buildroot/%_libdir/libexoIIv2for.so"
 
%check
make -C exodus/%{_target_platform}  check f_check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files devel
%{_includedir}/*
%{_libdir}/libexoIIv2c.so
%{_libdir}/libexoIIv2for.so

%files
%doc exodus/README
%license exodus/COPYRIGHT
%{_libdir}/libexoIIv2c-*.so
%{_libdir}/libexoIIv2for-*.so
 
%changelog
* Thu Sep 01 2016 Christoph Junghans <junghans@votca.org> - 6.02-1
- First release.
