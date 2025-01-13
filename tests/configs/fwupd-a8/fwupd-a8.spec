%global glib2_version 2.45.8
%global libxmlb_version 0.1.3
%global libgusb_version 0.2.11
%global libcurl_version 7.61.0
%global systemd_version 231
%global json_glib_version 1.1.1
%global fwupdplugin_version 5

# although we ship a few tiny python files these are utilities that 99.99%
# of users do not need -- use this to avoid dragging python onto CoreOS
%global __requires_exclude ^%{python3}$

# PPC64 is too slow to complete the tests under 3 minutes...
%ifnarch ppc64le
%global enable_tests 1
%endif

%global enable_dummy 1
%global __meson_wrap_mode default

# fwupd.efi is only available on these arches
%ifarch x86_64 aarch64
%global have_uefi 1
%endif

%ifarch i686 x86_64
%global have_msr 1
%endif

# libsmbios is only available on x86
%ifarch x86_64
%global have_dell 1
%endif

# only available recently
%if 0%{?fedora} >= 34 || 0%{?rhel} >= 9
%global have_modem_manager 1
%endif

Summary:   Firmware update daemon
Name:      fwupd
Version:   1.7.8
Release:   2%{?dist}
License:   LGPLv2+
URL:       https://github.com/fwupd/fwupd
Source0:   http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
Source1:   http://people.freedesktop.org/~hughsient/releases/libjcat-0.1.9.tar.xz
Source2:   http://people.freedesktop.org/~hughsient/releases/fwupd-efi-1.3.tar.xz

Source10:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20100307-x64.cab
Source11:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20140413-x64.cab
Source12:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20160809-x64.cab
Source13:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20200729-aa64.cab
Source14:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20200729-ia32.cab
Source15:  http://people.redhat.com/rhughes/dbx/DBXUpdate-20200729-x64.cab

# these are numbered high just to keep them wildly away from colliding with
# the real package sources, in order to reduce churn.
Source300:   redhatsecurebootca3.cer
Source301:   redhatsecureboot301.cer
Source500:   redhatsecurebootca5.cer
Source503:   redhatsecureboot503.cer

Patch1:    0001-redfish-Set-the-permissions-of-redfish.conf-at-insta.patch
Patch2:    0002-redfish-Only-create-users-using-IPMI-when-we-know-it.patch
Patch3:    0003-Never-save-the-Redfish-passwords-to-a-file-readable-.patch
Patch4:    0001-Use-usr-libexec-platform-python-for-RHEL.patch

BuildRequires: efi-srpm-macros
BuildRequires: gettext
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libxmlb-devel >= %{libxmlb_version}
BuildRequires: libgcab1-devel
BuildRequires: libgudev1-devel
BuildRequires: libgusb-devel >= %{libgusb_version}
BuildRequires: libcurl-devel >= %{libcurl_version}
BuildRequires: polkit-devel >= 0.103
BuildRequires: sqlite-devel
BuildRequires: gpgme-devel
BuildRequires: systemd >= %{systemd_version}
BuildRequires: systemd-devel
BuildRequires: libarchive-devel
BuildRequires: gobject-introspection-devel
BuildRequires: gcab
%ifarch %{valgrind_arches}
BuildRequires: valgrind
BuildRequires: valgrind-devel
%endif
BuildRequires: gtk-doc
BuildRequires: gnutls-devel
BuildRequires: gnutls-utils
BuildRequires: meson
BuildRequires: help2man
BuildRequires: json-glib-devel >= %{json_glib_version}
BuildRequires: vala
BuildRequires: bash-completion
BuildRequires: git-core

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
BuildRequires: pesign
%endif

%if 0%{?have_dell}
BuildRequires: efivar-devel >= 33
BuildRequires: libsmbios-devel >= 2.3.0
%endif

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: glib2%{?_isa} >= %{glib2_version}
Requires: libxmlb%{?_isa} >= %{libxmlb_version}
Requires: libgusb%{?_isa} >= %{libgusb_version}
Requires: bubblewrap
Requires: shared-mime-info

Obsoletes: fwupd-sign < 0.1.6
Obsoletes: libebitdo < 0.7.5-3
Obsoletes: libdfu < 1.0.0
Obsoletes: fwupd-labels < 1.1.0-1

Obsoletes: dbxtool < 9
Provides: dbxtool

%if 0%{?rhel} > 7
Obsoletes: fwupdate < 13
Obsoletes: fwupdate-efi < 13

Provides: fwupdate
Provides: fwupdate-efi
%endif

