# Compat macros for Sailfish OS releases which don't have newer cmake
# macros
%undefine __cmake_in_source_build
%if 0%{!?cmake_build:1}
%define _vpath_srcdir .
%define _vpath_builddir %{_target_platform}
%define cmake_build \
  mkdir -p %{_vpath_builddir};%__cmake --build "%{__cmake_builddir}" %{?_smp_mflags} --verbose
%define __cmake_builddir %{!?__cmake_in_source_build:%{_vpath_builddir}}%{?__cmake_in_source_build:.}
%endif
%if 0%{!?cmake_install:1}
%define cmake_install \
  DESTDIR="%{buildroot}" %__cmake --install "%{__cmake_builddir}"
%endif


Name: sailfish-voicecall-filter
Version: 0.2
Release: 1
Summary: a voicecall filter plugin for Sailfish OS
License: GPLv2
URL:     https://github.com/dcaliste/sailfish-voicecall-filter
Source0: %{name}-%{version}.tar.gz
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(ofono)
BuildRequires: pkgconfig(mlite5)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(commhistory-qt5) >= 1.12.3
BuildRequires: cmake

%description
Provides a plugin and a daemon to filter received voice
calls based on phone numbers.

%package devel
Summary: Headers for the voicecall filter library
Requires: %{name} = %{version}-%{release}

%description devel
Development headers and library for the voice call filter.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake
%cmake_build

%install
%cmake_install
UNIT_DIR=%{buildroot}%{_userunitdir}/user-session.target.wants
mkdir -p "$UNIT_DIR"
ln -sf ../voicecallfilterd.service "$UNIT_DIR/voicecallfilterd.service"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/*.so.*
%{_datadir}/glib-2.0/schemas/*.xml
%{_libdir}/ofono/plugins/*.so
%config %{_sysconfdir}/dbus-1/system.d/*.conf
%{_bindir}/voicecallfilterd
%{_userunitdir}/*.service
%{_userunitdir}/user-session.target.wants/*.service

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/voicecallfilter
