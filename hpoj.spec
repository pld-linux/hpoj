Summary:	HP OfficeJet Linux driver
Summary(pl):	Sterowniki dla urz±dzeñ HP OfficeJet
Name:		hpoj
Version:	0.90
Release:	1
License:	GPL
Group:		Applications/Graphics
Source0:	http://dl.sourceforge.net/hpoj/%{name}-%{version}.tgz
# Source0-md5:	dd76385c20bccabf6f5446b1004d8372
Patch0:		%{name}-opt.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-dirs.patch
Patch3:		%{name}-snmp.patch
URL:		http://hpoj.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	net-snmp-devel
BuildRequires:	qt-devel
PreReq:		rc-scripts
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

Dodatkowe aplikacje umo¿liwiaj± dostêp do widoku panelu LCD urz±dzenia
i kontrolê jego parametrów.

%package xojpanel
Summary:	Displays the contents of the device's LCD
Summary(pl):	Wy¶wietlanie zawarto¶ci wy¶wietlacza urz±dzenia
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}

%description xojpanel
xojpanel is a graphical Qt-based application that continuously
displays the contents of the LCD (liquid crystal display) on the
device's front panel, for devices which support readback of this
information.

%description xojpanel -l pl
xojpanel to oparta na Qt graficzna aplikacja stale wy¶wietlaj±ca
zawarto¶æ wy¶wietlacza ciek³okrystalicznego (LCD) umieszczonego
na przednim panelu urz±dzenia - dla urz±dzeñ, które obs³uguj±
odczyt tych informacji.

%package devel
Summary:	Header files for hpoj libraries
Summary(pl):	Pliki nag³ówkowe bibliotek hpoj
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for hpoj libraries.

%description devel -l pl
Pliki nag³ówkowe bibliotek hpoj.

%package -n cups-backend-hpoj
Summary:	hpoj backend for CUPS
Summary(pl):	Backend hpoj dla CUPS-a
Group:		Applications/Printing
Requires:	%{name} = %{version}
Requires:	cups

%description -n cups-backend-hpoj
hpoj backend for CUPS.

%description -n cups-backend-hpoj -l pl
Backend hpoj dla CUPS-a.

%package -n sane-backend-hpoj
Summary:	hpoj backend for SANE
Summary(pl):	Backend hpoj dla SANE
Group:		Applications/System
Requires:	%{name} = %{version}
Requires:	sane-backends

%description -n sane-backend-hpoj
The libsane-hpoj shared library is a SANE backend which supports
scanning on hpoj-supported multi-function peripherals. It implements
the SANE backend API standard and is accessible via any number of
SANE-compliant frontend applications, such as scanimage, xscanimage,
xsane, etc.

%description -n sane-backend-hpoj -l pl
Biblioteka dzielona libsane-hpoj to backend dla SANE obs³uguj±cy
skanowanie na urz±dzeniach wielofunkcyjnych obs³ugiwanych przez
sterowniki hpoj. Jest implementacj± standardu API dla backendów SANE i
jest dostêpny z poziomu ka¿dej aplikacji frontendowej zgodnej z SANE,
takiej jak scanimage, xscanimage, xsane itp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__autoconf}
%configure \
	--with-cups-backend=/usr/lib/cups/backend \
	--with-sane-backend=/usr/lib/sane \
	--with-sane-etc=/etc/sane.d

%{__make} \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_initrddir},/var/run/ptal-{mlcd,printd}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add ptal-init

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del ptal-init
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE* README doc/*.html
%attr(755,root,root) %{_bindir}/hpojip-test
%attr(755,root,root) %{_bindir}/ptal-connect
%attr(755,root,root) %{_bindir}/ptal-device
%attr(755,root,root) %{_bindir}/ptal-devid
%attr(755,root,root) %{_bindir}/ptal-hp
%attr(755,root,root) %{_bindir}/ptal-pml
%attr(755,root,root) %{_bindir}/ptal-print
%attr(755,root,root) %{_sbindir}/ptal-init
%attr(755,root,root) %{_sbindir}/ptal-mlcd
%attr(755,root,root) %{_sbindir}/ptal-photod
%attr(755,root,root) %{_sbindir}/ptal-printd
%attr(755,root,root) %{_libdir}/libhpojip.so.*.*
%attr(755,root,root) %{_libdir}/libptal.so.*.*
%attr(754,root,root) %{_initrddir}/ptal-init
%dir /var/run/ptal-printd
%dir /var/run/ptal-mlcd

%files xojpanel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xojpanel

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhpojip.so
%attr(755,root,root) %{_libdir}/libptal.so
%{_includedir}/hpojip.h
%{_includedir}/ptal.h

%files -n cups-backend-hpoj
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ptal-cups
%attr(755,root,root) %{_libdir}/cups/backend/ptal

%files -n sane-backend-hpoj
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/sane/libsane-hpoj.so.*
