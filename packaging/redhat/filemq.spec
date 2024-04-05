#
#    filemq - A FileMQ server and client
#
#    Copyright (c) the Contributors as noted in the AUTHORS file.
#    This file is part of FileMQ, a C implemenation of the protocol:
#    https://github.com/danriegsecker/filemq2.
#
#    This Source Code Form is subject to the terms of the Mozilla Public
#    License, v. 2.0. If a copy of the MPL was not distributed with this
#    file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

# To build with draft APIs, use "--with drafts" in rpmbuild for local builds or add
#   Macros:
#   %_with_drafts 1
# at the BOTTOM of the OBS prjconf
%bcond_with drafts
%if %{with drafts}
%define DRAFTS yes
%else
%define DRAFTS no
%endif

# build with python_cffi support enabled
%bcond_with python_cffi
%if %{with python_cffi}
%define py2_ver %(python2 -c "import sys; print ('%d.%d' % (sys.version_info.major, sys.version_info.minor))")
%endif

# build with python3_cffi support enabled
%bcond_with python3_cffi
%if %{with python3_cffi}
%define py3_ver %(python3 -c "import sys; print ('%d.%d' % (sys.version_info.major, sys.version_info.minor))")
%endif

Name:           filemq
Version:        2.0.0
Release:        1
Summary:        a filemq server and client
License:        MIT
URL:            https://github.com/zeromq/filemq
Source0:        %{name}-%{version}.tar.gz
Group:          System/Libraries
# Note: ghostscript is required by graphviz which is required by
#       asciidoc. On Fedora 24 the ghostscript dependencies cannot
#       be resolved automatically. Thus add working dependency here!
BuildRequires:  ghostscript
BuildRequires:  asciidoc
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  xmlto
BuildRequires:  zeromq-devel
BuildRequires:  czmq-devel
%if %{with python_cffi}
BuildRequires:  python-cffi
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%endif
%if %{with python3_cffi}
BuildRequires:  python3-devel
BuildRequires:  python3-cffi
BuildRequires:  python3-setuptools
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
filemq a filemq server and client.

%package -n libfilemq0
Group:          System/Libraries
Summary:        a filemq server and client shared library

%description -n libfilemq0
This package contains shared library for filemq: a filemq server and client

%post -n libfilemq0 -p /sbin/ldconfig
%postun -n libfilemq0 -p /sbin/ldconfig

%files -n libfilemq0
%defattr(-,root,root)
%{_libdir}/libfilemq.so.*

%package devel
Summary:        a filemq server and client
Group:          System/Libraries
Requires:       libfilemq0 = %{version}
Requires:       zeromq-devel
Requires:       czmq-devel

%description devel
a filemq server and client development tools
This package contains development files for filemq: a filemq server and client

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libfilemq.so
%{_libdir}/pkgconfig/libfilemq.pc
%{_mandir}/man3/*
%{_mandir}/man7/*

%if %{with python_cffi}
%package -n python2-filemq-cffi
Group: Python
Summary: Python CFFI bindings for filemq
Requires: python >= %{py2_ver}.0, python < 3.0.0

%description -n python2-filemq-cffi
This package contains Python CFFI bindings for filemq

%files -n python2-filemq-cffi
%{_libdir}/python%{py2_ver}/site-packages/filemq_cffi/
%{_libdir}/python%{py2_ver}/site-packages/filemq_cffi-*-py%{py2_ver}.egg-info/
%endif

%if %{with python3_cffi}
%package -n python3-filemq-cffi
Group: Python
Summary: Python 3 CFFI bindings for filemq
Requires: python = %{py3_ver}

%description -n python3-filemq-cffi
This package contains Python 3 CFFI bindings for filemq

%files -n python3-filemq-cffi
%{_libdir}/python%{py3_ver}/site-packages/filemq_cffi/
%{_libdir}/python%{py3_ver}/site-packages/filemq_cffi-*-py%{py3_ver}.egg-info/
%endif

%prep
#FIXME: error:... did not worked for me
%if %{with python_cffi}
%if %{without drafts}
echo "FATAL: python_cffi not yet supported w/o drafts"
exit 1
%endif
%endif

%setup -q

%build
sh autogen.sh
%{configure} --enable-drafts=%{DRAFTS}
make %{_smp_mflags}
%if %{with python_cffi} || %{with python3_cffi}
# Problem: we need pkg-config points to built and not yet installed copy of filemq
# Solution: chicken-egg problem - let's make "fake" pkg-config file
sed -e "s@^libdir.*@libdir=.libs/@" \
    -e "s@^includedir.*@includedir=include/@" \
    src/libfilemq.pc > bindings/python_cffi/libfilemq.pc
cd bindings/python_cffi
# This avoids problem with "weird" character quoting between shell and python3
ln -sfr ../../include/ .
ln -sfr ../../src/.libs/ .
export PKG_CONFIG_PATH=`pwd`
%endif
%if %{with python_cffi}
python2 setup.py build
%endif
%if %{with python3_cffi}
python3 setup.py build
%endif

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

# remove static libraries
find %{buildroot} -name '*.a' | xargs rm -f
find %{buildroot} -name '*.la' | xargs rm -f

%if %{with python_cffi} || %{with python3_cffi}
cd bindings/python_cffi
export PKG_CONFIG_PATH=`pwd`
%endif
%if %{with python_cffi}
python2 setup.py install --root=%{buildroot} --skip-build --prefix %{_prefix}
%endif
%if %{with python3_cffi}
python3 setup.py install --root=%{buildroot} --skip-build --prefix %{_prefix}
%endif

%files
%defattr(-,root,root)
%doc README.md
%{_bindir}/filemq_server
%{_mandir}/man1/filemq_server*
%{_bindir}/filemq_client
%{_mandir}/man1/filemq_client*

%changelog
* Wed Dec 31 2014 filemq Developers <email@hostname.com
- Initial packaging.
