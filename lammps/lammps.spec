%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%else
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

Name:           lammps
Version:        20170706
%global         uversion patch_6Jul2017
Release:        1%{?dist}
Summary:        Molecular Dynamics Simulator
License:        GPLv2
Url:            http://lammps.sandia.gov
Source0:        https://github.com/lammps/lammps/archive/%{uversion}.tar.gz#/%{name}-%{uversion}.tar.gz
#PATCH-FIX-UPSTREAM 573.diff, add cmake build system https://github.com/lammps/lammps/pull/573
Patch0:         https://patch-diff.githubusercontent.com/raw/lammps/lammps/pull/573.diff
#PATCH-FIX-UPSTREAM 594.patch, fix fsf adress https://github.com/lammps/lammps/pull/594
Patch1:         https://patch-diff.githubusercontent.com/raw/lammps/lammps/pull/594.patch
BuildRequires:  fftw-devel
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  openmpi-devel
BuildRequires:  python-devel
BuildRequires:  fftw3-devel
BuildRequires:  zlib-devel
BuildRequires:  gsl-devel
BuildRequires:  cmake
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
LAMMPS is a classical molecular dynamics code, and an acronym for Large-scale 
Atomic/Molecular Massively Parallel Simulator.

LAMMPS has potentials for soft materials (biomolecules, polymers) and 
solid-state materials (metals, semiconductors) and coarse-grained or 
mesoscopic systems. It can be used to model atoms or, more generically, as a 
parallel particle simulator at the atomic, meso, or continuum scale.

LAMMPS runs on single processors or in parallel using message-passing 
techniques and a spatial-decomposition of the simulation domain. The code is 
designed to be easy to modify or extend with new functionality.

%package openmpi
Summary:        LAMMPS Open MPI binaries and libraries
BuildRequires:  openmpi-devel

%description openmpi
LAMMPS is a classical molecular dynamics code, and an acronym for Large-scale 
Atomic/Molecular Massively Parallel Simulator.

LAMMPS has potentials for soft materials (biomolecules, polymers) and 
solid-state materials (metals, semiconductors) and coarse-grained or 
mesoscopic systems. It can be used to model atoms or, more generically, as a 
parallel particle simulator at the atomic, meso, or continuum scale.

LAMMPS runs on single processors or in parallel using message-passing 
techniques and a spatial-decomposition of the simulation domain. The code is 
designed to be easy to modify or extend with new functionality.

This package contains LAMMPS Open MPI binaries and libraries

%package mpich
Summary:        LAMMPS MPICH binaries and libraries
BuildRequires:  mpich-devel

%description mpich
LAMMPS is a classical molecular dynamics code, and an acronym for Large-scale 
Atomic/Molecular Massively Parallel Simulator.

LAMMPS has potentials for soft materials (biomolecules, polymers) and 
solid-state materials (metals, semiconductors) and coarse-grained or 
mesoscopic systems. It can be used to model atoms or, more generically, as a 
parallel particle simulator at the atomic, meso, or continuum scale.

LAMMPS runs on single processors or in parallel using message-passing 
techniques and a spatial-decomposition of the simulation domain. The code is 
designed to be easy to modify or extend with new functionality.

This package contains LAMMPS MPICH binaries and libraries

%package devel
Summary:        Development headers and libraries for LAMMPS
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  mpich-devel
BuildRequires:  openmpi-devel

%description devel
LAMMPS is a classical molecular dynamics code, and an acronym for Large-scale 
Atomic/Molecular Massively Parallel Simulator.

LAMMPS has potentials for soft materials (biomolecules, polymers) and 
solid-state materials (metals, semiconductors) and coarse-grained or 
mesoscopic systems. It can be used to model atoms or, more generically, as a 
parallel particle simulator at the atomic, meso, or continuum scale.

LAMMPS runs on single processors or in parallel using message-passing 
techniques and a spatial-decomposition of the simulation domain. The code is 
designed to be easy to modify or extend with new functionality.

This package contains development headers and libraries for LAMMPS.

%prep
%setup -q -n %{name}-%{uversion}
%patch0 -p1
%patch1 -p1

%build
#python wrapper isn't mpi specific
%global defopts \\\
  -DENABLE_ALL=ON \\\
  -DENABLE_PYTHON=ON \\\
  -DENABLE_TESTING=ON \\\
  -DPYTHON_INST_DIR=%{python_sitearch} \\\
  -DFFT=FFTW3

mkdir -p {serial,mpich,openmpi}
cd openmpi
%{_openmpi_load}
%{cmake} %{defopts} \
  -DENABLE_MPI=ON \
  -DCMAKE_INSTALL_BINDIR=$MPI_BIN \
  -DCMAKE_INSTALL_LIBDIR=$MPI_LIB \
  ../cmake
%make_build
%{_openmpi_unload}
cd ..

cd mpich
%{_mpich_load}
%{cmake} %{defopts} \
  -DENABLE_MPI=ON \
  -DCMAKE_INSTALL_BINDIR=$MPI_BIN \
  -DCMAKE_INSTALL_LIBDIR=$MPI_LIB \
  ../cmake
%make_build
%{_mpich_unload}
cd ..

cd serial
%{cmake} %{defopts} \
  -DENABLE_MPI=OFF \
  ../cmake
%make_build
cd ..

%install
%make_install -C serial
%make_install -C mpich
%make_install -C openmpi

%check
make -C serial %{?_smp_mflags} test
%{_mpich_load}
make -C mpich %{?_smp_mflags} test
%{_mpich_unload}
%{_openmpi_load}
make -C openmpi %{?_smp_mflags} test
%{_openmpi_unload}

# MPI subpackages don't need the ldconfig magic.  They are hidden by
# default, in MPI back-end-specific directory, and only show to the
# user after the relevant environment module has been loaded.
# rpmlint will report that as errors, but it is fine.
%post -n lammps -p /sbin/ldconfig
%postun -n lammps -p /sbin/ldconfig

%files
%doc README
%license LICENSE
%{_bindir}/lmp
%{_libdir}/liblammps.so.*

%files devel
%doc LICENSE
%{_includedir}/lammps.h
%{_libdir}/liblammps.so
%{_libdir}/mpich*/lib/liblammps.so
%{_libdir}/openmpi*/lib/liblammps.so
%{python_sitearch}/%{name}.py*

%files openmpi
%{_libdir}/openmpi*/bin/*
%{_libdir}/openmpi*/lib/liblammps.so.*

%files mpich
%{_libdir}/mpich*/bin/*
%{_libdir}/mpich*/lib/liblammps.so.*

%changelog
* Fri Jul 21 2017 Christoph Junghans <junghans@votca.org> - 20170706-1
- Initial import

