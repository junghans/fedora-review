Name:           libaec
Version:        1.0.0
Release:        1%{?dist}
Summary:        Adaptive Entropy Coding library
License:        BSD
Url:            https://gitlab.dkrz.de/k202009/libaec
Source:         https://gitlab.dkrz.de/k202009/libaec/uploads/631e85bcf877c2dcaca9b2e6d6526339/libaec-1.0.0.tar.gz

BuildRequires:  cmake

%description
Libaec provides fast loss-less compression of 1 up to 32 bit wide
signed or unsigned integers (samples). The library achieves best
results for low entropy data as often encountered in space imaging
instrument data or numerical model output from weather or climate
simulations. While floating point representations are not directly
supported, they can also be efficiently coded by grouping exponents
and mantissa.

Libaec implements Golomb Rice coding as defined in the Space Data
System Standard documents 121.0-B-2 and 120.0-G-2.

Libaec includes a free drop-in replacement for the SZIP
library (http://www.hdfgroup.org/doc_resource/SZIP).

%package devel
Summary:        Devel package for libaec (Adaptive Entropy Coding library)
Requires:       libaec

%description devel
Devel files and static library for libaec (Adaptive Entropy Coding library).

%prep
%setup -q

%build
mkdir build
pushd build
%cmake ..
%make_build
popd

%install
%make_install -C build
[ %{_lib} = lib ] || mv $RPM_BUILD_ROOT/%{_prefix}/{lib,%{_lib}}

%check
make -C build test 

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README README.SZIP ChangeLog
%license COPYING doc/patent.txt
%{_bindir}/aec
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/lib*.so

%changelog
* Mon Mar 13 2017 Christoph Junghans <junghans@votca.org> - 1.0.0-1
- initial import
