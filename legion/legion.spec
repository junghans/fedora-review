Name:           legion
Version:        16.10.0
Release:        1%{?dist}
Summary:        A data-centric parallel programming system
License:        ASL 2.0
Url:            http://legion.stanford.edu/
Source0:        https://github.com/StanfordLegion/legion/archive/%{name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz

#https://github.com/StanfordLegion/legion/issues/202
ExcludeArch:    aarch64 armv7hl

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

%package devel
Summary:        Development headers and libraries for %{name} library
Requires:       %{name}%{?_isa} = %{version}-%{release}

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

%build
mkdir %{_target_platform}
pushd %{_target_platform}
export LDFLAGS="%{__global_ldflags} -Wl,--as-needed"
%{cmake} .. -DLegion_USE_HWLOC=ON -DLegion_USE_GASNet=ON -DLegion_BUILD_EXAMPLES=ON
%make_build

%install
%make_install -C %{_target_platform}

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
%{_datadir}/Legion

%changelog
* Fri Oct 07 2016 Christoph Junghans <junghans@votca.org> - 16.10.0-1
- initial import

