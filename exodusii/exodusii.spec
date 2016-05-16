Name:           exodusii
Version:        6.02
Release:        0
Summary:        Library to store and retrieve transient finite element data
Group:          Productivity/Scientific/Math
License:        BSD-3-Clause
Url:            http://sourceforge.net/projects/exodusii/
Source:         http://distfiles.gentoo.org/distfiles/exodus-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  cmake
BuildRequires:  netcdf-devel
BuildRequires:  zlib-devel

%description
EXODUS II is a model developed to store and retrieve data for finite element
analyses. It is used for preprocessing (problem definition), postprocessing
(results visualization), as well as code to code data transfer. An EXODUS II
data file is a random access, machine independent, binary file that is written
and read via C, C++, or Fortran library routines which comprise the
Application Programming Interface (API).

%package -n libexoIIv2c
Summary:        ExodusII c library
Group:          Productivity/Scientific/Math

%description -n libexoIIv2c
EXODUS II is a model developed to store and retrieve data for finite element
analyses. It is used for preprocessing (problem definition), postprocessing
(results visualization), as well as code to code data transfer. An EXODUS II
data file is a random access, machine independent, binary file that is written
and read via C, C++, or Fortran library routines which comprise the
Application Programming Interface (API).

This package contains the c library for exodusII.

%package -n libexoIIv2for
Summary:        ExodusII fortran library
Group:          Productivity/Scientific/Math

%description -n libexoIIv2for
EXODUS II is a model developed to store and retrieve data for finite element
analyses. It is used for preprocessing (problem definition), postprocessing
(results visualization), as well as code to code data transfer. An EXODUS II
data file is a random access, machine independent, binary file that is written
and read via C, C++, or Fortran library routines which comprise the
Application Programming Interface (API).

This package contains the fortran library for exodusII.

%package devel
Summary:    Development headers and libraries for exodusII
Group:      Development/Libraries/C and C++

%description devel
EXODUS II is a model developed to store and retrieve data for finite element
analyses. It is used for preprocessing (problem definition), postprocessing
(results visualization), as well as code to code data transfer. An EXODUS II
data file is a random access, machine independent, binary file that is written
and read via C, C++, or Fortran library routines which comprise the
Application Programming Interface (API).

This package contains development headers and libraries for exodusII.

%prep
%setup -n exodus-%{version} -q

%build
cd exodus
mkdir %{_target_platform}
cd %{_target_platform}
%{cmake} \
 -DCMAKE_INSTALL_PREFIX=%{_prefix} \
 -DCMAKE_VERBOSE_MAKEFILE=TRUE \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags}" \
 -DCMAKE_CXX_FLAGS_RELEASE:STRING="%{optflags}" \
 -DCMAKE_BUILD_TYPE=Release \
 -DCMAKE_SKIP_RPATH:BOOL=ON \
 -DBUILD_SHARED=ON \
 ..
make %{?_smp_mflags}

%install
cd exodus
make -C %{_target_platform} install DESTDIR=%{buildroot}
[[ %{_lib} = lib ]] || mv %{buildroot}/%{_prefix}/{lib,%{_lib}}
for i in %{buildroot}/%{_libdir}/lib*.so; do
  mv $i $i.%{version}
  ln -s ${i##*/}.%{version} $i
done
 
%post -n libexoIIv2c -p /sbin/ldconfig
%post -n libexoIIv2for -p /sbin/ldconfig
%postun -n libexoIIv2c -p /sbin/ldconfig
%postun -n libexoIIv2for -p /sbin/ldconfig

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libexoIIv2*.so

%files -n libexoIIv2c
%defattr(-,root,root,-)
%{_libdir}/libexoIIv2c.so.*

%files -n libexoIIv2for
%defattr(-,root,root,-)
%{_libdir}/libexoIIv2for.so.*
 
%changelog
