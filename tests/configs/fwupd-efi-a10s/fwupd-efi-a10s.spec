%global debug_package %{nil}

Summary:   Firmware update EFI binaries
Name:      fwupd-efi
Version:   1.6
Release:   %autorelease
License:   LGPL-2.1-or-later
URL:       https://github.com/fwupd/fwupd-efi
Source0:   https://github.com/fwupd/fwupd-efi/releases/download/%{version}/%{name}-%{version}.tar.xz

Source300:   redhatsecurebootca3.cer
Source301:   redhatsecureboot301.cer
Source500:   redhatsecurebootca5.cer
Source503:   redhatsecureboot503.cer

# these are the only architectures supporting UEFI UpdateCapsule
ExclusiveArch: x86_64 aarch64

BuildRequires: gcc
BuildRequires: meson
BuildRequires: gnu-efi-devel >= 3.0.18
BuildRequires: pesign >= 113-20
BuildRequires: python3-pefile

%description
fwupd is a project to allow updating device firmware, and this package provides
the EFI binary that is used for updating using UpdateCapsule.

%prep
%autosetup -p1

%build

%meson \
    -Defi_sbat_distro_id="fedora" \
    -Defi_sbat_distro_summary="The Fedora Project" \
    -Defi_sbat_distro_pkgname="%{name}" \
    -Defi_sbat_distro_version="%{version}-%{release}" \
    -Defi_sbat_distro_url="https://src.fedoraproject.org/rpms/%{name}"

%meson_build

%install
%meson_install

# sign fwupd.efi loader
%ifarch x86_64
%global efiarch x64
%endif
%ifarch aarch64
%global efiarch aa64
%endif
%global fwup_efi_fn $RPM_BUILD_ROOT%{_libexecdir}/fwupd/efi/fwupd%{efiarch}.efi
%pesign -s -i %{fwup_efi_fn} -o %{fwup_efi_fn}.tmp -a %{SOURCE300} -c %{SOURCE301} -n redhatsecureboot301
%define __pesign_client_cert fwupd-signer
%pesign -s -i %{fwup_efi_fn}.tmp -o %{fwup_efi_fn}.signed -a %{SOURCE500} -c %{SOURCE503} -n redhatsecureboot503
rm -vf %{fwup_efi_fn}.tmp

%files
%doc README.md AUTHORS
%license COPYING
%{_libexecdir}/fwupd/efi/*.efi
%{_libexecdir}/fwupd/efi/*.efi.signed
%{_libdir}/pkgconfig/fwupd-efi.pc

%changelog
%autochangelog
