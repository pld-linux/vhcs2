Summary:	vhcs2 - Professional Control Panel Software
Summary(pl):	vhcs2 - profesjonalny panel kontrolny
Name:		vhcs2
Version:	2.4.7.1
Release:	0.1
# exact license must be checked - Open Source for sure...
License:	GPL ??
Group:		Applications/System
Source0:	http://dl.sourceforge.net/vhcs/%{name}-%{version}.tar.bz2
# Source0-md5:	19d2ddefaa41dd5a6298d3d122af5883
#Source1:	%{name}.conf
#Patch0:		%{name}-config.patch
URL:		http://vhcs.net/
#BuildRequires:	rpmbuild(macros) >= 1.268
#Requires(triggerpostun):	sed >= 4.0
#Requires:	php
#Requires:	php-mysql
#Requires:	php-pcre
#Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
VHCS delivers a complete hosting automation appliance by offering significant security, total-cost-of-ownership, and performance advantages over competing commercial solutions.

With VHCS Pro you can configure your server and applications, create user with domains with a few point-and-click operations that take less than a minute. There is no limit to the number of resellers, users and domains that can be created.At the core of VHCS Pro are 3 easy-to-use, Web-based control panels. VHCS provides graphic user interfaces for the administrators, resellers and users.

%prep
%setup -q

%build
# use sed for setting buildroot

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/{css,lang,libraries/{auth,dbg,dbi,engines,export,import,transformations}}}

#install *.php *.html *.css $RPM_BUILD_ROOT%{_appdir}
#install lang/*.php $RPM_BUILD_ROOT%{_appdir}/lang
#cp -rf themes $RPM_BUILD_ROOT%{_appdir}
#install css/* $RPM_BUILD_ROOT%{_appdir}/css
#install libraries/*.{js,php} $RPM_BUILD_ROOT%{_appdir}/libraries
#install libraries/auth/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/auth
#install libraries/dbg/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/dbg
#install libraries/dbi/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/dbi
#install libraries/engines/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/engines
#install libraries/export/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/export
#install libraries/import/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/import
#install libraries/transformations/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/transformations

#install config.default.php $RPM_BUILD_ROOT%{_sysconfdir}/config.inc.php
#ln -sf %{_sysconfdir}/config.inc.php $RPM_BUILD_ROOT%{_appdir}/config.inc.php

#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf

%clean
rm -rf $RPM_BUILD_ROOT

#%triggerin -- apache1
#%webapp_register apache %{_webapp}

#%triggerun -- apache1
#%webapp_unregister apache %{_webapp}

#%triggerin -- apache >= 2.0.0
#%webapp_register httpd %{_webapp}

#%triggerun -- apache >= 2.0.0
#%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
#%doc Documentation.* CREDITS ChangeLog INSTALL README TODO translators.html scripts
#%dir %attr(750,root,http) %{_sysconfdir}
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
#%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
#%dir %{_appdir}
#%{_appdir}/css
#%{_appdir}/themes
#%{_appdir}/lang
#%{_appdir}/libraries
#%{_appdir}/*.css
#%{_appdir}/*.html
#%{_appdir}/*.php
