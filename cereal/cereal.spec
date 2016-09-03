Name:           cereal
Version:        1.2.1
Release:        2%{?dist}
Summary:        A header-only C++11 serialization library
License:        BSD
Url:            http://uscilab.github.io/cereal/
Source0:        https://github.com/USCiLab/cereal/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

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
Summary:        Development headers and libraries for %{name}

%description devel
cereal is a header-only C++11 serialization library. cereal takes arbitrary 
data types and reversibly turns them into different representations, such as
compact binary encodings, XML, or JSON. cereal was designed to be fast, 
light-weight, and easy to extend - it has no external dependencies and can be 
easily bundled with other code or used standalone.

This package contains development headers and libraries for the cereal library

%prep
%setup -q
#https://github.com/USCiLab/cereal/pull/337
sed -i 's/-Werror//' CMakeLists.txt

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake} .. -DSKIP_PORTABILITY_TEST=ON
%make_build 

%install
%make_install -C %{_target_platform}

%check
#test_portable_binary_archive is broken
#https://github.com/USCiLab/cereal/issues/338
make -C %{_target_platform} test ARGS="-V -E test_portable_binary_archive"

%files devel
%doc README.md
%license LICENSE
%{_includedir}/%{name}
%dir %{_datadir}/cmake
%{_datadir}/cmake/%{name}

%changelog
* Sat Sep 03 2016 Christoph Junghans <junghans@votca.org> - 6.02-2
- Minor changes from review (bug #1372403)

* Thu Sep 01 2016 Christoph Junghans <junghans@votca.org> - 1.2.1-1
- First release.
