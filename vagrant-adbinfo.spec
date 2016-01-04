%{?scl:%scl_package %{vagrant_plugin_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from vagrant-adbinfo-0.0.4.gem by gem2rpm -*- rpm-spec -*-
%global vagrant_plugin_name vagrant-adbinfo

Name: %{?scl_prefix}%{vagrant_plugin_name}
Version: 0.0.9
Release: 3%{?dist}
Summary: Connection and configuration for a Docker daemon
Group: Development/Languages
License: GPLv2
URL: https://github.com/projectatomic/vagrant-adbinfo
Source0: https://rubygems.org/gems/%{vagrant_plugin_name}-%{version}.gem
Requires(posttrans): vagrant
Requires(preun): vagrant
Requires: %{?scl_prefix}vagrant
BuildRequires: %{?scl_prefix}vagrant
BuildArch: noarch
Provides: %{?scl_prefix}vagrant(%{vagrant_plugin_name}) = %{version}

%description
Vagrant plugin that provides the IP address:port and TLS certificate file
location for a Docker daemon.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{vagrant_plugin_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{vagrant_plugin_name}.gemspec
%{?scl:EOF}

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{vagrant_plugin_name}.gemspec
%{?scl:EOF}

# %%vagrant_plugin_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%vagrant_plugin_install

%install
mkdir -p %{buildroot}%{vagrant_plugin_dir}
cp -a .%{vagrant_plugin_dir}/* \
        %{buildroot}%{vagrant_plugin_dir}/

# Run the test suite

%check
pushd .%{vagrant_plugin_instdir}

popd

%posttrans
%{?scl:scl enable %{scl} - << \EOF}
%vagrant_plugin_register %{vagrant_plugin_name}
%{?scl:EOF}

%preun
%{?scl:scl enable %{scl} - << \EOF}
%vagrant_plugin_unregister %{vagrant_plugin_name}
%{?scl:EOF}

%files
%dir %{vagrant_plugin_instdir}
%exclude %{vagrant_plugin_instdir}/.*
%{vagrant_plugin_libdir}
%exclude %{vagrant_plugin_cache}
%{vagrant_plugin_spec}
%license %{vagrant_plugin_instdir}/LICENSE

%files doc
%doc %{vagrant_plugin_docdir}
%{vagrant_plugin_instdir}/Gemfile
%doc %{vagrant_plugin_instdir}/README.md
%{vagrant_plugin_instdir}/Rakefile
%{vagrant_plugin_instdir}/Vagrantfile
%doc %{vagrant_plugin_instdir}/CONTRIBUTING.md
%doc %{vagrant_plugin_instdir}/MAINTAINERS
%{vagrant_plugin_instdir}/vagrant-adbinfo.gemspec
%{vagrant_plugin_instdir}/vagrant-adbinfo.spec

%changelog
* Fri Dec 04 2015 Josef Stribny - 0.0.9-4
- Add scl macros

* Thu Dec  3 2015 Pavel Valena - 0.0.9-3
- Correct upstream URL
- Remove unnecessary BuildRequires

* Thu Dec  3 2015 Pavel Valena - 0.0.9-2
- Shorten summary to pass rpmlint
- Remove unnecessary rubygems-devel from BuildRequires
- Move license file to main package

* Wed Nov 25 2015 Brian Exelbierd - 0.0.9-1
- Fixes cert-generation script existence check, a bug was found where the cert
  was regenerated to often
- Bumps the plugin version to 0.0.9

* Tue Nov 24 2015 Navid Shaikh - 0.0.8-1
- Fixes cert-generation script existence check
- Bumps the plugin version to 0.0.8

* Tue Nov 24 2015 Navid Shaikh - 0.0.7-1
- Fixes adbinfo#40: Handle private networking in ADB for different providers
- Bumps the plugin version to 0.0.7

* Fri Nov 20 2015 Navid Shaikh - 0.0.6-1
- Finds IP address of the guest provisioned via private networking
- Fixes typo in eval command of adbinfo output
- Adds License, Contributing and Maintainers files
- Adds Quick Start and Contact us sections

* Thu Nov 19 2015 Navid Shaikh - 0.0.5-2
- Removes shadow-utils from Requires

* Tue Nov 17 2015 Navid Shaikh - 0.0.5-1
- vagrant-adbinfo#17: adbinfo format should be windows compatible 
- vagrant-adbinfo#18: adbinfo should be possible to evaluate in shell

* Thu Nov 12 2015 Navid Shaikh - 0.0.4-1
- Initial package
