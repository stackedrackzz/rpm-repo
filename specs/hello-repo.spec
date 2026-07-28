Name:           hello-repo
Version:        1.0.0
Release:        1%{?dist}
Summary:        Example package proving the rpm-repo pipeline end-to-end
License:        MIT
URL:            https://github.com/stackedrackzz/rpm-repo
BuildArch:      noarch
Source0:        hello-repo.sh

%description
Placeholder package used to verify that the build -> sign -> createrepo ->
GitHub Pages publish pipeline works. Replace or remove once real packages
are added under specs/.

%prep
# no-op, single source file installed directly

%build
# no-op, nothing to compile

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/hello-repo

%files
%{_bindir}/hello-repo

%changelog
* Mon Jul 27 2026 rpm-repo maintainers <noreply@example.com> - 1.0.0-1
- Initial placeholder release
