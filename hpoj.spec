Summary:	HP OfficeJet Linux driver
Summary(pl.UTF-8):   Sterowniki dla urządzeń HP OfficeJet
Name:		hpoj
Version:	0.91
Release:	1
License:	GPL
Group:		Applications/Graphics
Source0:	http://dl.sourceforge.net/hpoj/%{name}-%{version}.tgz
# Source0-md5:	0e083aeab9b00495aa433fa9465456e0
Patch0:		%{name}-opt.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-dirs.patch
Patch3:		%{name}-snmp.patch
URL:		http://hpoj.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	libusb-devel
BuildRequires:	net-snmp-devel
BuildRequires:	qt-devel
Requires(post,preun):	/sbin/chkconfig
Requires(post):	/sbin/ldconfig
Requires:	rc-scripts
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

%description -l pl.UTF-8
Sterowniki dla HP OfficeJet pozwalają na drukowanie i skanowanie
na większości urządzeń wielofunkcyjnych HP podłączonych do:
- portu równoległego,
- portu USB
- sieci poprzez serwer wydruku HP JetDirect.

Dodatkowe aplikacje umożliwiają dostęp do widoku panelu LCD urządzenia
i kontrolę jego parametrów.

%package xojpanel
Summary:	Displays the contents of the device's LCD
Summary(pl.UTF-8):   Wyświetlanie zawartości wyświetlacza urządzenia
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description xojpanel
xojpanel is a graphical Qt-based application that continuously
displays the contents of the LCD (liquid crystal display) on the
device's front panel, for devices which support readback of this
information.

%description xojpanel -l pl.UTF-8
xojpanel to oparta na Qt graficzna aplikacja stale wyświetlająca
zawartość wyświetlacza ciekłokrystalicznego (LCD) umieszczonego
na przednim panelu urządzenia - dla urządzeń, które obsługują
odczyt tych informacji.

%package devel
Summary:	Header files for hpoj libraries
Summary(pl.UTF-8):   Pliki nagłówkowe bibliotek hpoj
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for hpoj libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek hpoj.

%package -n cups-backend-hpoj
Summary:	hpoj backend for CUPS
Summary(pl.UTF-8):   Backend hpoj dla CUPS-a
Group:		Applications/Printing
Requires:	%{name} = %{version}-%{release}
Requires:	cups

%description -n cups-backend-hpoj
hpoj backend for CUPS.

%description -n cups-backend-hpoj -l pl.UTF-8
Backend hpoj dla CUPS-a.

%package -n sane-backend-hpoj
Summary:	hpoj backend for SANE
Summary(pl.UTF-8):   Backend hpoj dla SANE
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	sane-backends

%description -n sane-backend-hpoj
The libsane-hpoj shared library is a SANE backend which supports
scanning on hpoj-supported multi-function peripherals. It implements
the SANE backend API standard and is accessible via any number of
SANE-compliant frontend applications, such as scanimage, xscanimage,
xsane, etc.

%description -n sane-backend-hpoj -l pl.UTF-8
Biblioteka dzielona libsane-hpoj to backend dla SANE obsługujący
skanowanie na urządzeniach wielofunkcyjnych obsługiwanych przez
sterowniki hpoj. Jest implementacją standardu API dla backendów SANE i
jest dostępny z poziomu każdej aplikacji frontendowej zgodnej z SANE,
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
	--with-sane-backend=/usr/%{_lib}/sane \
	--with-sane-etc=/etc/sane.d

# -D... is a workaround for /usr/include/net-snmp/library/getopt.h
%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} -D_GETOPT_H_"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/run/ptal-{mlcd,printd}}

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
%attr(754,root,root) /etc/rc.d/init.d/ptal-init
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
%attr(755,root,root) /usr/lib/cups/backend/ptal

%files -n sane-backend-hpoj
%defattr(644,root,root,755)
%attr(755,root,root) /usr/%{_lib}/sane/libsane-hpoj.so.*
