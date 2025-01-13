Name:           virtiofsd
Version:        1.13.0
Release:        1%{?dist}
Summary:        Virtio-fs vhost-user device daemon (Rust version)

License:        Apache-2.0 AND BSD-3-Clause
URL:            https://gitlab.com/virtio-fs/virtiofsd
Source:         %{crates_source}
# To create the vendor tarball:
#   tar xf %%{name}-%%{version}.crate ; pushd %%{name}-%%{version} ; \
#   cargo vendor && tar Jcvf ../%%{name}-%%{version}-vendor.tar.xz vendor/ ; popd
Source1:        %{name}-%{version}-vendor.tar.gz

ExclusiveArch:  %{rust_arches}
# Some of our deps (i.e. vm-memory) are not available on 32 bits targets.
# In addition, there's no ppc64 qemu-kvm available for RHEL.
%if 0%{?rhel}
ExcludeArch:    i686 %{power64}
%else
ExcludeArch:    i686
%endif

%if 0%{?rhel}
BuildRequires:  rust-toolset
%else
BuildRequires:  rust-packaging >= 21
%endif
BuildRequires:  libcap-ng-devel
BuildRequires:  libseccomp-devel
%if 0%{?rhel}
Requires:       qemu-kvm-common
%else
Requires:       qemu-common
%endif
Provides:       vhostuser-backend(fs)
Conflicts:      qemu-virtiofsd
%if 0%{?fedora} > 38
Obsoletes:      qemu-virtiofsd <= 2:8.0.0-1
Provides:       qemu-virtiofsd = 2:7.2.1-1
%endif

%description
%{summary}.

%prep
%autosetup -n %{name}-%{version_no_tilde} -p1 %{?rhel:-a1}
%if 0%{?rhel}
%cargo_prep -v vendor
rm -f Cargo.lock
%else
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires
%endif

%build
%cargo_build
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%if 0%{?rhel}
%cargo_vendor_manifest
%endif

%install
mkdir -p %{buildroot}%{_libexecdir}
install -D -p -m 0755 target/release/virtiofsd %{buildroot}%{_libexecdir}/virtiofsd
install -D -p -m 0644 50-virtiofsd.json %{buildroot}%{_datadir}/qemu/vhost-user/50-qemu-virtiofsd.json

%files
%license LICENSE-APACHE LICENSE-BSD-3-Clause
%license LICENSE.dependencies
%if 0%{?rhel}
%license cargo-vendor.txt
%endif
%doc README.md
%{_libexecdir}/virtiofsd
%{_datadir}/qemu/vhost-user/50-qemu-virtiofsd.json

%changelog
* Mon Dec 02 2024 Miroslav Rezanina <mrezanin@redhat.com> - 1.13.0-1
- Rebase to 1.13.0 [RHEL-69290]
- Resolves: RHEL-69290
  (Rebase virtiofsd to latest version for RHEL 10.0)

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 1.11.1-2
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Tue Jul 16 2024 Miroslav Rezanina <mrezanin@redhat.com> - 1.11.1-1
- Update to upstream version 1.11.1 [RHEL-48645]
- Resolves: RHEL-48645
  (Rebase virtiofsd to latest version for RHEL 10.0 Beta)

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 1.10.0-3.1
- Bump release for June 2024 mass rebuild

* Thu Feb 01 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.10.0-2.1
- Update Rust macro usage

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 23 2024 Sergio Lopez <slp@redhat.com> - 1.10.0-1
- Update to version 1.10.0

* Sun Dec 24 2023 Sergio Lopez <slp@redhat.com> - 1.9.0-1
- Update to version 1.9.0

* Fri Sep 29 2023 Colin Walters <walters@verbum.org> - 1.7.0-5
- Rebuild with latest vhost-user-backend; xref
  https://gitlab.com/virtio-fs/virtiofsd/-/issues/62#note_1584371000

* Tue Sep 19 2023 Fabio Valentini <decathorpe@gmail.com> - 1.7.0-4
- Rebuild for vm-memory v0.12.2 / CVE-2023-41051.

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 19 2023 Sergio Lopez <slp@redhat.com> - 1.7.0-2
- Update license specification to conform SPDX format

* Tue Jul 18 2023 Sergio Lopez <slp@redhat.com> - 1.7.0-1
- Update to version 1.7.0
- Drop no longer needed temporary patch

* Tue May 09 2023 Sergio Lopez <slp@redhat.com> - 1.5.1-3
- Only use Obsoletes/Provides on Fedora 39 and later

* Wed Apr 26 2023 Daniel P. Berrangé <berrange@redhat.com> - 1.5.1-2
- Add Obsoletes/Provides for qemu-virtiofsd to get an upgrade path (rhbz #2189368)

* Thu Feb 09 2023 Sergio Lopez <slp@redhat.com> - 1.5.1-1
- Update to version 1.5.1

* Sun Feb 05 2023 Fabio Valentini <decathorpe@gmail.com> - 1.4.0-3
- Rebuild for fixed frame pointer compiler flags in Rust RPM macros.

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jul 26 2022 Sergio Lopez <slp@redhat.com> - 1.4.0-1
- Update to version 1.4.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 06 2022 Sergio Lopez <slp@redhat.com> - 1.3.0-1
- Update to version 1.3.0
- Build on all rust arches except i686 (32-bit targets are not supported)

* Mon May 16 2022 Sergio Lopez <slp@redhat.com> - 1.2.0-1
- Initial package

