

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%global app_name                fluent-operator
%global app_version             3.6.0
%global oracle_release_version  1
%global _buildhost              build-ol%{?oraclelinux}-%{?_arch}.oracle.com

Name:           %{app_name}
Version:        %{app_version}
Release:        %{oracle_release_version}%{?dist}
Summary:        Provides great flexibility in building a logging layer based on Fluent Bit and Fluentd.
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/fluent/fluent-operator.git
Source:         %{name}-%{version}.tar.bz2
Patch0:         Makefile.patch
BuildRequires:  golang
BuildRequires:  make

%description
Provides great flexibility in building a logging layer based on Fluent Bit and Fluentd.

%prep
%setup -q -n %{name}-%{version}
%patch0

%build
make binary

%install
install -m 755 bin/fb-manager %{buildroot}/manager
install -m 755 -d %{buildroot}/fluent-bit/bin
install -m 755 -d %{buildroot}/fluent-bit/etc
install -m 755 bin/fb-watcher %{buildroot}/fluent-bit/bin/fluent-bit-watcher

%files
%license LICENSE THIRD_PARTY_LICENSES.txt olm/SECURITY.md
/manager
/fluent-bit/


%changelog
* Thu Jan 22 2026 Oracle Cloud Native Environment Authors <noreply@oracle.com> - 3.6.0-1
- Added Oracle specific build files for fluent-operator.
