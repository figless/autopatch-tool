%global glib2_version 2.45.8
%global libxmlb_version 0.1.3
%global libgusb_version 0.3.5
%global libcurl_version 7.62.0
%global libjcat_version 0.1.0
%global systemd_version 231
%global json_glib_version 1.1.1

# although we ship a few tiny python files these are utilities that 99.99%
# of users do not need -- use this to avoid dragging python onto CoreOS
%global __requires_exclude ^%{python3}$

# PPC64 is too slow to complete the tests under 3 minutes...
%ifnarch ppc64le
%global enable_tests 1
%endif

%global enable_dummy 1

# fwupd.efi is only available on these arches
%ifarch x86_64 aarch64
%global have_uefi 1
%endif

# gpio.h is only available on these arches
%ifarch x86_64 aarch64
%global have_gpio 1
%endif

# flashrom is only available on these arches
%ifarch i686 x86_64 armv7hl aarch64 ppc64le
%global have_flashrom 1
%endif

%ifarch i686 x86_64
%global have_msr 1
%endif

# Until we actually have seen it outside x86
%ifarch i686 x86_64
%global have_thunderbolt 1
%endif

# only available recently
%if 0%{?fedora} >= 30
%global have_modem_manager 1
%endif

Summary:   Firmware update daemon
Name:      fwupd
Version:   1.9.13
Release:   2%{?dist}
License:   LGPLv2+
URL:       https://github.com/fwupd/fwupd
Source0:   http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
Source2:   http://people.freedesktop.org/~hughsient/releases/fwupd-efi-1.4.tar.xz

Patch101:  0001-generate_binary-Add-NX-COMPAT-flag-manually-when-gen.patch
Patch102:  0001-Correctly-migrate-from-v2-to-database-schema-v10.patch

Source10:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20100307-x64.cab
Source11:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20140413-x64.cab
Source12:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20160809-x64.cab
Source13:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20200729-aa64.cab
Source14:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20200729-ia32.cab
Source15:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20200729-x64.cab
Source16:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20210429-x64.cab
Source17:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20220812-aa64.cab
Source18:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20220812-ia32.cab
Source19:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20220812-x64.cab
Source20:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20230509-aa64.cab
Source21:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20230509-ia32.cab
Source22:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20230509-x64.cab

# these are numbered high just to keep them wildly away from colliding with
# the real package sources, in order to reduce churn.
Source300:   redhatsecurebootca3.cer
Source301:   redhatsecureboot301.cer
Source500:   redhatsecurebootca5.cer
Source503:   redhatsecureboot503.cer

BuildRequires: gettext
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libxmlb-devel >= %{libxmlb_version}
BuildRequires: libgudev1-devel
BuildRequires: libgusb-devel >= %{libgusb_version}
BuildRequires: libcurl-devel >= %{libcurl_version}
BuildRequires: libjcat-devel >= %{libjcat_version}
BuildRequires: polkit-devel >= 0.103
BuildRequires: sqlite-devel
BuildRequires: systemd >= %{systemd_version}
BuildRequires: systemd-devel
BuildRequires: libarchive-devel
BuildRequires: gobject-introspection-devel
%ifarch %{valgrind_arches}
BuildRequires: valgrind
BuildRequires: valgrind-devel
%endif
BuildRequires: gnutls-devel
BuildRequires: gnutls-utils
BuildRequires: meson
BuildRequires: json-glib-devel >= %{json_glib_version}
BuildRequires: vala
BuildRequires: bash-completion
BuildRequires: git-core
%if 0%{?have_flashrom}
BuildRequires: flashrom-devel >= 1.2-2
%endif
BuildRequires: libdrm-devel
BuildRequires: python3-jinja2

%if 0%{?have_modem_manager}
BuildRequires: ModemManager-glib-devel >= 1.10.0
BuildRequires: libqmi-devel >= 1.22.0
BuildRequires: libmbim-devel
%endif

%if 0%{?have_uefi}
BuildRequires: efivar-devel >= 33
BuildRequires: python3 python3-cairo python3-gobject
BuildRequires: pango-devel
BuildRequires: cairo-devel cairo-gobject-devel
BuildRequires: freetype
BuildRequires: fontconfig
BuildRequires: google-noto-sans-cjk-ttc-fonts
BuildRequires: gnu-efi-devel
BuildRequires: tpm2-tss-devel >= 2.2.3
BuildRequires: pesign >= 113-20
%endif

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: glib2%{?_isa} >= %{glib2_version}
Requires: libxmlb%{?_isa} >= %{libxmlb_version}
Requires: libgusb%{?_isa} >= %{libgusb_version}
Requires: shared-mime-info

Obsoletes: fwupd-sign < 0.1.6
Obsoletes: libebitdo < 0.7.5-3
Obsoletes: libdfu < 1.0.0
Obsoletes: fwupd-labels < 1.1.0-1

Obsoletes: dbxtool < 9
Provides: dbxtool

# optional, but a really good idea
Recommends: udisks2

%if 0%{?have_modem_manager}
Recommends: %{name}-plugin-modem-manager
%endif
%if 0%{?have_flashrom}
Recommends: %{name}-plugin-flashrom
%endif

%description
fwupd is a daemon to allow session software to update device firmware.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: libebitdo-devel < 0.7.5-3
Obsoletes: libdfu-devel < 1.0.0

%description devel
Files for development with %{name}.

%package tests
Summary: Data files for installed tests
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
Data files for installed tests.

%if 0%{?have_modem_manager}
%package plugin-modem-manager
Summary: fwupd plugin using ModemManger
Requires: %{name}%{?_isa} = %{version}-%{release}

%description plugin-modem-manager
This provides the optional package which is only required on hardware that
might have mobile broadband hardware. It is probably not required on servers.
%endif

%if 0%{?have_flashrom}
%package plugin-flashrom
Summary: fwupd plugin using flashrom
Requires: %{name}%{?_isa} = %{version}-%{release}

%description plugin-flashrom
This provides the optional package which is only required on hardware that
can be flashed using flashrom. It is probably not required on servers.
%endif

%prep
%setup -q
%patch102 -p1

mkdir -p subprojects/fwupd-efi
tar xfvs %{SOURCE2} -C subprojects/fwupd-efi --strip-components=1
cd subprojects/fwupd-efi
%patch101 -p1
cd -

%build

%meson \
    -Ddocs=disabled \
    -Dlvfs=disabled \
    -Dlaunchd=disabled \
    -Dpassim=disabled \
%if 0%{?enable_tests}
    -Dtests=true \
%else
    -Dtests=false \
%endif
%if 0%{?have_flashrom}
    -Dplugin_flashrom=enabled \
%else
    -Dplugin_flashrom=disabled \
%endif
%if 0%{?have_msr}
    -Dplugin_msr=enabled \
%else
    -Dplugin_msr=disabled \
%endif
%if 0%{?have_gpio}
    -Dplugin_gpio=enabled \
%else
    -Dplugin_gpio=disabled \
%endif
%if 0%{?have_uefi}
    -Dplugin_uefi_capsule=enabled \
    -Dplugin_uefi_pk=enabled \
    -Dplugin_tpm=enabled \
    -Defi_os_dir=%{efi_vendor} \
%ifarch x86_64
    -Dfwupd-efi:efi_sbat_distro_id="rhel" \
    -Dfwupd-efi:efi_sbat_distro_summary="Red Hat Enterprise Linux" \
    -Dfwupd-efi:efi_sbat_distro_pkgname="%{name}" \
    -Dfwupd-efi:efi_sbat_distro_version="%{version}" \
    -Dfwupd-efi:efi_sbat_distro_url="mail:secalert@redhat.com" \
    -Dfwupd-efi:efi-libdir="/usr/lib64" \
%endif
%else
    -Dplugin_uefi_capsule=disabled \
    -Dplugin_uefi_pk=disabled \
    -Dplugin_tpm=disabled \
%endif
%if 0%{?have_modem_manager}
    -Dplugin_modem_manager=enabled \
%else
    -Dplugin_modem_manager=disabled \