# optional, but a really good idea
Recommends: udisks2

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

%prep
%autosetup -p1

mkdir -p subprojects/libjcat
tar xfvs %{SOURCE1} -C subprojects/libjcat --strip-components=1

mkdir -p subprojects/fwupd-efi
tar xfvs %{SOURCE2} -C subprojects/fwupd-efi --strip-components=1

sed -ri '1s=^#!/usr/bin/(env )?python3=#!%{__python3}=' \
        contrib/ci/*.py \
        contrib/firmware_packager/*.py \
        contrib/*.py \
        contrib/standalone-installer/assets/*.py \
        contrib/standalone-installer/*.py \
        libfwupdplugin/*.py \
        plugins/dfu/contrib/*.py \
        plugins/uefi-capsule/make-images.py \
        po/test-deps

%build

# allow rh-signing-tools package for RHEL-8
export RHEL_ALLOW_PYTHON2_FOR_BUILD=1

%meson \
    -Ddocs=gtkdoc \
    -Dlvfs=disabled \
    -Defi_os_dir=%{efi_vendor} \
    -Dlibjcat:gtkdoc=false \
    -Dlibjcat:introspection=false \
    -Dlibjcat:tests=false \
%if 0%{?enable_tests}
    -Dtests=true \
%else
    -Dtests=false \
%endif
%if 0%{?enable_dummy}
    -Dplugin_dummy=true \
%else
    -Dplugin_dummy=false \
%endif
    -Dplugin_flashrom=false \
%if 0%{?have_msr}
    -Dplugin_msr=true \
%else
    -Dplugin_msr=false \
%endif
    -Dplugin_thunderbolt=true \
%if 0%{?have_uefi}
    -Dplugin_uefi_capsule=true \
    -Dplugin_uefi_pk=false \
%ifarch x86_64
    -Dfwupd-efi:efi_sbat_distro_id="rhel" \
    -Dfwupd-efi:efi_sbat_distro_summary="Red Hat Enterprise Linux" \
    -Dfwupd-efi:efi_sbat_distro_pkgname="%{name}" \
    -Dfwupd-efi:efi_sbat_distro_version="%{version}" \
    -Dfwupd-efi:efi_sbat_distro_url="mail:secalert@redhat.com" \
    -Dfwupd-efi:efi-libdir="/usr/lib64" \
%endif
    -Dplugin_tpm=false \
%else
    -Dplugin_uefi_capsule=false \
    -Dplugin_uefi_pk=false \
    -Dplugin_tpm=false \
%endif
%if 0%{?have_dell}
    -Dplugin_dell=true \
    -Dplugin_synaptics_mst=true \
%else
    -Dplugin_dell=false \
    -Dplugin_synaptics_mst=false \
%endif
%if 0%{?have_modem_manager}
    -Dplugin_modem_manager=true \
%else
    -Dplugin_modem_manager=false \
%endif
    -Dplugin_logitech_bulkcontroller=false \
    -Dman=true \
    -Dbluez=false \
    -Dplugin_cfu=false \
    -Dplugin_mtd=false \
    -Dplugin_powerd=false \
    -Dplugin_uf2=false \
    -Dsupported_build=true

%meson_build

%if 0%{?enable_tests}
%check
%meson_test
%endif

%install
%meson_install

# on RHEL the LVFS is disabled by default
mkdir -p %{buildroot}/%{_datadir}/dbxtool
install %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{buildroot}/%{_datadir}/dbxtool

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
%systemd_post fwupd.service

# change vendor-installed remotes to use the default keyring type
for fn in /etc/fwupd/remotes.d/*.conf; do
    if grep -q "Keyring=gpg" "$fn"; then
        sed -i 's/Keyring=gpg/#Keyring=pkcs/g' "$fn";
    fi
done

%preun
%systemd_preun fwupd.service

%postun
%systemd_postun_with_restart fwupd.service
%systemd_postun_with_restart pesign.service

%files -f %{name}.lang
%doc README.md AUTHORS
%license COPYING
%config(noreplace)%{_sysconfdir}/fwupd/daemon.conf
%if 0%{?have_uefi}
%config(noreplace)%{_sysconfdir}/fwupd/uefi_capsule.conf
%endif
%config(noreplace)%{_sysconfdir}/fwupd/redfish.conf
%config(noreplace)%{_sysconfdir}/fwupd/thunderbolt.conf
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
%if 0%{?have_uefi}
%{_bindir}/dbxtool
%endif
%{_bindir}/fwupdmgr
%{_bindir}/fwupdtool
%{_bindir}/fwupdagent
%{_bindir}/jcat-tool
%dir %{_sysconfdir}/fwupd
%dir %{_sysconfdir}/fwupd/remotes.d
%if 0%{?have_dell}
%config(noreplace)%{_sysconfdir}/fwupd/remotes.d/dell-esrt.conf
%endif
%config(noreplace)%{_sysconfdir}/fwupd/remotes.d/lvfs.conf
%config(noreplace)%{_sysconfdir}/fwupd/remotes.d/lvfs-testing.conf
%config(noreplace)%{_sysconfdir}/fwupd/remotes.d/vendor.conf
%config(noreplace)%{_sysconfdir}/fwupd/remotes.d/vendor-directory.conf
%config(noreplace)%{_sysconfdir}/pki/fwupd
%{_sysconfdir}/pki/fwupd-metadata
%if 0%{?have_msr}
/usr/lib/modules-load.d/fwupd-msr.conf
%config(noreplace)%{_sysconfdir}/fwupd/msr.conf
%endif
%{_datadir}/dbus-1/system.d/org.freedesktop.fwupd.conf
%{_datadir}/bash-completion/completions/fwupdmgr
%{_datadir}/bash-completion/completions/fwupdtool
%{_datadir}/bash-completion/completions/fwupdagent
%{_datadir}/fish/vendor_completions.d/fwupdmgr.fish
%{_datadir}/fwupd/metainfo/org.freedesktop.fwupd*.metainfo.xml
%if 0%{?have_dell}
%{_datadir}/fwupd/remotes.d/dell-esrt/metadata.xml
%endif
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
%{_mandir}/man1/fwupdtool.1*
%{_mandir}/man1/fwupdagent.1*
%{_mandir}/man1/dfu-tool.1*
%if 0%{?have_uefi}
%{_mandir}/man1/dbxtool.*
%endif
%{_mandir}/man1/fwupdmgr.1*
%if 0%{?have_uefi}
%{_mandir}/man1/fwupdate.1*
%endif
%{_mandir}/man1/jcat-tool.1*
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
%{_presetdir}/fwupd-refresh.preset
%{_unitdir}/system-update.target.wants/
%dir %{_localstatedir}/lib/fwupd
%dir %{_localstatedir}/cache/fwupd
%dir %{_datadir}/fwupd/quirks.d
%{_datadir}/fwupd/quirks.d/*.quirk
%{_datadir}/doc/fwupd/builder/README.md
%if 0%{?have_uefi}
%{_sysconfdir}/grub.d/35_fwupd
%endif
%{_libdir}/libfwupd.so.2*
%{_libdir}/libfwupdplugin.so.%{fwupdplugin_version}*
%{_libdir}/libjcat.so.*
%{_libdir}/girepository-1.0/Fwupd-2.0.typelib
%{_libdir}/girepository-1.0/FwupdPlugin-1.0.typelib
/usr/lib/udev/rules.d/*.rules
/usr/lib/systemd/system-shutdown/fwupd.shutdown
%dir %{_libdir}/fwupd-plugins-%{fwupdplugin_version}
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_acpi_dmar.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_acpi_facp.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_acpi_phat.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_amt.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_analogix.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_ata.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_bcm57xx.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_ccgx.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_colorhug.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_cros_ec.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_cpu.so
%if 0%{?have_dell}
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_dell.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_dell_esrt.so
%endif
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_dell_dock.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_dfu.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_dfu_csr.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_ebitdo.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_elantp.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_elanfp.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_emmc.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_ep963x.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_fastboot.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_fresco_pd.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_genesys.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_hailuck.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_iommu.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_jabra.so
%if 0%{?have_uefi}
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_lenovo_thinklmi.so
%endif
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_linux_lockdown.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_linux_sleep.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_linux_swap.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_linux_tainted.so
%if 0%{?have_msr}
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_msr.so
%endif
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_nitrokey.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_nordic_hid.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_nvme.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_optionrom.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_parade_lspcon.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_pci_bcr.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_pci_mei.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_pixart_rf.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_realtek_mst.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_redfish.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_rts54hid.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_rts54hub.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_scsi.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_steelseries.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_superio.so
%if 0%{?have_dell}
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_synaptics_mst.so
%endif
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_synaptics_cape.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_synaptics_cxaudio.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_synaptics_prometheus.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_synaptics_rmi.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_system76_launch.so
%if 0%{?enable_dummy}
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_test.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_invalid.so
%endif
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_thelio_io.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_thunderbolt.so
%if 0%{?have_uefi}
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_bios.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_uefi_capsule.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_uefi_dbx.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_uefi_recovery.so
%endif
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_usi_dock.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_logind.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_logitech_hidpp.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_upower.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_vli.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_wacom_raw.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_wacom_usb.so
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_goodixmoc.so
%ghost %{_localstatedir}/lib/fwupd/gnupg

%if 0%{?have_modem_manager}
%{_libdir}/fwupd-plugins-%{fwupdplugin_version}/libfu_plugin_modem_manager.so
%endif
%if 0%{?have_uefi}
%{_datadir}/fwupd/uefi-capsule-ux.tar.xz
%endif

%files devel
%{_datadir}/gir-1.0/Fwupd-2.0.gir
%{_datadir}/gir-1.0/FwupdPlugin-1.0.gir
%{_datadir}/gtk-doc/html/fwupd
%{_datadir}/vala/vapi
%{_includedir}/fwupd-1
%{_includedir}/libjcat-1
%{_libdir}/libfwupd*.so
%{_libdir}/libjcat.so
%{_libdir}/pkgconfig/fwupd.pc
%{_libdir}/pkgconfig/fwupdplugin.pc
%if 0%{?have_uefi}
%{_libdir}/pkgconfig/fwupd-efi.pc
%endif
%{_libdir}/pkgconfig/jcat.pc

%files tests
%if 0%{?enable_tests}
%dir %{_datadir}/installed-tests/fwupd
%{_datadir}/installed-tests/fwupd/tests/*
%{_datadir}/installed-tests/fwupd/fwupd-tests.xml
%{_datadir}/installed-tests/fwupd/*.test
%{_datadir}/installed-tests/fwupd/*.cab
%{_datadir}/installed-tests/fwupd/*.sh
%if 0%{?have_uefi}
%{_datadir}/installed-tests/fwupd/efi
%endif
%{_datadir}/fwupd/device-tests/*.json
%{_libexecdir}/installed-tests/fwupd/*
%dir %{_sysconfdir}/fwupd/remotes.d
%config(noreplace)%{_sysconfdir}/fwupd/remotes.d/fwupd-tests.conf
%endif

%changelog
* Mon Feb 20 2023 Richard Hughes <richard@hughsie.com> 1.7.8-2
- Backport the Redfish security fixes which affect IDRAC.
- Resolves: rhbz#2170950

* Wed Jun 15 2022 Richard Hughes <richard@hughsie.com> 1.7.8-1
- New upstream release
- Resolves: rhbz#2095668

* Thu Jan 13 2022 Richard Hughes <richard@hughsie.com> 1.7.4-1
- Include support for Lenovo TBT4 Docking stations
- Do not cause systemd-modules-load failures
- Resolves: rhbz#2038258
- Resolves: rhbz#2037294

* Thu Dec 09 2021 Richard Hughes <richard@hughsie.com> 1.7.1-2
- Disable the Logitech bulkcontroller plugin to avoid adding a dep to protobuf-c
  which lives in AppStream, not BaseOS.
- Resolves: rhbz#2029333

* Mon Nov 01 2021 Richard Hughes <richard@hughsie.com> 1.7.1-1
- New upstream release
- Backport upstream changes
- Include support for Dell TBT4 Docking stations
- Resolves: rhbz#1969472
- Resolves: rhbz#1976408

* Tue Apr 13 2021 Richard Hughes <richard@hughsie.com> 1.5.9-3
- Rebase to include the SBAT metadata section to allow fixing BootHole
- Resolves: rhbz#1933012
- Resolves: rhbz#1932953
- Resolves: rhbz#1932909
- Resolves: rhbz#1932882
- Resolves: rhbz#1932579
- Resolves: rhbz#1932553
- Resolves: rhbz#1932423

* Wed Feb 10 2021 Richard Hughes <richard@hughsie.com> 1.5.5-3
- Backport a fix from upstream to fix a crash in the Goodix MOC plugin.
- Resolves: #1927091

* Tue Feb 09 2021 Richard Hughes <richard@hughsie.com> 1.5.5-2
- Do not invalidate all remote timestamps during package install to fix rpm -V.
- Backport some important high priority fixes from upstream.
- Resolves: #1926382

* Mon Jan 11 2021 Richard Hughes <richard@hughsie.com> 1.5.5-1
- Rebase package to include support for latest OEM hardware and to
  support deploying UEFI SecureBoot dbx updates.
- Resolves: #1870811

* Wed Dec 16 2020 Richard Hughes <richard@hughsie.com> 1.5.4-1
- Rebase package to include support for latest OEM hardware and to
  support deploying UEFI SecureBoot dbx updates.
- Resolves: #1870811

* Fri Jul 24 2020 Peter Jones <pjones@redhat.com> - 1.4.2-4
- Add signing with redhatsecureboot503 cert
  Related: CVE-2020-10713

* Thu Jul 23 2020 Richard Hughes <richard@hughsie.com> 1.4.2-3
- Obsolete the now-dead fwupdate package to prevent file conflicts
- Resolves: #1859202

* Fri Jun 05 2020 Richard Hughes <richard@hughsie.com> 1.4.2-2
- Security fix for CVE-2020-10759
- Resolves: #1844324

* Mon May 18 2020 Richard Hughes <richard@hughsie.com> 1.4.2-1
- New upstream release
- Backport a patch to fix the synaptics fingerprint reader update.
- Resolves: #1775277

* Mon Apr 27 2020 Richard Hughes <richard@hughsie.com> 1.4.1-1
- New upstream release
- Resolves: #1775277

* Wed Feb 19 2020 Richard Hughes <richard@hughsie.com> 1.1.4-6
- Rebuild to get the EFI executable signed with the Red Hat key
- Resolves: #1713033

* Thu Feb 13 2020 Richard Hughes <richard@hughsie.com> 1.1.4-5
- Backport a patch to specify the EFI os name
- Resolves: #1713033

* Fri Nov 29 2019 Richard Hughes <richard@hughsie.com> 1.1.4-4
- Rebuild to get the EFI executable signed with the Red Hat key
- Resolves: #1680154

* Fri Nov 29 2019 Richard Hughes <richard@hughsie.com> 1.1.4-3
- Disable wacomhid by default as probing the device stops the tablet working
- Resolves: #1680154

* Mon Nov 25 2019 Richard Hughes <richard@hughsie.com> 1.1.4-2
- Do not require python3 in the base package
- Resolves: #1724593

* Wed Nov 07 2018 Richard Hughes <richard@hughsie.com> 1.1.4-1
- New upstream release
- Use HTTPS_PROXY if set
- Make the dell-dock plugin more robust in several ways
- Adjust EVB board handling
- Resolves: #1647557

* Fri Oct 12 2018 Richard Hughes <richard@hughsie.com> 1.1.3-1
- New upstream release
- Adds support for an upcoming Dell USB-C dock
- Don't use an obsolete font when building the UEFI images
- Resolves: #1607842

* Wed Oct 10 2018 Richard Hughes <richard@hughsie.com> 1.1.1-11
- Rebuild to get the EFI executable signed with the Red Hat key
- Related: #1614424

* Fri Sep 28 2018 Brendan Reilly <breilly@redhat.com> 1.1.1-10
- Rebuild
- Related: #1614424

* Thu Sep 20 2018 Brendan Reilly <breilly@redhat.com> 1.1.1-9
- Rebuild
- Related: #1614424

* Tue Sep 18 2018 Tomas Mlcoch <tmlcoch@hughsie.com> 1.1.1-8
- Rebuild
- Related: #1614424

* Tue Sep 04 2018 Richard Hughes <richard@hughsie.com> 1.1.1-7
- Rebuild to get the EFI executable signed with the Red Hat key
- Related: #1614424

* Fri Aug 31 2018 Richard Hughes <richard@hughsie.com> 1.1.1-6
- Include the certificates for secure boot signing

* Wed Aug 29 2018 Richard Hughes <richard@hughsie.com> 1.1.1-5
- Include the certificates for secure boot signing

* Tue Aug 23 2018 Richard Hughes <richard@hughsie.com> 1.1.1-4
- Rebuild to get the EFI executable signed with the Red Hat key

* Thu Aug 23 2018 Richard Hughes <richard@hughsie.com> 1.1.1-3
- Rebuild to get the EFI executable signed with the Red Hat key

* Mon Aug 20 2018 Richard Hughes <richard@hughsie.com> 1.1.1-2
- Rebuild to get the EFI executable signed with the Red Hat key

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

* Fri Aug  3 2018 Florian Weimer <fweimer@redhat.com> - 1.1.0-3
- Honor %%{valgrind_arches}

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

* Wed Jun 20 2018 Tomas Orsava <torsava@redhat.com> - 1.0.6-2
- Switch hardcoded python3 shebangs into the %%{__python3} macro
- Add missing BuildRequires on python3-devel so that %%{__python3} macro is
  defined

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
