%define lsbbuild lsb-build-base

# Libraries and pkgconfigs are not usable by regular pkgs
%define _provides_exceptions lib.*so\\|pkgconfig\\(.*\\)

Summary: 	LSB Build environment desktop package
Name: 		lsb-build-desktop
Version: 	3.1.1
Release: 	%mkrel 3
License: 	LGPL
Group: 		Development/C
Source: ftp://ftp.freestandards.org/pub/lsb/lsbdev/released-3.1.0/source/%{name}-%{version}.tar.bz2
URL:		http://www.linuxbase.org/build
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Requires: 	lsb-build-base
BuildRequires:	lsb-build-base lsb-build-cc

%description
This package provides LSB desktop building support for the
lsb-build packages.

%package        -n %{name}-devel
Summary:        LSB Build environment desktop package
Group:          Development/C

%description	-n %{name}-devel
This package provides LSB desktop building support for the
lsb-build packages.

%prep
%setup -q

# (sb) pkconfig all hardcoded to /opt/lsb
# plus libpng*.pc has a typo
sed -i 's|/opt/lsb/include|%{_includedir}/%{lsbbuild}/|g' build_env/stub_libs/pkgconfig*/*
sed -i 's|opt/lsb/include|%{_includedir}/%{lsbbuild}/|g' build_env/stub_libs/pkgconfig*/*
sed -i 's|/opt/lsb/lib|%{_libdir}/%{lsbbuild}/|g' build_env/stub_libs/pkgconfig/*
sed -i 's|/opt/lsb/lib64|%{_libdir}/%{lsbbuild}/|g' build_env/stub_libs/pkgconfig64/*
# (sb) need to fix the Makefile too
sed -i 's|\$(INSTALL_ROOT)/\$(LIBDIR)|\$(INSTALL_ROOT)|g' build_env/stub_libs/Makefile.all-arch
sed -i 's|\$(INSTALL_ROOT)/\$(LIBDIR)|\$(INSTALL_ROOT)|g' build_env/headers/makefile

%build
make CC=lsbcc LSBVERSION=${RPM_PACKAGE_VERSION} LSBLIBCHK_VERSION=${RPM_PACKAGE_VERSION}-${RPM_PACKAGE_RELEASE}

%install
rm -rf $RPM_BUILD_ROOT
pushd build_env/stub_libs
make install-desktop INSTALL_ROOT=$RPM_BUILD_ROOT%{_libdir}/%{lsbbuild}
popd
pushd build_env/headers
make install-desktop INSTALL_ROOT=$RPM_BUILD_ROOT%{_includedir}/%{lsbbuild}
popd

( cd $RPM_BUILD_ROOT%{_libdir}/%{lsbbuild} ; ln -s libpng12.so libpng.so )

# (sb) - make rpmlint happier
chmod -x $RPM_BUILD_ROOT%{_libdir}/%{lsbbuild}/pkgconfig/*.pc

%clean
rm -rf $RPM_BUILD_ROOT

# (sb) lsb-build-desktop has no files
%files -n %{name}-devel
%defattr(-,root,root)
%doc README Licence
%{_libdir}/%{lsbbuild}/*
%{_includedir}/%{lsbbuild}/*

