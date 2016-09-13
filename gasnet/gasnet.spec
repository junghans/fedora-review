Name:           gasnet
Version:        1.26.4
Release:        1%{?dist}
Summary:        A Portable High-Performance Communication Layer for GAS Languages
License:        PostgreSQL
Url:            https://bitbucket.org/berkeleylab/gasnet/
Source0:        https://bitbucket.org/berkeleylab/gasnet/downloads/GASNet-%{version}.tar.gz
# PATCH-FIX-UPSTREAM - ef402803a4791dd73792042a886e9c3fb0989d17.patch - Support overwriting of flags, see https://bitbucket.org/berkeleylab/gasnet/pull-requests/34
Patch0:         https://bitbucket.org/berkeleylab/gasnet/commits/ef402803a4791dd73792042a886e9c3fb0989d17/raw#/ef402803a4791dd73792042a886e9c3fb0989d17.patch
BuildRequires:  automake
BuildRequires:  gcc-c++
Requires:       %{name}-common = %{version}-%{release}

%description
GASNet is a language-independent, low-level networking layer that provides
network-independent, high-performance communication primitives tailored for
implementing parallel global address space SPMD languages
such as UPC, Titanium, and Co-Array Fortran.

%package common
Summary:        GASNet Open MPI binaries and libraries 

%description common
GASNet is a language-independent, low-level networking layer that provides
network-independent, high-performance communication primitives tailored for
implementing parallel global address space SPMD languages
such as UPC, Titanium, and Co-Array Fortran.

GASNet files shared between serial and parallel versions

%package openmpi
Summary:        GASNet Open MPI binaries and libraries 
Requires:       %{name}-common = %{version}-%{release}
BuildRequires:  openmpi-devel

%description openmpi
GASNet is a language-independent, low-level networking layer that provides
network-independent, high-performance communication primitives tailored for
implementing parallel global address space SPMD languages
such as UPC, Titanium, and Co-Array Fortran.

GASNet compiles with Open MPI, package incl. binaries and libraries

%package mpich
Summary:        GASNet Open MPI binaries and libraries 
Requires:       %{name}-common = %{version}-%{release}
BuildRequires:  mpich-devel

%description mpich
GASNet is a language-independent, low-level networking layer that provides
network-independent, high-performance communication primitives tailored for
implementing parallel global address space SPMD languages
such as UPC, Titanium, and Co-Array Fortran.

GASNet compiles with MPICH, package incl. binaries and libraries

%package devel
Summary:        Development package for GASNet
Requires:       %{name} = %{version}

%description devel
GASNet is a language-independent, low-level networking layer that provides
network-independent, high-performance communication primitives tailored for
implementing parallel global address space SPMD languages
such as UPC, Titanium, and Co-Array Fortran.

Development package for GASNet. Including header files and libraries.

%package doc
Summary:        Documentation package for GASNet
BuildArch:      noarch

%description doc
GASNet is a language-independent, low-level networking layer that provides
network-independent, high-performance communication primitives tailored for
implementing parallel global address space SPMD languages
such as UPC, Titanium, and Co-Array Fortran.

Documentation package for GASNet.

%prep
%setup -q -n GASNet-%{version}
%patch0 -p1
./Bootstrap -y

%build
mkdir serial openmpi mpich
%global dconfigure %(printf %%s '%configure' | sed 's!\./configure!../configure!g')

pushd serial
%dconfigure --enable-udp --disable-mpi CC="gcc -fPIC" CXX="g++ -fPIC"
%make_build MANUAL_CFLAGS="%optflags -fPIC" MANUAL_MPICFLAGS="%optflags -fPIC" MANUAL_CXXFLAGS="%optflags -fPIC"
popd

pushd openmpi
%{_openmpi_load}
%dconfigure --enable-udp --enable-mpi --bindir="${MPI_BIN}"  --includedir="${MPI_INCLUDE}" --libdir="${MPI_LIB}" CC="gcc -fPIC" CXX="g++ -fPIC"
%make_build MANUAL_CFLAGS="%optflags -fPIC" MANUAL_MPICFLAGS="%optflags -fPIC" MANUAL_CXXFLAGS="%optflags -fPIC"
%{_openmpi_unload}
popd

pushd mpich
%{_mpich_load}
%dconfigure --enable-udp --enable-mpi --bindir="${MPI_BIN}"  --includedir="${MPI_INCLUDE}" --libdir="${MPI_LIB}" CC="gcc -fPIC" CXX="g++ -fPIC"
%make_build MANUAL_CFLAGS="%optflags -fPIC" MANUAL_MPICFLAGS="%optflags -fPIC" MANUAL_CXXFLAGS="%optflags -fPIC"
%{_mpich_unload}
popd

%install
%make_install -C serial
%make_install -C openmpi
%make_install -C mpich

#shared between serial and parallel
rm -f %{_libdir}/*mpi*/bin/gasnet_trace

chmod +x %{buildroot}/%{_bindir}/*.pl
sed -i '1s@env @@' %{buildroot}/%{_bindir}/*.pl

#Upstream doesn't want to support shared libs: https://bitbucket.org/berkeleylab/gasnet/pull-requests/36
#but we need it down-stream (legion package)
for l in %{buildroot}/%{_libdir}/*.a %{buildroot}/%{_libdir}/*/lib/*.a; do \
    soname=`basename $l .a`; \
    libdir=`dirname $l`; \
    gcc -shared -Wl,-soname=${soname}-%{version}.so \
        -Wl,--whole-archive ${l} -Wl,--no-whole-archive \
        "$@" -o ${libdir}/${soname}-%{version}.so && \
    ln -s ${soname}-%{version}.so ${libdir}/${soname}.so; \
    rm ${l} ; \
done

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/amudprun
%{_libdir}/lib*-%{version}.so
%doc ChangeLog README README-release README-tools
%license license.txt

%files common
%{_bindir}/gasnet_trace*

%files openmpi
%{_libdir}/openmpi*/bin/*
%{_libdir}/openmpi*/lib/lib*-%{version}.so

%files mpich
%{_libdir}/mpich*/bin/*
%{_libdir}/mpich*/lib/lib*-%{version}.so

%files doc
%{_datadir}/doc/GASNet

%files devel
%doc ChangeLog README-git README-devel
%{_includedir}/*.h
%{_includedir}/*.mk
%{_includedir}/*-conduit
%{_libdir}/lib*[a-z].so
%{_libdir}/valgrind
%{_includedir}/openmpi-*/*
%{_libdir}/openmpi*/lib/lib*[a-z].so
%{_libdir}/openmpi*/lib/valgrind
%{_includedir}/mpich-*/*
%{_libdir}/mpich*/lib/lib*[a-z].so
%{_libdir}/mpich*/lib/valgrind

%changelog
* Mon Sep 12 2016 Christoph Junghans <junghans@votca.org> - 1.26.4-1
- First release.
