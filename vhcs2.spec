# TODO:
# - make pl translation
# - move CC ans CFLAGS definition to main Makefile
# - configs should be prepared for PLD
# - finish files section and separate subpackages
# - webapps support
# - generate keys on first start, not on build
# - change manual building and installing with good fixing of their
#   build system
# - use system: Smarty, adodb, not bundled ones
Summary:	vhcs2 - Virtual Hosting Control System
Summary(pl.UTF-8):	vhcs2 - system zarządzania virtualnymi hostami
Name:		vhcs2
Version:	2.4.7.1
Release:	0.6
License:	MPL 1.1
Group:		Applications/System
Source0:	http://dl.sourceforge.net/vhcs/%{name}-%{version}.tar.bz2
# Source0-md5:	19d2ddefaa41dd5a6298d3d122af5883
#Source1:	%{name}.conf
# Oficial patches:
Source10:	http://download.vhcs.net/vhcs_patch_2006-02.05.tar.bz2
# Source10-md5:	851626b3bf10032e191303a60c62ad50
Patch0:		%{name}-mkdirs_location.patch
Patch1:		%{name}-build_flags.patch
Patch2:		%{name}-nostrip_and_noroot.patch
URL:		http://vhcs.net/
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
#Requires(triggerpostun):	sed >= 4.0
#Requires:	php(mysql)
#Requires:	php(pcre)
#Requires:	webapps
#Requires:	webserver(php)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
VHCS delivers a complete hosting automation appliance by offering
significant security, total-cost-of-ownership, and performance
advantages over competing commercial solutions.

With VHCS Pro you can configure your server and applications, create
user with domains with a few point-and-click operations that take less
than a minute. There is no limit to the number of resellers, users and
domains that can be created. At the core of VHCS Pro are 3
easy-to-use, Web-based control panels. VHCS provides graphic user
interfaces for the administrators, resellers and users.

%description -l pl.UTF-8
VHCS dostarcza pełne rozwiązanie do automatycznego hostingu oferując
znacząco lepsze bezpieczeństwo, całkowity koszt wykorzystywania i
wydajność niż konkurencyjne rozwiązania komercyjne.

Przy użyciu VHCS Pro można skonfigurować serwer i aplikacje, stworzyć
użytkownika z domenami za pomocą kilku kliknięć w czasie poniżej
minuty. Nie ma ograniczeń co do liczby pośredników, użytkowników i
tworzonych domen. Sercem VHCS Pro są 3 łatwe w użyciu, oparte na WWW
panele sterowania. VHCS udostępnia graficzne interfejsy użytkownika
dla administratorów, pośredników i użytkowników.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

tar -jxvf %{SOURCE10}
mv vhcs_patch_2006-02-05/gui/include/login.php gui/include/login.php

%build
%{__make} -C tools/daemon vhcs2_daemon \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -ansi -Wall -Wstrict-prototypes -pedantic"

%{__make} -C keys gen-keys \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -ansi -Wall -Wstrict-prototypes -pedantic"

# Docs:
mv -f language-files/README.txt README_language-files.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_sbindir},/var/log/{%{name},archive/httpd}} \
	$RPM_BUILD_ROOT{/var/{lib/%{name},mail/virtual},/etc/init.d} \
	$RPM_BUILD_ROOT%{_appdir}/{gui,engine/{backup,quota,traffic,messager,setup,tools}}

# helper script - needed for building:
install tools/build/vhcs2-mkdirs.pl $RPM_BUILD_ROOT%{_sbindir}

# daemon binary:
install tools/daemon/vhcs2_daemon $RPM_BUILD_ROOT%{_sbindir}

# TODO: install config files!

# init-scripts for daemons:
install configs/init.d/vhcs2_{daemon,network} $RPM_BUILD_ROOT/etc/init.d

