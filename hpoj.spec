Summary:	HP OfficeJet Linux driver
Summary(pl):	Sterowniki dla urz±dzeñ HP OfficeJet
Name:		hpoj
URL:		http://hpoj.sourceforge.net/
Version:	0.8
Release:	1
License:	GPL
Group:          Applications/Graphics
Source0:	ftp://hpoj.sourceforge.net/download/%{name}-%{version}.tgz
Patch0:		%{name}-ptal-hp.patch
BuildRequires:	qt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The HP OfficeJet Linux driver provides printing and scanning support
for most Hewlett-Packard all-in-one peripherals connected to a
parallel port, USB port, or LAN via selected HP JetDirect print
servers. Additional applications are provided to view the contents of
the front-panel LCD and to access other control and status features of
the device.

It is work in progress, but printing and scanning are supported on
most models, when either connected to the parallel port or USB on a
Linux (Intel or Alpha) workstation, or to a LAN with selected HP
JetDirect print servers.

%description -l pl
Sterowniki dla HP OfficeJet pozwalaj± na drukowanie i skanowanie
na wiêkszo¶ci urz±dzeñ wielofunkcyjnych HP pod³±czonych do:
- portu równoleg³ego,
- portu USB
- sieci poprzez serwer wydruku HP JetDirect.

Dodatkowe aplikacje umo¿liwiaj± dostêp do widoku panela LCD urz±dzenia
i kontrolê jego parametrów.

%prep
%setup -q
%patch -p0

%build
%configure
make etcdir=%{_sysconfdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_initrddir}
%makeinstall etcdir=$RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT/dev/ptal-mlcd
install -d $RPM_BUILD_ROOT/dev/ptal-printd
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
%defattr(644,root,root,755)
%doc  README
%doc doc/*.html
%attr(755,root,root) %{_bindir}/ptal-connect
%attr(755,root,root) %{_bindir}/ptal-print
%attr(755,root,root) %{_bindir}/ptal-devid
%attr(755,root,root) %{_bindir}/ptal-pml
%attr(755,root,root) %{_bindir}/ptal-hp
%attr(755,root,root) %{_bindir}/xojpanel
%attr(755,root,root) %{_sbindir}/ptal-mlcd
%attr(755,root,root) %{_sbindir}/ptal-printd
%attr(755,root,root) %{_sbindir}/ptal-init
%{_includedir}/ptal.h
%{_libdir}/libptal.so*
%config %{_sysconfdir}/ptal-start.conf
%config %{_sysconfdir}/ptal-stop.conf
%{_initrddir}/ptal-init
%dir /dev/ptal-printd
%dir /dev/ptal-mlcd
