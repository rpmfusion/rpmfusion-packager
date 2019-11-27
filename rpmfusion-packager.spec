%define compdir %(pkg-config --variable=completionsdir bash-completion)
%if "%{compdir}" == ""
%define compdir "/etc/bash_completion.d"
%endif

# rpmfusion-packager switched to python3 on Fedora 30 and RHEL > 7:
%if 0%{?fedora} > 29 || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           rpmfusion-packager
Version:        0.6.6
Release:        1%{?dist}
Summary:        Tools for setting up a rpmfusion maintainer environment

License:        GPLv2+
URL:            https://github.com/rpmfusion-infra/rpmfusion-packager
Source0:        %url/archive/v%{version}/rpmfusion-packager-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  pkgconfig(bash-completion)
%if %{with python3}
BuildRequires:  python3-devel
%else
BuildRequires:  python2-devel
%endif

# Packager tools
Requires:       rpm-build
Requires:       rpmdevtools
Requires:       rpmlint
Requires:       mock
Requires:       rfpkg
Requires:       koji
Requires:       libabigail
Requires:       mock-rpmfusion-free

# Tools required by the scripts included
%if %{with python3}
Requires:       python3-pycurl
%else
Requires:       python-pycurl
%endif

%description
rpmfusion-packager provides a set of utilities designed to help a RPM Fusion
packager in setting up their environment and access the RPM Fusion
infrastructure.


%if %{with python3}
%package     -n python3-rpmfusion-cert
Summary:        Fedora certificate tool and python library
Requires:       python3-pyOpenSSL
Requires:       python3-requests
Requires:       python3-fedora
Requires:       python3-six
Provides:       rpmfusion-cert  = %{version}-%{release}
Obsoletes:      rpmfusion-cert  < %{version}-%{release}

%description -n python3-rpmfusion-cert
Provides rpmfusion-cert and the rpmfusion_cert python3 library
%else
%package     -n rpmfusion-cert
Summary:        Fedora certificate tool and python library
Requires:       pyOpenSSL
Requires:       python2-requests
Requires:       python2-fedora
Requires:       python2-six

%description -n rpmfusion-cert
Provides rpmfusion-cert and the rpmfusion_cert python library
%endif



%prep
%setup -q
autoreconf -i


%build
%if %{with python3}
%configure --with-python3
%else
%configure --with-python2
%endif
%make_build

%install
%make_install


%files
%doc AUTHORS ChangeLog README TODO
%license COPYING
%config(noreplace) %{_sysconfdir}/koji.conf.d/rpmfusion.conf
%{_bindir}/rfabipkgdiff
%{_bindir}/rpmfusion-packager-setup
%{_bindir}/koji-rpmfusion
%{compdir}/

%if %{with python3}
%files -n python3-rpmfusion-cert
%license COPYING
%{_bindir}/rpmfusion-cert
%{python3_sitelib}/rpmfusion_cert
%else
%files -n rpmfusion-cert
%license COPYING
%{_bindir}/rpmfusion-cert
%{python2_sitelib}/rpmfusion_cert
%endif

%changelog
* Wed Nov 27 2019 Sérgio Basto <sergio@serjux.com> - 0.6.6-1
- Fix Python2 with sync with an old version of Fedora-packager

* Thu Oct 03 2019 Sérgio Basto <sergio@serjux.com> - 0.6.5-1
- Add bash completions for koji-rpmfusion command
- Update .gitignore
- Turn off crl certificate check, never worked anyway
- Add bash-completion file to the package

* Sat Aug 24 2019 Leigh Scott <leigh123linux@gmail.com> - 0.6.4-2
- Rebuild for python-3.8

* Thu May 09 2019 Sérgio Basto <sergio@serjux.com> - 0.6.4-1
- Fix input mess

* Thu Mar 28 2019 Sérgio Basto <sergio@serjux.com> - 0.6.3-4
- In Python 3 we need add the b flag

* Thu Mar 28 2019 Sérgio Basto <sergio@serjux.com> - 0.6.3-3
- python3-rpmfusion-cert obsoletes rpmfusion-cert to fix upgrade path

* Mon Mar 25 2019 Sérgio Basto <sergio@serjux.com> - 0.6.3-2
- Revert the sources format to tar.gz, to avoid possible confusion in the future.

* Sun Dec 09 2018 FeRD (Frank Dana) <ferdnyc AT gmail com> - 0.6.3-1
- Port to python3

* Sun Sep 02 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.6.2-3
- Fix python deps for el7

* Sun Sep 02 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.6.2-2
- Use versioned python deps

* Sat Feb 17 2018 Sérgio Basto <sergio@serjux.com> - 0.6.2-1
- Fix a bug with rpmfusion-cert

* Sat Feb 03 2018 Sérgio Basto <sergio@serjux.com> - 0.6.1-1
- Add rpmfusion-cert sub-package

* Tue Apr 25 2017 Sérgio Basto <sergio@serjux.com> - 0.6.0-1
- New release version 0.6.0 .
- Fix one issue with recent koji, by explictely using authtype
  ssl in the rpmfusion.conf config file.
- Remove old CVS scripts (for old rpmfusion infrastruture), cvs requirement
  from rpmfusion-packager package and clean-up cvs scripts from makefile.
- Add rfabipkgdiff script and some requirements to run it.

* Wed Nov 02 2016 Sérgio Basto <sergio@serjux.com> - 0.5.3-1
- Move fas.rpmfusion.org to admin.rpmfusion.org/accounts rfbz#4314

* Wed Sep 14 2016 Sérgio Basto <sergio@serjux.com> - 0.5.2-1
- Use koji-rpmfusion name instead rpmfusion-koji, also koji-rpmfusion is symlink
  of koji and use one koji profile instead use secondary arch script.
- Requires rfpkg instead fedpkg.

* Tue Sep 13 2016 Sérgio Basto <sergio@serjux.com> - 0.5.1-1
- 0.5.1 add rpmfusion-koji and License tag

* Sat Jun 11 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.5.0-1
- Remove plague-client
- Introduce fedpkg and koji dependencies
- Add koji configuration file
- Add some hacks to build.

* Fri Sep 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4-2
- Add Requires mock-rpmfusion-free

* Fri Jun 19 2009 Stewart Adam <s.adam at diffingo.com> - 0.4-1
- Update to 0.4 (configures ~/.plague-client-rpmfusion.cfg)

* Sat Apr 4 2009 Stewart Adam <s.adam at diffingo.com> - 0.3-1
- Update to 0.3 (use pycurl, display cvs output in realtime, add support for 
  anonymous CVS, add plague-client-rf wrapper)

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.2-2
- rebuild for new F11 features

* Sat Feb 28 2009 Stewart Adam <s.adam at diffingo.com> - 0.2-1
- Update to 0.2 (splits rpmfusion-cvs into rpmfusion-{free,nonfree}-cvs)

* Tue Feb 24 2009 Stewart Adam <s.adam at diffingo.com> - 0.1-1
- Initial release based on fedora-packager