###############
### ENGINE:
# Some scripts:
install engine/traffic/maillogconvert/maillogconvert.pl $RPM_BUILD_ROOT%{_sbindir}
install engine/vhcs2_common_code.pl $RPM_BUILD_ROOT%{_appdir}/engine
install engine/vhcs2-db-keys.pl $RPM_BUILD_ROOT%{_appdir}/engine
install engine/vhcs2-db-keys.pl $RPM_BUILD_ROOT%{_appdir}/engine/messager
install engine/*-mngr $RPM_BUILD_ROOT%{_appdir}/engine
install engine/vhcs2-db-passwd $RPM_BUILD_ROOT%{_appdir}/engine
# Backup scripts:
install engine/backup/vhcs2-bk-task $RPM_BUILD_ROOT%{_appdir}/engine/backup
install engine/backup/vhcs2-backup-all $RPM_BUILD_ROOT%{_appdir}/engine/tools
# Quota script:
install engine/quota/vhcs2-dsk-quota $RPM_BUILD_ROOT%{_appdir}/engine/quota

install engine/traffic/*traff{,-SUSE} $RPM_BUILD_ROOT%{_appdir}/engine/traffic

install engine/messager/*-msgr $RPM_BUILD_ROOT%{_appdir}/engine/messager

# Setup and administration tools:
install engine/setup/{*.sh,*setup} $RPM_BUILD_ROOT%{_appdir}/engine/setup
install engine/tools/vhcs2-httpd-logs-mngr $RPM_BUILD_ROOT%{_appdir}/engine/tools

###############
## GUI:
install gui/*.php $RPM_BUILD_ROOT%{_appdir}/gui
cp -dR gui/{admin,reseller,client,include} $RPM_BUILD_ROOT%{_appdir}/gui
rm -f $RPM_BUILD_ROOT%{_appdir}/gui/{admin,reseller,client,include}/Makefile
cp -dR gui/{domain_default_page,errordocs,images,themes,tools,orderpanel} $RPM_BUILD_ROOT%{_appdir}/gui

#%{__make} install \
#	CC="%{__cc}" \
#	CFLAGS="%{rpmcflags} -ansi -Wall -Wstrict-prototypes -pedantic" \
#	INST_PREF=$RPM_BUILD_ROOT \
#	SYSTEM_ROOT=$RPM_BUILD_ROOT%{_appdir} \
#	SYSTEM_MAKE_DIRS=$RPM_BUILD_ROOT%{_sbindir}/vhcs2-mkdirs.pl \
#	SYSTEM_APACHE_BACK_LOG=$RPM_BUILD_ROOT/var/log/archive/httpd \
#	CMD_INSTALL="install" \
#	CMD_MAIL_INSTALL="install" \
#	CMD_DIR_INSTALL="install -d"

#install config.default.php $RPM_BUILD_ROOT%{_sysconfdir}/config.inc.php
#ln -sf %{_sysconfdir}/config.inc.php $RPM_BUILD_ROOT%{_appdir}/config.inc.php

#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf

%clean
rm -rf $RPM_BUILD_ROOT

#%triggerin -- apache1 < 1.3.37-3, apache1-base
#%webapp_register apache %{_webapp}

#%triggerun -- apache1 < 1.3.37-3, apache1-base
#%webapp_unregister apache %{_webapp}

#%triggerin -- apache < 2.2.0, apache-base
#%webapp_register httpd %{_webapp}

#%triggerun -- apache < 2.2.0, apache-base
#%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CHANGELOG README* docs/{Changes*,HOWTO*,README}
#%doc Documentation.* CREDITS ChangeLog INSTALL README TODO translators.html scripts
#%dir %attr(750,root,http) %{_sysconfdir}
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
#%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%dir %{_appdir}
%dir %{_appdir}/engine
%attr(750,root,http) %{_appdir}/engine/vhcs2*
%dir %attr(750,root,http) %{_appdir}/engine/backup
%attr(750,root,http) %{_appdir}/engine/backup/*
%dir %attr(750,root,http) %{_appdir}/engine/quota
%attr(750,root,http) %{_appdir}/engine/quota/*
%dir %attr(750,root,http) %{_appdir}/engine/setup
%attr(750,root,http) %{_appdir}/engine/setup/*
%dir %attr(750,root,http) %{_appdir}/engine/tools
%attr(750,root,http) %{_appdir}/engine/tools/*
%dir %attr(750,root,http) %{_appdir}/engine/traffic
%attr(750,root,http) %{_appdir}/engine/traffic/*
%dir %attr(750,root,http) %{_appdir}/engine/messager
%attr(750,root,http) %{_appdir}/engine/messager/*
# GUI to separate package:
%dir %attr(750,root,http) %{_appdir}/gui
%{_appdir}/gui/*.php
%{_appdir}/gui/domain_default_page
%{_appdir}/gui/errordocs
%{_appdir}/gui/images
%{_appdir}/gui/include
%dir %attr(750,root,http) %{_appdir}/gui/themes
%{_appdir}/gui/themes/blue
%{_appdir}/gui/themes/modern_blue
%dir %attr(750,root,http) %{_appdir}/gui/tools

## Admin panel GUI:
%dir %attr(750,root,http) %{_appdir}/gui/admin
%{_appdir}/gui/admin/*.php

## Client panel GUI:
%dir %attr(750,root,http) %{_appdir}/gui/client
%{_appdir}/gui/client/*.php

## Orderpanel GUI:
%dir %attr(750,root,http) %{_appdir}/gui/orderpanel
%attr(750,root,http) %{_appdir}/gui/orderpanel/*.php

## Reseller GUI:
%dir %attr(750,root,http) %{_appdir}/gui/reseller
%attr(750,root,http) %{_appdir}/gui/reseller/*.php

## Filemanager:
%dir %attr(750,root,http) %{_appdir}/gui/tools/filemanager
%dir %attr(750,root,http) %{_appdir}/gui/tools/filemanager/tools
%{_appdir}/gui/tools/filemanager/images
%dir %attr(750,root,http) %{_appdir}/gui/tools/filemanager/lang
%{_appdir}/gui/tools/filemanager/lang/*
%{_appdir}/gui/tools/filemanager/tools/helpdesk
%{_appdir}/gui/tools/filemanager/tools/*.php
%{_appdir}/gui/tools/filemanager/themes
%{_appdir}/gui/tools/filemanager/viewers
%{_appdir}/gui/tools/filemanager/*.php

## PMA:
%dir %attr(750,root,http) %{_appdir}/gui/tools/pma
%{_appdir}/gui/tools/pma/*.php
%{_appdir}/gui/tools/pma/css
%dir %attr(750,root,http) %{_appdir}/gui/tools/pma/lang
# Mark it as separate langs:
%{_appdir}/gui/tools/pma/lang/*.php
%{_appdir}/gui/tools/pma/libraries
%{_appdir}/gui/tools/pma/scripts
%dir %attr(750,root,http) %{_appdir}/gui/tools/pma/themes
%{_appdir}/gui/tools/pma/themes/darkblue_orange
%{_appdir}/gui/tools/pma/themes/original

# Everything for webmail:
%dir %attr(750,root,http) %{_appdir}/gui/tools/webmail
%{_appdir}/gui/tools/webmail/*.php
%{_appdir}/gui/tools/webmail/database
%{_appdir}/gui/tools/webmail/images
%{_appdir}/gui/tools/webmail/inc
%dir %attr(750,root,http) %{_appdir}/gui/tools/webmail/langs
# Mark it as separate langs:
%{_appdir}/gui/tools/webmail/langs/*.txt
# Use separate Smarty, not bundled:
%{_appdir}/gui/tools/webmail/smarty
%dir %attr(750,root,http) %{_appdir}/gui/tools/webmail/themes
%{_appdir}/gui/tools/webmail/themes/basic
%{_appdir}/gui/tools/webmail/themes/blue
%{_appdir}/gui/tools/webmail/themes/classic
%{_appdir}/gui/tools/webmail/themes/green
%{_appdir}/gui/tools/webmail/themes/hungi.mozilla
%{_appdir}/gui/tools/webmail/themes/modern_blue
%{_appdir}/gui/tools/webmail/themes/red
%{_appdir}/gui/tools/webmail/themes/yellow
