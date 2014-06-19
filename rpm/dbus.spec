# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.27
# 

Name:       dbus

# >> macros
%define dbus_user_uid 81
# << macros

Summary:    D-Bus message bus
Version:    1.8.4
Release:    1
Group:      System/Libraries
License:    GPLv2+ or AFL
URL:        http://www.freedesktop.org/software/dbus/
Source0:    %{name}-%{version}.tar.xz
Source1:    dbus-user.socket
Source2:    dbus-user.service
Source100:  dbus.yaml
Patch0:     ensure-machine-id-in-start.patch
Requires:   %{name}-libs = %{version}
Requires(pre): /usr/sbin/useradd
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  expat-devel >= 1.95.5
BuildRequires:  gettext
BuildRequires:  libcap-devel
BuildRequires:  libtool
BuildRequires:  systemd-devel
BuildRequires:  xmlto

%description
D-Bus is a system for sending messages between applications. It is used both
for the systemwide message bus service, and as a per-user-login-session
messaging facility.


%package libs
Summary:    Libraries for accessing D-Bus
Group:      System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
Lowlevel libraries for accessing D-Bus.

%package doc
Summary:    Developer documentation for D-Bus
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description doc
This package contains DevHelp developer documentation for D-Bus along with
other supporting documentation such as the introspect dtd file.


%package devel
Summary:    Libraries and headers for D-Bus
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig

%description devel
Headers and static libraries for D-Bus.

%package x11
Summary:    X11-requiring add-ons for D-Bus
Group:      System/X11
Requires:   %{name} = %{version}-%{release}

%description x11
D-Bus contains some tools that require Xlib to be installed, those are in this
separate package so server systems need not install X.


%prep
%setup -q -n %{name}-%{version}/upstream

# ensure-machine-id-in-start.patch
%patch0 -p1
# >> setup
# << setup

%build
# >> build pre
# << build pre

%reconfigure --disable-static \
    --libexecdir=%{_libdir}/dbus-1 \
    --sysconfdir=%{_sysconfdir} \
    --disable-tests \
    --disable-asserts \
    --disable-xml-docs \
    --disable-doxygen-docs \
    --disable-selinux \
    --disable-libaudit \
    --disable-dnotify \
    --with-system-pid-file=/run/dbus/pid \
    --with-system-socket=/run/dbus/system_bus_socket \
    --with-console-auth-dir=/run/console/ \
    --with-dbus-user=dbus \
    --with-systemdsystemunitdir="%{_libdir}/systemd/system" \
    --enable-systemd \
    --enable-inotify

make %{?_smp_mflags}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
mkdir -p %{buildroot}%{_datadir}/dbus-1/interfaces

mkdir -p %{buildroot}%{_libdir}/systemd/user
install -m0644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/user/dbus.socket
install -m0644 %{SOURCE2} %{buildroot}%{_libdir}/systemd/user/dbus.service

# << install post

%pre
# >> pre
# Add the "dbus" user and group
[ -e /usr/sbin/groupadd ] && /usr/sbin/groupadd -r -g %{dbus_user_uid} dbus 2>/dev/null || :
[ -e /usr/sbin/useradd ] && /usr/sbin/useradd -c 'System message bus' -u %{dbus_user_uid} \
-g %{dbus_user_uid} -s /sbin/nologin -r -d '/' dbus 2> /dev/null || :
# << pre

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/dbus-cleanup-sockets
%{_bindir}/dbus-daemon
%{_bindir}/dbus-monitor
%{_bindir}/dbus-send
%{_bindir}/dbus-uuidgen
%dir %{_sysconfdir}/dbus-1
%config(noreplace) %{_sysconfdir}/dbus-1/session.conf
%dir %{_sysconfdir}/dbus-1/session.d
%config(noreplace) %{_sysconfdir}/dbus-1/system.conf
%dir %{_sysconfdir}/dbus-1/system.d
%dir /%{_prefix}/%{_lib}/dbus-1
%{_libdir}/systemd/user/*
%{_libdir}/systemd/system/dbus.service
%{_libdir}/systemd/system/dbus.socket
%{_libdir}/systemd/system/dbus.target.wants/dbus.socket
%{_libdir}/systemd/system/multi-user.target.wants/dbus.service
%{_libdir}/systemd/system/sockets.target.wants/dbus.socket
%attr(4750,root,dbus) %{_libdir}/dbus-1/dbus-daemon-launch-helper
%dir %{_datadir}/dbus-1
%{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/services
%{_datadir}/dbus-1/system-services
%doc %{_mandir}/man1/dbus-cleanup-sockets.1.gz
%doc %{_mandir}/man1/dbus-daemon.1.gz
%doc %{_mandir}/man1/dbus-monitor.1.gz
%doc %{_mandir}/man1/dbus-send.1.gz
%doc %{_mandir}/man1/dbus-uuidgen.1.gz
%ghost %dir /run/dbus
%dir %{_localstatedir}/lib/dbus
# >> files
# << files

%files libs
%defattr(-,root,root,-)
%{_libdir}/libdbus-1.so.3*
# >> files libs
# << files libs

%files doc
%defattr(-,root,root,-)
%doc doc/dbus-faq.html
%doc doc/dbus-specification.html
%doc doc/dbus-test-plan.html
%doc doc/dbus-tutorial.html
%doc doc/introspect.dtd
%doc doc/introspect.xsl
%doc doc/system-activation.txt
%doc %{_datadir}/doc/dbus/dbus-faq.html
%doc %{_datadir}/doc/dbus/dbus-specification.html
%doc %{_datadir}/doc/dbus/dbus-test-plan.html
%doc %{_datadir}/doc/dbus/dbus-tutorial.html
%doc %{_datadir}/doc/dbus/diagram.png
%doc %{_datadir}/doc/dbus/diagram.svg
%doc %{_datadir}/doc/dbus/system-activation.txt
# >> files doc
# << files doc

%files devel
%defattr(-,root,root,-)
%{_libdir}/libdbus-1.so
%{_includedir}/dbus-1.0/dbus/dbus*.h
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include/dbus/dbus-arch-deps.h
%{_libdir}/pkgconfig/dbus-1.pc
# >> files devel
# << files devel

%files x11
%defattr(-,root,root,-)
%{_bindir}/dbus-launch
%doc %{_mandir}/man1/dbus-launch.1.gz
# >> files x11
# << files x11