Name:    spglib
Summary: C library for finding and handling crystal symmetries
Version: 1.9.9
Release: 1%{?dist}
License: BSD
URL:     https://atztogo.github.io/spglib/
Source0: https://github.com/atztogo/spglib/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: autoconf, automake, libtool

%description
C library for finding and handling crystal symmetries.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files for developing
applications that use spglib.

%package -n python3-%{name}
Summary: Python3 library of %{name}
BuildRequires: python3-devel
BuildRequires: python3-numpy
BuildRequires: python3-nose
Requires: python3-numpy
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
This package contains the libraries to 
develop applications with spglib Python3 bindings.

%prep
%setup -q

%build
aclocal
autoheader
libtoolize
touch INSTALL NEWS README AUTHORS
automake -acf
autoconf -v
%configure --disable-static --disable-silent-rules
 
%make_build

pushd python
%py3_build
popd

%install
%make_install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

pushd python
%py3_install
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
pushd python/test
#PYTHONPATH=$RPM_BUILD_ROOT%{python3_sitearch} nosetests-%{python3_version} -v
popd

%files
%doc README AUTHORS
%license COPYING
%{_libdir}/lib*.so.*

%files devel
%{_libdir}/lib*.so
%{_includedir}/spglib/

%files -n python3-%{name}
%license COPYING
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-*.egg-info/

%changelog
* Fri Mar 10 2017 Antonio Trande <sagitter@fedoraproject.org> - 1.9.9-1
- First package
