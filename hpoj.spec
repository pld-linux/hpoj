Summary:	HP OfficeJet Linux driver
Summary(pl):	Sterowniki dla urz±dzeñ HP OfficeJet
Name:		hpoj
Version:	0.8
Release:	1
License:	GPL
Group:          Applications/Graphics
Source0:	ftp://hpoj.sourceforge.net/download/%{name}-%{version}.tgz
# Source0-md5:	225b5b946d4b11a29a051e04df4c825d
Patch0:		%{name}-ptal-hp.patch
URL:		http://hpoj.sourceforge.net/
BuildRequires:	qt-devel
Requires(post,preun):	/sbin/chkconfig
Requires(post):	/sbin/ldconfig
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
%{__make} etcdir=%{_sysconfdir}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_initrddir},/dev/ptal-{mlcd,printd}}

%makeinstall etcdir=$RPM_BUILD_ROOT%{_sysconfdir}

mv -f $RPM_BUILD_ROOT%{_sbindir}/ptal-init $RPM_BUILD_ROOT%{_initrddir}/ptal-init

ln -sf %{_initrddir}/ptal-init $RPM_BUILD_ROOT%{_sbindir}/ptal-init

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add ptal-init
/sbin/ldconfig

%preun
/sbin/chkconfig --del ptal-init

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
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
%config(noreplace) %verify(size mtime md5) %{_sysconfdir}/ptal-start.conf
%config(noreplace) %verify(size mtime md5) %{_sysconfdir}/ptal-stop.conf
%{_initrddir}/ptal-init
%dir /dev/ptal-printd
%dir /dev/ptal-mlcd