%endif
    -Dman=true \
    -Dsystemd_unit_user="" \
    -Dcompat_cli=true \
    -Dbluez=disabled \
    -Dcbor=disabled \
    -Dplugin_android_boot=disabled \
    -Dplugin_cfu=disabled \
    -Dplugin_igsc=disabled \
    -Dplugin_intel_me=disabled \
    -Dplugin_logitech_bulkcontroller=disabled \
    -Dplugin_logitech_scribe=disabled \
    -Dplugin_mtd=disabled \
    -Dplugin_powerd=disabled \
    -Dplugin_uf2=disabled \
    -Dsupported_build=enabled

%meson_build

%if 0%{?enable_tests}
%check
%meson_test
%endif

%install
%meson_install

# on RHEL the LVFS is disabled by default
mkdir -p %{buildroot}/%{_datadir}/dbxtool
install \
  %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} \
  %{SOURCE16} %{SOURCE17} %{SOURCE18} %{SOURCE19} %{SOURCE20} %{SOURCE21} %{SOURCE22} \
  %{buildroot}/%{_datadir}/dbxtool

# sign fwupd.efi loader
%ifarch x86_64
%global efiarch x64
%global fwup_efi_fn $RPM_BUILD_ROOT%{_libexecdir}/fwupd/efi/fwupd%{efiarch}.efi
%pesign -s -i %{fwup_efi_fn} -o %{fwup_efi_fn}.tmp -a %{SOURCE300} -c %{SOURCE301} -n redhatsecureboot301
%pesign -s -i %{fwup_efi_fn}.tmp -o %{fwup_efi_fn}.signed -a %{SOURCE500} -c %{SOURCE503} -n redhatsecureboot503
rm -fv %{fwup_efi_fn}.tmp
%endif

mkdir -p --mode=0700 $RPM_BUILD_ROOT%{_localstatedir}/lib/fwupd/gnupg

# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1757948
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/fwupd

%find_lang %{name}

%post
%systemd_post fwupd.service fwupd-refresh.timer

