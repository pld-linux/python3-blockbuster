#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Utility to detect blocking calls in the async event loop
Summary(pl.UTF-8):	Narzędzie do wykrywania blokujących wywołań w pętli zdarzeń asynchronicznych
Name:		python3-blockbuster
Version:	1.5.24
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/blockbuster/
Source0:	https://files.pythonhosted.org/packages/source/b/blockbuster/blockbuster-%{version}.tar.gz
# Source0-md5:	be86e674816fc3e6653af8983dbd3b67
URL:		https://pypi.org/project/blockbuster/
BuildRequires:	python3-build
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
%if %{with tests}
BuildRequires:	python3-forbiddenfruit
BuildRequires:	python3-pytest >= 8.3.3
BuildRequires:	python3-pytest-asyncio >= 0.24.0
BuildRequires:	python3-requests >= 2.32.3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Blockbuster is a Python package designed to detect and prevent
blocking calls within an asynchronous event loop. It is particularly
useful when executing tests to ensure that your asynchronous code does
not inadvertently call blocking operations, which can lead to
performance bottlenecks and unpredictable behavior.

%description -l pl.UTF-8
Blockbuster to pakiet Pythona zaprojektowany, aby wykrywać i
zapobiegać blokującym wywołaniom wewnątrz pętli zdarzeń
asynchronicznych. Jest to przydatne w szczególności przy wykonywaniu
testów, aby upewnić się, że kod asynchroniczny nie wywołuje
nieumyślnie operacji blokujących, co może prowadzić do pogorszenia
wydajności i nieprzewidywanych zachowań.

%prep
%setup -q -n blockbuster-%{version}

%build
%py3_build_pyproject

%if %{with tests}
# disabled tests require networking
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_asyncio.plugin \
%{__python3} -m pytest tests -k 'not test_socket_send and not test_socket_send_non_blocking and not test_ssl_socket'
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%{py3_sitescriptdir}/blockbuster
%{py3_sitescriptdir}/blockbuster-%{version}.dist-info
