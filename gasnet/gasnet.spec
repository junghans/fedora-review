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
BuildRequires:  openmpi
BuildRequires:  openmpi-devel

%description
GASNet is a language-independent, low-level networking layer that provides
network-independent, high-performance communication primitives tailored for
implementing parallel global address space SPMD languages
such as UPC, Titanium, and Co-Array Fortran.

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
%{_openmpi_load}
%configure --enable-udp --enable-mpi CC="gcc -fPIC" CXX="g++ -fPIC"
%make_build MANUAL_CFLAGS="%optflags -fPIC" MANUAL_MPICFLAGS="%optflags -fPIC" MANUAL_CXXFLAGS="%optflags -fPIC"

%install
%make_install
chmod +x %{buildroot}/%{_bindir}/*.pl
sed -i '1s@env @@' %{buildroot}/%{_bindir}/*.pl

#Upstream doesn't want to support shared libs: https://bitbucket.org/berkeleylab/gasnet/pull-requests/36
#but we need it down-stream (legion package)
for l in %{buildroot}/%{_libdir}/*.a; do \
    soname=`basename $l .a`; \
    gcc -shared -Wl,-soname=${soname}-%{version}.so \
        -Wl,--whole-archive ${l} -Wl,--no-whole-archive \
        "$@" -o %{buildroot}/%{_libdir}/${soname}-%{version}.so && \
    ln -s ${soname}-%{version}.so %{buildroot}/%{_libdir}/${soname}.so; \
    rm ${l} ; \
done

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/*
%{_libdir}/lib*-%{version}.so
%doc ChangeLog README README-release README-tools
%license license.txt

%files doc
%{_datadir}/doc/GASNet

%files devel
%doc ChangeLog README-git README-devel
%{_includedir}/*
%{_libdir}/lib*[a-z].so
%{_libdir}/valgrind

%changelog
* Mon Sep 12 2016 Christoph Junghans <junghans@votca.org> - 1.26.4-1
- First release.
