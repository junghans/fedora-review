# The (empty) main package is arch, to have the package built and tests run
# on all arches, but the actual result package is the noarch -devel subpackge.
# Debuginfo packages are disabled to prevent rpmbuild from generating an empty
# debuginfo package for the empty main package.
%global debug_package %{nil}

Name:           cereal
Version:        1.2.1
Release:        0
Summary:        A header-only C++11 serialization library
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++
Url:            http://uscilab.github.io/cereal/
Source0:        https://github.com/USCiLab/cereal/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  cmake

%description
cereal is a header-only C++11 serialization library. cereal takes arbitrary 
data types and reversibly turns them into different representations, such as
compact binary encodings, XML, or JSON. cereal was designed to be fast, 
light-weight, and easy to extend - it has no external dependencies and can be 
easily bundled with other code or used standalone.

%package devel
Summary:        Development headers and libraries for cereal library
Group:          Development/Libraries/C and C++
BuildArch:      noarch

%description devel
cereal is a header-only C++11 serialization library. cereal takes arbitrary 
data types and reversibly turns them into different representations, such as
compact binary encodings, XML, or JSON. cereal was designed to be fast, 
light-weight, and easy to extend - it has no external dependencies and can be 
easily bundled with other code or used standalone.

This package contains development headers and libraries for the cereal library

%prep
%setup -q
sed -i 's/-Werror//' CMakeLists.txt

%build
mkdir %{_target_platform}
cd %{_target_platform}
%{cmake} .. -DSKIP_PORTABILITY_TEST=ON
make %{?_smp_mflags}

%install
make -C %{_target_platform} install DESTDIR=%{buildroot}

%check
#test_portable_binary_archive is broken
make -C %{_target_platform} test ARGS="-V -E test_portable_binary_archive"

%files devel
%doc LICENSE README.md
%{_includedir}/cereal
%{_datadir}/cmake/cereal
