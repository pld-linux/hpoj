Summary: HP OfficeJet Linux driver
Name: hpoj
URL:http://hpoj.sourceforge.net/
Version: 0.8
Release: 1
Copyright: GPL
Group: System Environment/Daemons
Source: ftp://hpoj.sourceforge.net/download/%{name}-%{version}.tgz
Patch: %{name}-%{version}-ptal-hp.patch
Prereq: /sbin/ldconfig /sbin/chkconfig
BuildPrereq: qt-devel
Prefix: %{_prefix}
BuildRoot: %{_tmppath}/%{name}-root

%description
The HP OfficeJet Linux driver provides printing and scanning support for
most Hewlett-Packard all-in-one peripherals connected to a parallel port,
USB port, or LAN via selected HP JetDirect print servers. Additional
applications are provided to view the contents of the front-panel LCD
and to access other control and status features of the device.

It is work in progress, but printing and scanning are supported on
most models, when either connected to the parallel port or USB on a
Linux (Intel or Alpha) workstation, or to a LAN with selected HP
JetDirect print servers.

%prep
%setup -q
%patch -p0

%build
%configure
make etcdir=%{_sysconfdir}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
%makeinstall etcdir=%{buildroot}%{_sysconfdir}
install -d %{buildroot}/dev/ptal-mlcd
install -d %{buildroot}/dev/ptal-printd
mv %{buildroot}%{_sbindir}/ptal-init %{buildroot}%{_initrddir}/ptal-init
ln -s %{_initrddir}/ptal-init %{buildroot}%{_sbindir}/ptal-init

%post
# Add daemon as a system service
chkconfig --add ptal-init
# Update run-time link bindings
/sbin/ldconfig

%preun
# Remove daemon from system services
/sbin/chkconfig --del ptal-init

%postun
# Update run-time link bindings
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%files
%defattr (-,root,root,-)
%doc COPYING LICENSE README
%doc doc/*.html
%{_bindir}/ptal-connect
%{_bindir}/ptal-print
%{_bindir}/ptal-devid
%{_bindir}/ptal-pml
%{_bindir}/ptal-hp
%{_bindir}/xojpanel
%{_sbindir}/ptal-mlcd
%{_sbindir}/ptal-printd
%{_sbindir}/ptal-init
%{_includedir}/ptal.h
%{_libdir}/libptal.so*
%config /etc/ptal-start.conf
%config /etc/ptal-stop.conf
%{_initrddir}/ptal-init
%dir /dev/ptal-printd
%dir /dev/ptal-mlcd

%changelog
* Fri Aug 10 2001 John L. Chmielewski <jlc@cfl.rr.com>
- spec file cleanup and improvements
- updated discription and summary
- added gcc-3.0 compile patch

* Mon Jul 23 2001 John L. Chmielewski <jlc@cfl.rr.com>
- Updated for 0.8 release

* Tue Dec 20 2000 Timothy Lee <timothy@worldlight.com.hk>
- Added pixmaps to %file section
- %post and %postun scripts now update ld.so.conf

* Tue Dec 20 2000 Timothy Lee <timothy@worldlight.com.hk>
- Updated for 0.7 release
- Added init script and config file for ptal-printd

* Tue Nov 28 2000 Timothy Lee <timothy@worldlight.com.hk>
- First package
- Prepared for 0.6 release
