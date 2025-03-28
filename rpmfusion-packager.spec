Name:           rpmfusion-packager
Version:        0.7.2
Release:        11%{?dist}
Summary:        Tools for setting up a rpmfusion maintainer environment

License:        GPLv2+
URL:            https://github.com/rpmfusion-infra/rpmfusion-packager
Source0:        %url/archive/v%{version}/rpmfusion-packager-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  python3-devel

# Packager tools
Requires:       rfpkg
Requires:       koji
%if 0%{?fedora}
Requires:       libabigail-fedora
%else
# EPEL8, ATM, don't have /usr/bin/fedabipkgdiff
# PR proposed: https://src.fedoraproject.org/rpms/libabigail/pull-request/5
#Requires:       libabigail
%endif

# Tools required by the scripts included
Requires:       python3-pycurl
Requires:       python3-rpmfusion-cert

%description
rpmfusion-packager provides a set of utilities designed to help a RPM Fusion
packager in setting up their environment and access the RPM Fusion
infrastructure.


%package     -n python3-rpmfusion-cert
Summary:        Fedora certificate tool and python library
Requires:       python3-pyOpenSSL
Requires:       python3-requests
# need for fedora.client.fas2.AccountSystem
Requires:       python3-rpmfusion
Requires:       python3-six
Provides:       rpmfusion-cert  = %{version}-%{release}
Obsoletes:      rpmfusion-cert  < %{version}-%{release}

%description -n python3-rpmfusion-cert
Provides rpmfusion-cert and the rpmfusion_cert python3 library


%prep
%autosetup -p1
autoreconf -i


%build
%configure --with-python3
%py3_shebang_fix \
  src/rpmfusion-cert.py \
  src/rpmfusion-packager-setup.py
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
%{bash_completions_dir}/

%files -n python3-rpmfusion-cert
%license COPYING
%{_bindir}/rpmfusion-cert
%{python3_sitelib}/rpmfusion_cert

%changelog
* Wed Mar 19 2025 Sérgio Basto <sergio@serjux.com> - 0.7.2-11
- Replace python3-fedora which was removed on rawhide/F42, with python3-rpmfusion

* Sat Feb 01 2025 Sérgio Basto <sergio@serjux.com>
- Drop support to el7 and python2
- Use macro bash_completions_dir

* Tue Dec 24 2024 Nicolas Chauvet <kwizart@gmail.com> - 0.7.2-10
- Mandates rfpkg, use requires instead suggests
  (SB note) maybe recomends is a better choice

* Thu Jun 13 2024 Leigh Scott <leigh123linux@gmail.com> - 0.7.2-9
- Rebuilt for Python 3.13

* Mon Sep 04 2023 Leigh Scott <leigh123linux@gmail.com> - 0.7.2-8
- rpmfusion-packager-setup command requires rpmfusion-cert (rfbz#6760)

* Sat Jul 08 2023 Leigh Scott <leigh123linux@gmail.com> - 0.7.2-7
- Same again

* Sat Jul 08 2023 Leigh Scott <leigh123linux@gmail.com> - 0.7.2-6
- Fix shebang

* Sat Jul 08 2023 Leigh Scott <leigh123linux@gmail.com> - 0.7.2-5
- Rebuilt for Python 3.12

* Tue Jul 26 2022 Sérgio Basto <sergio@serjux.com> - 0.7.2-4
- Only requires rfpkg, rfpkg will requires the rest

* Sat Jun 25 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.2-3
- Rebuilt for Python 3.11

* Tue Jun 15 2021 Leigh Scott <leigh123linux@gmail.com> - 0.7.2-2
- Rebuild for python-3.10

* Tue Nov 24 2020 Sérgio Basto <sergio@serjux.com> 0.7.2-1
- Using https for koji cli configuration

* Sun Nov 22 2020 Sérgio Basto <sergio@serjux.com> - 0.7.1-1
- Drop serverca parameters, it means the koji client will use the system
  certificates, not a given hardcoded one

* Fri Sep 11 2020 Sérgio Basto <sergio@serjux.com> - 0.7.0-1
- Fix the warning that we see with koji 1.22 about browser cert and the related
  ca option in config file, is deprecated and will be removed in koji 1.24,
  references https://pagure.io/koji/issue/2182

* Fri Jul 10 2020 Sérgio Basto <sergio@serjux.com> - 0.6.8-4
- fedabipkgdiff is now in libabigail-fedora package, fedabipkgdiff is needed by
  rfabipkgdiff

* Mon Jul 06 2020 Sérgio Basto <sergio@serjux.com> - 0.6.8-3
- Fix the bin/rfabipkgdiff to work with the new libabigail-fedora

* Sat May 30 2020 Leigh Scott <leigh123linux@gmail.com> - 0.6.8-2
- Rebuild for python-3.9

* Mon Mar 16 2020 Sérgio Basto <sergio@serjux.com> - 0.6.8-1
- If cert expires soon, ask for a new user certificate

* Sun Feb 02 2020 Leigh Scott <leigh123linux@gmail.com> - 0.6.7-2
- Fix cert name

* Thu Nov 28 2019 Sérgio Basto <sergio@serjux.com> - 0.6.7-1
- Finally, all synced from the latest version of fedora-packager-setup which
  used koji certificate for maintainers' authentication
  rpmfusion-packager-setup now will generate the user certificate and overwrite
  server certificate and CA certificate preventing other errors.

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
