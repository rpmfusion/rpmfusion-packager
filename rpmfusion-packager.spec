Name:           rpmfusion-packager
Version:        0.5.1
Release:        1%{?dist}
Summary:        Tools for setting up a rpmfusion maintainer environment

Group:          Applications/Productivity
License:        GPLv2+
URL:            https://github.com/rpmfusion-infra/rpmfusion-packager
Source0:        https://github.com/rpmfusion-infra/rpmfusion-packager/archive/v%{version}/rpmfusion-packager-%{version}.tar.gz

BuildRequires:  autoconf automake
# Packager tools
Requires:       rpm-build rpmdevtools rpmlint mock
Requires:       fedpkg
Requires:       koji
Requires:       mock-rpmfusion-free

# Tools required by the scripts included
Requires:       python-pycurl cvs

# See FIXME in rpmfusion-cvs
#Requires:       pyOpenSSL

BuildArch:      noarch

%description
rpmfusion-packager provides a set of utilities designed to help a RPM Fusion
packager in setting up their environment and access the RPM Fusion
infrastructure.

%prep
%setup -q
autoreconf -i


%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"


%files
%doc AUTHORS ChangeLog README TODO
%license COPYING
%config(noreplace) %{_sysconfdir}/koji/rpmfusion-config
%{_bindir}/rpmfusion-packager-setup
%{_bindir}/rpmfusion-*-cvs
%{_bindir}/rpmfusion-koji


%changelog
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
