{{{$version := printf "%s.%s.%s" .major .minor .patch }}}

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%{!?registry: %global registry container-registry.oracle.com/olcne}
%global app_name               fluent-operator
%global app_version            {{{$version}}}
%global oracle_release_version 1
%global _buildhost             build-ol%{?oraclelinux}-%{?_arch}.oracle.com

Name:           %{app_name}-container-image
Version:        %{app_version}
Release:        %{oracle_release_version}%{?dist}
Summary:        Provides great flexibility in building a logging layer based on Fluent Bit and Fluentd.
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/fluent/fluent-operator.git
Source:         %{name}-%{version}.tar.bz2

%description
Provides great flexibility in building a logging layer based on Fluent Bit and Fluentd.

%prep
%setup -q -n %{name}-%{version}

%build
%global rpm_name %{app_name}-%{version}-%{release}.%{_build_arch}
%global docker_tag %{registry}/%{app_name}:v%{version}
%global docker_tag_fluentbit %{registry}/fluent-bit:v4.2.0
%global app_name_fluentbit fluent-bit

yum clean all
yumdownloader --destdir=${PWD}/rpms %{rpm_name}

# Build fluent-operator image
docker build --pull \
    --build-arg https_proxy=${https_proxy} \
    -t %{docker_tag} -f ./olm/builds/Dockerfile .
docker save -o %{app_name}.tar %{docker_tag}

# Build fluent-bit image
docker build --pull \
    --build-arg https_proxy=${https_proxy} \
    -t %{docker_tag_fluentbit} -f ./olm/builds/Dockerfile.fluentbit .
docker save -o %{app_name_fluentbit}.tar %{docker_tag_fluentbit}

%install
%__install -D -m 644 %{app_name}.tar %{buildroot}/usr/local/share/olcne/%{app_name}.tar
%__install -D -m 644 %{app_name_fluentbit}.tar %{buildroot}/usr/local/share/olcne/%{app_name_fluentbit}.tar

%files
%license LICENSE THIRD_PARTY_LICENSES.txt olm/SECURITY.md
/usr/local/share/olcne/%{app_name}.tar
/usr/local/share/olcne/%{app_name_fluentbit}.tar

%changelog
* {{{.changelog_timestamp}}} - {{{$version}}}-1
- Added Oracle specific build files for fluent-operator.
