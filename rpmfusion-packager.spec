Name:           rpmfusion-packager
Version:        0.4
Release:        1%{?dist}
Summary:        Tools for setting up a rpmfusion maintainer environment

Group:          Applications/Productivity
License:        GPLv2+
URL:            http://rpmfusion.org/Package/rpmfusion-packager
Source0:        http://downloads.diffingo.com/rpmfusion/rpmfusion-packager/rpmfusion-packager-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Packager tools
Requires:       rpm-build rpmdevtools rpmlint mock plague-client

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


%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/rpmfusion-packager-setup
%{_bindir}/rpmfusion-*-cvs
%{_bindir}/plague-client-rf


%changelog
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
