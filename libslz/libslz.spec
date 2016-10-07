%global _hardened_build 1

Name:		libslz
Version:	1.1.0
Release:	1%{?dist}
Summary:	StateLess Zip

Group:		System Environment/Libraries
License:	MIT
URL:		http://1wt.eu/projects/libslz/
Source:		http://git.1wt.eu/web?p=%{name}.git;a=snapshot;h=v%{version};sf=tgz#/%{name}-%{version}.tar.gz
Patch:		build.patch
# TODO when upstream is ready
# URL:		http://libslz.org/
# Source:	http://libslz.org/path/to/%{name}-%{version}.tar.gz


%description
SLZ is a fast and memory-less stream compressor which produces an output that
can be decompressed with zlib or gzip. It does not implement decompression at
all, zlib is perfectly fine for this.

The purpose is to use SLZ in situations where a zlib-compatible stream is
needed and zlib's resource usage would be too high while the compression ratio
is not critical. The typical use case is in HTTP servers and gateways which
have to compress many streams in parallel with little CPU resources to assign
to this task, and without having to limit the compression ratio due to the
memory usage. In such an environment, the server's memory usage can easily be
divided by 10 and the CPU usage by 3.


%package devel

Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}


%description devel
Development files for SLZ, the zenc and zdec commands that respectively
compress using SLZ and dump the decoding process.


%prep
%setup -qn %{name}
%patch -p1


%build
%make_build CFLAGS="%{optflags}"


%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
rm %{buildroot}%{_libdir}/*.a


%files
%doc README
%license LICENSE
%{_libdir}/*.so.*


%files devel
%{_libdir}/*.so
%{_bindir}/*
%{_includedir}/*


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%changelog
* Sun Sep 25 2016 - Dridi Boukelmoune <dridi.boukelmoune@gmail.com> - 1.1.0-1
- Initial spec.