# change vendor-installed remotes to use the default keyring type
for fn in /etc/fwupd/remotes.d/*.conf; do
    if grep -q "Keyring=gpg" "$fn"; then
        sed -i 's/Keyring=gpg/#Keyring=pkcs/g' "$fn";
    fi
done

%preun
%systemd_preun fwupd.service fwupd-refresh.timer

%postun
%systemd_postun_with_restart fwupd.service fwupd-refresh.timer
%systemd_postun_with_restart pesign.service

%files -f %{name}.lang
%doc README.md
%license COPYING
%config(noreplace)%{_sysconfdir}/fwupd/fwupd.conf
%dir %{_libexecdir}/fwupd
%{_libexecdir}/fwupd/fwupd
%ifarch i686 x86_64
%{_libexecdir}/fwupd/fwupd-detect-cet
%endif
%{_libexecdir}/fwupd/fwupdoffline
%if 0%{?have_uefi}
%{_libexecdir}/fwupd/efi/*.efi
%ifarch x86_64
%{_libexecdir}/fwupd/efi/*.efi.signed
%endif
%{_bindir}/fwupdate
%endif
%{_bindir}/dfu-tool
%{_bindir}/dbxtool
%{_bindir}/fwupdmgr
%{_bindir}/fwupdtool
%{_bindir}/fwupdagent
%dir %{_sysconfdir}/fwupd
%dir %{_sysconfdir}/fwupd/bios-settings.d
%{_sysconfdir}/fwupd/bios-settings.d/README.md
%dir %{_sysconfdir}/fwupd/remotes.d
%config(noreplace)%{_sysconfdir}/fwupd/remotes.d/lvfs.conf
%config(noreplace)%{_sysconfdir}/fwupd/remotes.d/lvfs-testing.conf
%config(noreplace)%{_sysconfdir}/fwupd/remotes.d/vendor-directory.conf
%config(noreplace)%{_sysconfdir}/pki/fwupd
%{_sysconfdir}/pki/fwupd-metadata
%if 0%{?have_msr}
/usr/lib/modules-load.d/fwupd-msr.conf
%endif
%{_datadir}/dbus-1/system.d/org.freedesktop.fwupd.conf
%{_datadir}/bash-completion/completions/fwupdmgr
%{_datadir}/bash-completion/completions/fwupdtool
%{_datadir}/fish/vendor_completions.d/fwupdmgr.fish
%{_datadir}/fwupd/metainfo/org.freedesktop.fwupd*.metainfo.xml
%{_datadir}/fwupd/remotes.d/vendor/firmware/README.md
%{_datadir}/dbus-1/interfaces/org.freedesktop.fwupd.xml
%{_datadir}/polkit-1/actions/org.freedesktop.fwupd.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.fwupd.rules
%{_datadir}/dbus-1/system-services/org.freedesktop.fwupd.service
%dir %{_datadir}/dbxtool
%{_datadir}/dbxtool/DBXUpdate-20100307-x64.cab
%{_datadir}/dbxtool/DBXUpdate-20140413-x64.cab
%{_datadir}/dbxtool/DBXUpdate-20160809-x64.cab
%{_datadir}/dbxtool/DBXUpdate-20200729-aa64.cab
%{_datadir}/dbxtool/DBXUpdate-20200729-ia32.cab
%{_datadir}/dbxtool/DBXUpdate-20200729-x64.cab
%{_datadir}/dbxtool/DBXUpdate-20210429-x64.cab
%{_datadir}/dbxtool/DBXUpdate-20220812-aa64.cab
%{_datadir}/dbxtool/DBXUpdate-20220812-ia32.cab
%{_datadir}/dbxtool/DBXUpdate-20220812-x64.cab
%{_datadir}/dbxtool/DBXUpdate-20230509-aa64.cab
%{_datadir}/dbxtool/DBXUpdate-20230509-ia32.cab
%{_datadir}/dbxtool/DBXUpdate-20230509-x64.cab
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_datadir}/metainfo/org.freedesktop.fwupd.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/org.freedesktop.fwupd.svg
%{_datadir}/fwupd/firmware_packager.py
%{_datadir}/fwupd/simple_client.py
%{_datadir}/fwupd/add_capsule_header.py
%{_datadir}/fwupd/install_dell_bios_exe.py
%{_unitdir}/fwupd-offline-update.service
%{_unitdir}/fwupd.service
%{_unitdir}/fwupd-refresh.service
%{_unitdir}/fwupd-refresh.timer
%{_unitdir}/system-update.target.wants/
%dir %{_localstatedir}/lib/fwupd
%dir %{_localstatedir}/cache/fwupd
%dir %{_datadir}/fwupd/quirks.d
%{_datadir}/fwupd/quirks.d/builtin.quirk.gz
%if 0%{?have_uefi}
%config(noreplace)%{_sysconfdir}/grub.d/35_fwupd
%endif
%{_libdir}/libfwupd.so.2*
%{_libdir}/girepository-1.0/Fwupd-2.0.typelib
/usr/lib/udev/rules.d/*.rules
/usr/lib/systemd/system-shutdown/fwupd.shutdown
%dir %{_libdir}/fwupd-%{version}
%{_libdir}/fwupd-%{version}/libfwupd*.so
%ghost %{_localstatedir}/lib/fwupd/gnupg

%if 0%{?have_modem_manager}
%files plugin-modem-manager
%{_libdir}/fwupd-%{version}/libfu_plugin_modem_manager.so
%endif
%if 0%{?have_flashrom}
%files plugin-flashrom
%{_libdir}/fwupd-%{version}/libfu_plugin_flashrom.so
%endif
%if 0%{?have_uefi}
%{_datadir}/fwupd/uefi-capsule-ux.tar.xz
%endif

%files devel
%{_datadir}/gir-1.0/Fwupd-2.0.gir
%{_datadir}/vala/vapi
%{_includedir}/fwupd-1
%{_libdir}/libfwupd*.so
%{_libdir}/pkgconfig/fwupd.pc
%if 0%{?have_uefi}
%{_libdir}/pkgconfig/fwupd-efi.pc
%endif

%files tests
%if 0%{?enable_tests}
%{_datadir}/fwupd/host-emulate.d/*.json.gz
%dir %{_datadir}/installed-tests/fwupd
%{_datadir}/installed-tests/fwupd/tests/*
%{_datadir}/installed-tests/fwupd/fwupd-tests.xml
%{_datadir}/installed-tests/fwupd/*.test
%{_datadir}/installed-tests/fwupd/*.cab
%{_datadir}/installed-tests/fwupd/fakedevice124.jcat
%{_datadir}/installed-tests/fwupd/fakedevice124.bin
%{_datadir}/installed-tests/fwupd/fakedevice124.metainfo.xml
%{_datadir}/installed-tests/fwupd/*.sh
%{_datadir}/installed-tests/fwupd/*.zip
%if 0%{?have_uefi}
%{_datadir}/installed-tests/fwupd/efi
%endif
%{_datadir}/installed-tests/fwupd/chassis_type
%{_datadir}/installed-tests/fwupd/sys_vendor
%{_libexecdir}/installed-tests/fwupd/*
%dir %{_sysconfdir}/fwupd/remotes.d
%{_datadir}/fwupd/remotes.d/fwupd-tests.conf
%endif

%changelog
* Mon Feb 19 2024 Richard Hughes <richard@hughsie.com> 1.9.13-2
- Fix upgrade from fwupd < v1.9.5
- Resolves: #RHEL-15328

* Thu Feb 15 2024 Richard Hughes <richard@hughsie.com> 1.9.13-1
- Update to latest stable upstream version.
- Resolves: #RHEL-15328

* Wed Jan 24 2024 Richard Hughes <richard@hughsie.com> 1.9.12-1
- Update to latest stable upstream version.
- Resolves: #RHEL-15328

* Wed Jan 03 2024 Richard Hughes <richard@hughsie.com> 1.9.11-1
- Update to latest stable upstream version.
- Resolves: #RHEL-15328

* Mon Dec 04 2023 Richard Hughes <richard@hughsie.com> 1.9.10-1
- Update to latest stable upstream version.
- Resolves: #RHEL-15328

* Fri Jun 09 2023 Richard Hughes <richard@hughsie.com> 1.8.16-1
- Update to latest stable upstream version.
- Resolves: rhbz#2209944

* Thu Feb 02 2023 Richard Hughes <richard@hughsie.com> 1.8.10-2
- Rebuild because distrobaker did entirely the wrong thing.
- Resolves: rhbz#2128384, needed for rhbz#2119436 and rhbz#2128384

* Fri Jan 27 2023 Richard Hughes <richard@hughsie.com> 1.8.10-1
- Rebase to latest upstream release to fix multiple ESP detection problems
- Resolves: rhbz#2128384, needed for rhbz#2119436 and rhbz#2128384

* Fri Sep 23 2022 Richard Hughes <richard@hughsie.com> 1.7.10-1
- New upstream release
- Resolves: rhbz#2129280

* Thu Sep 01 2022 Richard Hughes <rhughes@redhat.com> 1.7.9-2
- Include the new dbx updates on the filesystem; clients typically do not have LVFS enabled.
- Resolves: rhbz#2120708

* Mon Jul 25 2022 Richard Hughes <richard@hughsie.com> 1.7.8-1
- New upstream release
- Resolves: rhbz#2059075

* Wed Apr 06 2022 Richard Hughes <richard@hughsie.com> 1.7.4-3
- Disable the Logitech bulkcontroller plugin to avoid adding a dep to protobuf-c
  which lives in AppStream, not BaseOS.
- Use the efi_vendor variable from EFI-RPM
- Resolves: rhbz#2064904

* Thu Jan 13 2022 Richard Hughes <richard@hughsie.com> 1.7.4-1
- New upstream release
- Backport Fedora 34 changes
- Include support for Lenovo TBT4 Docking stations
- Do not cause systemd-modules-load failures
- Build against a new enough pesign
- Resolves: rhbz#2007520

* Mon Nov 01 2021 Richard Hughes <richard@hughsie.com> 1.7.1-1
- New upstream release
- Backport Fedora 34 changes
- Include support for Dell TBT4 Docking stations
- Resolves: rhbz#1974347
- Resolves: rhbz#1991426

* Fri Sep 24 2021 Richard Hughes <richard@hughsie.com> 1.5.9-4
- Rebuilt to use redhatsecureboot503 signatures
- Undo last Fedora sync to use the RHEL-specific patches
- Resolves: rhbz#2007520

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.5.9-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Tue Jun 22 2021 Mohan Boddu <mboddu@redhat.com> - 1.5.9-2
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Mon Apr 19 2021 Richard Hughes <richard@hughsie.com> 1.5.9-1
- Rebase to include the SBAT metadata section to allow fixing BootHole
- Resolves: rhbz#1951030

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 1.5.5-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Mon Apr 12 2021 Richard Hughes <richard@hughsie.com> 1.5.5-3
- Backport a patch from master to drop the python3-pillow dep
- Resolves: rhbz#1935838

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Richard Hughes <richard@hughsie.com> 1.5.5-1
- New upstream release
- Add a plugin to update PixArt RF devices
- Add new hardware to use the elantp and rts54hid plugins
- Detect the AMD TSME encryption state for HSI-4
- Detect the AMI PK test key is not installed for HSI-1
- Fix flashing a fingerprint reader that is in use
- Fix several critical warnings when parsing invalid firmware
- Fix updating DFU devices that use DNLOAD_BUSY
- Ignore the legacy UEFI OVMF dummy GUID
- Make libfwupd more thread safe to fix a crash in gnome-software
- Never show unprintable chars from invalid firmware in the logs

* Wed Dec 16 2020 Richard Hughes <richard@hughsie.com> 1.5.4-1
- New upstream release
- Add Maple Ridge Thunderbolt firmware parsing support
- Allow creating FMAP and Synaptics firmware using builder.xml
- Allow using fwupdtool as non-root for firmware commands
- Do not trust the Block.HintSystem boolean for ESP filtering
- Fix a memory leak when parsing Synaptics firmware
- Fix a possible crash when reading the Goodix MOC USB request
- Fix possible crashes when parsing invalid firmware

* Tue Dec 08 2020 Richard Hughes <richard@hughsie.com> 1.5.3-1
- New upstream release
- Add a UEFI quirk for Star Labs Lite Mk III
- Add the device firmare ID for serio class hardware
- Allow setting the GMainContext when used for sync methods
- Allow the client to send legacy PKCS7 and GPG signatures
- Export the driver name from FuUdevDevice
- Fix a possible critical warning due to missing retval
- Fix the endianness for the CRC check in bcm57xx
- Make sure the correct interface number is used for QMI
- Mark more user-visible strings as translatable
- Restrict loading component types of firmware
- Validate ModemManager firmware update method combinations

* Mon Nov 23 2020 Richard Hughes <richard@hughsie.com> 1.5.2-1
- New upstream release
- Add a flag to indicate if packages are supported
- Add a plugin for the Pinebook Pro laptop
- Allow components to set the icon from the metadata
- Fall back to FAT32 internal partitions for detecting ESP
- Fix detection of ColorHug version on older firmware versions
- Fix reading BCM57XX vendor and device ids from firmware
- Fix replugging the MSP430 device
- Fix sync method when called from threads without a context
- Ignore an invalid vendor-id when adding releases for display
- Improve synaptics-mst reliability when writing data
- Install modules-load configs in the correct directory
- Notify the service manager when idle-quitting
- Only download the remote metadata as required
- Remove HSI update and attestation suffixes
- Restore recognizing GPG and PKCS7 signature types in libfwupd
- Set the SMBIOS chassis type to portable if a DT battery exists
- Switch from libsoup to libcurl for downloading data

* Fri Nov 20 2020 Adam Williamson <awilliam@redhat.com> - 1.5.1-2
- Backport #2605 for #2600, seems to help RHBZ #1896540

* Mon Nov 01 2020 Richard Hughes <richard@hughsie.com> 1.5.1-1
- New upstream release
- Delete unused EFI variables when deploying firmware
- Fix probe warning for the Logitech Unifying device
- Include the amount of NVRAM size in use in the LVFS failure report
- Make bcm57xx hotplug more reliable
- Recognize authorized thunderbolt value of 2
- Remove the duplicate parent-child data in FwupdDevice and FuDevice
- Show a less scary fwupdate output for devices without info
- Use a different Device ID for the OptionROM devices
- Use UDisks to find out if swap devices are encrypted

* Mon Oct 26 2020 Richard Hughes <richard@hughsie.com> 1.5.0-1
- New upstream release
- Add async versions of the library for GUI tools
- Add commands for interacting with the ESP to fwupdtool
- Add plugin for Goodix fingerprint sensors
- Add plugin that can update the BCM5719 network adapter
- Add plugin to update Elan Touchpads using HID
- Add support for ChromeOS Quiche and Gingerbread
- Add support for the Host Security ID
- Add support for ThunderBolt retimers
- Add switch-branch command to fwupdtool and fwupdmgr
- Allow blocking specific firmware releases by checksum
- Allow constructing a firmware with multiple images
- Allow firmware to require specific features from front-end clients
- Fix setting BootNext correctly when multiple updates are scheduled
- Fix the topology of the audio device on the Lenovo TR dock
- Include the HSI results and attributes in the uploaded report
- Make return code different for get-updates with no updates
- Make specific authorizations also imply others
- Parse the HEX version before comparing for equality
- Prevent dell-dock updates to occur via synaptics-mst plugin
- Record the UEFI failure in more cases
- Support loading DMI data from DT systems
- Support LVFS::UpdateImage for GUI clients
- Use pkttyagent to request user passwords if running without GUI

* Mon Sep 07 2020 Richard Hughes <richard@hughsie.com> 1.4.6-1
- New upstream release
- Add a re-implementation of the rhboot dbxtool
- Add missing Synaptics Prometheus GUIDs for ConfigId
- Add support for the LabTop Mk IV
- Add support for the Realtek RTD21XX I²C protocol
- Allow blocking specific firmware releases by checksum
- Allow DFU device to attach to runtime without a bus reset
- Allow plugins to set remove delay only on the child
- Cancel the file monitor before disposal to avoid a potential deadlock
- Correctly label the vebdor for more NVMe devices
- Specify a remove delay for Poly USB Cameras
- Support download of large DFU firmware
- Support polling the status from device in dfuManifest state
- Use newer libxmlb features to properly display more AppStream markup

* Tue Aug 18 2020 Richard Hughes <richard@hughsie.com> 1.4.5-4
- Rebuild for the libxmlb API bump.

* Mon Aug 03 2020 Peter Jones <pjones@redhat.com> - 1.4.5-3
- Make dual signing happen.
  Related: CVE-2020-10713

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 30 2020 Richard Hughes <richard@hughsie.com> 1.4.5-1
- New upstream release
- Add dual-image feature for VL103 backup firmware
- Add more CCGX hybrid dock support
- Add support for a delayed activation flow for Thunderbolt
- Allow firmware to require specific features from front-end clients
- Be more defensive when remotes are missing required keys
- Check all AppStream components when verifying
- Check for free space after cleaning up ESP
- Fix TPM PCR0 calculation
- Modernize the thunderbolt plugin for future hardware
- Only show UpdateMessage when state is success
- Read the modem vendor ID correctly
- Set the runtime version to 0.0.0 for pre-1.0.0 Thelio Io firmware
- Support compiling libqmi-glib 1.26.0 and later
- Support LVFS::UpdateImage in GUI clients
- Use the GPIOB reset for the MiniDock VL103
- Wait for the root device to be replugged when updating the MSP430

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 10 2020 Richard Hughes <richard@hughsie.com> 1.4.4-1
- New upstream release
- Fix refreshing when checking for downgraded metadata

* Tue Jun 09 2020 Richard Hughes <richard@hughsie.com> 1.4.3-1
- New upstream release
- Add support for HP DMC dock devices
- Always enforce the metadata signature has a valid timestamp
- Capture the dock SKU in metadata
- Check the device requirements when returning from GetDetails
- Prevent Dell dock updates to occur via synaptics-mst plugin

* Fri May 22 2020 Richard Hughes <richard@hughsie.com> 1.4.2-2
- Backport a patch to fix the synaptics fingerprint reader update.

* Mon May 18 2020 Richard Hughes <richard@hughsie.com> 1.4.2-1
- New upstream release
- Add several more ATA OUI quirks
- Avoid communicating with DFU devices when bitManifestationTolerant is off
- Correct the display of final calculated PCRs
- Delay activation for Dell Thunderbolt updates
- Do not use synaptics-rmi on the Dell K12A
- Fix switching wacom-raw to bootloader mode
- Switch the default of EnumerateAllDevices to false
- Use GPIOB to reset the VL817 found in two Lenovo products

* Mon Apr 27 2020 Richard Hughes <richard@hughsie.com> 1.4.1-1
- New upstream release
- Allow specifying the device on the command line by GUID
- Correctly format firmware version of Dynabook X30 and X40
- Do not show safe mode errors for USB4 host controllers
- Do not show the USB 2 VLI recovery devices for USB 3 hubs
- Fix the correct DeviceID set by GetDetails
- Only update the FW2 partition of the ThinkPad USB-C Dock Gen2
- Prefer to update the child device first if the order is unspecified
- Refresh device name and format before setting supported flag
- Reset the progressbar time estimate if the percentage is invalid
- Set the CCGX device name and summary from quirk files
- Wait for the cxaudio device to reboot after writing firmware

* Tue Apr 14 2020 Richard Hughes <richard@hughsie.com> 1.4.0-1
- New upstream release
- Actually reload the DFU device after upgrade has completed
- Add plugin for CPU microcode
- Add plugin for Cypress CCGX hardware
- Add plugin for EP963x hardware
- Add STM32F745 DfuSe version quirk
- Allow server metadata to set the device name and version format
- Always check for 'PLAIN' when doing vercmp() operations
- Apply version format to releases and devices at same time
- Check the firmware requirements before adding 'SUPPORTED'
- Correctly attach VL103 after a firmware update
- Do not allow devices that have no vendor ID to be 'UPDATABLE'
- Do not use shim for non-secure boot configurations
- Export the device state, release creation time and urgency
- Fix a crash when removing device parents
- Fix a difficult-to-trigger daemon hang when replugging devices
- Fix a runtime error when detaching MSP430
- Fix CounterpartGuid when there is more than one supported device
- Fix reporting Synaptics cxaudio version number
- Introduce a new VersionFormat of 'hex'
- Load the signature to get the aliased CDN-safe version of the metadata
- Never add USB hub devices that are not upgradable
- Only auto-add counterpart GUIDs when required
- Parse the CSR firmware as a DFU file
- Set the protocol when updating logitech HID++ devices
- Use Jcat files in firmware archives and for metadata
- When TPM PCR0 measurements fail, query if secure boot is available and enabled

* Thu Mar 05 2020 Nicolas Mailhot <nim@fedoraproject.org> 1.3.9-2
- Rebuild against the new Gusb.

* Wed Mar 04 2020 Richard Hughes <richard@hughsie.com> 1.3.9-1
- New upstream release
- Added completion script for fish shell
- Always check for PLAIN when doing vercmp() operations
- Always return AppStream markup for remote agreements
- Apply UEFI capsule update even with single valid capsule
- Check the device protocol before de-duping devices
- Copy the version and format from donor device in get-details
- Correctly append the release to devices in `fwupdtool get-details`
- Decrease minimum battery requirement to 10%
- Discard the reason upgrades aren't available
- Do not fail loading in /etc/machine-id is not available
- Fix a critical warning when installing some firmware
- For the `get-details` command make sure to always show devices
- Inhibit all power management actions using logind when updating
- Set the MSP430 version format to pair
- Switch off the ATA verbose logging by default
- Use unknown for version format by default on get-details

* Thu Feb 13 2020 Richard Hughes <richard@hughsie.com> 1.3.8-1
- New upstream release
- Add an extra instance ID to disambiguate USB hubs
- Add a plugin to update PD controllers by Fresco Logic
- Correctly reset VL100 PD devices
- Do not rewrite BootOrder in the EFI helper
- Do not use vercmp when the device version format is plain
- Fix firmware regression in the EFI capsule helper
- Fix updating Synaptics MST devics with no PCI parent
- Ignore Unifying detach failures
- Make the cxaudio version match that of the existing Windows tools
- Replay the TPM event log to get the PCRx values
- Set up more parent devices for various Lenovo USB hubs
- Support the new gnuefi file locations
- Use the correct command to get the VLI device firmware version

* Fri Jan 31 2020 Richard Hughes <richard@hughsie.com> 1.3.7-1
- New upstream release
- Add 'get-remotes' and 'refresh' to fwupdtool
- Add support for standalone VIA PD devices
- Allow applying all releases to get to a target version
- Correctly delete UEFI variables
- Correctly import PKCS-7 remote metadata
- Discourage command line metadata refreshes more than once per day
- Do not always get the vendor ID for udev devices using the parent
- Get the list of updates in JSON format from fwupdagent
- Show the device parent if there is an interesting child
- Shut down automatically when there is system memory pressure
- Use a different protocol ID for VIA i2c devices
- Use the correct timeout for Logitech IO channel writes

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 30 2019 Richard Hughes <richard@hughsie.com> 1.3.6-1
- New upstream release
- Add a dell-bios version format to match what is shown on the vendor website
- Add a new plugin that exposes the TPM device
- Allow incremental version major and minor number for Synaptics Prometheus devices
- Clarify error messages when no upgrades are available
- Correct the default prompt for reboot/shutdown
- Do not expose bootloader version errors to users
- Enforce that device protocol matches the metadata value
- Export the device protocol and raw device version to the client --verbose output
- Fix the quirk for the legacy VIA 813 usbhub chip
- Only check the vendor ID if the device has one set
- Return exit status success if there is no firmware to be updated
- Set the correct vendor eMMC ID prefix
- Use the baseboard vendor as the superio vendor ID
- Use the BIOS vendor as the coreboot and flashrom vendor ID

* Fri Nov 29 2019 Richard Hughes <richard@hughsie.com> 1.3.5-1
- New upstream release
- Convert libfwupdprivate to a shared library libfwupdplugin
- Create a REV_00 instance ID as this may be what the vendor needs to target
- Improve coreboot version detection
- Invert default behavior to be safer for reboot and shutdown prompts
- Reload the Synaptics prometheus device version after update
- Use the correct unlocker when using GRWLock
- Whitelist VIA USB hub PD and I²C devices

* Fri Nov 22 2019 Richard Hughes <richard@hughsie.com> 1.3.4-1
- New upstream release
- Add support for Foxconn T77W968 and DW5821e eSIM
- Add support for matching firmware requirements on device parents
- Add support for writing VIA PD and I2C devices
- Add versions formats for the Microsoft Surface devices
- Correct Wacom panel HWID support
- Fix a fastboot regression when updating modem firmware
- Fix regression when coldplugging superio devices
- Fix the linking of the UEFI update binary
- Fix the vendor id of hidraw devices
- Make loading USB device strings non-fatal
- Reject invalid Synaptics MST chip IDs
- Skip cleanup after device is done updating if required

* Fri Nov 01 2019 Richard Hughes <richard@hughsie.com> 1.3.3-1
- New upstream release
- Add a plugin for systems running coreboot
- Add a plugin to update eMMC devices
- Add a plugin to update Synaptics RMI4 devices
- Add a plugin to update VIA USB hub hardware
- Add several quirks for Realtek webcams
- Add some success messages when CLI tasks have completed
- Add support for automatically uploading reports
- Add support for `fwupdmgr reinstall`
- Add support for the 8bitdo SN30Pro+
- Add support for the ThinkPad USB-C Dock Gen2 audio device
- Allow fwupdtool to dump details of common firmware formats
- Always report the update-error correctly for multiple updates
- Create a unique GUID for the Thunderbolt controller path
- Fix a regression for Wacom EMR devices
- Recognize new 'generation' Thunderbolt sysfs attribute for USB4
- Rework ESP path detection and lifecycle to auto-unmount when required
- Show a useful error for Logitech devices that cannot self-reset
- Use correct method for stopping systemd units
- Use device safety flags to show prompts before installing updates
- Use will-disappear flag for 8bitdo SF30/SN30 controllers
- Use XMLb to query quirks to reduce the RSS when running

* Tue Oct 08 2019 Richard Hughes <richard@hughsie.com> 1.3.2-2
- Manually create /var/cache/fwupd to work around #1757948

* Thu Sep 26 2019 Richard Hughes <richard@hughsie.com> 1.3.2-1
- New upstream release
- Add aliases for get-upgrades and upgrade
- Add support for Conexant audio devices
- Add support for the Minnowboard Turbot
- Add support for the SoloKey Secure
- Add support for the Thelio IO board
- Add support to integrate into the motd
- Allow disabling SSL strict mode for broken corporate proxies
- Allow filtering devices when using the command line tools
- Allow specifying a firmware GUID to check any version exists
- Be more accepting when trying to recover a failed database migration
- Display more helpful historical device information
- Do not ask the user to upload a report if ReportURI is not set
- Do not segfault when trying to quit the downgrade selection
- Ensure HID++ v2.0 peripheral devices get added
- Never show AppStream markup on the console
- Only write the new UEFI device path if different than before
- Partially rewrite the Synapticsmst plugin to support more hardware
- Print devices, remotes, releases using a tree
- Support issues in AppStream metadata
- Use tpm2-tss library to read PCR values

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Richard Hughes <richard@hughsie.com> 1.2.10-1
- New upstream release
- Add a specific error code for the low battery case
- Add support for 8bitdo USB Retro Receiver
- Export new API to build objects from GVariant blobs
- Fix installing synaptics-prometheus config updates
- Prompt for reboot when unlocking on the command line if applicable
- Show a warning when running in UEFI legacy mode
- Show devices with an UpdateError in get-devices output
- Support a UEFI quirk to disable the use of the UX capsule
- Support empty proxy server strings
- Try harder to find duplicate UEFI boot entries

* Mon May 20 2019 Richard Hughes <richard@hughsie.com> 1.2.9-1
- New upstream release
- Add support for Synaptics Prometheus fingerprint readers
- Check the daemon version is at least the client version
- Correctly identify DFU firmware that starts at offset zero
- Display the remote warning on the console in an easy-to-read way
- Export the version-format used by devices to clients
- Fix a libasan failure when reading a UEFI variable
- Never guess the version format from the version string
- Only use class-based instance IDs for quirk matching
- Prompt the user to shutdown if required when installing by ID
- Reset the forced version during DFU attach and detach
- Set the version format for more device types

* Tue Apr 23 2019 Richard Hughes <richard@hughsie.com> 1.2.8-1
- New upstream release
- Allow the fwupdmgr tool to modify the daemon config
- Correctly parse DFU interfaces with extra vendor-specific data
- Do not report transient or invalid system failures
- Fix problems with the version format checking for some updates

* Wed Apr 17 2019 Richard Hughes <richard@hughsie.com> 1.2.7-3
- Revert a patch from upstream that was causing problems with Dell hardware

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 1.2.7-2
- Rebuild with Meson fix for #1699099

* Thu Apr 11 2019 Richard Hughes <richard@hughsie.com> 1.2.7-1
- New upstream release
- Add a component categories to express the firmware type
- Add support for 8BitDo M30
- Add support for the not-child extension from Logitech
- Blacklist the synapticsmst plugin when using amdgpu
- Correct ATA activation functionality to work for all vendors
- Implement QMI PDC active config selection for modems
- Make an error message clearer when there are no updates available
- Match the old or new version number when setting NEEDS_REBOOT
- More carefully check the output from tpm2_pcrlist
- Recreate the history database if migration failed
- Require AC power when updating Thunderbolt devices
- Require --force to install a release with a different version format
- Shut down the daemon if the on-disk binary is replaced

* Wed Mar 27 2019 Richard Hughes <richard@hughsie.com> 1.2.6-2
- Enable the ModemManager plugin

* Tue Mar 26 2019 Richard Hughes <richard@hughsie.com> 1.2.6-1
- New upstream release
- Add support for delayed activation of docks and ATA devices
- Add support for reading the SuperIO device checksum and writing to e-flash
- Add the fwupdagent binary for use in shell scripts
- Allow restricting firmware updates for enterprise use
- Allow running offline updates when in system-update.target
- Allow signing the fwupd report with a client certificate
- Ask to reboot after scheduling an offline firmware update
- Correctly check the new version for devices that replug
- Do not fail to start the daemon if tpm2_pcrlist hangs
- Do not fail when scheduling more than one update to be run offline
- Do not schedule an update on battery power if it requires AC power
- Include all device checksums in the LVFS report
- Rename the shimx64.efi binary for known broken firmware
- Upload the UPDATE_INFO entry for the UEFI UX capsule
- Use Plymouth when updating offline firmware

* Mon Feb 25 2019 Richard Hughes <richard@hughsie.com> 1.2.5-1
- New upstream release
- Allow a device to be updated using more than one plugin
- Call composite prepare and cleanup using fwupdtool
- Detect and special case Dell ATA hardware
- Fix flashing failure with latest Intuos Pro tablet
- Fix potential segfault when applying UEFI updates
- Fix unifying regression when recovering from failed flash
- Report the DeviceInstanceIDs from fwupdmgr when run as root

* Tue Feb 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.4-2
- Remove obsolete scriptlets

* Fri Feb 01 2019 Richard Hughes <richard@hughsie.com> 1.2.4-1
- New upstream release
- Add a directory remote that generates metadata
- Add a plugin to update Wacom embedded EMR and AES panels
- Add a plugin to upgrade firmware on ATA-ATAPI hardware
- Add a quirk to use the legacy bootmgr description
- Add SuperIO IT89xx device support
- Add support for Dell dock passive flow
- Add the needs-shutdown quirk to Phison NVMe drives
- Add 'update' and 'get-updates' commands to fwupdtool
- Allow Dell dock flashing Thunderbolt over I2C
- Check the battery percentage before flashing
- Correct Nitrokey Storage invalid firmware version read
- Do not check the BGRT status before uploading a UX capsule
- Do the UEFI UX checksum calculation in fwupd
- Fix flashing various Jabra devices
- Fix the parser to support extended segment addresses
- Flash the fastboot partition after downloading the file
- Show a console warning if loading an out-of-tree plugin
- Show a per-release source and details URL
- Show a `UpdateMessage` and display it in tools
- Support FGUID to get the SKU GUID for NVMe hardware

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 04 2019 Richard Hughes <richard@hughsie.com> 1.2.3-1
- New upstream release
- Correctly migrate the history database

* Sun Dec 30 2018 Richard Hughes <richard@hughsie.com> 1.2.2-1
- New upstream release
- Add support for devices that support fastboot
- Add more standard USB identifier GUIDs
- Add the PCR0 value as the device checksum for system firmware
- Add Dell TB18DC to the supported devices list
- Allow replacing the last byte in the image when using 'dfu-tool replace-data'
- Append the UEFI capsule header in userspace rather than in the loader
- Check the device checksum as well as the content checksum during verify
- Correctly parse format the version numbers correctly using old metadata
- Fix a crash if AMT returns an empty response
- Fix a regression when doing GetReleases on unsupported hardware
- Remove the Wacom DTH generation hardware from the whitelist
- Sanitize the version if the version format has been specified

* Tue Nov 27 2018 Richard Hughes <richard@hughsie.com> 1.2.1-1
- New upstream release
- Add per-release install duration values
- Fix a use-after-free when using --immediate-exit
- Fix flashing the 8bitdo SF30
- Fix showing the custom remote agreements
- Include the os-release information in the release metadata
- Shut down the daemon after 2h of inactivity when possible
- Speed up startup by loading less thunderbolt firmware
- Speed up startup by using a silo index for GUID queries
- Use less memory and fragment the heap less when starting

* Wed Nov 07 2018 Richard Hughes <richard@hughsie.com> 1.2.0-1
- New upstream release
- Add a standalone installer creation script
- Add version format quirks for several Lenovo machines
- Adjust synapticsmst EVB board handling
- Allow setting the version format from a quirk entry
- Port from libappstream-glib to libxmlb for a large reduction in RSS
- Set the full AMT device version including the BuildNum
- Sort the firmware sack by component priority
- Stop any running daemon over dbus when using fu-tool
- Support the Intel ME version format
- Use HTTPS_PROXY if set

* Fri Oct 12 2018 Richard Hughes <richard@hughsie.com> 1.1.3-1
- New upstream release
- Add a plugin for an upcoming Dell USB-C dock
- Add support for devices to show an estimated flash time
- Add support for Realtek USB devices using vendor HID and HUB commands
- Adjust panamera ESM update routine for some reported issues
- Allow firmware files to depend on versions from other devices
- Check the amount of free space on the ESP before upgrading
- Don't show devices pending a reboot in GetUpgrades
- Fix possible crash in the thunderbolt-power plugin
- Make various parts of the daemon thread-safe
- Redirect all debugging output to stderr instead of stdout
- Run the Dell plugin initialization after the UEFI plugin
- Update all sub-devices for a composite update

* Mon Sep 10 2018 Richard Hughes <richard@hughsie.com> 1.1.2-1
- New upstream release
- Add a new plugin to enumerate EC firmware
- Add a new plugin to update NVMe hardware
- Allow updating just one specific device from the command line
- Always use the same HardwareIDs as Windows
- Download firmware if the user specifies a URI
- Implement the systemd recommendations for offline updates
- Improve performance when reading keys from the quirk database
- Rewrite the unifying plugin to use the new daemon-provided functionality
- Show a time estimate on the progressbar after an update has started

* Mon Aug 13 2018 Richard Hughes <richard@hughsie.com> 1.1.1-1
- New upstream release
- Add support for the Synaptics Panamera hardware
- Add validation for Alpine and Titan Ridge
- Allow flashing unifying devices in recovery mode
- Allow running synapticsmst on non-Dell hardware
- Check the ESP for sanity at at startup
- Do not hold hidraw devices open forever
- Fix a potential segfault in smbios data parsing
- Fix encoding the GUID into the capsule EFI variable
- Fix various bugs when reading the thunderbolt version number
- Improve the Redfish plugin to actually work with real hardware
- Reboot synapticsmst devices at the end of flash cycle
- Show the correct title when updating devices

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Richard Hughes <richard@hughsie.com> 1.1.0-2
- Rebuild to get the EFI executable signed with the Red Hat key

* Wed Jul 11 2018 Richard Hughes <richard@hughsie.com> 1.1.0-1
- New upstream release
- Add a initial Redfish support
- Allow devices to assign a plugin from the quirk subsystem
- Detect the EFI system partition location at runtime
- Do not use 8bitdo bootloader commands after a successful flash
- Fix a potential buffer overflow when applying a DFU patch
- Fix downgrading older releases to devices
- Fix flashing devices that require a manual replug
- Fix unifying failure to detach when using a slow host controller
- Merge fwupdate functionality into fwupd
- Support more Wacom tablets

* Thu Jun 07 2018 Richard Hughes <richard@hughsie.com> 1.0.8-1
- New upstream release
- Adjust all licensing to be 100% LGPL 2.1+
- Add a firmware diagnostic tool called fwupdtool
- Add an plugin to update some future Wacom tablets
- Add support for Motorola S-record files
- Add the Linux Foundation public GPG keys for firmware and metadata
- Allow installing more than one firmware using 'fwupdmgr install'
- Allow specifying hwids with OR relationships
- Fix a potential DoS in libdfu by limiting holes to 1MiB
- Fix Hardware-ID{0,1,2,12} compatibility with Microsoft
- Hide devices that aren't updatable by default in fwupdmgr
- Stop matching Nintendo Switch Pro in the 8bitdo plugin

* Mon Apr 30 2018 Richard Hughes <richard@hughsie.com> 1.0.7-1
- New upstream release
- Add enable-remote and disable-remote commands to fwupdmgr
- Allow requiring specific versions of libraries for firmware updates
- Don't recoldplug thunderbolt to fix a flashing failure
- Fix SQL error when running 'fwupdmgr clear-offline'
- Only enumerate Dell Docks if the type is known
- Reboot after scheduling using logind not systemd
- Show a warning with interactive prompt when enabling a remote

* Mon Mar 12 2018 Richard Hughes <richard@hughsie.com> 1.0.6-1
- New upstream release
- Add bash completion for fwupdmgr
- Add support for newest Thunderbolt chips
- Allow devices to use the runtime version when in bootloader mode
- Allow overriding ESP mount point via conf file
- Correct handling of unknown Thunderbolt devices
- Correctly detect new remotes that are manually copied
- Delete any old fwupdate capsules and efivars when launching fwupd
- Fix a crash related to when passing device to downgrade in CLI
- Fix Unifying signature writing and parsing for Texas bootloader
- Generate Vala bindings

* Fri Feb 23 2018 Richard Hughes <richard@hughsie.com> 1.0.5-2
- Use the new CDN for metadata.

* Wed Feb 14 2018 Richard Hughes <richard@hughsie.com> 1.0.5-1
- New upstream release
- Be more careful deleting and modifying device history
- Fix crasher with MST flashing
- Fix DFU detach with newer releases of libusb
- Offer to reboot when processing an offline update
- Show the user a URL when they report a known problem
- Stop matching 8bitdo DS4 controller VID/PID
- Support split cabinet archives as produced by Windows Update

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Richard Hughes <richard@hughsie.com> 1.0.4-1
- New upstream release
- Add a device name for locked UEFI devices
- Add D-Bus methods to get and modify the history information
- Allow the user to share firmware update success or failure
- Ask the user to refresh metadata when it is very old
- Never add two devices to the daemon with the same ID
- Rescan supported flags when refreshing metadata
- Store firmware update success and failure to a local database

* Fri Jan 12 2018 Richard Hughes <richard@hughsie.com> 1.0.3-2
- Backport a patch that fixes applying firmware updates using gnome-software.

* Tue Jan 09 2018 Richard Hughes <richard@hughsie.com> 1.0.3-1
- New upstream release
- Add a new plugin to add support for CSR "Driverless DFU"
- Add initial SF30/SN30 Pro support
- Block owned Dell TPM updates
- Choose the correct component from provides matches using requirements
- Do not try to parse huge compressed archive files
- Handle Thunderbolt "native" mode
- Use the new functionality in libgcab >= 1.0 to avoid writing temp files

* Tue Nov 28 2017 Richard Hughes <richard@hughsie.com> 1.0.2-1
- New upstream release
- Add a plugin for the Nitrokey Storage device
- Add quirk for AT32UC3B1256 as used in the RubberDucky
- Add support for the original AVR DFU protocol
- Allow different plugins to claim the same device
- Disable the dell plugin if libsmbios fails
- Fix critical warning when more than one remote fails to load
- Ignore useless Thunderbolt device types
- Set environment variables to allow easy per-plugin debugging
- Show a nicer error message if the requirement fails
- Sort the output of GetUpgrades correctly
- Use a SHA1 hash for the internal DeviceID

* Thu Nov 09 2017 Kalev Lember <klember@redhat.com> 1.0.1-3
- Rebuild against libappstream-glib 0.7.4

* Thu Nov 09 2017 Kalev Lember <klember@redhat.com> 1.0.1-2
- Fix libdfu obsoletes versions

* Thu Nov 09 2017 Richard Hughes <richard@hughsie.com> 1.0.1-1
- New upstream release
- Add support for HWID requirements
- Add support for programming various AVR32 and XMEGA parts using DFU
- Add the various DFU quirks for the Jabra Speak devices
- Catch invalid Dell dock component requests
- Correctly output Intel HEX files with > 16bit offset addresses
- Do not try to verify the element write if upload is unsupported
- Fix a double-unref when updating any 8Bitdo device
- Fix uploading large firmware files over DFU
- Format the BCD USB revision numbers correctly
- Guess the DFU transfer size if it is not specified
- Include the reset timeout as wValue to fix some DFU bootloaders
- Move the database of supported devices out into runtime loaded files
- Support devices with truncated DFU interface data
- Use the correct wDetachTimeOut when writing DFU firmware
- Verify devices with legacy VIDs are actually 8Bitdo controllers

* Mon Oct 09 2017 Richard Hughes <richard@hughsie.com> 1.0.0-1
- New upstream release
- This release breaks API and ABI to remove deprecated symbols
- libdfu is now not installed as a shared library
- Add FuDeviceLocker to simplify device open/close lifecycles
- Add functionality to blacklist Dell HW with problems
- Disable the fallback USB plugin
- Do not fail to load the daemon if cached metadata is invalid
- Do not use system-specific infomation for UEFI PCI devices
- Fix various printing issues with the progressbar
- Never fallback to an offline update from client code
- Only set the Dell coldplug delay when we know we need it
- Parse the SMBIOS v2 and v3 DMI tables directly
- Support uploading the UEFI firmware splash image
- Use the intel-wmi-thunderbolt kernel module to force power

* Fri Sep 01 2017 Richard Hughes <richard@hughsie.com> 0.9.7-1
- New upstream release
- Add a FirmwareBaseURI parameter to the remote config
- Add a firmware builder that uses bubblewrap
- Add a python script to create fwupd compatible cab files from .exe files
- Add a thunderbolt plugin for new kernel interface
- Fix an incomplete cipher when using XTEA on data not in 4 byte chunks
- Show a bouncing progress bar if the percentage remains at zero
- Use the new bootloader PIDs for Unifying pico receivers

* Fri Sep 01 2017 Kalev Lember <klember@redhat.com> 0.9.6-2
- Disable i686 UEFI support now that fwupdate is no longer available there
- Enable aarch64 UEFI support now that all the deps are available there

* Thu Aug 03 2017 Richard Hughes <richard@hughsie.com> 0.9.6-1
- New upstream release
- Add --version option to fwupdmgr
- Display all errors recorded by efi_error tracing
- Don't log a warning when an unknown unifying report is parsed
- Fix a hang on 32 bit machines
- Make sure the unifying percentage completion goes from 0% to 100%
- Support embedded devices with local firmware metadata
- Use new GUsb functionality to fix flashing Unifying devices

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 04 2017 Richard Hughes <richard@hughsie.com> 0.9.5-1
- New upstream release
- Add a plugin to get the version of the AMT ME interface
- Allow flashing Unifying devices in bootloader modes
- Filter by Unifying SwId when making HID++2.0 requests
- Fix downgrades when version_lowest is set
- Fix the self tests when running on PPC64 big endian
- Use the UFY DeviceID prefix for Unifying devices

* Thu Jun 15 2017 Richard Hughes <richard@hughsie.com> 0.9.4-1
- New upstream release
- Add installed tests that use the daemon
- Add the ability to restrict firmware to specific vendors
- Compile with newer versions of meson
- Fix a common crash when refreshing metadata
- Generate a images for status messages during system firmware update
- Show progress download when refreshing metadata
- Use the correct type signature in the D-Bus introspection file

* Wed Jun 07 2017 Richard Hughes <richard@hughsie.com> 0.9.3-1
- New upstream release
- Add a 'downgrade' command to fwupdmgr
- Add a 'get-releases' command to fwupdmgr
- Add support for Microsoft HardwareIDs
- Allow downloading metadata from more than just the LVFS
- Allow multiple checksums on devices and releases
- Correctly open Unifying devices with original factory firmware
- Do not expect a Unifying reply when issuing a REBOOT command
- Do not re-download firmware that exists in the cache
- Fix a problem when testing for a Dell system
- Fix flashing new firmware to 8bitdo controllers

* Tue May 23 2017 Richard Hughes <richard@hughsie.com> 0.9.2-2
- Backport several fixes for updating Unifying devices

* Mon May 22 2017 Richard Hughes <richard@hughsie.com> 0.9.2-1
- New upstream release
- Add support for Unifying DFU features
- Do not spew a critial warning when parsing an invalid URI
- Ensure steelseries device is closed if it returns an invalid packet
- Ignore spaces in the Unifying version prefix

* Thu Apr 20 2017 Richard Hughes <richard@hughsie.com> 0.8.2-1
- New upstream release
- Add a config option to allow runtime disabling plugins by name
- Add DFU quirk for OpenPICC and SIMtrace
- Create directories in /var/cache as required
- Fix the Requires lines in the dfu pkg-config file
- Only try to mkdir the localstatedir if we have the right permissions
- Support proxy servers in fwupdmgr

* Thu Mar 23 2017 Bastien Nocera <bnocera@redhat.com> - 0.8.1-2
+ fwupd-0.8.1-2
- Release claimed devices on error, fixes unusable input devices

* Mon Feb 27 2017 Richard Hughes <richard@hughsie.com> 0.8.1-1
- New upstream release
- Adjust systemd confinement restrictions
- Don't initialize libsmbios on unsupported systems
- Fix a crash when enumerating devices

* Wed Feb 08 2017 Richard Hughes <richard@hughsie.com> 0.8.0-1
- New upstream release
- Add support for Intel Thunderbolt devices
- Add support for Logitech Unifying devices
- Add support for Synaptics MST cascades hubs
- Add support for the Altus-Metrum ChaosKey device
- Always close USB devices before error returns
- Return the pending UEFI update when not on AC power
- Use a heuristic for the start address if the firmware has no DfuSe footer
- Use more restrictive settings when running under systemd

* Sat Dec 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.7.5-2
- Rebuild for gpgme 1.18

* Wed Oct 19 2016 Richard Hughes <richard@hughsie.com> 0.7.5-1
- New upstream release
- Add quirks for HydraBus as it does not have a DFU runtime
- Don't create the UEFI dummy device if the unlock will happen on next boot
- Fix an assert when unlocking the dummy ESRT device
- Fix writing firmware to devices using the ST reference bootloader
- Match the Dell TB16 device

* Mon Sep 19 2016 Richard Hughes <richard@hughsie.com> 0.7.4-1
- New upstream release
- Add a fallback for older appstream-glib releases
- Allow the argument to 'dfu-tool set-release' be major.minor
- Fix a possible crash when uploading firmware files using libdfu
- Fix libfwupd self tests when a host-provided fwupd is not available
- Load the Altos USB descriptor from ELF files
- Show the human-readable version in the 'dfu-tool dump' output
- Support writing the IHEX symbol table
- Write the ELF files with the correct section type

* Mon Aug 29 2016 Kalev Lember <klember@redhat.com> 0.7.3-2
- Fix an unexpanded macro in the spec file
- Tighten libebitdo-devel requires with the _isa macro
- Add ldconfig scripts for libdfu and libebitdo subpackages

* Mon Aug 29 2016 Richard Hughes <richard@hughsie.com> 0.7.3-1
- New upstream release
- Add Dell TPM and TB15/WD15 support via new Dell provider
- Add initial ELF reading and writing support to libdfu
- Add support for installing multiple devices from a CAB file
- Allow providers to export percentage completion
- Don't fail while checking versions or locked state
- Show a progress notification when installing firmware
- Show the vendor flashing instructions when installing
- Use a private gnupg key store
- Use the correct firmware when installing a composite device

* Fri Aug 19 2016 Peter Jones <pjones@redhat.com> - 0.7.2-6
- Rebuild to get libfwup.so.1 as our fwupdate dep.  This should make this the
  last time we need to rebuild for this.

* Wed Aug 17 2016 Peter Jones <pjones@redhat.com> - 0.7.2-5
- rebuild against new efivar and fwupdate

* Fri Aug 12 2016 Adam Williamson <awilliam@redhat.com> - 0.7.2-4
- rebuild against new efivar and fwupdate

* Thu Aug 11 2016 Richard Hughes <richard@hughsie.com> 0.7.2-3
- Use the new CDN for firmware metadata

* Thu Jul 14 2016 Kalev Lember <klember@redhat.com> - 0.7.2-2
- Tighten subpackage dependencies

* Mon Jun 13 2016 Richard Hughes <richard@hughsie.com> 0.7.2-1
- New upstream release
- Allow devices to have multiple assigned GUIDs
- Allow metainfo files to match only specific revisions of devices
- Only claim the DFU interface when required
- Only return updatable devices from GetDevices()
- Show the DFU protocol version in 'dfu-tool list'

* Fri May 13 2016 Richard Hughes <richard@hughsie.com> 0.7.1-1
- New upstream release
- Add device-added, device-removed and device-changed signals
- Add for a new device field "Flashes Left"
- Fix a critical warning when restarting the daemon
- Fix BE issues when reading and writing DFU files
- Make the device display name nicer
- Match the AppStream metadata after a device has been added
- Return all update descriptions newer than the installed version
- Set the device description when parsing local firmware files

* Fri Apr 01 2016 Richard Hughes <richard@hughsie.com> 0.7.0-1
- New upstream release
- Add Alienware to the version quirk table
- Add a version plugin for SteelSeries hardware
- Do not return updates that require AC when on battery
- Return the device flags when getting firmware details

* Mon Mar 14 2016 Richard Hughes <richard@hughsie.com> 0.6.3-1
- New upstream release
- Add an unlock method for devices
- Add ESRT enable method into UEFI provider
- Correct the BCD version number for DFU 1.1
- Ignore the DFU runtime on the DW1820A
- Only read PCI OptionROM firmware when devices are manually unlocked
- Require AC power before scheduling some types of firmware update

* Fri Feb 12 2016 Richard Hughes <richard@hughsie.com> 0.6.2-1
- New upstream release
- Add 'Created' and 'Modified' properties on managed devices
- Fix get-results for UEFI provider
- Support vendor-specific UEFI version encodings

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Richard Hughes <richard@hughsie.com> 0.6.1-1
- New upstream release
- Do not misdetect different ColorHug devices
- Only dump the profiling data when run with --verbose

* Mon Dec 07 2015 Richard Hughes <richard@hughsie.com> 0.6.0-1
- New upstream release
- Add support for automatically updating USB DFU-capable devices
- Emit the changed signal after doing an update
- Export the AppStream ID when returning device results
- Use the same device identification string format as Microsoft

* Wed Nov 18 2015 Richard Hughes <richard@hughsie.com> 0.5.4-1
- New upstream release
- Use API available in fwupdate 0.5 to avoid writing temp files
- Fix compile error against fwupdate 0.5 due to API bump

* Thu Nov 05 2015 Richard Hughes <richard@hughsie.com> 0.5.3-1
- New upstream release
- Avoid seeking when reading the file magic during refresh
- Do not assume that the compressed XML data will be NUL terminated
- Use the correct user agent string for fwupdmgr

* Wed Oct 28 2015 Richard Hughes <richard@hughsie.com> 0.5.2-1
- New upstream release
- Add the update description to the GetDetails results
- Clear the in-memory firmware store only after parsing a valid XML file
- Ensure D-Bus remote errors are registered at fwupdmgr startup
- Fix verify-update to produce components with the correct provide values
- Show the dotted-decimal representation of the UEFI version number
- Support cabinet archives files with more than one firmware

* Mon Sep 21 2015 Richard Hughes <richard@hughsie.com> 0.5.1-1
- Update to 0.5.1 to fix a bug in the offline updater

* Tue Sep 15 2015 Richard Hughes <richard@hughsie.com> 0.5.0-1
- New upstream release
- Do not reboot if racing with the PackageKit offline update mechanism

* Thu Sep 10 2015 Richard Hughes <richard@hughsie.com> 0.1.6-3
- Do not merge the existing firmware metadata with the submitted files

* Thu Sep 10 2015 Kalev Lember <klember@redhat.com> 0.1.6-2
- Own system-update.target.wants directory
- Make fwupd-sign obsoletes versioned

* Thu Sep 10 2015 Richard Hughes <richard@hughsie.com> 0.1.6-1
- New upstream release
- Add application metadata when getting the updates list
- Remove fwsignd, we have the LVFS now

* Fri Aug 21 2015 Kalev Lember <klember@redhat.com> 0.1.5-3
- Disable fwupd offline update service

* Wed Aug 19 2015 Richard Hughes <richard@hughsie.com> 0.1.5-2
- Use the non-beta download URL prefix

* Wed Aug 12 2015 Richard Hughes <richard@hughsie.com> 0.1.5-1
- New upstream release
- Add a Raspberry Pi firmware provider
- Fix validation of written firmware
- Make parsing the option ROM runtime optional
- Use the AppStream 0.9 firmware specification by default

* Sat Jul 25 2015 Richard Hughes <richard@hughsie.com> 0.1.4-1
- New upstream release
- Actually parse the complete PCI option ROM
- Add a 'fwupdmgr update' command to update all devices to latest versions
- Add a simple signing server that operates on .cab files
- Add a 'verify' command that verifies the cryptographic hash of device firmware

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Richard Hughes <richard@hughsie.com> 0.1.3-2
- Compile with libfwupdate for UEFI firmware support.

* Thu May 28 2015 Richard Hughes <richard@hughsie.com> 0.1.3-1
- New upstream release
- Coldplug the devices before acquiring the well known name
- Run the offline actions using systemd when required
- Support OpenHardware devices using the fwupd vendor extensions

* Wed Apr 22 2015 Richard Hughes <richard@hughsie.com> 0.1.2-1
- New upstream release
- Only allow signed firmware to be upgraded without a password

* Mon Mar 23 2015 Richard Hughes <richard@hughsie.com> 0.1.1-1
- New upstream release
- Add a 'get-updates' command to fwupdmgr
- Add and document the offline-update lifecycle
- Create a libfwupd shared library
- Create runtime directories if they do not exist
- Do not crash when there are no devices to return

* Mon Mar 16 2015 Richard Hughes <richard@hughsie.com> 0.1.0-1
- First release
