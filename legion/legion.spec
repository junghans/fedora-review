Name:           legion
Version:        16.10.0
Release:        0
Summary:        A data-centric parallel programming system
License:        Apache-2.0
Group:          Productivity/Networking/Other
Url:            http://legion.stanford.edu/
Source0:        https://github.com/StanfordLegion/legion/archive/%{name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz

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
Group:          Development/Libraries/C and C++
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
%{cmake} .. -DLegion_USE_HWLOC=ON -DLegion_USE_GASNet=ON -DLegion_BUILD_EXAMPLES=ON
%make_build

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_datadir}/Legion

%files
%doc README.md CHANGES.txt
%license LICENSE.txt
%{_libdir}/lib*.so.1

%changelog