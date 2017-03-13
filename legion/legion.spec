Name:           legion
Version:        17.02.0
Release:        1%{?dist}
Summary:        A data-centric parallel programming system
License:        ASL 2.0
Url:            http://legion.stanford.edu/
Source0:        https://github.com/StanfordLegion/legion/archive/%{name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
# PATCH-FIX-UPSTREAM - 229.patch -  add make test to cmake build system
Patch0:         https://patch-diff.githubusercontent.com/raw/StanfordLegion/legion/pull/229.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  hwloc-devel
BuildRequires:  gasnet-devel
BuildRequires:  cmake

%description
Legion is a data-centric parallel programming system for writing portable
high performance programs targeted at distributed heterogeneous architectures.
Legion presents abstractions which allow programmers to describe properties of
program data (e.g. independence, locality). By making the Legion programming
system aware of the structure of program data, it can automate many of the
tedious tasks programmers currently face, including correctly extracting task-
and data-level parallelism and moving data around complex memory hierarchies.
A novel mapping interface provides explicit programmer controlled placement of
data in the memory hierarchy and assignment of tasks to processors in a way that
is orthogonal to correctness, thereby enabling easy porting and tuning of Legion
applications to new architectures.

%package openmpi
Summary:        Legion Open MPI binaries and libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  openmpi-devel

%description openmpi
Legion is a data-centric parallel programming system for writing portable
high performance programs targeted at distributed heterogeneous architectures.
Legion presents abstractions which allow programmers to describe properties of
program data (e.g. independence, locality). By making the Legion programming
system aware of the structure of program data, it can automate many of the
tedious tasks programmers currently face, including correctly extracting task-
and data-level parallelism and moving data around complex memory hierarchies.
A novel mapping interface provides explicit programmer controlled placement of
data in the memory hierarchy and assignment of tasks to processors in a way that
is orthogonal to correctness, thereby enabling easy porting and tuning of Legion
applications to new architectures.

Legion compiled with Open MPI, package incl. binaries and libraries

%package mpich
Summary:        Legion MPICH binaries and libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  mpich-devel

%description mpich
Legion is a data-centric parallel programming system for writing portable
high performance programs targeted at distributed heterogeneous architectures.
Legion presents abstractions which allow programmers to describe properties of
program data (e.g. independence, locality). By making the Legion programming
system aware of the structure of program data, it can automate many of the
tedious tasks programmers currently face, including correctly extracting task-
and data-level parallelism and moving data around complex memory hierarchies.
A novel mapping interface provides explicit programmer controlled placement of
data in the memory hierarchy and assignment of tasks to processors in a way that
is orthogonal to correctness, thereby enabling easy porting and tuning of Legion
applications to new architectures.

Legion compiled with MPICH, package incl. binaries and libraries

%package devel
Summary:        Development headers and libraries for %{name} library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-openmpi%{?_isa} = %{version}
Requires:       %{name}-mpich%{?_isa} = %{version}
Requires:       mpich-devel
Requires:       openmpi-devel

%description devel
Legion is a data-centric parallel programming system for writing portable
high performance programs targeted at distributed heterogeneous architectures.
Legion presents abstractions which allow programmers to describe properties of
program data (e.g. independence, locality). By making the Legion programming
system aware of the structure of program data, it can automate many of the
tedious tasks programmers currently face, including correctly extracting task-
and data-level parallelism and moving data around complex memory hierarchies.
A novel mapping interface provides explicit programmer controlled placement of
data in the memory hierarchy and assignment of tasks to processors in a way that
is orthogonal to correctness, thereby enabling easy porting and tuning of Legion
applications to new architectures.

This package contains development headers and libraries for the legion library

%prep
%setup -q -n %{name}-%{name}-%{version}
%patch0 -p1

%build
mkdir serial openmpi mpich

pushd serial
export LDFLAGS="%{__global_ldflags} -Wl,--as-needed"
%{cmake} .. -DLegion_USE_HWLOC=ON -DLegion_USE_GASNet=OFF -DLegion_BUILD_EXAMPLES=ON -DLegion_BUILD_TESTS=ON -DLegion_BUILD_TUTORIAL=ON \
  -DLegion_BUILD_TESTS=ON -DLegion_BUILD_TUTORIAL=ON -DLegion_ENABLE_TESTING=ON
%make_build
popd

pushd openmpi
%{_openmpi_load}
export LDFLAGS="%{__global_ldflags} -Wl,--as-needed"
%{cmake} .. -DLegion_USE_HWLOC=ON -DLegion_USE_GASNet=ON -DLegion_BUILD_EXAMPLES=ON -DCMAKE_INSTALL_LIBDIR=${MPI_LIB} -DGASNet_CONDUIT=mpi \
  -DGASNet_mpi-par_LIBRARY=${MPI_LIB}/libgasnet-mpi-par.so -DGASNet_gasnet_tools-par_LIBRARY=$MPI_LIB/libgasnet_tools-par.so -DGASNet_INCLUDE_DIR=$MPI_INCLUDE \
  -DLegion_BUILD_TESTS=ON -DLegion_BUILD_TUTORIAL=ON -DLegion_ENABLE_TESTING=ON
%make_build
%{_openmpi_unload}
popd

pushd mpich
%{_mpich_load}
export LDFLAGS="%{__global_ldflags} -Wl,--as-needed"
%{cmake} .. -DLegion_USE_HWLOC=ON -DLegion_USE_GASNet=ON -DLegion_BUILD_EXAMPLES=ON -DCMAKE_INSTALL_LIBDIR=${MPI_LIB} -DGASNet_CONDUIT=mpi \
  -DGASNet_mpi-par_LIBRARY=${MPI_LIB}/libgasnet-mpi-par.so -DGASNet_gasnet_tools-par_LIBRARY=$MPI_LIB/libgasnet_tools-par.so -DGASNet_INCLUDE_DIR=$MPI_INCLUDE \
  -DLegion_BUILD_TESTS=ON -DLegion_BUILD_TUTORIAL=ON -DLegion_ENABLE_TESTING=ON
%make_build
%{_mpich_unload}
popd

%install
%make_install -C serial
%{_openmpi_load}
%make_install -C openmpi
%{_openmpi_unload}
%{_mpich_load}
%make_install -C mpich
%{_mpich_unload}

%check
make -C serial test
%{_openmpi_load}
make -C openmpi test
%{_openmpi_unload}
%{_mpich_load}
make -C mpich test
%{_mpich_unload}

#move cmake files in a place where cmake can find them
mkdir -p %{buildroot}%{_libdir}/cmake
mv %{buildroot}{%{_datadir}/Legion,%{_libdir}/cmake/legion}

# MPI subpackages don't need the ldconfig magic.  They are hidden by
# default, in MPI back-end-specific directory, and only show to the
# user after the relevant environment module has been loaded.
# rpmlint will report that as errors, but it is fine.
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md CHANGES.txt
%license LICENSE.txt
%{_libdir}/lib*.so.1

%files devel
%{_includedir}/*.h
%{_includedir}/*.inl
%{_includedir}/legion
%{_includedir}/mappers
%{_includedir}/realm
%{_libdir}/lib*.so
%{_libdir}/openmpi*/lib/lib*.so
%{_libdir}/mpich*/lib/lib*.so
%{_libdir}/cmake/legion

%files openmpi
%{_libdir}/openmpi*/lib/lib*.so.1

%files mpich
%{_libdir}/mpich*/lib/lib*.so.1

%changelog
* Fri Feb 24 2017 Christoph Junghans <junghans@votca.org> - 17.02.0-1
- initial import

