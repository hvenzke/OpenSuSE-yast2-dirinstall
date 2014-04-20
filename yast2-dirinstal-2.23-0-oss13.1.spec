# spec file for package yast2-dirinstall
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

#pkg source https://build.opensuse.org/package/binaries/openSUSE:12.3/yast2-dirinstall?repository=standard

# NOTE : yast2-dirinstall are discontinued.
# see notes at https://github.com/yast/yast-dirinstall

# please submit any Bugs at https://github.com/yast/yast-dirinstall


Name:           yast2-dirinstall
Version:        2.23.0
Release:        1_oss13.1

BuildRoot: %{_tmppath}/%{name}-%{version}-build
Source0:        yast2-dirinstall-%{version}.tar.bz2

# Installation::dirinstall_target
# Wizard::SetDesktopTitleAndIcon
Requires:       yast2 >= 2.21.22
# Package-split
Requires:       yast2-packager >= 2.16.3

Requires:       autoyast2-installation
Requires:       yast2
Requires:       yast2-country
Requires:       yast2-runlevel

BuildRequires:  perl-XML-Writer
BuildRequires:  update-desktop-files
BuildRequires:  yast2 >= 2.16.7
BuildRequires:  yast2-devtools
BuildRequires:  yast2-testsuite
# xmllint - for dirinstall.xml validation
BuildRequires:  libxml2
# control.rng - validation schema
BuildRequires:  yast2-installation >= 2.17.44

Provides:       /usr/share/YaST2/clients/dirinstall.ycp

BuildArch:      noarch

Summary:        YaST2 - Installation into Directory
License:        GPL-2.0+
Group:          System/YaST

%description
This package contains scripts for installing a new system into separate
directory.

%prep
%setup -n %{name}-%{version}
%build

autoreconf -fiv

export CFLAGS="$CFLAGS -I%{_libdir}"
export CXXFLAGS="$CFLAGS -I%{_libdir}"
export CFLAGS="$CFLAGS -fpic -DPIC"
export LIBS="-pie -lcdb"
%configure \
        --prefix=%{_prefix} \
        --exec-prefix=%{_sbindir} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir}\
        --datadir=%{_libdir}/%{pkg_name} \
        --sysconfdir=%{_sysconfdir}/%{pkg_name} \
        --localstatedir=%{_localstatedir}/run/%{name} \
        --docdir=%{_docdir}/%{pkg_name}                 \
        --libexecdir=%{_prefix}/lib/

# V=1: verbose build in case we used AM_SILENT_RULES(yes)
# so that RPM_OPT_FLAGS check works
make %{?jobs:-j%jobs} V=1


%install

make install DESTDIR="$RPM_BUILD_ROOT"
[ -e "%{_prefix}/share/YaST2/data/devtools/NO_MAKE_CHECK" ] || Y2DIR="$RPM_BUILD_ROOT/usr/share/YaST2" make check DESTDIR="$RPM_BUILD_ROOT"
for f in `find $RPM_BUILD_ROOT/%{_prefix}/share/applications/YaST2/ -name "*.desktop"` ; do
    d=${f##*/}
    %suse_update_desktop_file -d ycc_${d%.desktop} ${d%.desktop}
done



%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%dir /usr/share/YaST2/include/dirinstall
/usr/share/YaST2/include/dirinstall/*
/usr/share/YaST2/clients/*.ycp
/usr/share/YaST2/modules/*
%{_prefix}/share/applications/YaST2/*.desktop
%dir /usr/share/YaST2/control
/usr/share/YaST2/control/*.xml
%doc %{_prefix}/share/doc/packages/yast2-dirinstall

%changelog

* Sun Apr 20  2014 support@remsnet.de
- rebuild pkg on opensuse 13.1
- removed require mouse ( who needs an Mouse on TEXT CONSOLE ... )
