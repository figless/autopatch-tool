Summary: Graphical system installer
Name:    anaconda
Version: 33.16.10.5
Release: 1%{?dist}
License: GPLv2+ and MIT
URL:     http://fedoraproject.org/wiki/Anaconda

# To generate Source0 do:
# git clone https://github.com/rhinstaller/anaconda
# git checkout -b archive-branch anaconda-%%{version}-%%{release}
# ./autogen.sh
# make dist
Source0: %{name}-%{version}.tar.bz2

# Versions of required components (done so we make sure the buildrequires
# match the requires versions of things).

%if ! 0%{?rhel}
%define blivetguiver 2.1.12-1
%endif
%define dbusver 1.2.3
%define dnfver 3.6.0
%define dracutver 034-7
%define fcoeutilsver 1.0.12-3.20100323git
%define gettextver 0.19.8
%define gtk3ver 3.22.17
%define helpver 22.1-1
%define isomd5sum 1.0.10
%define langtablever 0.0.49
%define libarchivever 3.0.4
%define libblockdevver 2.1
%define libtimezonemapver 0.4.1-2
%define libxklavierver 5.4
%define mehver 0.23-1
%define nmver 1.0
%define pykickstartver 3.16.16-1
%define pypartedver 2.5-2
%define rpmver 4.10.0
%define simplelinever 1.1.3-1
%define utillinuxver 2.15.1
%define dasbusver 0.4

BuildRequires: audit-libs-devel
BuildRequires: libtool
BuildRequires: gettext-devel >= %{gettextver}
BuildRequires: gtk3-devel >= %{gtk3ver}
BuildRequires: gtk-doc
BuildRequires: gtk3-devel-docs >= %{gtk3ver}
BuildRequires: glib2-doc
BuildRequires: gobject-introspection-devel
BuildRequires: glade-devel
BuildRequires: libgnomekbd-devel
BuildRequires: libxklavier-devel >= %{libxklavierver}
BuildRequires: make
BuildRequires: pango-devel
BuildRequires: python3-kickstart >= %{pykickstartver}
BuildRequires: python3-devel
BuildRequires: python3-nose
BuildRequires: systemd
# rpm and libarchive are needed for driver disk handling
BuildRequires: rpm-devel >= %{rpmver}
BuildRequires: libarchive-devel >= %{libarchivever}
%ifarch s390 s390x
BuildRequires: s390utils-devel
%endif
BuildRequires: libtimezonemap-devel >= %{libtimezonemapver}

# Tools used by the widgets resource bundle generation
BuildRequires: gdk-pixbuf2-devel
BuildRequires: libxml2

Requires: anaconda-core = %{version}-%{release}
Requires: anaconda-gui = %{version}-%{release}
Requires: anaconda-tui = %{version}-%{release}
Requires: anaconda-install-env-deps = %{version}-%{release}

%description
The anaconda package is a metapackage for the Anaconda installer.

%package core
Summary: Core of the Anaconda installer
Requires: python3-libs
Requires: python3-dnf >= %{dnfver}
Requires: python3-blivet >= 1:3.4.0-12
Requires: python3-blockdev >= %{libblockdevver}
Requires: python3-meh >= %{mehver}
Requires: libreport-anaconda >= 2.0.21-1
Requires: libselinux-python3
Requires: rpm-python3 >= %{rpmver}
Requires: python3-pyparted >= %{pypartedver}
Requires: python3-requests
Requires: python3-requests-file
Requires: python3-requests-ftp
Requires: python3-kickstart >= %{pykickstartver}
Requires: python3-langtable >= %{langtablever}
Requires: util-linux >= %{utillinuxver}
Requires: python3-gobject-base
Requires: python3-dbus
Requires: python3-pwquality
Requires: python3-systemd
Requires: python3-productmd
Requires: python3-dasbus >= %{dasbusver}
Requires: flatpak-libs
%if %{defined rhel} && %{undefined centos}
Requires: python3-syspurpose
Requires: subscription-manager >= 1.28.33
%endif

# pwquality only "recommends" the dictionaries it needs to do anything useful,
# which is apparently great for containers but unhelpful for the rest of us
Requires: cracklib-dicts

Requires: python3-pytz
Requires: teamd
%ifarch s390 s390x
Requires: openssh
%endif
Requires: NetworkManager >= %{nmver}
Requires: NetworkManager-libnm >= %{nmver}
Requires: NetworkManager-team
Requires: kbd
Requires: chrony
Requires: python3-ntplib
Requires: systemd
Requires: python3-pid
Requires: python3-ordered-set >= 2.0.0

# Required by the systemd service anaconda-fips.
Requires: crypto-policies
Requires: /usr/bin/update-crypto-policies

# required because of the rescue mode and VNC question
Requires: anaconda-tui = %{version}-%{release}

# Make sure we get the en locale one way or another
Requires: glibc-langpack-en

# anaconda literally runs its own dbus-daemon, so it needs this,
# even though the distro default is dbus-broker in F30+
Requires: dbus-daemon

# Ensure it's not possible for a version of grubby to be installed
# that doesn't work with btrfs subvolumes correctly...
Conflicts: grubby < 8.40-10

Obsoletes: anaconda-images <= 10
Provides: anaconda-images = %{version}-%{release}
Obsoletes: anaconda-runtime < %{version}-%{release}
Provides: anaconda-runtime = %{version}-%{release}
Obsoletes: booty <= 0.107-1

%description core
The anaconda-core package contains the program which was used to install your
system.

%package live
Summary: Live installation specific files and dependencies
BuildRequires: desktop-file-utils
# live installation currently implies a graphical installation
Requires: anaconda-gui = %{version}-%{release}
Requires: usermode
Requires: zenity

%description live
The anaconda-live package contains scripts, data and dependencies required
for live installations.

%package install-env-deps
Summary: Installation environment specific dependencies
Requires: udisks2-iscsi
Requires: libblockdev-plugins-all >= %{libblockdevver}
# active directory/freeipa join support
Requires: realmd
Requires: isomd5sum >= %{isomd5sum}
%ifarch %{ix86} x86_64
Requires: fcoe-utils >= %{fcoeutilsver}
%endif
# likely HFS+ resize support
%ifarch %{ix86} x86_64
%if ! 0%{?rhel}
Requires: hfsplus-tools
%endif
%endif
# kexec support
Requires: kexec-tools
Requires: createrepo_c
# run's on TTY1 in install env
Requires: tmux
# install time crash handling
Requires: gdb
Requires: rsync

%description install-env-deps
The anaconda-install-env-deps metapackage lists all installation environment dependencies.
This makes it possible for packages (such as Initial Setup) to depend on the main Anaconda package without
pulling in all the install time dependencies as well.

%package gui
Summary: Graphical user interface for the Anaconda installer
Requires: anaconda-core = %{version}-%{release}
Requires: anaconda-widgets = %{version}-%{release}
Requires: python3-meh-gui >= %{mehver}
Requires: adwaita-icon-theme
Requires: tigervnc-server-minimal
Requires: libxklavier >= %{libxklavierver}
Requires: libgnomekbd
Requires: libtimezonemap >= %{libtimezonemapver}
Requires: nm-connection-editor
Requires: keybinder3
%ifnarch s390 s390x
Requires: NetworkManager-wifi
%endif
Requires: anaconda-user-help >= %{helpver}
Requires: yelp
%if ! 0%{?rhel}
Requires: blivet-gui-runtime >= %{blivetguiver}
%endif
Requires: system-logos

# Needed to compile the gsettings files
BuildRequires: gsettings-desktop-schemas
BuildRequires: metacity

%description gui
This package contains graphical user interface for the Anaconda installer.

%package tui
Summary: Textual user interface for the Anaconda installer
Requires: anaconda-core = %{version}-%{release}
Requires: python3-simpleline >= %{simplelinever}

%description tui
This package contains textual user interface for the Anaconda installer.

%package widgets
Summary: A set of custom GTK+ widgets for use with anaconda
Requires: %{__python3}

%description widgets
This package contains a set of custom GTK+ widgets used by the anaconda installer.

%package widgets-devel
Summary: Development files for anaconda-widgets
Requires: glade
Requires: %{name}-widgets%{?_isa} = %{version}-%{release}

%description widgets-devel
This package contains libraries and header files needed for writing the anaconda
installer.  It also contains Python and Glade support files, as well as
documentation for working with this library.

%package dracut
Summary: The anaconda dracut module
Requires: dracut >= %{dracutver}
Requires: dracut-network
Requires: dracut-live
Requires: xz
Requires: python3-kickstart

%description dracut
The 'anaconda' dracut module handles installer-specific boot tasks and
options. This includes driver disks, kickstarts, and finding the anaconda
runtime on NFS/HTTP/FTP servers or local disks.

%prep
%autosetup -p 1

%build
# use actual build-time release number, not tarball creation time release number
%configure ANACONDA_RELEASE=%{release}
%{__make} %{?_smp_mflags}

%install
%{make_install}
find %{buildroot} -type f -name "*.la" | xargs %{__rm}

# Create an empty directory for addons
mkdir %{buildroot}%{_datadir}/anaconda/addons

# required for live installations
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/liveinst.desktop

# If no langs found, keep going
%find_lang %{name} || :


# main package and install-env-deps are metapackages
%files

%files install-env-deps

# Allow the lang file to be empty
%define _empty_manifest_terminate_build 0

%files core -f %{name}.lang
%license COPYING
%{_unitdir}/*
%{_prefix}/lib/systemd/system-generators/*
%{_bindir}/instperf
%{_bindir}/anaconda-disable-nm-ibft-plugin
%{_sbindir}/anaconda
%{_sbindir}/handle-sshpw
%{_datadir}/anaconda
%{_prefix}/libexec/anaconda
%exclude %{_datadir}/anaconda/gnome
%exclude %{_datadir}/anaconda/pixmaps
%exclude %{_datadir}/anaconda/ui
%exclude %{_datadir}/anaconda/window-manager
%exclude %{_datadir}/anaconda/anaconda-gtk.css
%exclude %{_prefix}/libexec/anaconda/dd_*
%{python3_sitearch}/pyanaconda
%exclude %{python3_sitearch}/pyanaconda/rescue.py*
%exclude %{python3_sitearch}/pyanaconda/__pycache__/rescue.*
%exclude %{python3_sitearch}/pyanaconda/ui/gui/*
%exclude %{python3_sitearch}/pyanaconda/ui/tui/*
%{_bindir}/analog
%{_bindir}/anaconda-cleanup
%dir %{_sysconfdir}/%{name}
%config %{_sysconfdir}/%{name}/*
%dir %{_sysconfdir}/%{name}/conf.d
%config %{_sysconfdir}/%{name}/conf.d/*
%dir %{_sysconfdir}/%{name}/product.d
%config %{_sysconfdir}/%{name}/product.d/*

%files live
%{_bindir}/liveinst
%{_sbindir}/liveinst
%config(noreplace) %{_sysconfdir}/pam.d/*
%config(noreplace) %{_sysconfdir}/security/console.apps/*
%{_libexecdir}/liveinst-setup.sh
%{_datadir}/applications/*.desktop
%{_datadir}/anaconda/gnome
%{_sysconfdir}/xdg/autostart/*.desktop

%files gui
%{python3_sitearch}/pyanaconda/ui/gui/*
%{_datadir}/anaconda/pixmaps
%{_datadir}/anaconda/ui
%if 0%{?rhel}
# Remove blivet-gui
%exclude %{_datadir}/anaconda/ui/spokes/blivet_gui.*
%exclude %{python3_sitearch}/pyanaconda/ui/gui/spokes/blivet_gui.*
%endif
%{_datadir}/anaconda/window-manager
%{_datadir}/anaconda/anaconda-gtk.css

%files tui
%{python3_sitearch}/pyanaconda/rescue.py
%{python3_sitearch}/pyanaconda/__pycache__/rescue.*
%{python3_sitearch}/pyanaconda/ui/tui/*

%files widgets
%{_libdir}/libAnacondaWidgets.so.*
%{_libdir}/girepository*/AnacondaWidgets*typelib
%{python3_sitearch}/gi/overrides/*

%files widgets-devel
%{_libdir}/libAnacondaWidgets.so
%{_libdir}/glade/modules/libAnacondaWidgets.so
%{_includedir}/*
%{_datadir}/glade/catalogs/AnacondaWidgets.xml
%{_datadir}/gtk-doc

%files dracut
%dir %{_prefix}/lib/dracut/modules.d/80%{name}
%{_prefix}/lib/dracut/modules.d/80%{name}/*
%{_prefix}/libexec/anaconda/dd_*

%changelog
* Tue Mar 05 2024 Radek Vykydal <rvykydal@redhat.com> - 33.16.10.5-1
- Update translations
  Resolves: RHEL-24836

* Fri Feb 16 2024 Jiri Konecny <jkonecny@redhat.com> - 33.16.10.4-1
- Lower log file permission in /tmp (jkonecny)
  Resolves: RHEL-23344
- Add utility function to set file mode (jkonecny)
  Related: RHEL-23344

* Wed Feb 07 2024 Martin Kolman <mkolman@redhat.com> - 33.16.10.3-1
- Fixed file-write operation to a public directory (ataf)
  Resolves: RHEL-23344

* Tue Jan 23 2024 Martin Kolman <mkolman@redhat.com> - 33.16.10.2-1
- Propagate a lazy proxy of the storage model (vponcova)
  Resolves: RHEL-16276
- rescue: Don't allow to mount systems without a root device (vponcova)
  Resolves: RHEL-4784

* Wed Dec 13 2023 Jiri Konecny <jkonecny@redhat.com> - 33.16.10.1-1
- timezone: for kickstart allow also timezones not offered by GUI (rvykydal)
  Resolves: RHEL-13151
  Resolves: RHEL-4795
- Rename Organization to Organization ID on subscription screen (mkolman)
  Resolves: RHEL-11168

* Mon Sep 18 2023 Jiri Konecny <jkonecny@redhat.com> - 33.16.9.5-1
- [ja_JP] - Need to update string on anaconda screen for installation completed
  Resolves: rhbz#2216746

* Wed Aug 09 2023 Jiri Konecny <jkonecny@redhat.com> - 33.16.9.4-1
- iscsi: Allow changing iSCSI initiator name once set (vtrefny)
  Resolves: rhbz#2223980

* Tue Jul 11 2023 Jiri Konecny <jkonecny@redhat.com> - 33.16.9.3-1
- Be more indulgent when reclaiming disk space (jstodola)
  Resolves: rhbz#1855371
- Do not print error on inst.ks=cdrom|hd (jkonecny)
  Resolves: rhbz#2211857

* Mon Jun 12 2023 Vladimír Slávik <vslavik@redhat.com> - 33.16.9.2-1
- Stop infinite wait for CDROM when KS is processed (jkonecny)
  Resolves: rhbz#2209602
- Apply --noverifyssl option for liveimg kickstart command (jstodola)
  Resolves: rhbz#1886985
- Change driver_updates exit info messages to debug (jkonecny)
  Related: rhbz#2154904

* Thu May 11 2023 Radek Vykydal <rvykydal@redhat.com> - 33.16.9.1-1
- driver_updates: migrate driver_updates.py to pep8 format (jkonecny)
  Related: rhbz#2154904
- driver_updates: adding tests for the new logging solution (jkonecny)
  Related: rhbz#2154904
- driver_updates: add lot of debug logs for easier debugging (jkonecny)
  Related: rhbz#2154904
- driver_updates: extend where we print log messages (jkonecny)
  Resolves: rhbz#2154904
- Add DNS search and ignore options from kickstart (vslavik)
  Resolves: rhbz#1656662
- Add DNS search and ignore options from kickstart (vslavik)
  Resolves: rhbz#1656662
- Add missing documentation about OEMDRV (jkonecny)
  Related: rhbz#1770969
- oemdrv: wait up to 5 seconds for disks to be handled (rmetrich)
  Resolves: rhbz#1770969

* Fri Mar 17 2023 Martin Kolman <mkolman@redhat.com> - 33.16.8.9-1
- Update translations
  Resolves: rhbz#2139689

* Thu Feb 09 2023 Jiri Konecny <jkonecny@redhat.com> - 33.16.8.8-1
- Update outdated translations

* Thu Feb 02 2023 Jiri Konecny <jkonecny@redhat.com> - 33.16.8.7-1
- Report registration errors from kickstart (mkolman)
  Resolves: rhbz#2127072
- Make text in custom_storage_helper more accurate (ozobal)
  Resolves: rhbz#2063288

* Mon Jan 09 2023 Jiri Konecny <jkonecny@redhat.com> - 33.16.8.6-1
- payload: fix repo --includepkgs option (rvykydal)
  Resolves: rhbz#2014103
- bootloader/zipl.py: update for zipl >= 2.25.0 (dan)
  Resolves: rhbz#2157917

* Tue Jan 03 2023 Jiri Konecny <jkonecny@redhat.com> - 33.16.8.5-1
- Delegate auto-attach handling to RHSM (mkolman)
  Resolves: rhbz#2083318
- Test the InstallerStorage.copy method (vponcova)
  Related: rhbz#1913035
- Show multiple bootloader devices on the Manual Partitioning screen (vponcova)
  Resolves: rhbz#1913035
- Implement the Root.copy method (vponcova)
  Related: rhbz#1913035
- Redefine the Blivet.roots attribute (vponcova)
  Related: rhbz#1913035
- Redefine the Blivet.copy method (vponcova)
  Related: rhbz#1913035
- Use correct hint for VNC password boot option (jstodola)
  Resolves: rhbz#2125679

* Tue Nov 29 2022 Radek Vykydal <rvykydal@redhat.com> - 33.16.8.4-1
- Disable the concurrency check in the error dialog in TUI (vponcova)
  Resolves: rhbz#1807491
- Support bond device activated in initramfs from kickstart (rvykydal)
  Resolves: rhbz#1940919

* Wed Nov 09 2022 Martin Kolman <mkolman@redhat.com> - 33.16.8.3-1
- network: commit changes synchronously when dumping autoconnections (rvykydal)
  Related: rhbz#2127057
- Initialize empty disks on the Manual Partitioning screen (vponcova)
  Resolves: rhbz#2094977
- infra: Set test vars from templates (vslavik)
- infra: Port check for matching templates from master (vslavik)
- infra: Port templating mechanism from master (vslavik)
- dracut: read filename dhcp option from dhcpopts file (rvykydal)
  Related: rhbz#1991516

* Thu Oct 27 2022 Martin Kolman <mkolman@redhat.com> - 33.16.8.2-1
- network: remove activate_connection_sync (rvykydal)
  Related: rhbz#2127057
- network: use new NM client in ConsolidateInitramfsConnetionsTask (rvykydal)
  Related: rhbz#2127057
- network: use new NM client instance in SetRealOnbootValuesTask (rvykydal)
  Related: rhbz#2127057
- network: add tests for sync_call_glib (rvykydal)
  Related: rhbz#2127057
- network: use separate main conext for NM client in threads (rvykydal)
  Related: rhbz#2127057
- network: split add_and_activate_connection_sync function (rvykydal)
  Related: rhbz#2127057
- network: add NM connections synchronously (rvykydal)
  Related: rhbz#2127057
- infra: Use the Bugzilla API key in the `makebumpver` script (vponcova)
- infra: Remove Jenkins from makebumpver (vslavik)

* Wed Sep 14 2022 Vendula Poncova <vponcova@redhat.com> - 33.16.8.1-1
- Do not crash on network --device link with wireless device (rvykydal)
  Resolves: rhbz#2125270

* Thu Aug 04 2022 Vladimir Slavik <vslavik@redhat.com> - 33.16.7.10-1
- Disable the Unregister button during unregistration (mkolman)
  Resolves: rhbz#2068195
- Install rdma-core if infiniband network device is found (rvykydal)
  Resolves: rhbz#2050356

* Wed Jul 20 2022 Jiri Konecny <jkonecny@redhat.com> - 33.16.7.9-1
- Add tooltip to the Insights checkbox (jkonecny)
  Resolves: rhbz#2069178
- Increase the minimal suggested size for /boot (vslavik)
  Resolves: rhbz#1844423

* Thu Jul 14 2022 Martin Kolman <mkolman@redhat.com> - 33.16.7.8-1
- Allow to omit WWPN and LUN for NPIV-enabled zFCP devices (jstodola)
  Resolves: rhbz#1497086
- Reduce the width of the zFCP dialog (jstodola)
  Related: rhbz#1497086

* Tue Jun 28 2022 Radek Vykydal <rvykydal@redhat.com> - 33.16.7.7-1
- bootloader: do not consider non-ibft iscsi disk as usable for bootloader
  (rvykydal)
  Resolves: rhbz#2002629

* Thu Jun 16 2022 Radek Vykydal <rvykydal@redhat.com> - 33.16.7.6-1
- dnf: apply the /etc/dnf/dnf.conf configuration file in the installer
  (rvykydal)
  Resolves: rhbz#1899494

* Fri Jun 10 2022 Radek Vykydal <rvykydal@redhat.com> - 33.16.7.5-1
- Report registration errors from kickstart (mkolman)
  Resolves: rhbz#2000650
- GUI: Show the dialog for a missing passphrase in an enlight box (vponcova)
  Related: rhbz#2029101
- GUI: Ask for a missing passphrase during automated installations (vponcova)
  Resolves: rhbz#2029101
- Create functions for a missing passphrase in pyanaconda.ui.lib (vponcova)
  Related: rhbz#2029101
- Add missing period when concatenating password error strings (jkonecny)
  Resolves: rhbz#2075419

* Wed Jun 01 2022 Radek Vykydal <rvykydal@redhat.com> - 33.16.7.4-1
- Check if the mount point exists before calling statvfs (vponcova)
  Resolves: rhbz#1826760

* Thu May 26 2022 Radek Vykydal <rvykydal@redhat.com> - 33.16.7.3-1
- Cleanup unneeded NFS repo with rd.live.ram parameter (mmatsuya)
  Resolves: rhbz#1970726
- Fix root password and LUKS passphrase visibility toggle (mkolman)
  Resolves: rhbz#1885879

* Tue May 24 2022 Radek Vykydal <rvykydal@redhat.com> - 33.16.7.2-1
- Run restorecon in chroot when handling home dirs (vslavik)
  Resolves: rhbz#2069305

* Thu Mar 10 2022 Radek Vykydal <rvykydal@redhat.com> - 33.16.7.1-1
- ovirt: move /var/tmp and /var/crash to own partition (sbonazzo)
  Resolves: rhbz#2060376

* Wed Feb 23 2022 Vendula Poncova <vponcova@redhat.com> - 33.16.6.6-1
- Bump subscription-manager version (mkolman)
  Related: rhbz#1968574
- Improve UX in Simple Content Access mode (mkolman)
  Resolves: rhbz#1968574
- Add IsSimpleContentAccessEnabled property (mkolman)
  Related: rhbz#1968574
- Add support for SCA mode detection from registration data (mkolman)
  Related: rhbz#1968574

* Tue Jan 04 2022 Martin Kolman <mkolman@redhat.com> - 33.16.6.5-1
- Fix the status of the root configuration screen (vponcova)
  Related: rhbz#1981807
- Fix the condition for entering the root configuration (vponcova)
  Related: rhbz#1981807
- Fix the condition for completing the root configuration (vponcova)
  Resolves: rhbz#1981807

* Fri Nov 26 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.6.4-1
- Wait for all background threads to finish before filling installation task
  queue (mkolman)
  Resolves: rhbz#1824422

* Fri Nov 05 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.6.3-1
- Fix application of network --mtu kickstart option in Anaconda (rvykydal)
  Resolves: rhbz#2018301
- Configure the multilib policy of the target system (vponcova)
  Resolves: rhbz#1571727
- network: apply kickstart network --nodefroute also from stage2 (rvykydal)
  Resolves: rhbz#1990145

* Wed Oct 20 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.6.2-1
- Make network spoke GUI more robust in cases of missing NM Client. (rvykydal)
  Resolves: rhbz#2003115
- Do not crash on missing NM Client on --vnc installations (rvykydal)
  Related: rhbz#2003115
- In installer environment set static, not transient hostname (rvykydal)
  Resolves: rhbz#1975349
- Add product config for AlmaLinux (andrew.lukoshko)
  Resolves: rhbz#2003692
- Fix creation of user account with empty password (mkolman)
  Resolves: rhbz#1687315

* Thu Sep 30 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.6.1-1
- Payload should wait for all storage related threads to finish (mkolman)
  Resolves: rhbz#2007615
- Remove misleading warning about inst.ks.device replacing ksdevice (rvykydal)
  Resolves: rhbz#2002722

* Mon Aug 02 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.5.4-1
- Disable anaconda-core's requirement on subscription-manager on CentOS (carl)
  Resolves: rhbz#1984958
- Show suggestions for an error caused by inconsistent sector sizes (vponcova)
  Resolves: rhbz#1935722
- Use a custom stylesheet to define CentOS-specific stylesheet data (carl)
  Related: rhbz#1974149
- Use RHEL help content for RHV/Ovirt (mkolman)
  Resolves: rhbz#1915910
- Move post installation scripts to the end of queue (lveyde)
  Resolves: rhbz#1970879
- Do not generate dracut arguments multiple times for some storage devices
  (rvykydal)
  Related: rhbz#1937208
- Make failure in generating of dracut arguments for iSCSI device non-fatal.
  (rvykydal)
  Resolves: rhbz#1937208

* Thu Jul 01 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.5.3-1
- Check source type directly, not via DBus (mkolman)
  Resolves: rhbz#1941578
- Remove autostep functionality (vslavik)
  Resolves: rhbz#1976913
- Make it possible to skip install time Insights errors (mkolman)
  Resolves: rhbz#1931069
- Fix CDN button visibility (mkolman)
  Resolves: rhbz#1903178
- network: do not bind virtual devices to mac (rvykydal)
  Resolves: rhbz#1963834
- Add a log message for successful installation (vslavik)
  Resolves: rhbz#1949487

* Mon May 24 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.5.2-1
- Use modinfo to check ko before modprobe (t.feng94)
  Resolves: rhbz#1577544
- network: do not crash on team without IP config (rvykydal)
  Resolves: rhbz#1929008
- Add the "Encrypt my data" checkbox to the custom partitioning spoke
  (vponcova)
  Resolves: rhbz#1903786
- Allow encryption of thin logical volumes (vponcova)
  Resolves: rhbz#1877777
- Don't automatically execute the default partitioning (vponcova)
  Resolves: rhbz#1954408
- Don't run the execute method in the kickstart installation in TUI by default
  (vponcova)
  Related: rhbz#1954408
- Don't run the execute method in the kickstart installation in GUI by default
  (vponcova)
  Related: rhbz#1954408
- Enable closest mirror in CentOS Stream config (carl)
  Resolves: rhbz#1953698
- Add CentOS Stream config (riehecky)
  Resolves: rhbz#1953698

* Wed May 19 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.5.1-1
- subscription: allow dates in ISO 8601 format (ptoscano)
  Resolves: rhbz#1947445
- Add RHEL-specific advice to X timeout message (vslavik)
  Related: rhbz#1918702
- Fix AskVNCSpoke call (vslavik)
  Related: rhbz#1918702
- Improve X startup error messages (vslavik)
  Related: rhbz#1918702
- Terminate X server after timeout and restore crash test handler (vslavik)
  Related: rhbz#1918702
- Reorganize control flow in startX (vslavik)
  Related: rhbz#1918702
- Handle SIGUSR1 correctly after Xorg timeout (vslavik)
  Resolves: rhbz#1918702
- Refactor minor details in startX (vslavik)
  Related: rhbz#1918702
- Add base repo name for CentOS Stream after repository renaming (jkonecny)
  Resolves: rhbz#1946347
- Avoid a race condition during Connect to Red Hat spoke initialization
  (mkolman)
  Resolves: rhbz#1950053

* Wed Mar 24 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.15-1
- network: clone connections from intramfs to persistent config (rvykydal)
  Resolves: rhbz#1910438
- network: match also connections named by MAC created by NM in initramfs
  (rvykydal)
  Related: rhbz#1910438
- network: do not reset ipv6.addr-gen-mode in tui network configuration
  (rvykydal)
  Related: rhbz#1873021
- network: set addr-gen-mode of Anaconda default connections to eui64
  (rvykydal)
  Related: rhbz#1873021
- network: default to addr-gen-mode eui64 (rvykydal)
  Resolves: rhbz#1873021

* Mon Mar 22 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.14-1
- Fix crash in NTP servers GUI dialog on late network configuration (rvykydal)
  Resolves: rhbz#1938168

* Mon Mar 15 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.13-1
- ostree: ignore exit code 65 for systemd-tmpfiles (christian)
  Resolves: rhbz#1935648

* Fri Mar 05 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.12-1
- Pull in new translations (rvykydal)
  Related: rhbz#1899672

* Thu Feb 04 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.11-1
- Take dnf substitutions from installer environment configuration (rvykydal)
  Resolves: rhbz#1920735
- Fix exclude arguments of tar payload extracting. (rvykydal)
  Resolves: rhbz#1924118

* Wed Feb 03 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.10-1
- Mark the rhsm and syspurpose kickstart commands as useless (vponcova)
  Resolves: rhbz#1921787
- Fix getting kernel version list for liveimg (rvykydal)
  Resolves: rhbz#1919463

* Tue Feb 02 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.9-1
- Change warning messages of missing prefix for RH products (jkonecny)
  Resolves: rhbz#1897657
- Do not use cache for container build (jkonecny)
  Related: rhbz#1885635
- Fix missing inst. prefixes for bootloader options in documentation (jkonecny)
  Related: rhbz#1897657
- Fix show missing inst. prefix warning appropriately (jkonencny)
  Related: rhbz#1897657
- Remove docs where we tell users that inst. prefix is not required (jkonecny)
  Related: rhbz#1897657
- Print warning for boot options without inst. prefix (jkonecny)
  Related: rhbz#1897657
- Add missing dracut commands as missing inst. prefix warning (jkonecny)
  Related: rhbz#1897657
- Enable warning when inst. prefix is not used (jkonecny)
  Related: rhbz#1897657

* Mon Jan 18 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.8-1
- network: handle wireless configure button sensitiveness (rvykydal)
  Resolves: rhbz#1917437

* Thu Jan 14 2021 Martin Kolman <mkolman@redhat.com> - 33.16.4.7-1
- Allow to disable the Security module (vponcova)
  Resolves: rhbz#1913689
- Allow to disable the Services module (vponcova)
  Resolves: rhbz#1913689
- Support should_run for standalone GUI spokes (vponcova)
  Resolves: rhbz#1913689
- Allow to disable the Localization module (vponcova)
  Resolves: rhbz#1913689
- Allow to disable the Timezone module (vponcova)
  Resolves: rhbz#1913689
- Allow to disable the network installation (vponcova)
  Resolves: rhbz#1913689
- Allow to disable the Users module (vponcova)
  Resolves: rhbz#1913689
- Always show pykickstart parse warnings (vslavik)
  Resolves: rhbz#1897663

* Mon Jan 11 2021 Martin Kolman <mkolman@redhat.com> - 33.16.4.6-1
- Initialize librepo logger (pkratoch)
  Resolves: rhbz#1908286
- Add RPM tests support for owners on rhel-8 (jkonecny)
  Related: rhbz#1885635
- Use latests RHEL-8 buildroot in containers (jkonecny)
  Related: rhbz#1885635
- Implement rpm-tests execution in the container (jkonecny)
  Related: rhbz#1885635

* Tue Jan 05 2021 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.5-1
- network: fix double-free using libnm function filter_connections() (rvykydal)
  Resolves: rhbz#1873561

* Tue Dec 08 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.4-1
- network: rename Gtk cell renderer to prevent name collision (rvykydal)
  Related: rhbz#1847681
- network: add unit tests for SecretsAgent (rvykydal)
  Related: rhbz#1847681
- network: make SecretAgentDialog a bit more robust (rvykydal)
  Related: rhbz#1847681
- network: move wireless secret agent bits into a separate file (rvykydal)
  Related: rhbz#1847681
- network: migrate SecretAgent from python-dbus to dasbus (rvykydal)
  Related: rhbz#1847681
- network: do not use dialog for just single wireless connection to configure
  (rvykydal)
  Related: rhbz#1847681
- network: fix configuration of wireless networks (rvykydal)
  Related: rhbz#1847681
- network: use dialog instead of combobox to select wireless network (rvykydal)
  Related: rhbz#1847681
- network: deal with obsolete ssid when configuring wireless (rvykydal)
  Related: rhbz#1847681
- network: use function instead of assigned lambda in wireless activation
  (rvykydal)
  Related: rhbz#1847681
- network: do not update wireless AP combo active item when not necessary
  (rvykydal)
  Related: rhbz#1847681
- network: do not use obsolete access points in wireless configuration
  (rvykydal)
  Resolves: rhbz#1847681
- Update the function get_default_partitioning (vponcova)
  Related: rhbz#1887370
- Update the property default_partitioning (vponcova)
  Related: rhbz#1887370
- Change the default_partitioning option (vponcova)
  Resolves: rhbz#1887370

* Wed Nov 25 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.3-1
- Fix incomplete configuration of repositories loaded from treeinfo
  (honza.stodola)
  Resolves: rhbz#1745064
- Fix checking ssl certificate for metadata (honza.stodola)
  Resolves: rhbz#1745064
- Apply pylint excessive memory usage fix (mpitt)
  Related: rhbz#1885635
- Use bootlist command to update the PowerPC-64 Boot Order (javierm)
  Resolves: rhbz#1854307
- Discard current boot list when updating the boot-device NRVAM variable
  (javierm)
  Resolves: rhbz#1854307
- Improve the error dialog for storage reset (vponcova)
  Resolves: rhbz#1877050
- Fix issue when ns_info cannot be retrieved for NVDimm namespace (jkonecny)
  Resolves: rhbz#1891827
- Relabel the anaconda logs after copying them to the installed system
  (jstodola)
  Resolves: rhbz#1870493
- post-scripts need to be sorted (honza.stodola)
  Related: rhbz#1870493

* Mon Nov 23 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.2-1
- Install Red Hat IT root certificate into anaconda-ci container (mpitt)
  Related: rhbz#1885635
- Install python-copr into anaconda-ci container (mpitt)
  Related: rhbz#1885635
- Change handling of UID and GID values (vslavik)
  Related: rhbz#1786680
- Send UID and GID over D-Bus as UInt32 (vslavik)
  Related: rhbz#1786680
- Correct limits for UIDs and GIDs in GUI (vslavik)
  Resolves: rhbz#1786680
- Add rhel unit-tests workflow for pull_request_trigger back (jkonecny)
  Related: rhbz#1885635
- Select disks for implicit partitions (vponcova)
  Resolves: rhbz#1642391
- Extend the PartSpec class (vponcova)
  Related: rhbz#1642391

* Fri Nov 06 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.4.1-1
- Allow to format selected DASDs (vponcova)
  Resolves: rhbz#1874394
- Don't clobber host checkout on `make container-ci` (mpitt)
  Related: rhbz#1885635
- Drop anaconda-ci container entrypoint (mpitt)
  Related: rhbz#1885635
- Remove PR test trigger (mpitt)
  Related: rhbz#1885635
- Rename ci-tasks container to anaconda-ci (jkonecny)
  Related: rhbz#1885635
- network: do not crash on infiniband devices activated in initramfs (rvykydal)
  Resolves: rhbz#1890009
- Fix testing target branch instead of PR branch (jkonecny)
  Related: rhbz#1885635
- Add a mechanism to hide help button, use on inst. progress (vslavik)
  Resolves: rhbz#1890092
- Document how to start a self-hosted GitHub actions runner locally (mpitt)
  Related: rhbz#1885635
- Run unit tests on self-hosted GitHub runner (mpitt)
  Related: rhbz#1885635
- Fix local tests run inside of container (jkonecny)
  Related: rhbz#1885635
- Fix ci-tasks container shell instructions (mpitt)
  Related: rhbz#1885635
- More aggressive pylint downscaling (mpitt)
  Related: rhbz#1885635
- Fix pylint downscaling (mpitt)
  Related: rhbz#1885635
- Add ci-tasks container for running unit tests (mpitt)
  Related: rhbz#1885635
- Restrict pylint parallelism to available RAM (mpitt)
  Related: rhbz#1885635
- Separate RPM installability test from rpm_tests (martin)
  Related: rhbz#1885635
- Define make targets for building source and binary rpms (martin)
  Related: rhbz#1885635
- Drop superfluous build in `make run-rpm-tests-only` (martin)
  Related: rhbz#1885635
- Mock system operations in MountFilesystemsTask task (martin)
  Related: rhbz#1885635
- Add missing "rpm-build" test dependency (martin)
  Related: rhbz#1885635
- Add missing "make" BuildRequires (martin)
  Related: rhbz#1885635

* Tue Sep 22 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.26-1
- Never mount partitions on a disk with the iso9660 filesystem (vponcova)
  Resolves: rhbz#1878784

* Thu Sep 17 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.25-1
- Root password is mandatory if there is *not* admin user. (rvykydal)
  Related: rhbz#1876727
- Make locked root be completed only for kickstart (vslavik)
  Resolves: rhbz#1876727

* Mon Sep 07 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.24-1
- network: do not add superfluous quotes to inst.dhcpclass identifier
  (rvykydal)
  Related: rhbz#1870692

* Fri Sep 04 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.23-1
- subscription: Assure payload restart on DVD install after registration
  (mkolman)
  Resolves: rhbz#1873164
- Document the restart_payload argument of subscription helper functions
  (mkolman)
  Related: rhbz#1873164

* Thu Sep 03 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.22-1
- network: fix inst.dhcpclass boot option (rvykydal)
  Resolves: rhbz#1870692
- network: fix kickstart network --dhcpclass option (rvykydal)
  Resolves: rhbz#1869224

* Mon Aug 24 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.21-1
- Fix traceback when removing additional repository (jkonecny)
  Resolves: rhbz#1871037
- Do not mount as RW in Dracut (jkonecny)
  Resolves: rhbz#1871049
- Clean up s390 partitioning check (vslavik)
  Resolves: rhbz#1855724

* Thu Aug 20 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.20-1
- network: do not try to activate connection that has not been found (rvykydal)
  Resolves: rhbz#1869323
- network: add timeout for synchronous activation of a connection (rvykydal)
  Related: rhbz#1869323

* Wed Aug 19 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.19-1
- Propagate verify_ssl to RHSM (mkolman)
  Resolves: rhbz#1858126

* Wed Aug 12 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.18-1
- subscription: Only restart payload when needed (mkolman)
  Resolves: rhbz#1861351
- Reset the state of the custom partitioning spoke (vponcova)
  Resolves: rhbz#1868330
- network: fix parsing of hostname from ip= if mac is defined in dhcp
  (rvykydal)
  Resolves: rhbz#1852560

* Thu Aug 06 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.17-1
- Revert root password spoke to 8.2 behavior (vslavik)
  Resolves: rhbz#1851220
- Remove the DBus method ConfigureNTPServiceEnablementWithTask (vponcova)
  Resolves: rhbz#1862492
- Add the function is_service_installed (vponcova)
  Related: rhbz#1862492

* Tue Aug 04 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.16-1
- Implement get_source_proxy() in payload base class (mkolman)
  Resolves: rhbz#1861456
- Restore RHEL-specific stylesheet data (vponcova)
  Resolves: rhbz#1865882
- subscription: Convert the RHSM default config values to expected format
  (mkolman)
  Resolves: rhbz#1862116
- Create ssh user using only existing fields (vslavik)
  Resolves: rhbz#1860058
- Remove subscription workaround to not use treeinfo repositories (jkonecny)
  Related: rhbz#1851207
- Fix issue that treeinfo repositories were never disabled (jkonecny)
  Related: rhbz#1851207
- Keep treeinfo repositories disabled after payload reset (jkonecny)
  Related: rhbz#1851207
- Reset repositories from the main thread (vponcova)
  Related: rhbz#1851207
- Initialize the closest mirror from the main thread (vponcova)
  Related: rhbz#1851207
- Fix crash on first entering of source spoke (jkonecny)
  Related: rhbz#1851207
- Remove treeinfo repositories instead of disabling (jkonecny)
  Related: rhbz#1851207
- Reload treeinfo repositories on every payload reset (jkonecny)
  Resolves: rhbz#1851207

* Thu Jul 30 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.15-1
- Apply onboot policy even when network was configured in UI. (rvykydal)
  Resolves: rhbz#1856632
- Fix creating cached LVs on encrypted PVs (vtrefny)
  Resolves: rhbz#1855973

* Mon Jul 27 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.14-1
- Fix everything in payload should be mounted as read only (jkonecny)
  Related: rhbz#1856264
- Add support for mount options to device_tree.MountDevice (jkonecny)
  Related: rhbz#1856264
- Adapt tests for CDRom for the new inst.stage2 discovery (jkonecny)
  Related: rhbz#1856264
- CDRom source should prioritize stage2 device during discover (jkonecny)
  Resolves: rhbz#1856264
- Protect all devices with the iso9660 file system (vponcova)
  Related: rhbz#1856264
- Don't ignore NVDIMM devices with the iso9660 file system (vponcova)
  Related: rhbz#1856264
- Add tests for the DBus method FindOpticalMedia (vponcova)
  Related: rhbz#1856264
- Don't return negative container free space (vponcova)
  Resolves: rhbz#1853071
- Revert "Do not build Anaconda on i686" (mkolman)
  Resolves: rhbz#1857180
- Move slower part of Subscription spoke initialization to a thread (mkolman)
  Related: rhbz#1823578
- Only pass one initrd image to kexec (javierm)
  Resolves: rhbz#1855290
- Wait for payload initialization to finish in Subscription spoke (mkolman)
  Related: rhbz#1823578

* Thu Jul 09 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.13-1
- Fix the position of the info bar in standalone spokes (vponcova)
  Resolves: rhbz#1847423
- Add workaround to fix support for installtree without repo (jkonecny)
  Resolves: rhbz#1854825
- Revert "Update pyanaconda/exception.py" (jstodola)
  Resolves: rhbz#1853470
- network: fix configuration of virtual devices by boot options (rvykydal)
  Resolves: rhbz#1851218

* Wed Jul 08 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.12-1
- subscription: Fix rhsm --proxy kickstart command usage with no username
  specified (mkolman)
  Resolves: rhbz#1849792
- Create the initial storage model during the initialization (vponcova)
  Resolves: rhbz#1844098
- Make spoke tiles stack more tightly (vslavik)
  Resolves: rhbz#1845493
- Reconfigure DNF payload after options are set (vslavik)
  Resolves: rhbz#1847603

* Thu Jul 02 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.11-1
- Fix displaying of empty software group description (rvykydal)
  Resolves: rhbz#1812061
- Fix software spoke message when source changes (mkolman)
  Resolves: rhbz#1788458

* Mon Jun 29 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.10-1
- Fix RHSM HTTP proxy configuration crash in the GUI (mkolman)
  Resolves: rhbz#1849792
- subscription: Handle cases where CDN should not be the default (mkolman)
  Related: rhbz#1845605
- subscription: Set DNF payload source via config file option (mkolman)
  Related: rhbz#1845605
- subscription: Manual CDN selection support (mkolman)
  Related: rhbz#1845605
- subscription: Handle source switching at registration/unregistration
  (mkolman)
  Related: rhbz#1845605
- subscription: Introduce the default_source configuration option (mkolman)
  Related: rhbz#1845605
- network: do not enforce network standalone spoke on default source (rvykydal)
  Resolves: rhbz#1848069
- Don't mount DBus sources at /run/install/source (vponcova)
  Resolves: rhbz#1851037

* Thu Jun 25 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.9-1
- network: fix obtaining of s390 options of a wired connection (rvykydal)
  Resolves: rhbz#1850199
- Always specify the boot disk (vponcova)
  Resolves: rhbz#1630299
- Remove the workaround with LD_PRELOAD (vponcova)
  Resolves: rhbz#1843533
- Exclude stderr from returned output when executing powerpc-utils tools
  (javierm)
  Related: rhbz#1847604
- Rename function for a simple check for DNF repository (jkonecny)
  Related: rhbz#1849093
- Add tests for verify_valid_installtree function (jkonecny)
  Related: rhbz#1849093
- Move verify_valid_installtree to source module utils (jkonecny)
  Related: rhbz#1849093
- Do not test if repo is valid based on .treeinfo file (jkonencny)
  Resolves: rhbz#1849093
- Add test for NFS URL with ISO in path (jkonecny)
  Related: rhbz#1849083
- Fix issue when NFS path is pointing directly to ISO (jkonencny)
  Resolves: rhbz#1849083

* Tue Jun 23 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.8-1
- Move Subscription spoke under Software (vslavik)
  Resolves: rhbz#1845493
- Fix hiding of network device activation switch (rvykydal)
  Resolves: rhbz#1628521

* Mon Jun 22 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.7-1
- Fix wireless network configuration on get_ssid() returning None (rvykydal)
  Resolves: rhbz#1847681
- Relabel whole /etc instead of only some parts (vslavik)
  Related: rhbz#1775975
  Related: rhbz#1834189
- Clean up lists of files and directories to relabel (vslavik)
  Related: rhbz#1775975
  Related: rhbz#1834189
- Fix spanish translations (rvykydal)
  Resolves: rhbz#1847977

* Mon Jun 15 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.6-1
- Fix regression reading kernel list when collecting configurations (jkonecny)
  Resolves: rhbz#1846156
- Prevent crash on unregistration (mkolman)
  Resolves: rhbz#1845962
- Check Subscription module is available before use in payload code (mkolman)
  Related: rhbz#1845605
- Fix updating of user gid/uid value checkbox in gui (rvykydal)
  Related: rhbz#1844386
- Fix crash on user uid/gid unchecked in gui (rvykydal)
  Resolves: rhbz#1844386
- Fix passing of arguments when creating dracut arguments for FCoE (rvykydal)
  Resolves: rhbz#1843741
- Do not build Anaconda on i686 (mkolman)
  Related: rhbz#1691319

* Thu Jun 04 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.5-1
- Don't use data.method.proxy (vponcova)
  Related: rhbz#1691319
- Fix more SElinux contexts (vslavik)
  Resolves: rhbz#1834189
  Resolves: rhbz#1775975
- localization: do not crash on failed parsing of X layout (rvykydal)
  Resolves: rhbz#1843379

* Fri May 29 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.4-1
- Create /etc/systemd/network dir for ifname= renaming if needed. (rvykydal)
  Resolves: rhbz#1841469
- Update requirements for fips - update-crypto-policies script (rvykydal)
  Resolves: rhbz#1841471

* Thu May 28 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.3-1
- Convert help system to use help id (mkolman)
  Related: rhbz#1691319
- Remove unused constants (mkolman)
  Related: rhbz#1691319
- Adjust help related configuration options (mkolman)
  Related: rhbz#1691319
- Replace helpFile property with help_id (mkolman)
  Related: rhbz#1691319
- Close responses from session.get (vponcova)
  Related: rhbz#1691319
- Improve the documentation of the SetUpMountTask class (vponcova)
  Related: rhbz#1691319
- Raise an exception if the source's mount point is not unmounted (vponcova)
  Related: rhbz#1691319
- Change the default source to CDROM (vponcova)
  Related: rhbz#1691319
- Don't set up sources in the refresh method of the Source spoke (vponcova)
  Related: rhbz#1691319
- Set up FIPS in the target system (vponcova)
  Related: rhbz#1800697
- Update the service anaconda-sshd (vponcova)
  Related: rhbz#1800697
- Set up FIPS in the installation environment (vponcova)
  Resolves: rhbz#1800697
- Add NFS ISO support back to the NFS SetupSourceTask (jkonecny)
  Resolves: rhbz#1840346
- Add NFS ISO support to the NFSSourceModule (jkonencny)
  Related: rhbz#1840346
- Fix changelog to keep rhel history (rvykydal)
  Related: rhbz#1691319
- Tear down HDD device mount if no valid installation source is found
  (jkonecny)
  Related: rhbz#1840346
- Extract ISO find algorith from harddrive (jkonecny)
  Related: rhbz#1840346
- Update required ack in makebumpver script for rhel > 7 (rvykydal)
  Related: rhbz#1691319
- Fix string based on translator comments (vslavik)
  Related: rhbz#1691319
- subscription: Fix authentication method switching in GUI (mkolman)
  Related: rhbz#1691319

* Wed May 27 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.2-1
- subscription: Make sure CDN repos are loaded and usable (mkolman)
  Related: rhbz#1691319
- Fix issue that unified ISO from URL is not loaded (jkonecny)
  Related: rhbz#1691319
- Add split_protocol payload helper function (jkonecny)
  Related: rhbz#1691319
- Fix imports of Blivet-GUI in unit tests (vponcova)
  Related: rhbz#1691319
- Make cppcheck ignore the G_DEFINE_TYPE macros (vslavik)
  Related: rhbz#1691319
- Fix test to not use Python 3.8 feature (vslavik)
  Related: rhbz#1691319
- Fix test for root SSH login allowed (vslavik)
  Related: rhbz#1691319
- Remove blivet-GUI tests (vslavik)
  Related: rhbz#1691319
- Ignore no return from BTRFS (vslavik)
  Related: rhbz#1691319
- Remove unused imports (vslavik)
  Related: rhbz#1691319

* Mon May 25 2020 Radek Vykydal <rvykydal@redhat.com> - 33.16.3.1-1
- Change git branch configuration (jkonecny)
  Related: rhbz#1805757
- Update translation badge (jkonecny)
  Related: rhbz#1805757
- Use rhel-8 weblate translation repository (jkonecny)
  Resolves: rhbz#1805757
- Use platform-python instead of python3 (vslavik)
  Related: rhbz#1691319
- root spoke gui: do not expose some root account options (eg locking) (rvykydal)
  Related: rhbz#1691319
- Modify locking of root defauls for rhel (rvykydal)
  Related: rhbz#1691319
- Update required version of blivet (rvykydal)
  Related: rhbz#1691319
- Remove tests for --ignorebroken packages section option (rvykydal)
  Related: rhbz#1691319
- Remove support for --ignorebroken packages option (rvykydal)
  Related: rhbz#1691319
- Use F25_Timezone (rvykydal)
  Related: rhbz#1691319
- Make sure rhsm.service is running at Anaconda startup (mkolman)
  Related: rhbz#1691319
- Replace SimpleQueue with Queue (vponcova)
  Related: rhbz#1691319
- Change fedora-welcome to rhel-welcome (bcl)
  Related: rhbz#1691319
- Make RHEL the default (fallback) product (vslavik)
  Related: rhbz#1691319
- Exclude blivet gui source from rpm_test (rvykydal)
  Related: rhbz#1691319
- Exclude dependencies for tests from RHEL-8 (jkonecny)
  Related: rhbz#1691319
- Update pykickstart version for rhel (rvykydal)
  Related: rhbz#1691319
- Use RHEL8 versions of commands (rvykydal)
  Related: rhbz#1691319
- Use RHEL8 kickstart handler (rvykydal)
  Related: rhbz#1691319
- Remove kickstart btrfs support (rvykydal)
  Related: rhbz#1691319
- Rebase to upstream 33.16 version (rvykydal)
  Resolves: rhbz#1691319

* Fri Mar 13 2020 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.17-1
- Make sure rhsm.service is running at Anaconda startup (mkolman)
  Resolves: rhbz#1805266

* Fri Feb 21 2020 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.16-1
- Fix crash on single disk selection in GUI (rvykydal)
  Resolves: rhbz#1805613

* Thu Feb 20 2020 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.15-1
- Fix installation source switching to/from CDN (mkolman)
  Resolves: rhbz#1788487
  Resolves: rhbz#1790383
  Resolves: rhbz#1791376

* Thu Feb 20 2020 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.14-1
- Do not allow selecting ignored disk in GUI even if it is the only one
  (rvykydal)
  Resolves: rhbz#1786561

* Tue Feb 11 2020 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.13-1
- Disable package download to / /tmp (jkonecny)
  Resolves: rhbz#1781517

* Thu Feb 06 2020 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.12-1
- network: fix GUI crash on invalid devices in the list (rvykydal)
  Resolves: rhbz#1697256

* Mon Feb 03 2020 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.11-1
- Fix DBus error detection (mkolman)
  Related: rhbz#1794767
- Make sure RHSM HTTP proxy port from kickstart is an integer (mkolman)
  Resolves: rhbz#1794025

* Thu Jan 23 2020 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.10-1
- Log exceptions raised in subscription data fetching method (mkolman)
  Related: rhbz#1788036
- Fix subscription status not being displayed in some cases (mkolman)
  Resolves: rhbz#1788036
- Make sure syspurpose is set before registration in GUI (mkolman)
  Resolves: rhbz#1788207
  Related: rhbz#1788036
- Update pep8speaks checker configuration for the branch (rvykydal)
  Related: rhbz#1788036

* Thu Jan 16 2020 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.9-1
- Fix RHSM HTTP proxy configuration clearing (mkolman)
  Resolves: rhbz#1789814
- Add scrolling for the registration tab (mkolman)
  Resolves: rhbz#1788422

* Thu Jan 09 2020 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.8-1
- Fix output kickstart generation for subscription commands (mkolman)
  Resolves: rhbz#1788579
  Resolves: rhbz#1788513
- Fix GTK access from subscription thread (mkolman)
  Resolves: rhbz#1787615

* Mon Jan 06 2020 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.7-1
- Fix branding in the Connect to Red Hat spoke (mkolman)
  Resolves: rhbz#1787342

* Fri Dec 13 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.6-1
- Fix RHSM HTTP proxy setup (mkolman)
  Related: rhbz#1748281
- Fix text color on info bars (mkolman)
  Resolves: rhbz#1782174

* Tue Dec 10 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.5-1
- Adjust unit tests (mkolman)
  Resolves: rhbz#1748281
  Resolves: rhbz#1746391
- Extend list of false positives in the style guide (mkolman)
  Resolves: rhbz#1748281
  Resolves: rhbz#1746391
- Subscription support - changes in GUI (mkolman)
  Resolves: rhbz#1748281
  Resolves: rhbz#1746391
- Extend the anaconda-gtk.css (mkolman)
  Resolves: rhbz#1748281
  Resolves: rhbz#1746391
- Subscription support - changes in installation payload (mkolman)
  Resolves: rhbz#1748281
  Resolves: rhbz#1746391
- Subscription support - changes in DBus modules (mkolman)
  Resolves: rhbz#1748281
  Resolves: rhbz#1746391
- Subscription support - changes outside of DBus modules (mkolman)
  Resolves: rhbz#1748281
  Resolves: rhbz#1746391
- Add temporary subscription scheduling module (mkolman)
  Resolves: rhbz#1748281
  Resolves: rhbz#1746391
- Add basic CDN support to Payload DBus module (mkolman)
  Resolves: rhbz#1748281
  Resolves: rhbz#1746391
- Add support for custom interface for DBus Tasks (mkolman)
  Resolves: rhbz#1748281
  Resolves: rhbz#1746391
- Backport locale support for modules (mkolman)
  Resolves: rhbz#1748281
  Resolves: rhbz#1746391
- Add subscription manager as an Anaconda dependency (mkolman)
  Resolves: rhbz#1748281
  Resolves: rhbz#1746391

* Tue Nov 12 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.4-1
- Add UI support for the ZIPL Secure boot (vponcova)
  Related: rhbz#1659400
- Add DBus support for the ZIPL Secure Boot (vponcova)
  Resolves: rhbz#1659400
- Don't mention new-kernel-pkg anymore in /etc/sysconfig/kernel (javierm)
  Resolves: rhbz#1747382
- Don't print warnings for new-kernel-pkg not being present (javierm)
  Related: rhbz#1747382

* Tue Oct 22 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.3-1
- Only attempt to open the ibm,max-boot-devices sysfs entry if it exists
  (javierm)
  Related: rhbz#1748756

* Mon Oct 21 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.2-1
- Don't add more devices in boot-device NVRAM than the maximum allowed
  (javierm)
  Resolves: rhbz#1748756
- Fix local repo files aren't enabled (jkonecny)
  Resolves: rhbz#1641620
- Remove ldconfig spec macros (jkonecny)
  Resolves: rhbz#1700685
- Don't try to format FBA DASD devices (mmatsuya)
  Resolves: rhbz#1715303

* Mon Oct 14 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.2.1-1
- Skip buildins when processing kernel boot args (jkonecny)
  Resolves: rhbz#1637472
- network: fix handling of ksdevice=bootif in initramfs (rvykydal)
  Related: rhbz#1649359
- Make sure we work with fresh data when trying to do netroot (vpodzime)
  Resolves: rhbz#1649359
- Make our manual triggering on network in dracut work (vpodzime)
  Resolves: rhbz#1649359

* Fri Sep 27 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.13-1
- Change the bases of the install classes for RHVH (vponcova)
  Related: rhbz#1753316

* Tue Sep 24 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.12-1
- Add the install class for Red Hat Virtualization (vponcova)
  Resolves: rhbz#1753316
- Extend support for custom storage checking (vponcova)
  Related: rhbz#1753316
- Enable to define the autopart type in an install class (vponcova)
  Related: rhbz#1753316

* Mon Aug 26 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.11-1
- Fix noverifyssl when downloading .treeinfo file (jkonecny)
  Resolves: rhbz#1726156
  Resolves: rhbz#1723811

* Fri Aug 02 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.10-1
- Do not try to mount cdrom source also if it has been mounted in dracut.
  (rvykydal)
  Resolves: rhbz#1733507

* Tue Jul 02 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.9-1
- Adjust the exclude arguments for livepayloads (bcl)
  Related: rhbz#1684542
- Recreate the BLS entries when using liveimg (bcl)
  Resolves: rhbz#1684542
- Cache the liveimg tar kernel list (bcl)
  Related: rhbz#1684542
- Add common function for creating rescue images (bcl)
  Related: rhbz#1684542
- Re-generate BLS loader file snippets on live installs (awilliam)
  Related: rhbz#1684542

* Tue Jul 02 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.8-1
- Respect changesok password policy for root password (mkolman)
  Resolves: rhbz#1584145
- Fix default value for pwpolicy emptyok (mkolman)
  Resolves: rhbz#1664704

* Tue Jun 25 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.7-1
- Add support for disabling modules via module --disable (mkolman)
  Resolves: rhbz#1655523
  Related: rhbz#1719347

* Fri Jun 14 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.6-1
- Require blivet with flags.protect_cdrom support (rvykydal)
  Related: rhbz#1671713
- Be more strict when checking for mounted dvd source. (rvykydal)
  Resolves: rhbz#1671713
- Protect cdroms during tree population for image installs. (rvykydal)
  Resolves: rhbz#1671713

* Thu Jun 13 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.5-1
- Fix the rescue mode (vponcova)
  Resolves: rhbz#1628653

* Wed Jun 12 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.4-1
- Set default entry to the BLS id instead of the entry index (javierm)
  Resolves: rhbz#1671047
- Fix non-root dir of install tree HD installation (jkonecny)
  Resolves: rhbz#1689194

* Tue Jun 11 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.3-1
- Handle bytes and strings from RPM (vponcova)
  Resolves: rhbz#1689909
- Set the flag lvm_metadata_backup (vponcova)
  Resolves: rhbz#1673901
- Rename add-ons to additional software (jkonecny)
  Resolves: rhbz#1674011
- Move product version modifications for ui into function and add unit test.
  (rvykydal)
  Resolves: rhbz#1671384
- Do not show quarterly release part of the version in UI. (rvykydal)
  Resolves: rhbz#1671384

* Mon Jun 10 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.2-1
- Rename zanata rhel-devel version (rvykydal)
  Related: rhbz#1666319
- Adapt makebumpver to rhel-devel -> rhel-8 branch renaming. (rvykydal)
  Resolves: rhbz#1666319

* Thu Jun 06 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.1.1-1
- Use new ssl certificate kickstart options (lars)
  Resolves: rhbz#1663954

* Thu Mar 14 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.40-1
- Pull in new translations (rvykydal)
  Related: rhbz#1684056

* Tue Mar 12 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.39-1
- Make SMT warning message smaller (jkonecny)
  Related: rhbz#1684056
- Remove blank line in the SMT warning (jkonecny)
  Related: rhbz#1684056

* Mon Mar 11 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.38-1
- Pull in new translations (rvykydal)
  Related: rhbz#1684056

* Fri Mar 08 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.37-1
- Update the SMT warning message (rvykydal)
  Related: rhbz#1684056
- Detect and warn if SMT is enabled (vponcova)
  Resolves: rhbz#1684056

* Mon Feb 25 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.36-1
- Pass nosmt boot option to installed system. (rvykydal)
  Resolves: rhbz#1677411
- Use unformatted DASDs for the partitioning (vponcova)
  Resolves: rhbz#1676630

* Fri Feb 22 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.35-1
- Check for dirinstall target on s390 (bcl)
  Resolves: rhbz#1677417

* Thu Feb 14 2019 Martin Kolman <mkolman@redhat.com> - 29.19.0.34-3
- Change the overflow color (vponcova)
  Related: rhbz#1637686

* Mon Feb 11 2019 Martin Kolman <mkolman@redhat.com> - 29.19.0.34-2
- Remove a confusing message for headless systems (#1638791) (vponcova)
  Resolves: rhbz#1638791

* Wed Jan 30 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.34-1
- Restore RHEL-specific stylesheet data (vponcova)
  Resolves: rhbz#1638383
- Do not crash on missing multipath device wwn. (rvykydal)
  Resolves: rhbz#1666242

* Wed Jan 16 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.33-1
- Relabel X11/xorg.conf.d directory (jkonecny)
  Resolves: rhbz#1660436
- Reorder items in selinux relabeling post script (jkonecny)
  Related: rhbz#1660436

* Mon Jan 14 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.32-1
- Update gjs dependency filter for fedora->rhel filename changes (rvykydal)
  Related: rhbz#1650295

* Mon Jan 14 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.31-1
- Change fedora-welcome to rhel-welcome (bcl)
  Related: rhbz#1650295

* Tue Jan 08 2019 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.30-1
- Add python3-coverage to testing dependencies (jkonecny)
  Related: rhbz#1502323
- Set Automatic Installation Media for HDD not ISO (jkonecny)
  Related: rhbz#1502323
- Adapt old code to new partition name translation (jkonecny)
  Related: rhbz#1502323
- Fix source spoke status for expanded tree on HDD (jkonecny)
  Related: rhbz#1502323
- Enable installation from install tree on HDD (jkonecny)
  Resolves: rhbz#1502323

* Mon Dec 17 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.29-1
- Pull in fixed translations
  Resolves: rhbz#1659890

* Fri Dec 14 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.28-1
- Update python-coverage dependency (rvykydal)
  Resolves: rhbz#1658777
- Require password confirmation in GUI (mkolman)
  Resolves: rhbz#1584064
- Only quit GTK mainloop on GUI quit request (mkolman)
  Resolves: rhbz#1643111
- Drop the inst.noblscfg option (javierm)
  Resolves: rhbz#1658980
- Don't allow to use LDL DASD disks (vponcova)
  Resolves: rhbz#1635825
- Don't allow /boot on LVM (vponcova)
  Resolves: rhbz#1641986
- Use the default LUKS version for auto partitioning (vponcova)
  Resolves: rhbz#1628519
- Make it possible to exit empty user spoke (mkolman)
  Resolves: rhbz#1620135
- Fix pylint errors (vponcova)
  Related: rhbz#1652727

* Wed Dec 12 2018 Martin Kolman <mkolman@redhat.com> - 29.19.0.27-2
- Run zipl again after generating initramfs (#1652727) (vponcova)
  Resolves: rhbz#1652727

* Wed Dec 05 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.27-1
- Fix module installation error reporting (mkolman)
  Resolves: rhbz#1644635
- Drop xorg-x11-server-Xorg check from graphical target detection (mkolman)
  Resolves: rhbz#1583958

* Mon Nov 19 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.26-1
- Pull in fixed translations
  Resolves: rhbz#1650431

* Tue Nov 06 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.25-1
- Hotfix - disable unsupported hardware detection (mkolman)
  Resolves: rhbz#1645686

* Thu Oct 18 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.24-1
- Make the pyanaconda/image.py more pep8 (jkonecny)
  Related: rhbz#1631673
- Test image repodata folder based on treeinfo file (jkonecny)
  Resolves: rhbz#1631673
- Use var instead of strings in findFirstIsoImage (jkonecny)
  Related: rhbz#1631673
- Use new InstallTreeMetadata instead of TreeInfo (jkonecny)
  Related: rhbz#1631673
- Add InstallTreeMetadata class (jkonecny)
  Related: rhbz#1631673
- Move DEFAULT_REPOS to the constants (jkonecny)
  Related: rhbz#1631673

* Mon Oct 15 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.23-1
- nvdimm: update ks data for actions in UI (rvykydal)
  Resolves: rhbz#1620093
- nvdimm: use pykickstart constant for setting reconfigure mode (rvykydal)
  Related: rhbz#1620093
- Fix strings not marked for translation (jkonecny)
  Resolves: rhbz#1637399
- Increase EFI System Partition (ESP) size to 200-600 MiB (javierm)
  Resolves: rhbz#1633640
- Save lsblk output to the Anaconda traceback file (vtrefny)
  Resolves: rhbz#1627220

* Thu Oct 11 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.22-1
- Remove EXPERIMENTAL label for mountpoint assignment in TUI (mkolman)
  Resolves: rhbz#1636940
- Wrap line in storage/osinstall.py to 99 chars (jkonecny)
  Related: rhbz#1637096
- Add missing pylint false positive (jkonecny)
  Related: rhbz#1637096
- Make syspurpose description text size biger (mkolman)
  Related: rhbz#1612060
- Fix double quoting in syspurpose values (mkolman)
  Resolves: rhbz#1637135
- Fix ihelp pylint issues (jkonecny)
  Related: rhbz#1637096
- Add ignored field to rpm_tests (jkonecny)
  Related: rhbz#1637096
- Remove unused false positives (jkonecny)
  Related: rhbz#1637096
- Use new BTRFS pykickstart version (jkonecny)
  Related: rhbz#1637096
- Add back missing import (jkonecny)
  Related: rhbz#1637096
- Add --no-pip to setup-mock-test-env script (jkonecny)
  Related: rhbz#1637096
- Rename coverage3 to coverage-3.6 (jkonecny)
  Related: rhbz#1637096
- Fix error message in setup-mock-test-env script (jkonecny)
  Related: rhbz#1637096
- Rename nosetests binary to 3.6 - link is missing (jkonecny)
  Resolves: rhbz#1637096
- Remove not used BuildRequires for RHEL (jkonecny)
  Related: rhbz#1637096
- Add shortcut function to get dependency script (jkonecny)
  Related: rhbz#1637096
- Add install-pip parameter to setup-mock-test-env (jkonecny)
  Related: rhbz#1637096
- Add initial 32-bit ARMv7 EFI support (pbrobinson)
  Resolves: rhbz#1637618
- Drop legacy get_arm_machine pieces (pbrobinson)
  Related: rhbz#1637618
- arch: arm: drop omap checks and specifics (pbrobinson)
  Related: rhbz#1637618
- Small optimalization in setup-mock-test-env (jkonecny)
  Related: rhbz#1637096
- Add package installation from pip for test script (jkonecny)
  Related: rhbz#1637096
- Remove hfsplus-tools not used on RHEL (jkonecny)
  Related: rhbz#1637096

* Wed Oct 10 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.21-1
- Add Not Specified option for System Purpose lists (mkolman)
  Resolves: rhbz#1637602
- Set the VNC password directly (vponcova)
  Resolves: rhbz#1634667

* Mon Oct 08 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.20-1
- Ignore errors when trying to activate unsupported swaps (vtrefny)
  Resolves: rhbz#1635253
- Adapt built in help system to new content structure (mkolman)
  Resolves: rhbz#1593723
- Update help folder paths (mkolman)
  Related: rhbz#1593723
- Replace helpFile property with help_id (mkolman)
  Related: rhbz#1593723
- Small optimization in boot arg parsing method (jkonecny)
  Related: rhbz#1622429
- Fix bad --addrepo command line parsing (jkonecny)
  Related: rhbz#1622429
- Raise correct exception on bad addrepo boot param (jkonecny)
  Resolves: rhbz#1622429

* Thu Oct 04 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.19-1
- Add option to set kernel.hung_task_timeout_secs option (rvykydal)
  Resolves: rhbz#1633549
- Change default install class to RHEL (jkonecny)
  Resolves: rhbz#1634094
- Don't check for firmware compatibility to enable BootLoaderSpec support
  (javierm)
  Resolves: rhbz#1635547

* Tue Oct 02 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.18-1
- Update kernel command line parameters in BLS files (javierm)
  Resolves: rhbz#1635180
- Drop attempt to add 'nocrypto' to tsflags (#1634791) (awilliam)
  Resolves: rhbz#1634791
- Make sure fips is correctly enabled on target system (#1619568) (mkolman)
  Resolves: rhbz#1619568

* Mon Oct 01 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.17-1
- Syspurpose related test & pylint fixes (mkolman)
  Related: rhbz#1612060
- Add missing folder to Makefile (mkolman)
  Related: rhbz#1612060
- Add system purpose support (mkolman)
  Resolves: rhbz#1612060

* Wed Sep 26 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.16-1
- Sync spec file (rvykydal)
  Related: rhbz#1619153
- Fix python3 requires in spec file (rvykydal)
  Resolves: rhbz#1619153
- Revert "Add system purpose support" (rvykydal)
  Related: rhbz#1619153
- Add support for GRUB_ENABLE_BLSCFG and inst.noblscfg (pjones)
  Resolves: rhbz#1615442
- Get rid of new-kernel-pkg invocations (pjones)
  Related: rhbz#1615442
- Minor pylint cleanups (pjones)
  Related: rhbz#1615442

* Mon Sep 24 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.15-1
- Add system purpose support (mkolman)
  Resolves: rhbz#1612060

* Wed Sep 19 2018 Tomas Orsava <torsava@redhat.com> - 29.19.0.14-2
- Require the Python interpreter directly instead of using the package name
- Related: rhbz#1619153

* Wed Sep 19 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.14-1
- Update the spoke for unsupported hardware in TUI (#1601545) (vponcova)
  Resolves: rhbz#1601545
- Update the dialog for unsupported hardware in GUI (#1601545) (vponcova)
  Resolves: rhbz#1601545
- Support detection of kernel taints (vponcova)
  Resolves: rhbz#1601545

* Tue Sep 18 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.13-1
- prefixdevname: fix a typo in filename (rvykydal)
  Related: rhbz#1615997
- prefixdevname: pass persistent configuration to installed system (rvykydal)
  Resolves: rhbz#1615997
- prefixdevname: pass net.ifnames.prefix option to installed system (rvykydal)
  Resolves: rhbz#1615997
- prefixdevname: install package to target system if needed (rvykydal)
  Resolves: rhbz#1615997
- prefixdevname: import state from initramfs to stage 2 (rvykydal)
  Resolves: rhbz#1615997

* Mon Sep 17 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.12-1
- Don't connect to signals of the Network Manager DBus objects
  (vponcova)
  Resolves: rhbz#1582233
- Fix librepo logging with new DNF (jkonecny)
  Resolves: rhbz#1626609

* Fri Sep 07 2018 Josh Boyer <jwboyer@redhat.com> - 29.19.0.11-2
- Require python3-librepo
  Resolves: rhbz#1626609

* Fri Sep 07 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.11-1
- DNF 3.5 compatibility (mkolman)
  Related: rhbz#1613296
- Don't try to get hostnamed proxy in non-installer-image environments
  (rvykydal)
  Resolves: rhbz#1622917

* Fri Aug 24 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.10-1
- Revert "Don't allow booting from nvdimm devices" (rvykydal)
  Resolves: rhbz#1620566
- Fix pylint errors (vponcova)
  Related: rhbz#1618633

* Wed Aug 22 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.9-1
- Fix crash in tui when default partitioning scheme is not supported
  (rvykydal)
  Related: rhbz#1617958

* Thu Aug 16 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.8-1
- Add inst.addrepo documentation for HD variant (jkonecny)
  Related: rhbz#1595415
- Warn when repo names are not unique (jkonecny)
  Related: rhbz#1595415
- HD addon repos have mount directories permanent (jkonecny)
  Related: rhbz#1595415
- Unmount hard drive additional repositories (jkonecny)
  Related: rhbz#1595415
- Move RepoData copy creation to the RepoData class (jkonecny)
  Related: rhbz#1595415
- Show empty file protocol on HD addon repo fail (jkonecny)
  Related: rhbz#1595415
- Mount and use HDD additional repositories (jkonecny)
  Related: rhbz#1595415
- Separate _find_and_mount_iso from _setup_media (jkonecny)
  Related: rhbz#1595415
- Load hard drive repo type from inst.addrepo (jkonecny)
  Related: rhbz#1595415
- Do not fail if .discinfo file can't be read (jkonecny)
  Related: rhbz#1595415
- Use productmd to parse .discinfo file (jkonecny)
  Related: rhbz#1595415
- Add payload sources tests (jkonecny)
  Related: rhbz#1595415
- Cleanup payload tests source file (jkonecny)
  Related: rhbz#1595415
- Add documentation for inst.addrepo boot option (jkonecny)
  Related: rhbz#1595415
- Add additional repositories to KS data (jkonecny)
  Resolves: rhbz#1595415
- Use new source solution (jkonecny)
  Related: rhbz#1595415
- Add payload sources implementation (jkonecny)
  Related: rhbz#1595415
- Mark disks with additional repos as protected (jkonecny)
  Related: rhbz#1595415
- Support boot args parsing to list (jkonecny)
  Related: rhbz#1595415
- Add inst.addrepo new options (jkonecny)
  Related: rhbz#1595415
- Make parenthesis consistent (jkonecny)
  Related: rhbz#1595415
- Remove unused parameter from live_startup method (jkonecny)
  Related: rhbz#1595415
- Disable treeinfo based repos only once (jkonecny)
  Related: rhbz#1610806
- Disable treeinfo repos when base repo change (jkonecny)
  Related: rhbz#1610806
- Treeinfo repos can't be changed nor removed (jkonecny)
  Related: rhbz#1610806
- Add all repositories from the treeinfo file (jkonecny)
  Resolves: rhbz#1610806
- Load base repository location from treeinfo (jkonecny)
  Related: rhbz#1610806
- Add limited file:// protocol to GUI Source spoke (jkonecny)
  Related: rhbz#1610806
- Add BaseOS between default base repositories (jkonecny)
  Related: rhbz#1610806
- Split _setupInstallDevice method in payload (jkonecny)
  Related: rhbz#1610806

* Mon Aug 13 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.7-1
- Revert back to running DNF in a subprocess (mkolman)
  Related: rhbz#1613296
- Add back reverted patches for modularity support (rvykydal)
  Related: rhbz#1613296

* Mon Aug 13 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.6-1
- Check the LUKS2 memory requirements (vponcova)
  Related: rhbz#1547908
- Add an option for choosing version of LUKS in GUI (vponcova)
  Related: rhbz#1547908
- Add tests for LUKS2 in the auto partitioning module (vponcova)
  Related: rhbz#1547908
- Apply the LUKS2 options from the auto partitioning module (vponcova)
  Related: rhbz#1547908
- Support LUKS2 options in the auto partitioning module (vponcova)
  Related: rhbz#1547908
- Support LUKS2 options in logvol, part and raid commands (vponcova)
  Related: rhbz#1547908
- Enable to set a default version of LUKS (vponcova)
  Related: rhbz#1547908
- Update dependencies and kickstart commands to support LUKS2 (vponcova)
  Resolves: rhbz#1547908
- Use SimpleConfigFile to get PLATFORM_ID from /etc/os-release (mkolman)
  Related: rhbz#1613296
- Use wwn attr instead of removed wwid. (#1565693) (dlehman)
  Resolves: rhbz#1615408

* Thu Aug 09 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.5-1
- Fix a 5 year old typo in the spec file (mkolman)
  Resolves: rhbz#1613488
- Bump required DNF version (mkolman)
  Related: rhbz#1613296
- Fix some small issues with the platform id patch (mkolman)
  Related: rhbz#1613296
- Set platform id for DNF (mkolman)
  Related: rhbz#1613296
- Fix crash when software environment is False (jkonecny)
  Resolves: rhbz#1612942
- Allow to delete all file systems used by Unknown (#1597199) (vponcova)
  Resolves: rhbz#1597199

* Mon Aug 06 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.4-1
- DD: Use text mode when calling tools with subprocess (rvykydal)
  Resolves: rhbz#1609744
- Update RHEL placeholder names (mkolman)
  Related: rhbz#1593723

* Thu Aug 02 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.3-3
- Revert Use productmd library to parse .treeinfo (rvykydal)
  Related: rhbz#1611622

* Wed Aug 01 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.3-2
- Revert of module support enablement (install specs DNF API) (rvykydal)

* Wed Aug 01 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.3-1
- Typo fixup (rvykydal)
- Define if blivet-gui is supported via installclasses (rvykydal)
  Related: rhbz#1599838
- Offer Blivet-GUI partitioning only if supported (rvykydal)
  Related: rhbz#1599838
- Only show the "closest mirror" source option where appropriate (mkolman)
  Resolves: rhbz#1608241
- Starting from 3.0 DNF expects strings in comps queries (mkolman)
- Remove blivet-gui spoke and its dependencies (rvykydal)
  Resolves: rhbz#1599838
- Use the manual partitioning module in TUI (vponcova)
- Use the manual partitioning module in UI (vponcova)
- Add tests for the manual partitioning module (vponcova)
- Create the manual partitioning module (vponcova)
- Reserve enough static space for 2 lines in spoke status on hub (#1584160) (rvykydal)
- Handle new module specific error states (mkolman)
- Handle missing package errors reported by the install_specs() function (mkolman)
- Initial module enablement and installation support (mkolman)
- Fix disable additional repositories (jkonecny)
- Show better messages for NoSuchPackage and NoSuchGroup (#1599190) (vponcova)
  Resolves: rhbz#1599190
- Bootloader stage2 can't be on btrfs on rhel (#1533904) (rvykydal)
  Related: rhbz#1533904
- Remove --fstype=btrfs support from LogVol, Raid and Partition (rvykydal)
  Resolves: rhbz#1533904
- Remove btrfs support. (rvykydal)
  Resolves: rhbz#1533904
- Use RHEL8 versions of commands added to RHEL8 handler for test (rvykydal)
- Use RHEL8 kickstart handler (rvykydal)
- Use productmd library to parse .treeinfo (#1411673) (jkonecny)
- Import kickstart classes as version-less in the dracut script (vponcova)
- Use only version-less kickstart classes (vponcova)
- Define version-less variants of kickstart classes (vponcova)
- Pylint should skip the file livepayload.py (vponcova)
- Fix pylint errors (vponcova)

* Wed Jul 25 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.2-1
- Change the pop-up text with the pre-release warning (#1542998) (vpodzime)
  Resolves: rhbz#1608243
- Sort categories on the hub by defined order (#1584160) (rvykydal)
  Resolves: rhbz#1584166
- Show a note about EULA where relevant (mkolman)
  Resolves: rhbz#1569596
- Change message log level to INFO when adding repo (jkonecny)
  Related: rhbz#1603178
- Set packaging log level to DEBUG by default (jkonecny)
  Resolves: rhbz#1603178
- Remove the python-wrapt dependency (vponcova)
- Do not use capitals for spoke names (#1584160) (rvykydal)
  Resolves: rhbz#1584166
- Wrap category label and add space between columns (#1584160) (rvykydal)
  Resolves: rhbz#1584166
- Use 32 px icons (instead of 16 px) on hubs (#1584160) (rvykydal)
  Resolves: rhbz#1584166
- Make pyanaconda.dbus.typing work with Python 3.7 (#1598574) (awilliam)
- Use Platform Python where appropriate (mkolman)
- Replace deprecated dracut options for booting with ibft. (rvykydal)
  Resolves: rhbz#1566052
- Protected devices might be hidden (#1561766) (vponcova)
- Improve handling of unsupported filesystems in UI. (rvykydal)
  Resolves: rhbz#1533904
- Reserve two lines for status message (#1584160) (rvykydal)
  Resolves: rhbz#1584166
- Use three spoke columns on hub for better scaling (#1584160) (rvykydal)
  Resolves: rhbz#1584166
- fstab: include a note about systemctl daemon-reload (zbyszek)
- Access the ZFCP module only on s390x (vponcova)
- Tell libreport if it is a final release or not (#1596392) (vpodzime)
  Resolves: rhbz#1596392
- bootloader: GRUB2: Set menu_auto_hide when enabled by the instClass
  (hdegoede)
- installclass: Add bootloader_menu_autohide property (hdegoede)
- Add tests for the zFCP module (vponcova)
- Handle the zfcp command in the zFCP module (vponcova)
- Use the zFCP discovery task in UI (vponcova)
- Create the zFCP discovery task (vponcova)
- Create the zFCP module (vponcova)

* Mon Jul 16 2018 Radek Vykydal <rvykydal@redhat.com> - 29.19.0.1-1
- Define zanata branch statically for rhel-devel branch (rvykydal)

* Wed Jun 27 2018 Martin Kolman <mkolman@redhat.com> - 29.19-1
- DNF 3: progress callback constants moved to dnf.transaction (awilliam)
- DNF 3: Update size calculations for transaction item changes (awilliam)
- DNF 3: config substitutions moved from dnf to libdnf (awilliam)

* Mon Jun 25 2018 Martin Kolman <mkolman@redhat.com> - 29.18-1
- Add tests for the DASD module (vponcova)
- Run the DASD formatting task in UI (vponcova)
- Extend the sync_run_task method with a callback (vponcova)
- Create a task for formatting DASDs (vponcova)
- Run the DASD discovery task from UI (vponcova)
- Create a task for discovering DASDs (vponcova)
- Create the DASD module (vponcova)
- Add tests for the language installation task (vponcova)
- Run an installation task to install a language (vponcova)
- nvdimm: fix crash on non-block devices (rvykydal)

* Tue Jun 12 2018 Martin Kolman <mkolman@redhat.com> - 29.17-1
- Wait for kickstart modules to quit (vponcova)
- Ask for a default passphrase if required (vponcova)
- Add support for setting different types of passwords in TUI (vponcova)

* Thu Jun 07 2018 Martin Kolman <mkolman@redhat.com> - 29.16-1
- Add tests for changes in tasks and the install manager (vponcova)
- Add a simple installation task in the Baz module (vponcova)
- Update the boss classes (vponcova)
- Update the base clases for modules (vponcova)
- Use the system installation task in the install manager (vponcova)
- Add the system installation task (vponcova)
- Add methods for running remote DBus tasks (vponcova)
- Improved base clases for DBus tasks (vponcova)
- Do not manually create LUKSDevice when unlocking a LUKS format (vtrefny)
- Fix pylint errors (vponcova)
- Skip the pylint check for the bootloader.py (vponcova)
- Enable DNF depsolver debugging in debug mode (mkolman)
- Don't reset locale of our DBus daemon (vponcova)
- Close the DNF base later (#1571299) (vponcova)
- Add 10%% for storage metadata to the total required space (#1578395)
  (vponcova)
- Add hook to prevent mistake upstream pushes (jkonecny)
- Revert "WIP" (vponcova)
- WIP (vponcova)
- Set locale to en_US.UTF-8 in every module (#1575415) (vponcova)
- Move initial module configuration to the init function (vponcova)
- Fix the mount command (vponcova)
- Use the auto partitioning module in UI (vponcova)
- Only check space during a tui kickstart if ksprompt is enabled (bcl)
- Fix can't exit TUI storage spoke (jkonecny)
- Use PROCESSED_AND_CLOSE and PROCESSED_AND_REDRAW (jkonecny)
- Remove not required PROCESSED return (jkonecny)
- Remove PROCESSED from refresh method (jkonecny)

* Wed May 16 2018 Martin Kolman <mkolman@redhat.com> - 29.15-1
- nvdimm: make debug messages more clear (rvykydal)
- nvdimm: use libblockdev enum to check namespace mode (rvykydal)
- Add data loss warning to nvdimm reconfigure dialog. (rvykydal)
- Add UI feedback for disk repopulating after nvdimm reconfiguration.
  (rvykydal)
- Fix ignoring of nvdimm devices (rvykydal)
- Don't allow booting from nvdimm devices (rvykydal)
- Improve UI feedback for invalid boot on non-iBFT iSCSI devices. (rvykydal)
- Add inst.nonibftiscsiboot boot option. (rvykydal)
- Use only devices specified by nvdimm command for installation. (rvykydal)
- Add option to reconfigure nvdimm devices into sector mode. (rvykydal)
- Allow only devices in sector mode to be selected. (rvykydal)
- Add nvdimm devices to Advanced Storage spoke. (rvykydal)
- Add kickstart support for nvdimm reconfiguration to sector mode. (rvykydal)
- Ignore nvdimm disks which are not in sector mode. (rvykydal)
- Do not ignore nvdimm (pmemX) devices (rvykydal)
- Update the pykickstart commands (vponcova)
- Fix firewall DBUS module API usage (#1577405) (mkolman)
- Fix formatting in the TUI storage spoke (jkonecny)
- Fix TUI crash in mountpoint assignment (#1564067) (jkonecny)
- Fix KS logvol metadata and chunksize parameters (#1572511) (jkonecny)
- Show correct bootloader error on the MacEFI platform (vponcova)
- Revert "Fix broken kickstart command test" (rvykydal)
- Support fcoe --autovlan option (#1564096) (rvykydal)

* Fri May 04 2018 Martin Kolman <mkolman@redhat.com> - 29.14-1
- Increase module startup timeout to 600 seconds (mkolman)
- Fix name of the Zanata Python client package (mkolman)
- Add tests for the auto partitioning module (vponcova)
- Create the auto partitioning module (vponcova)
- Add the firewall submodule (mkolman)
- Once again fix cmdline error handling. (#1360223) (sbueno+anaconda)
- Extend the timeout period to 180s in the case of cmdline error. (#1360223)
  (sbueno+anaconda)
- Fix the clearpart test with disklabel option (vponcova)
- The specified nosetests failed to run (vponcova)

* Tue Apr 24 2018 Martin Kolman <mkolman@redhat.com> - 29.13-1
- Show correct root account locked status in reconfig mode (#1507940) (mkolman)
- Add missing lines and modularization only log to test coverage (jkonecny)
- Remove makebumpver dependency from spec file (jkonecny)
- network module: use connectivity checking in anaconda (rvykydal)
- network module: add connectivity checking (rvykydal)
- Permit adding disabled external repos to installation. (riehecky)
- Handle empty active attribute for consoles (#1569045) (mkolman)
- Support temporary kickstart generating (vponcova)
- Create the dynamic module User (vponcova)
- Select Workstation install class for Workstation live (#1569083) (awilliam)
- Rename the main module User to Users (vponcova)

* Thu Apr 19 2018 Martin Kolman <mkolman@redhat.com> - 29.12-1
- Save logs to result folder after rpm-tests (jkonecny)
- Add Installed pyanaconda tests (jkonecny)
- Fix name of the RPM test (jkonecny)
- Support running just chosen rpm test (jkonecny)
- Add test cache files to gitignore (jkonecny)
- Move test install test from Makefile to rpm tests (jkonecny)
- Create structure to run rpm tests (jkonecny)
- Move all nosetests to separate directory (jkonecny)
- Fix broken kickstart command test (jkonecny)
- Fix broken kickstart command test (jkonecny)
- localization: use LanguageKickstarted module property (#1568119) (rvykydal)
- Start only the specified kickstart modules (#1566621) (vponcova)
- Use the Bootloader module in UI (vponcova)
- Add tests for the bootloader module (vponcova)
- Create the bootloader module (vponcova)
- rpmostreepayload: do not require network for dvd installation (#1565369)
  (rvykydal)
- Fix double logging to stdout (vponcova)
- Don't try to create required partitions if there are none (vponcova)

* Thu Apr 12 2018 Martin Kolman <mkolman@redhat.com> - 29.11-1
- Add anaconda-install-env-deps as dependency of the anaconda package (mkolman)
- Add %%files for install-env-deps so it actually exists (awilliam)

* Tue Apr 10 2018 Martin Kolman <mkolman@redhat.com> - 29.10-1
- Bump simpleline version (mkolman)
- Do not redraw screen after text YesNo dialog (#1557951)(jkonecny)
- Revert "Adapt to a new simpleline changes (#1557472)(jkonecny)
- authselect: enable silent last log (pbrezina)
- authselect: fix typo to enable fingerprint authentication (pbrezina)

* Mon Apr 09 2018 Martin Kolman <mkolman@redhat.com> - 29.9-1
- Move install time dependencies to a metapackage (mkolman)

* Thu Apr 05 2018 Martin Kolman <mkolman@redhat.com> - 29.8-1
- Fix forgotten usage of the selinux kickstart command (vponcova)
- Fix tests for the storage module (vponcova)
- Use the disk selection and initialization modules in UI (vponcova)
- Enable to use object identifiers instead of object paths (vponcova)

* Thu Mar 29 2018 Martin Kolman <mkolman@redhat.com> - 29.7-1
- Add Makefiles for disk initialization and selection modules (vponcova)
- Remove the invalid self argument (vponcova)
- Run all unit tests (vponcova)

* Tue Mar 27 2018 Martin Kolman <mkolman@redhat.com> - 29.6-1
- Create the disk initialization and disk selection modules (vponcova)
- Use watch_property to watch changes of DBus properties (vponcova)
- Better organize the base classes for modules (vponcova)
- Fixed KS forcing zerombr onto RO disk (japokorn)
- Add tests for the kickstart specifications (vponcova)
- Standardize calls to parent via super() (riehecky)
- Fix 'isDisk' property name (#1558906) (vtrefny)
- Make the class for removed kickstart commands more strict (vponcova)
- Fix the progress bar steps (vponcova)
- Use enum for the first boot action (vponcova)
- Use enum for the SELinux modes (vponcova)
- datetime spoke: still pass ksdata to NTPconfigDialog (UIObject) (rvykydal)

* Mon Mar 19 2018 Martin Kolman <mkolman@redhat.com> - 29.5-1
- Write rootpw command to kickstart (#1557529) (mkolman)
- Don't make safe to observe services on buses that don't run (vponcova)
- Add the LanguageKickstarted property (vponcova)
- Don't autoquit by default if the last hub is empty (#1553935) (mkolman)
- Use the Services module in UI (vponcova)
- Create the Services module (vponcova)
- Enable hibernation only on x86 (#1554345) (vponcova)
- Add the Storage module with no API (vponcova)
- Add the Payload module with no API (vponcova)
- Remove DBus modules Foo and Bar (vponcova)
- network module: fix accessing org.freedesktop.hostname1 for current hostname
  (rvykydal)

* Mon Mar 12 2018 Martin Kolman <mkolman@redhat.com> - 29.4-1
- network module: add basic test (rvykydal)
- Add prepare command to setup-mock-test-env script (jkonecny)
- Mark partition live device's disk protected. (#1524700) (dlehman)

* Fri Mar 09 2018 Martin Kolman <mkolman@redhat.com> - 29.3-1
- Remove useless constants from pyanaconda.dbus.constants (vponcova)
- Use identifiers to get observers and proxies (vponcova)
- Remove the publish method from DBus interfaces (vponcova)
- Replace constants in publish and register methods (vponcova)
- Replace constants in DBus interface names (vponcova)
- Define DBus errors with the dbus_error decorator (vponcova)
- Use namespaces and identifiers to describe Anaconda DBus objects (vponcova)
- Add support for identification of DBus objects and services (vponcova)
- User module should parse only rootpw for now (#1553488) (vponcova)
- localization module: plug localization module into keyboard GUI spoke
  (rvykydal)
- localization module: add KeyboardKickstarted property (rvykydal)
- localization module: add KS support for keyboard command (rvykydal)
- localization module: don't use Kickstarted so another command can be added
  (rvykydal)
- Fix release docs (mkolman)
- network: set TYPE value in ifcfg from kickstart in initrmfs (rvykydal)
- Make formatting consistent in AnacondaWidgets.xml (riehecky)

* Mon Mar 05 2018 Martin Kolman <mkolman@redhat.com> - 29.2-1
- Use the user DBUS module in the UI (mkolman)
- Use the user DBUS module for the rootpw command in kickstart.py (mkolman)
- Add initial user DBUS module (mkolman)
- Add tests for the Security module (vponcova)
- Use the Security module in UI (vponcova)
- Don't send empty kickstart to DBus modules (vponcova)
- Add the Security module (vponcova)
- Fix makeupdates script to work with new DBus structure (jkonecny)
- Fix Makefile of the kickstart manager (vponcova)
- Fix check if dbus daemon quit properly (jkonecny)
- Remove check if dbus is running (#1551096) (jkonecny)
- Use Anaconda's special env variable for dbus address (#1551096) (jkonecny)
- Migrate Anaconda to our private dbus session (#1551096) (jkonecny)
- localization module: use l12 shortcut for module name in UI (rvykydal)
- localization module: replace ksdata.lang with the module in anaconda.
  (rvykydal)
- localization module: add KS support for lang command (rvykydal)
- Return restorecon utility to Fedora 28 mock (jkonecny)
- Include dbus.log when exporting logs (mkolman)
- Reorganize pyanaconda.modules.boss (vponcova)
- Move all DBus errors to pyanaconda.modules.common.errors (vponcova)
- Move common classes and functions to pyanaconda.modules.common (vponcova)
- Close DBus log file when quitting DBus session (jkonecny)
- Enable payload configuration for Install classes (jkonecny)
- Rename files that provide kickstart specifications (vponcova)
- Move the kickstart specification to pyanaconda.core.kickstart (vponcova)
- Start and quit Boss properly (jkonecny)
- Make class from dbus.launcher module (jkonecny)
- Add the kernel option resume= by default (#1206936) (vponcova)

* Wed Feb 28 2018 Martin Kolman <mkolman@redhat.com> - 29.1-1
- Use observers to access the hostname service (vponcova)
- Make safe to observe services on buses that don't have to run (vponcova)
- DBus logs are now saved to /tmp/dbus.log (jkonecny)
- Add tests for toplevel installclass attribs (riehecky)
- Wait for DBus modules for longer time (vponcova)
- Drop dependency on authselect and firewalld (vponcova)
- Fix kickstart version test (vponcova)
- Authconfig is replaced with authselect (#1542968) (vponcova)
- Add support for different message buses (vponcova)
- Fix makeupdates script (vponcova)
- Set up basic logging for DBus modules (vponcova)
- Remove get_dbus_module_logger (vponcova)
- Fix logging of the DBus modules (vponcova)
- Fix the reimport error (vponcova)
- Fix the network module specification (vponcova)
- network module: update_network_data test (rvykydal)
- network module: use Module.Kickstarted instead of ksdata.seen (rvykydal)
- network module: use for hostname in tui (rvykydal)
- network module: handle current hostname (rvykydal)
- network module: handle ksdata.network.hostname (rvykydal)
- network module: add module skeleton (rvykydal)
- Log changes in the kickstart modules. (vponcova)
- Use the Timezone module in UI. (vponcova)
- Start Boss from Anaconda (jkonecny)
- Do not use System DBus (jkonecny)
- Remove anaconda-boss.service (jkonecny)
- Move Anaconda dbus services and confs to session dbus (jkonecny)
- Run DBus session if not present (jkonecny)
- Change pykickstart version (vponcova)
- Move system-logos dependency from anaconda-core to anaconda-gui (mkolman)
- makebumpver: fix parsing of -m option (rvykydal)
- makebumpver: fix -i option (rvykydal)
- Fix tests of the Timezone module (vponcova)
- installclass: add comments to server install class (dusty)
- Don't use deprecated formatErrorMsg (vponcova)
- Use the KickstartError attributes (vponcova)
- kickstart: "clearpart --list" does not work (#1410335) (marcel)
- Use handler in the Timezone module (vponcova)
- Fix the specification of the Bar module (vponcova)
- Use the KickstartHandler class (vponcova)

* Mon Feb 19 2018 Martin Kolman <mkolman@redhat.com> - 28.22-1
- Prevent anaconda-core requiring gjs-console (awilliam)
- Temporarily don't test versions of specified kickstart objects (vponcova)

* Mon Feb 19 2018 Martin Kolman <mkolman@redhat.com> - 28.21-1
- Explain when run dependency_solver without options (jkonecny)
- Clean dd_test code (jkonecny)
- We can't set file permission mode for .so in dd test (jkonecny)
- Rename installclass_atomic to Fedora Atomic Host (jkonecny)
- Support running only nosetests or only some nosetests (jkonecny)
- Do not run tests as root (jkonecny)
- Save start and end time for pylint run (jkonecny)
- Separate grab-logs from ci target in Makefile (jkonecny)
- Remove false positive but disable Pylint in makeupdates script (jkonecny)
- Add copyright to scripts in ./scripts/testing (jkonecny)

* Thu Feb 15 2018 Adam Williamson <awilliam@redhat.com> - 28.20-2
- Prevent anaconda-core requiring gjs-console (awilliam)

* Fri Feb 09 2018 Martin Kolman <mkolman@redhat.com> - 28.20-1
- Check the proxy attribute before accessing it (vponcova)
- Check the noverifyssl attribute before accessing it (vponcova)
- Don't access the url attribute (#1530428) (vponcova)
- Use Fedora Server default partitioning in Atomic (jkonecny)
- Clean code of Atomic install class (jkonecny)
- Migrate Atomic install class (#1491287) (jkonecny)
- Move Atomic install class to Anaconda (#1491287) (#1536853) (jkonecny)
- Make sure that fetch_url is defined. (vponcova)

* Mon Feb 05 2018 Martin Kolman <mkolman@redhat.com> - 28.19-1
- Change pykickstart version. (vponcova)
- Do not deepcopy the kickstart data in the storage (vponcova)
- Replace deepcopy of the method command (vponcova)
- Use pykickstart 3 (vponcova)
- Provide comprehensive log messages about the display mode (vponcova)
- Fix missing logging in some cases of update of ONBOOT value. (rvykydal)
- Fix tests for the timezone module. (vponcova)
- Add the Kickstarted property to the kickstart modules. (vponcova)
- Connect to the observed service and other stuff. (vponcova)
- Prevent 99-copy-lgs.ks from exiting with a 1 (bcl)
- Rename SetUTC to SetIsUTC in the timezone module. (vponcova)

* Thu Jan 18 2018 Martin Kolman <mkolman@redhat.com> - 28.18-1
- Move how to use setup-mock-test-env script to help (jkonecny)
- Add --init as new parameter to setup-mock-test-env (jkonecny)
- Initialize the thread manager at the first import. (vponcova)
- Added tests for the timezone module and other. (vponcova)
- Remove 'i' from iutil module (jkonecny)
- Remove 'i' from isignal module (jkonecny)
- Move isignal module to core/isignal (jkonecny)
- Extract process watch functions to a static class (jkonecny)
- Move regexes module to core/regexes (jkonecny)
- Move i18n module to core/i18n (jkonecny)
- Move constants module to core/constants (jkonecny)
- Move iutil module to core/iutil (jkonecny)
- Move async_utils to core/async_utils (jkonecny)
- Replace gobject GLib by our core/glib (jkonecny)
- Rename run_in_main_thread to run_in_loop (jkonecny)
- Add Timer and PidWatcher abstraction above GLib (jkonecny)
- Create abstraction above GLib event loop (jkonecny)
- Add core/glib module for GLib access (jkonecny)
- Ignore errors for KickstartSpecificationHandler. (vponcova)
- Try to use the PropertiesChanged signal. (vponcova)
- Add timezone module. (vponcova)
- Collect properties changes before emit. (vponcova)
- Use Ping method from the standard interface. (vponcova)
- Recognize members of standard interfaces. (vponcova)
- Add an object observer with cached properties (vponcova)
- Rename modules with Fedora install classes. (vponcova)
- Add support for Variant in .buildstamp (vponcova)
- Fix the Bar module. (vponcova)
- Add pykickstart version to branching policy doc (jkonecny)
- Remove `unstable` branch from documentation (jkonecny)
- Move system-logos to anaconda-core (#1529239) (bcl)

* Fri Jan 05 2018 Martin Kolman <mkolman@redhat.com> - 28.17-1
- Modules should use the proxy pattern. (vponcova)
- Variants need to be instances of the Variant class (vponcova)
- kickstart: support firewall --use-system-defaults (#1526450) (dusty)
- Check payload is set before accessing its data (#1524785) (mkolman)
- Do not fail when test are failing in setup-env script (jkonecny)
- Support running multiple commands at once (jkonecny)
- Support copy Anaconda result dir out of mock (jkonecny)
- Remove dependencies from Makefile (jkonecny)
- Add path to Anaconda in mock to constant (jkonecny)
- Properly exclude packages from the install set (ngompa13)
- Add the _prepare_command helper function to setup-test-env (jkonecny)
- Add run-tests parameter to setup-test-env script (jkonecny)
- Remove /anaconda in mock before copying new one (jkonecny)

* Tue Jan 02 2018 Martin Kolman <mkolman@redhat.com> - 28.16-1
- Improve password checking status and error messages (mkolman)
- Spin kickstarts shouldn't be test dependency (jkonecny)

* Wed Dec 20 2017 Martin Kolman <mkolman@redhat.com> - 28.15-1
- Remove spurious echo call from tmux service file (#1526861) (mkolman)
- Restore fix for RHBZ #1323012 (`set_name` not `setName`) (awilliam)
- Fix Makefile for modules/[foo,bar]/tasks and for install_manager (rvykydal)
- Make passing kickstart to boss more visible. (rvykydal)
- Add tests for KickstartManager. (rvykydal)
- Add kickstart dispatching to anaconda. (rvykydal)
- Add kickstart dispatching to local boss run script (rvykydal)
- Add KickstartManager for Boss. (rvykydal)
- Add method for getting line mapping from kickstart elements to kickstart
  (rvykydal)
- Add info about handled kickstart commands to modules (rvykydal)
- Add missing Makefile for kickstart_dispatcher (rvykydal)

* Mon Dec 18 2017 Martin Kolman <mkolman@redhat.com> - 28.14-1
- Use observers in the install manager (vponcova)
- Modify readme file for tests (jkonecny)
- Do not bump version when testing installation (jkonecny)
- Add set up test environment script (jkonecny)
- Add dependency solver script (jkonecny)
- Differentiate upstream and build-time version (#1493952) (mkolman)
- Fix bad bash '*' expansion when loading kernel modules (#1525841) (jkonecny)
- Fix connection to a signal in the install manager (vponcova)
- Use the InterfaceTemplate in the InstallationInterface (vponcova)
- Use the InterfaceTemplate in the TaskInterface (vponcova)
- Add a base class for DBus interfaces (vponcova)
- Update module manager to use observers (vponcova)
- Add DBus observers for better access to proxies. (vponcova)
- Remove running CI in mock from Makefile (jkonecny)
- Add xfsprogs and git to the test requirements (jkonecny)
- The gettext-devel is required by autogen (jkonecny)
- Remove kickstart-test dependencies from test requires (jkonecny)

* Tue Dec 12 2017 Martin Kolman <mkolman@redhat.com> - 28.13-1
- Unregister and unpublish all DBus services and objects (vponcova)
- Add tests for InstallManager (jkonecny)
- Add tests for Tasks (jkonecny)
- Add run_in_glib decorator for tests (jkonecny)
- Instantiate and publish InstallManager in Boss (jkonecny)
- Add Makefile for install_manager (jkonecny)
- Implement InstallManager with interface (jkonecny)
- Init threading in modules (jkonecny)
- Provide installation tasks from modules (jkonecny)
- Remove *.Anaconda.Modules interface from Boss (jkonecny)
- Implementing example tasks for modules (jkonecny)
- Add Makefile for Task (jkonecny)
- Base implementation of Task (jkonecny)
- Add Task interface class (jkonecny)
- Remove in-memory kickstart representation from traceback file (#1519895)
  (mkolman)
- Support call_when_thread_terminates in ThreadManager (jkonecny)
- Change gtk_action_wait/nowait as general use decorators (jkonecny)
- Add controllable loop to run_boss_locally script (jkonecny)
- Tweak run_boss_locally script (jkonecny)
- Enable SE/HMC file access to repo (vponcova)
- Change string formatting to format method (jkonecny)
- Pass handler instance, not class to SplitKickstartParser (rvykydal)
- Add kickstart parser for splitting kickstart (rvykydal)

* Thu Dec 07 2017 Martin Kolman <mkolman@redhat.com> - 28.12-1
- Fix unit tests (mkolman)
- Fixes in makefiles (vponcova)
- Use the input_checking module for TUI password validation (mkolman)
- Use the input_checking module for user checking (mkolman)
- Use the input_checking module for root password checking (mkolman)
- Use the input_checking module for checking the LUKS passphrase (mkolman)
- Reflect GUISpokeInputCheckHandler changes in installation source spoke
  (mkolman)
- Convert the input checking helpers to use the input_checking module (mkolman)
- Provide more robust method of using the warning message bar (mkolman)
- Remove the validatePassword() method (mkolman)
- Add new input checking module (mkolman)
- fixup! Migrate Workstation InstallClass to anaconda (sgallagh)
- Handle an invalid install class style sheet (vponcova)
- Enhance password checking constants (mkolman)
- Fix interactive defaults (mkolman)
- Modify the PYTHONPATH in run_boss_locally (vponcova)
- Replace get_bus with the class DBus (vponcova)
- Migrate Workstation InstallClass to anaconda (sgallagh)
- Point at new path for fedora-server.css (sgallagh)
- Rename dbus_constants to constants (vponcova)
- Add the boot option inst.ks.all (vponcova)
- Add the boot option inst.stage2.all (vponcova)
- Remove errors for mounting and unmounting (vponcova)
- Override the right method in the task (vponcova)
- Remove useless code (vponcova)
- Support timeout and retries options in %%packages section (vponcova)
- Fix device_name_is_disk to fully support raid devices (vponcova)
- Onlyuse devices of the ignoredisk command should be only disks (vponcova)
- Add the boot option inst.xtimeout (vponcova)
- Do not shadow build-in module variable (jkonecny)
- Module manager is replaceable (jkonecny)
- Remove pyanaconda.constants_text module (vponcova)

* Mon Nov 27 2017 Martin Kolman <mkolman@redhat.com> - 28.11-1
- Bump Blivet GUI version (mkolman)
- Change path to start-module script when running locally (mkolman)
- Handle DBUS module related files in makeupdates (mkolman)
- Handle DBUS_STARTER_ADDRESS not being defined (mkolman)
- Use start-module script in DBUS service files (mkolman)
- Add a DBUS module startup script (mkolman)
- Add Makefile.am for DBUS modules an addons (mkolman)
- Add the setup-updates script (mkolman)
- Add __init__.py file to anaconda/modules (mkolman)
- Add a unit file for Boss startup (mkolman)
- Really install all the right packages on Mac UEFI installs (awilliam)
- Refactor DASD formatting and support detection of LDL DASDs. (vponcova)
- Remove unused import sys from run_boss_locally script (jkonecny)
- Fix blivet imports in the Fedora Server install class (#1513024) (vponcova)
- Update the use of suggest_container_name method (vponcova)
- Devicetree doesn't have protected_dev_names (vponcova)
- Add pyanaconda.dbus to Makefile (vponcova)
- Add pyanaconda.storage to Makefile (#1511735) (vponcova)
- network: GUI, be more robust when displaying vlan parent and id (#1507913)
  (rvykydal)
- network: GUI, fix lookup of existing device configurations (#1507913)
  (rvykydal)
- network: GUI, don't crash on added vlan without device name specified
  (#1507913) (rvykydal)
- Add a script for running Boss & modules locally (mkolman)
- Add an example addon (mkolman)
- Add DBUS module examples (mkolman)
- Add Boss (mkolman)
- Add a base class for DBUS modules (mkolman)
- Add .service and .conf files for the DBUS modules (mkolman)
- Add constants for DBUS module namespaces (mkolman)
- Add support for logging from DBUS modules (mkolman)
- Add the get_bus() method (mkolman)
- Remove storage check for too small swap (#1466964) (vponcova)
- Migrate fedora-server installclass into the anaconda repository (#1466967)
  (rvykydal)

* Thu Nov 09 2017 Martin Kolman <mkolman@redhat.com> - 28.10-1
- Bump required Blivet version to 3.0 (mkolman)
- Add modular server repo to the base repositories (#1506894) (jkonecny)
- Split addon and environment refresh in software TUI (jkonecny)
- Fix changing source don't erase old environment TUI (#1505090) (jkonecny)
- Add logging to TUI software selection spoke (#1505090) (jkonecny)
- Do not try to use protected disks for autopart (vtrefny)
- Adapt new storage tui spoke to storage code move. (dlehman)
- Update blivet upstream URL in testing README. (dlehman)
- Adapt to devicefactory API change. (dlehman)
- Adapt to removal of default rounding in blivet.size.Size. (dlehman)
- Use anaconda's logic for ostree sys/physical root. (dlehman)
- Adapt to removal of blivet.udev.device_is_realdisk. (dlehman)
- Adapt to move of disklabel type logic into DiskLabel. (dlehman)
- Move blivet.partspec into pyanaconda.storage. (dlehman)
- Move blivet.platform to pyanaconda.platform. (dlehman)
- Fix traceback from mocked partitions in clearpart test. (dlehman)
- Move blivet.osinstall to pyanaconda.storage. (dlehman)
- Move autopart from blivet to pyanaconda.storage. (dlehman)

* Thu Oct 26 2017 Martin Kolman <mkolman@redhat.com> - 28.9-1
- Mac EFI installs need grub2-tools (#1503496) (awilliam)
- network: create default ifcfg also for missing default NM connection
  (#1478141) (rvykydal)
- Print screen stack next to exception in TUI (jkonecny)
- Enable Custom GRUB2 Password Utility (#985962) (rmarshall)

* Tue Oct 17 2017 Martin Kolman <mkolman@redhat.com> - 28.8-1
- Bump simpleline version requires (jkonecny)
- Remove DataHolder class (jkonecny)
- Remove EditTUISpoke EditTUIDialog and EditTUISpokeEntry (jkonecny)
- Replace EditTUI* from the TUI Storage spoke (jkonecny)
- Replace EditTUI* from the TUI User spoke (jkonecny)
- Replace EditTUI* from the TUI Source spoke (jkonecny)
- Replace EditTUI* from the TUI Network spoke (jkonecny)
- Password spoke is using PasswordDialog now (jkonecny)
- Return default policy if nothing match (jkonecny)
- Add Dialog and PasswordDialog TUI objects (jkonecny)
- Remove EditTUIDialog from time_spoke (jkonecny)
- packaging: clear downloaded packages repo cache before using it (#1480790)
  (rvykydal)
- Do substitutions only after translating the string (mkolman)
- Fix a translation check error (mkolman)
- Do not run commands in messages in Makefile (jkonecny)
- Fix storage spoke completeness checking (#1496416) (rvykydal)

* Thu Oct 12 2017 Martin Kolman <mkolman@redhat.com> - 28.7-1
- Mark the mount point assignment in TUI as experimental (vpodzime)
- Reset storage on change in text mode (vpodzime)
- Only allow the supported file systems in text mode (vpodzime)
- Textual configuration of mount points (vpodzime)
- Add support for the new 'mount' kickstart command (vpodzime)
- Fix dnf exception repository not set (#1495211) (jkonecny)
- Add logging of complete spokes in GUI. (rvykydal)
- Do not execute storage when the spoke is left with no selected disk
  (#1496327) (rvykydal)
- Reflect building from master branch in the release docs (mkolman)
- Add checks for group names (#1497676) (vponcova)
- Add new checks for user names (#1491006) (vponcova)

* Fri Sep 29 2017 Martin Kolman <mkolman@redhat.com> - 28.6-1
- Add changelog entries from the unstable branch (mkolman)
- Log when we are executing command in chroot (jkonecny)
- Use name instead of index in TUI env selection (#1495204) (jkonecny)
- Fix missing container in TUI source spoke (#1494801) (jkonecny)
- Add MOCK_EXTRA_ARGS to Makefile (jkonecny)
- tui source spoke: initialize nfs values when switching to nfs (rvykydal)
- Deselect encryption when switching to blivet-gui partitioning (vtrefny)
- Add 2 spaces between functions in iutil (jkonecny)
- rpmostreepayload: Fix logic for copying of EFI data (walters)
- rpmostreepayload: Avoid recursing for fstab mounts (walters)
- payload: Add handlesBootloaderConfiguration(), teach bootloader.py (walters)

* Thu Sep 21 2017 Martin Kolman <mkolman@redhat.com> - 28.5-1
- Fix missing id to name environment transition (#1491119) (jkonecny)
- Fix test for unset TUI software environment (#1491119) (jkonecny)
- Rename processingDone to processing_done variable (jkonecny)

* Mon Sep 18 2017 Martin Kolman <mkolman@redhat.com> - 28.4-1
- network: add support for kickstart --bindto=mac for virtual devices
  (#1328576) (rvykydal)
- network: support mac bound network settings as first class (#1328576)
  (rvykydal)
- network: add support for kickstart --bindto=mac for wired devices (#1328576)
  (rvykydal)
- Don't setup the hub twice (#1491333) (vponcova)
- rpmostreepayload: Substitute ${basearch} in ostreesetup ref (walters)
- Perform repo checks only when there are checks available. (rvykydal)
- Add support for repo --metalink (GUI) (#1464843) (rvykydal)
- Add support for repo --metalink (kickstart, tui) (#1464843) (rvykydal)
- Add inst.notmux option (dusty)

* Mon Sep 11 2017 Martin Kolman <mkolman@redhat.com> - 28.3-1
- Add missing dot to the availability status message (mail)
- Bump Simpleline version (jkonecny)
- Make EFIGRUB._efi_binary a property, not a method (awilliam)
- Better storing logs from build and tests (jkonecny)
- Provide a default install class. (vponcova)
- Do not use hidden install classes. (vponcova)
- Make geolocation with kickstart possible (#1358331) (mkolman)
- Run python-meh as modal in TUI (jkonecny)
- Use GLib event loop in the simpleline (jkonecny)
- TUI progress reporting is handled by show_all (jkonecny)
- Add efi_dir to the BaseInstallClass (#1412391) (vponcova)
- Use /usr/bin/python3 shebang once again (miro)

* Mon Sep 04 2017 Martin Kolman <mkolman@redhat.com> - 28.2-1
- Fix catch TUI not main thread exceptions (jkonecny)
- Document Anaconda branching workflow (mkolman)
- Use constants for version number bumps and additions (mkolman)
- Fix closest mirror now needs network (jkonecny)
- Fix restart payload thread in Network spoke GUI (#1478970) (jkonecny)
- Network spoke freeze when testing availability (#1478970) (jkonecny)
- Add support for adding version numbers to makebumpver (mkolman)
- Add support for major version bump to makebumpver (mkolman)
- Fix proxy settings badly used when testing repos (#1478970) (jkonecny)

* Tue Aug 29 2017 Martin Kolman <mkolman@redhat.com> - 28.1-1
- Remove the metacity theme. (vponcova)
- Add the option inst.decorated to allow title bar in GUI (vponcova)
- Move python3-gobject Requires to core (jkonecny)
- Return simpleline removed ipmi calls back (jkonecny)
- Use new list container from Simpleline (jkonecny)
- Remove old simpleline from anaconda (jkonecny)
- Ask multiple times for wrong input (jkonecny)
- Show TUI exception only first time (jkonecny)
- Add simpleline logger to the Anaconda (jkonecny)
- Modify TUI to use new Simpleline package (jkonecny)
- Make 64-bit kernel on 32-bit firmware work for x86 efi machines (pjones)
- Add missing gtk3 required version to spec file (jkonecny)
- Sort spec required versions alphabetically (jkonecny)
- Fix testing of the kickstart version (vponcova)
- Move the installclass command to the %%anaconda section. (vponcova)
- Fix SL install class to use right efi dir (riehecky)
- Fix accelerator key for blivet-gui partitioning (#1482438) (vtrefny)
- Add blivet-gui logs to python-meh file list (vtrefny)
- Remove the title bar in anaconda by default (#1468801) (vponcova)
- Add simple script to read journal with message code source and thread info.
  (rvykydal)

* Mon Aug 14 2017 Martin Kolman <mkolman@redhat.com> - 27.20-1
- Add support for automatic generating of DBus specification. (vponcova)
- Add support for generating XML (vponcova)
- Add support for DBus typing system (vponcova)
- dnfpayload: do not try to contact disabled repo (artem.bityutskiy)
- Add message to setup-test-env is ran (jkonecny)
- Use SHA256 instead of MD5 for repoMDHash (#1341280) (bcl)
- Add lorax-packages.log to bug report. (rvykydal)
- Use SHA256 instead of MD5 for repoMDHash (#1341280) (jkonecny)
- 80-setfilecons: Add a few paths (/var/run, /var/spool) (walters)
- Also capture anaconda-pre logs if they exist (riehecky)
- Don't mock modules with sys in unit tests (vponcova)
- logging: replace SyslogHandler with JournalHandler (rvykydal)
- Add setup-test-env target to the Makefile (jkonecny)
- Add tests for the install class factory (vponcova)
- Support for the installclass kickstart command (vponcova)
- Modules with install classes should define __all__ (vponcova)
- Refactorization of the installclass.py (vponcova)
- docs: minor fixups of release document (rvykydal)
- rescue: add RTD documentation (rvykydal)
- rescue: clean up method for mounting root (rvykydal)
- rescue: separate UI and execution logic (rvykydal)
- Make kickstart rescue command noninteractive. (rvykydal)
- Remove unused argument and code. (rvykydal)

* Thu Jul 27 2017 Radek Vykydal <rvykydal@redhat.com> - 27.19-1
- rpmostreepayload: Set up /var first (walters)
- rpmostreepayload: Explicitly create /var/lib before tmpfiles (walters)
- rpmostreepayload: Rework mount setup to support admin-defined mounts
  (walters)
- rpmostreepayload: try to verify local ostree repo cache (dusty)
- rpmostreepayload: ignore <F25 location, support RHEL (dusty)
- rpmostreepayload: use correct secondary url location (dusty)
- Add tracking of requirements application to requirements container.
  (rvykydal)
- Add langpacks via payload requirements (rvykydal)
- Add NTP_PACKAGE via installation requirements (rvykydal)
- timezone: simplify kickstart setup metod (rvykydal)
- Store payload (packages, groups) requirements in a container. (rvykydal)
- Fix anaconda --help fail with traceback (#1470514) (jkonecny)
- rpmostreepayload: Do /sysroot mount non-recursively (walters)
- Add isolated-test makefile target (jkonecny)
- gui: show supported locales on Atomic Host installs (jlebon)

* Mon Jul 03 2017 Martin Kolman <mkolman@redhat.com> - 27.18-1
- rpmostreepayload: Reuse the local repo as a cache (walters)
- Document how to create Anaconda releases and package builds (mkolman)

* Sat Jul 01 2017 Martin Kolman <mkolman@redhat.com> - 27.17-1
- Require "blivet-gui-runtime" instead of "blivet-gui" (vtrefny)
- Fix a typo in python-meh initialization (#1462825) (mkolman)

* Mon Jun 26 2017 Martin Kolman <mkolman@redhat.com> - 27.16-1
- Install class shouldn't set the default boot fstype (#1463297) (vponcova)
- Store testing logs properly (jkonecny)
- Fix location of the blivet-gui user help (vtrefny)
- netowrk: fix noipv6 option check regression (#1464297) (rvykydal)
- Refactor imports in kickstart.py (jkonecny)
- Use context manager to check KickstartError (jkonecny)

* Wed Jun 21 2017 Martin Kolman <mkolman@redhat.com> - 27.15-1
- Honor --erroronfail kickstart option in cmdline mode (rvykydal)
- Fix import from a renamed module (#1462538) (vponcova)
- Fix the 'non-ASCII characters in password' checks (#1413813) (awilliam)
- Move mock config files to slaves (jkonecny)

* Thu Jun 15 2017 Martin Kolman <mkolman@redhat.com> - 27.14-1
- Bump version of Pykickstart and Blivet (#1113207) (jkonecny)
- Add XFS uuid changer (#1113207) (jkonecny)
- Support --when parameter in snapshot (#1113207) (jkonecny)
- Add snapshot support (#1113207) (jkonecny)

* Wed Jun 14 2017 Martin Kolman <mkolman@redhat.com> - 27.13-1
- Fix source.glade renaming mixup (#1461469) (mkolman)
- Separate blivet-daily builds in mock config (jkonecny)
- network: bind to device name (not hwaddr) when dumping connections (#1457215)
  (rvykydal)

* Tue Jun 13 2017 Martin Kolman <mkolman@redhat.com> - 27.12-1
- Show warning if swap is smaller then recommended (#1290360) (vponcova)

* Tue Jun 06 2017 Martin Kolman <mkolman@redhat.com> - 27.11-1
- Fix renaming error (mkolman)
- Add a getter for the Anaconda root logger (mkolman)
- Disable test-install in Makefile (jkonecny)

* Thu Jun 01 2017 Martin Kolman <mkolman@redhat.com> - 27.10-1
- Bump Blivet version (mkolman)
- Remove GUI logging prefixes from Network spoke (mkolman)
- Rename TUI spokes (mkolman)
- Rename GUI spokes (mkolman)
- Rename anaconda_argparse.py to argument_parsing.py (mkolman)
- Rename install_tasks.py to installation_tasks.py (mkolman)
- Rename install.py to installation.py (mkolman)
- Rename threads.py to threading.py (mkolman)
- Get special purpose loggers from anaconda_loggers (mkolman)
- Use structured logging in Anaconda modules (mkolman)
- Use unique 3 letter log level names (mkolman)
- Use constants for special purpose logger names (mkolman)
- Add the anaconda_loggers module (mkolman)
- Rename anaconda_log.py to anaconda_logging.py (mkolman)
- Add support for structured logging to the anaconda logger (mkolman)
- Make it possible to set filters for file handlers (mkolman)
- Add custom filter and formatter support for the syslog handler (mkolman)
- Add AnacondaPrefixFilter (mkolman)
- Fixes for Pylint 1.7 (vponcova)
- Add support for IPoIB in tui (#1366935) (rvykydal)
- Fix pylint unused import error (jkonecny)
- network: handle multiple connections for one device better (#1444887)
  (rvykydal)
- Fix setting errors and warnings in the StorageCheckHandler (vponcova)
- Add inst.waitfornet option (#1315160) (rvykydal)
- network: catch exception when reading in-memory connection being removed
  (#1439220) (rvykydal)

* Thu May 25 2017 Martin Kolman <mkolman@redhat.com> - 27.9-1
- Add support for DNF-2.5.0 (jkonecny)
- Fix simpleline_getpass related Pylint warning (mkolman)
- Provide access to simpleline App instance (mkolman)
- Make it possible to use a custom getpass() (mkolman)
- Set the default filesystem type from a kickstart file (vponcova)
- Adapt to our new daily builds of Anaconda (jkonecny)
- Provide access to simpleline App instance (mkolman)
- Make it possible to use a custom getpass() (mkolman)
- Perform recursive copying of driver disk RPM repo contents (esyr)
- network: fix setting hostname via boot options (#1441337) (rvykydal)
- Fix a typo in an error message (esyr)
- Use the function we already have for applying disk selection (#1412022)
  (rvykydal)
- Ignore disks labeled OEMDRV (#1412022) (rvykydal)
- network: create dracut arguments for iSCSI root accessed via vlan (#1374003)
  (rvykydal)
- Test if Anaconda can be installed inside of mock (jkonecny)
- Remove run_install_test test (jkonecny)
- rpmostreepayload: Handle /var as a user-specified mountpoint (walters)
- Fix the addon handlers for the checkbox (#1451754) (vponcova)
- Show the text of completions in the datetime spoke. (vponcova)
- Use new daily-blivet copr builds (jkonecny)
- Prevent TUI from crashing with a single spoke on a hub (mkolman)

* Tue May 09 2017 Martin Kolman <mkolman@redhat.com> - 27.8-1
- Bump Pykickstart version (mkolman)

* Fri May 05 2017 Martin Kolman <mkolman@redhat.com> - 27.7-1
- Make some missed adjustments to blivet API changes. (#1440134) (dlehman)
- Bump required version for blivet-gui (vtrefny)
- BlivetGuiSpoke: Set keyboard shortcuts for blivet-gui (#1439608) (vtrefny)
- BlivetGuiSpoke: Refresh blivet-gui UI after spoke is entered (vtrefny)
- Really fix with tmux 2.4 (version comparison was busted) (awilliam)
- Show or hide the content of the expander on Fedora (vponcova)
- itertools.chain can be iterated only once (#1414391) (vponcova)

* Fri Apr 28 2017 Martin Kolman <mkolman@redhat.com> - 27.6-1
- Use `time.tzset()` to apply timezone changes when we can (awilliam)
- Tweak epoch definition to fix system clock setting (#1433560) (awilliam)
- Optimize payload thread restart on network change (jkonecny)
- Add unit test for RepoMDMetaHash object (#1373449) (jkonecny)
- Make the formating in payload consistent (#1373449) (jkonecny)
- Fix Anaconda forces payload restart when network (not)change (#1373449)
  (jkonecny)
- Catch race-condition error reading from in-memory connection being removed
  (#1373360) (rvykydal)
- network tui: fix changing ipv4 config from static to dhcp (#1432886)
  (rvykydal)
- Allow setting up bridge for fetching installer image from kickstart
  (#1373360) (rvykydal)

* Thu Apr 27 2017 Martin Kolman <mkolman@redhat.com> - 27.5-1
- make anaconda working back again with tmux2.4 (pallotron)
- Trigger the entered signal only once the screen is shown (#1443011) (mkolman)
- Use constants in storage checker constraints. (vponcova)
- Gtk: Fix creating images from resources. (vponcova)
- Fix partial kickstart software selection in GUI (#1404158) (jkonecny)
- Removed unused code in the Software spoke (#1404158) (jkonecny)
- Fix selection logic in Software spoke (#1404158) (jkonecny)
- Fix Driver Disc documentation (#1377233) (jkonecny)
- Support DD rpm loading from local disk device (#1377233) (jkonecny)
- Gtk: Replace deprecated get_misc_set_alignment in widgets. (vponcova)
- Gtk: Replace deprecated Gtk.Viewport.get_v/hadjustment. (vponcova)
- Gtk: Replace deprecated methods. (vponcova)
- Set the info bar only once if the partitioning method changes. (vponcova)
- Fix pylint issue Catching too general exception Exception (jkonecny)
- Support --noboot and --noswap options in autopartitioning (#1220866)
  (vponcova)
- Support --nohome option in the autopartitioning (vponcova)

* Tue Apr 11 2017 Martin Kolman <mkolman@redhat.com> - 27.4-1
- Hide options based on storage configuration method (#1439519) (mkolman)
- Catch exception when reading from in-memory connection being removed
  (#1439051) (rvykydal)
- docs/boot-options.rst: Fix #dhcpd anchor (mopsfelder)
- docs/boot-options.rst: Remove trailing spaces (mopsfelder)
- Fix logging of the storage checker report. (vponcova)
- Fix a property name of luks devices in storage checking (#1439411) (vponcova)
- Bump required version for blivet-gui (vtrefny)
- Use newly created swaps after the installation (#1439729) (vtrefny)
- docs/boot-options.rst: Fix #dhcpd anchor (mopsfelder)
- docs/boot-options.rst: Remove trailing spaces (mopsfelder)
- Set default FS type for blivet-gui (#1439581) (vtrefny)
- Display progress for the post installation phase (mkolman)
- Display progress for the post installation phase (mkolman)
- Increase verbosity of lvmdump in pre logging script (#1255659) (jkonecny)

* Thu Mar 30 2017 Martin Kolman <mkolman@redhat.com> - 27.3-1
- Enable the install class to customize the storage checking (vponcova)
- Replace sanity check with more advanced storage checker (vponcova)
- Various log-capture script improvements (mkolman)
- Rename StorageChecker to StorageCheckHandler (vponcova)

* Thu Mar 16 2017 Martin Kolman <mkolman@redhat.com> - 27.2-1
- Correction of some typographic mistakes in documentation. (rludva)
- Fix bullet point formatting in contribution guidelines (mkolman)
- Propagate firstboot --disable to Screen Access Manager (mkolman)
- util: Add script to capture logs (riehecky)
- Fix a typo (mkolman)
- Correction of some typographic mistakes in documentation. (rludva)
- Enhance git-find-branch script (jkonecny)
- Improve how storage configuration settings are displayed (mkolman)
- util: Add script to capture logs (riehecky)
- Propagate firstboot --disable to Screen Access Manager (mkolman)

* Mon Mar 06 2017 Martin Kolman <mkolman@redhat.com> - 27.1-1
- We should not have pyanaconda submodules on PYTHONPATH (vponcova)
- Lock empty root password during kickstart installation (#1383656) (mkolman)
- Use system Python when running Anaconda (mkolman)
- Remove unused false positives for pylint (vtrefny)
- Fix pylint error in BlivetGUI spoke (vtrefny)
- Fix tests by renaming packaging to payload (jkonecny)
- Rescue mode should wait for the storage and luks devices (#1376638) (vponcova)

* Mon Feb 27 2017 Martin Kolman <mkolman@redhat.com> - 26.21-1
- Add blivet-gui as requirement for the GUI package (vtrefny)
- Add a bottom bar to the Blivet GUI spoke (mkolman)
- Hide storage config spokes marked by SAM as visited (mkolman)
- Keep last used partitioning method selected (mkolman)
- Rollback planned storage changes if partitioning method changes (mkolman)
- Add blivet-gui spoke (vpodzime)
- docs: fix formating a bit for Links (Frodox)
- Fix a typo (mkolman)
- Polish unsupported filesystems in the custom spoke (jkonecny)

* Tue Feb 07 2017 Martin Kolman <mkolman@redhat.com> - 26.20-1
- Update dracut test for network --ipv6gateway (rvykydal)
- Correctly propagate --ipv6gateway to ifcfg files(#1170845) (mkolman)
- network: respect --activate value for bridge from kickstart (rvykydal)
- network: fix --activate for bridge slaves configured via %%pre ks (rvykydal)
- network: activate bridge for first network command in ks via %%pre (rvykydal)
- network: unify slave connection names for ks %%pre with ks and gui (rvykydal)
- network: bind slave connections to DEVICE, not HWADDR (#1373360) (rvykydal)
- Do not allow creating ntfs filesystem in custom spoke (vtrefny)
- Various minor formatting fixes (mkolman)
- PEP8 and refactoring for packaging (mkolman)
- PEP8 and refactoring for vnc.py (mkolman)
- PEP8 and refactoring for storage_utils.py (mkolman)
- PEP8 and refactoring for network.py (mkolman)
- PEP8 and refactoring for kickstart.py (mkolman)
- PEP8 and refactoring for image.py (mkolman)
- Cosmetic PEP8 and refactoring for flags.py (mkolman)
- PEP8 and refactoring for exception.py (mkolman)
- PEP8 and refactoring for bootloader.py (mkolman)
- PEP8 and refactoring for anaconda_log.py (mkolman)
- Validate dasd and zfcp user input (#1335092) (vponcova)
- network: use introspection data from libnm instead of libnm-glib (lkundrak)

* Mon Jan 16 2017 Martin Kolman <mkolman@redhat.com> - 26.19-1
- Use initialization controller for spoke initialization (mkolman)
- Add module initialization controller (mkolman)
- Fix link to the documentation in the README file (jkonecny)
- There is no thread for dasd formatting in tui. (vponcova)
- Move the (mkolman)
- Fix the status of the StorageSpoke for dasd formatting (#1274596) (vponcova)

* Mon Jan 09 2017 Martin Kolman <mkolman@redhat.com> - 26.18-1
- Always refresh the size of swap before autopartitioning. (vponcova)
- Run the space check only if the spokes are complete (#1403505) (vponcova)
- Ignore result directory with logs from tests (jkonecny)
- Disable pylint no-member error for re.MULTILINE (jkonecny)
- Fix nosetests to use newest python3 (jkonecny)
- Disable the button if iscsi is not available (#1401263) (vponcova)
- Include Python 3.6 sysconfigdata module in initramfs (#1409177) (awilliam)
- Nicer __repr__ for hubs and spokes (mkolman)
- Close the .treeinfo file after the retrieve. (vponcova)

* Wed Jan 04 2017 Martin Kolman <mkolman@redhat.com> - 26.17-1
- Fix a GTK Widget related deprecation warning (mkolman)
- Fix GTK screen/display related deprecation warnings (mkolman)
- Fix GObject and GLib deprecation warnings (mkolman)
- Fix selection of no software environment (#1400045) (vponcova)
- Use signals for Spoke & Hub entry/exit callbacks (mkolman)
- Fix the name of StorageDiscoveryConfig attribute (#1395350) (vponcova)
- Iutil PEP8 & formatting fixes (mkolman)
- Add inst.ksstrict option to show kickstart warnings as errors. (vponcova)
- Use the structured installation task classes (mkolman)
- Improved password quality checking (mkolman)
- Add unit tests for password quality checking (mkolman)
- Use Enum for password status constants (mkolman)
- Use a sane unified password checking policy (mkolman)
- Add install task processing classes and unit tests (mkolman)
- Add a signal/slot implementation (mkolman)
- Set correctly the default partitioning. (vponcova)

* Wed Dec 14 2016 Martin Kolman <mkolman@redhat.com> - 26.16-1
- rpmostreepayload: Rework binds to be recursive (walters)
- Let DNF do its own substitutions (riehecky)
- Bump Blivet version due to systemd-udev dependency (mkolman)
- Don't log "Invalid bridge option" when network has no --bridgeopts.
  (rvykydal)
- Fix updating of bridge slave which is bond. (rvykydal)

* Mon Dec 05 2016 Martin Kolman <mkolman@redhat.com> - 26.15-1
- Don't pass storage to firstboot.setup() (mkolman)
- RTD fixes (mkolman)
- Catch ValueError from LVM part in Blivet library (jkonecny)
- Handle unexpected storage exception from blivet (jkonecny)
- Add sudo to test requires (jkonecny)
- network: fix network --noipv4 in %%pre (rvykydal)
- fix typo in systemd service keyword (mail)
- Fix pylint issue in ks_version_test (jkonecny)
- Move Anaconda tests to mock (jkonecny)
- Add checks to git-find-branch script (jkonecny)
- Remove intermediate pot files in po-push (mkolman)
- Allow install classes to set alternate states for firstboot/initial-setup
  (riehecky)

* Wed Nov 23 2016 Martin Kolman <mkolman@redhat.com> - 26.14-1
- Changed the required version of BlockDev to 2.0. (vponcova)
- Remove auto generated documentation (mkolman)
- Fix generated zanata.xml from https unstable branch (jkonecny)
- Don't crash if the UIC file can't be written (#1375702) (mkolman)

* Wed Nov 23 2016 Martin Kolman <mkolman@redhat.com> - 26.13-1
- Fix calling of can_touch_runtime_system function (jkonecny)
- fix formating a bit (gitDeveloper)
- Fix zanata.xml.in in substitution variables (mkolman)

* Thu Nov 17 2016 Martin Kolman <mkolman@redhat.com> - 26.12-1
- Mock chroot environment is chosed by a git branch (jkonecny)
- Set Zanata branch from git-find-branch script (jkonecny)
- Add git-find-branch script for finding parent branch (jkonecny)
- fix pykickstart docks link (gitDeveloper)
- aarch64 now has kexec-tools (pbrobinson)
- Resolve directory ownership (mkolman)
- Fix user interaction config handling in image & directory install modes
  (#1379106) (mkolman)
- tui: Available help system (vponcova)
- network: index team slave connection names starting with 1 (rvykydal)

* Thu Nov 10 2016 Martin Kolman <mkolman@redhat.com> - 26.11-1
- Relax blivet dependency to >= 2.1.6-3 (awilliam)
- Bump required Blivet version (#1378156) (mkolman)
- Fix bad exception handling from blivet in iscsi (#1378156) (jkonecny)
- tui: New class for prompt (vponcova)
- iSCSI: adjust to change in blivet auth info (#1378156) (awilliam)
- Disable false positive pylint error (jkonecny)
- Add some error checking when users don't provide input for DASD devices.
  (sbueno+anaconda)
- Add some error checking when users don't provide input for zFCP devices.
  (sbueno+anaconda)
- Fix tui timezone region selection by name (vponcova)

* Fri Nov 04 2016 Martin Kolman <mkolman@redhat.com> - 26.10-1
- F26_DisplayMode was added by non-interactive mode (jkonecny)
- Fix pyanaconda tests for display mode (jkonecny)
- Fix parse-dracut to support new kickstart displaymode (jkonecny)
- Add boot option inst.noninteractive to the docs (jkonecny)
- Abort installation when Playload exc rise in a NonInteractive mode (jkonecny)
- Support non interactive mode in standalone spokes (jkonecny)
- Non-interactive mode support for Password and User spokes (jkonecny)
- Raise NonInteractive exception in Hubs event loop (jkonecny)
- Raise exception for noninteractive mode in Hub (jkonecny)
- Add new pykickstart noninteractive mode (jkonecny)
- Disable bad kickstart command on F25 (jkonecny)
- Improve DNF error message to be more understandable (jkonecny)
- tui: Add software group selection (vponcova)
- use blivet iSCSI singleton directly in storage spoke (awilliam)
- Correct deviceLinks to device_links (blivet renamed it) (awilliam)
- Instantiate the zFCP object ourselves now. (#1384532) (sbueno+anaconda)
- Fix the way DASD list is determined. (#1384532) (sbueno+anaconda)
- Add tests for payload location picking (#1328151) (jkonecny)
- Fix picking mountpoint for package download (#1328151) (jkonecny)
- Improve packaging logs without DEBUG logging (jkonecny)

* Tue Oct 25 2016 Martin Kolman <mkolman@redhat.com> - 26.9-1
- Move the collect() function to iutil (mkolman)
- Update messiness level (mkolman)
- PEP8 and general refactoring for the main anaconda.py (mkolman)
- Move kickstart file parsing code to startup_utils (mkolman)
- Don't directly import items from anaconda_log (mkolman)
- Remove old useless code (mkolman)
- Move the rescue ui startup code to the rescue module (mkolman)
- Move set-installation-thod-from-anaconda code to startup_utils (mkolman)
- Move the live startup code to startup_utils (mkolman)
- Move code printing the startup note to startup_utils (mkolman)
- Move the pstore cleanup function to startup_utils (mkolman)
- Move the prompt_for_ssh function to startup_utils (mkolman)
- Move logging setup to startup_utils (mkolman)
- Move the geolocation startup code to a separate function (mkolman)
- Unify addons path variable name (mkolman)
- PEP 8 for startup_utils.py (mkolman)
- PEP 8 for display.py (mkolman)
- Move VNC startup checking to a separate function (mkolman)
- Move imports to the top of the file in display.py (mkolman)
- Refactor display mode handling (mkolman)
- Move display setup & startup tasks out of anaconda.py (mkolman)
- Remove main and extra Zanata pot files on master (jkonecny)
- Remove main and extra pot files before zanata push (jkonecny)
- Don't send intermediate pot files to zanata (gh#791) (awilliam)
- Improve message to be clearer in rescue.py (jkonecny)
- Add option to show password in password field (vponcova)
- Generate a list of DASDs in GUI storage spoke. (#1378338) (sbueno+anaconda)
- Echoing 4de0ec44bdf0f68545bb55bb5fea00464b65fcab May as well include the SL
  file (riehecky)
- Fixup class name for CentOS install class (riehecky)
- Fix a typo in SAM file header (mkolman)
- Skip live image on usb when checking storage for mounted partitions
  (#1369786) (rvykydal)

* Mon Oct 03 2016 Martin Kolman <mkolman@redhat.com> - 26.8-1
- Fix network spoke being incorrectly marked as mandatory (#1374864) (mkolman)

* Fri Sep 30 2016 Samantha N. Bueno <sbueno+anaconda@redhat.com> - 26.7-1
- Increse python3-blivet version to 1:2.1.5 (jkonecny)
- Fix dnf.repo.Repo now requires dnf.conf.Conf (jkonecny)
- Provides compatibility with DNF-2.0 (jmracek)

* Tue Sep 27 2016 Martin Kolman <mkolman@redhat.com> - 26.6-1
- Don't deactivate all storage in anaconda-cleanup. (#1225184) (dlehman)
- Stop setting ANACONDA udev environment variable. (#1225184) (dlehman)

* Tue Sep 27 2016 Martin Kolman <mkolman@redhat.com> - 26.5-1
- Improved driver disk copying (#1269915) (mkolman)
- Fix screenshot taking logic (#1327456) (mkolman)
- Change blank lines to pep8 for Dracut DUD test (jkonecny)
- Tweak lambda use in Dracut test (jkonecny)
- Add Dracut test for reloading mod dependencies (jkonecny)

* Wed Sep 21 2016 Martin Kolman <mkolman@redhat.com> - 26.4-1
- Fix NTP server list fetching when running in IS (#1374810) (mkolman)
- rpmostreepayload: Clean up use of sysroot files a bit (walters)
- rpmostreepayload: Fix remote handling to use correct sysroot (walters)

* Mon Sep 19 2016 Martin Kolman <mkolman@redhat.com> - 26.3-1
- network: set onboot correctly for vlan on bond device in ks (#1234849)
  (rvykydal)
- network: don't show ibft configured devices in UI (#1309661) (rvykydal)
- iscsi: don't generate kickstart iscsi commands for offload devices (#1252879)
  (rvykydal)
- iscsi: allow installing bootloader on offload iscsi disks (qla4xxx)
  (#1325134) (rvykydal)
- network: adapt to changed NM ibft plugin enablement configuration (#1371188)
  (rvykydal)
- network: don't activate bond/team devices regardless of --activate (#1358795)
  (rvykydal)
- Fix traceback when payload have None as url (#1371494) (jkonecny)
- Add new Dracut test and fix another ones (#1101653) (jkonecny)
- Fix bug when we add set to list (#1101653) (jkonecny)
- Add new helper script files to build system (#1101653) (jkonecny)
- Document new helper scripts to the DriverDisk README (#1101653) (jkonecny)
- Fix driver unload is disabling network settings (#1101653) (jkonecny)
- dud: fix multiple inst.dd=http:// instances stalling in dracut (#1268792)
  (rvykydal)
- network: fix ksdata generating for for non-active virtual devices (#1321288)
  (rvykydal)
- network: update kickstart data also with bond bridge slaves (#1321288)
  (rvykydal)
- network: add support for bridge bond slaves (#1321288) (rvykydal)
- screen_access: Ensure we write config to real sysroot (walters)
- Add release commit support to makebumpver (mkolman)
- Makefile improvents for separate release commits & tarball creation
  (mkolman)
- network: add support for --no-activate kickstart opton (#1277975) (rvykydal)
- fixup! Add base.close() after base.do_transaction (RhBug:1313240) (jmracek)
- Add base.close() after base.do_transaction (RhBug:1313240) (jmracek)

* Tue Sep 06 2016 Martin Kolman <mkolman@redhat.com> - 26.2-1
- Add git merging examples to the contribution guidelines (mkolman)
- network: don't stumble upon new Device.Statistics NM dbus iface (#1370099)
  (rvykydal)
- Current Anaconda is not compatible with DNF 2.0.0 (jkonecny)
- Filter out all merge commits from the changelog (mkolman)
- Make it possible to override Zanata branch name (mkolman)
- Switch to argparse & autodetect name, version and bug email address (mkolman)
- Fix multi-inheritance (phil)
- Fix replacement of deprecated DNF method (jkonecny)
- Replace deprecated method of DNF (jmracek)
- Static checker recommended improvements (mkolman)
- Fix replacement of deprecated DNF method (jkonecny)
- Replace deprecated method of DNF (jmracek)

* Mon Aug 29 2016 Samantha N. Bueno <sbueno+anaconda@redhat.com> - 26.1-1
- Fix a pylint no-member warning (mkolman)
- Translate press-c-to-continue correctly in TUI (#1364539) (mkolman)
- Fix bootDrive driveorder fallback (#1355795) (jkonecny)
- Fix bootloader when re-using existing /boot part (#1355795) (jkonecny)
- Add support for device specification variants (#1200833) (mkolman)
- Revert "Update zanata.xml for f25-devel branch." (sbueno+anaconda)
- Update zanata.xml for f25-devel branch. (sbueno+anaconda)
- Add option to override efi_dir (phil)
- efiboot: stderr= is not an option to efibootmgr (phil)
- Fix EFI grub1 case (phil)
- Make Fedora module not so grabby (phil)
- Add centos module to pyanaconda (phil)
- network: don't require gateway for static ipv4 config in TUI (#1365532)
  (rvykydal)
- Improve connection network change detection (jkonecny)
- Revert "Revalidate source only if nm-con-ed change settings (#1270354)"
  (jkonecny)
- Fix anaconda-pre.service wasn't properly installed (#1255659) (jkonecny)
- Rename function for better consistency (#1259284) (rvykydal)
- Update error message for consistency (#1259284) (rvykydal)
- Add more specific username check messages also to gui (#1360334) (rvykydal)
- fix style guide test false positive on username variable (#1350375)
  (rvykydal)
- tui: use functions instead of fake REs for checking values (#1350375)
  (rvykydal)
- tui: get proper index of entry we are handling in input (#1331054) (rvykydal)
- tui: fix user name validity checking (#1350375) (rvykydal)
- More descriptive message on invalid username (kvalek)
- Fix another pep8 name issue (jkonecny)
- iscsi: fix getting iscsi target iface of bound target (#1359739) (rvykydal)
- Fix needsNetwork testing only additional repositories (#1358788) (jkonecny)
- Fix restart payload only when repo needs network (#1358788) (jkonecny)
- Cleanup remaining runlevel references (mkolman)
- Clarify a nosave related log message (mkolman)
- Use Screen Access Manager (mkolman)
- Add screen entry/exit callbacks (mkolman)
- Add screen access manager (mkolman)
- A simple formatting fix (mkolman)
- Fix another blivet-2.0 pep8 error (jkonecny)
- Quickfix of failing test (japokorn)
- Some docstring refactoring & typo fixes for the TUI base classes (mkolman)
- Add a file about contributing. (sbueno+anaconda)
- Store logs before anaconda starts (#1255659) (japokorn)
- DD can now replace existing drivers (#1101653) (japokorn)
- Use the F25 timezone kickstart command version (mkolman)
- Use sshd-keygen.target instead of hardcoded sshd-keygen script (jjelen)
- Make it possible to disable sshd service from running. (#1262707)
  (sbueno+anaconda)
- Change bootloader boot drive fallback (jkonecny)
- Fix of Python3x uncompatible commands (japokorn)
- Add NTP server configuration to the TUI (#1269399) (mkolman)
- Move the NTP server checking constants to constants.py (mkolman)
- Use a constant for the NTP check thread name prefix (mkolman)
- Fix another victim of the python 2->3 conversion. (#1354020) (dshea)
- Attempt to unload modules updated by a driver disk (dshea)
- Fix the processing of device nodes as driver disks (dshea)

* Fri Jul 08 2016 Brian C. Lane <bcl@redhat.com> - 25.20-1
- Allow kickstart users to ignore the free space error (dshea)
- Stop kickstart when space check fails (bcl)
- Service anaconda-nm-config is missing type oneshot (jkonecny)
- Fix dhcpclass to work both via kickstart and the boot cmdline. (clumens)
- network: handle also ifcfg files of not activated virtual devices (#1313173)
  (rvykydal)
- network: check onboot value in ksdata, not NM connections (#1313173)
  (rvykydal)
- network: do not activate device on kickstart --onboot="yes" (#1341636)
  (rvykydal)

* Fri Jun 24 2016 Brian C. Lane <bcl@redhat.com> - 25.19-1
- hostname: don't set installer env hostname to localhost.localdomain
  (#1290858) (rvykydal)
- hostname: add tooltip to Apply button (#1290858) (rvykydal)
- hostname: fix accelerator collision (#1290858) (rvykydal)
- hostname: don't set hostname in initrafms of target system (#1290858)
  (rvykydal)
- hostname: set current hostname from target system hostname on demand
  (#1290858) (rvykydal)
- hostname: suggest current hostname for storage containers (#1290858)
  (rvykydal)
- hostname: don't set target system static hostname to current hostname
  (#1290858) (rvykydal)
- network tui: do not activate device when setting its onboot value (#1261864)
  (rvykydal)
- network tui: edit persistent configuration, not active connection (#1261864)
  (rvykydal)
- network: validate netmask in tui (#1331054) (rvykydal)
- Add wordwrap to text mode and use it by default (#1267881) (rvykydal)
- Fix adding new VG in Custom spoke can't be applied (#1263715) (jkonecny)
- Fix SimpleConfigFile file permissions (#1346364) (bcl)
- Re-configure proxy when updateBaseRepo is called (#1332472) (bcl)

* Fri Jun 17 2016 Brian C. Lane <bcl@redhat.com> - 25.18-1
- Only use <> for markup (#1317297) (bcl)
- Update iscsi dialog for Blivet 2.0 API change (bcl)
- Use the signal handlers to set initial widget sensitivies (dshea)
- Fix bad sensitivity on boxes in source spoke (jkonecny)
- Fix install-buildrequires (bcl)
- Added optional [/prefix] as pattern (kvalek)
- Require network for network-based driver disks (dshea)
- Add missing pkgs to install-buildrequires (#612) (phil)
- Increase the required version of gettext (dshea)
- Fix the name sensitivity in the custom spoke. (dshea)

* Fri Jun 10 2016 Brian C. Lane <bcl@redhat.com> - 25.17-1
- Revert "Temporarily disable translations" (bcl)
- Change where to look for the iscsi object (#1344131) (dshea)
- Fix old blivet identifiers (#1343907) (dshea)
- Fix a covscan warning about fetch-driver-net (#1269915) (bcl)
- Fix crash when NM get_setting* methods return None (#1273497) (jkonecny)
- Overwrite network files when using ks liveimg (#1342639) (bcl)
- Stop using undocumented DNF logging API (bcl)
- Use the LUKS device for encrypted swap on RAID (dshea)
- Keep the subdir in driver disk update paths (dshea)
- Warn about broken keyboard layout switching in VNC (#1274228) (jkonecny)
- Make the anaconda-generator exit early outside of the installation
  environment (#1289179) (mkolman)

* Fri Jun 03 2016 Brian C. Lane <bcl@redhat.com> - 25.16-1
- Add a button to refresh the disk list. (dlehman)
- Only try to restart payload in the Anaconda environment (mkolman)
- Make current runtime environment identifiers available via flags (mkolman)
- Display storage errors that cause no disks to be selected (#1340240) (bcl)
- Fix the SourceSwitchHandler pylint errors differently. (clumens)
- Fix pylint errors. (clumens)
- Update the disk summary on Ctrl-A (dshea)
- Revert "Refresh the view of on-disk storage state every 30 seconds."
  (dlehman)
- Refresh the view of on-disk storage state every 30 seconds. (dlehman)
- Handle unsupported disklabels. (dlehman)
- Use a blivet method to remove everything from a device. (dlehman)
- Tighten up ResizeDialog._recursive_remove a bit. (dlehman)
- Only look for partitions on partitioned disks. (dlehman)
- NFS DDs installation now works correctly (#1269915) (japokorn)
- Remove unused on_proxy_ok_clicked from Source spoke (jkonecny)
- send all layouts to localed for keymap conversion (#1333998) (awilliam)
- Small cleanup (mkolman)

* Fri May 27 2016 Brian C. Lane <bcl@redhat.com> - 25.15-1
- Resolve shortcut conflict between "Desired Capacity" and "Done" (yaneti)
- network: don't crash on devices with zero MAC address (#1334632) (rvykydal)
- Remove Authors lines from the tops of all files. (clumens)
- Related: rhbz#1298444 (rvykydal)
- New Anaconda documentation - 25.14 (bcl)
- Catch DNF MarkingError during group installation (#1337731) (bcl)
- Fix TUI ErrorDialog processing (#1337427) (bcl)
- Clean up yelp processes (#1282432) (dshea)

* Fri May 20 2016 Brian C. Lane <bcl@redhat.com> - 25.14-1
- Temporarily disable translations (bcl)
- Don't crash when selecting the same hdd ISO again (#1275771) (mkolman)

* Thu May 19 2016 Brian C. Lane <bcl@redhat.com> - 25.13-1
- Fix writeStorageLate for live installations (#1334019) (bcl)
- Remove the locale list from zanata.xml (dshea)
- Ditch autopoint. (dshea)
- Ditch intltool. (dshea)
- Rename fedora-welcome to fedora-welcome.js (dshea)
- Fix UEFI installation after EFIBase refactor (bcl)
- Fix error handling for s390 bootloader errors (sbueno+anaconda)
- Deselect all addons correctly (#1333505) (bcl)
- gui-testing needs isys to be compiled. (clumens)
- Add more to the selinux check in tests/gui/base.py. (clumens)

* Fri May 13 2016 Brian C. Lane <bcl@redhat.com> - 25.12-1
- Add single language mode (#1235726) (mkolman)
- Move default X keyboard setting out of the Welcome spoke (mkolman)
- Rerun writeBootLoader on Live BTRFS installs (bcl)
- Check for mounted partitions as part of sanity_check (#1330820) (bcl)
- Merge pull request #620 from dashea/new-canary (dshea)
- Update the required pykickstart version. (dshea)
- Implement %%packages --excludeWeakdeps (#1331100) (james)
- Fix bad addon handling when addon import failed (jkonecny)
- Add retry when downloading .treeinfo (#1292613) (jkonecny)
- Return xprogressive delay back (jkonecny)
- Change where tests on translated strings are run. (dshea)
- Merge the latest from translation-canary (dshea)
- Squashed 'translation-canary/' changes from 5a45c19..3bc2ad6 (dshea)
- Add new Makefile target for gui tests (atodorov)
- Define missing srcdir in run_gui_tests.sh and enable coverage (atodorov)
- Split gui test running out into its own script. (clumens)
- Look higher for the combobox associated with an entry (#1333530) (dshea)
- Use createrepo_c in the ci target. (dshea)
- Compile glib schema overrides with --strict. (dshea)

* Fri May 06 2016 Brian C. Lane <bcl@redhat.com> - 25.11-1
- Don't join two absolute paths (#1249598) (mkolman)
- Don't crash when taking a screenshot on the hub (#1327456) (mkolman)
- Fix pylint errors. (phil)
- Factor out common grub1/grub2 stuff into mixin, and other factoring (phil)
- Add GRUB1 (legacy) support back to Anaconda (phil)

* Fri Apr 29 2016 Brian C. Lane <bcl@redhat.com> - 25.10-1
- Handle unmounting ostree when exiting (bcl)
- ostree: Use bind mounts to setup ostree root (bcl)
- ostree: Skip root= setup when using --dirinstall (bcl)
- disable_service: Specify string format args as logging params. (clumens)
- Ignore failure when disable services that do not exist (phil)
- Get rid of an unused variable in the network spoke. (clumens)
- Revalidate source only if nm-con-ed change settings (#1270354) (jkonecny)
- Merge solutions for test source when network change (#1270354) (jkonecny)
- Changes in network state revalidate sources rhbz#1270354 (riehecky)

* Wed Apr 27 2016 Brian C. Lane <bcl@redhat.com> - 25.9-1
- Use the iutil functions for interacting with systemd services. (dshea)
- Add methods to enable and disable systemd services. (dshea)
- Do not add .service to the end of service names. (dshea)
- Remove detach-client from tmux.conf (dshea)
- Use Blivet 2.0 for set_default_fstype (#607) (sgallagh)
- Remove dnf from the list of required packages. (#605) (dshea)
- Add access to the payload from addons (#1288636) (jkonecny)
- Disable pylint warnings related to the log handler fixer. (dshea)
- Allow the metacity config dir to be overriden. (dshea)
- Do not include /usr/share/anaconda files in the gui package. (dshea)
- Work around logging's crummy lock behavior. (dshea)
- Use rm -r to remove the temporary python site directory. (dshea)
- Remove the subnet label for wired devices. (#1327615) (dshea)
- Fix how unusued network labels are hidden (#1327615) (dshea)
- Remove yum_logger (bcl)
- Remove the lock loglevel (bcl)
- Use a temporary user-site directory for the tests. (dshea)
- Build everything for make ci. (dshea)
- Ignore some E1101 no-member errors when running pylint (bcl)
- Sprinkle the code with pylint no-member disable statements (bcl)
- Catch GLib.GError instead of Exception (bcl)
- Update storage test for Blivet 2.0 API change. (bcl)
- Initialize missing private methods in BasePage class (bcl)
- Update kickstart.py for Blivet 2.0 API change. (bcl)
- Use namedtuple correctly in kexec.py (bcl)
- Add more requires to make password checking still work. (#1327411) (dshea)
- Rename isS390 to match the renames in blivet. (dshea)
- Suppress signal handling when setting zone from location (#1322648) (dshea)
- Refresh metadata when updates checkbox changes (#1211907) (bcl)

* Fri Apr 15 2016 Brian C. Lane <bcl@redhat.com> - 25.8-1
- network: handle null wireless AP SSID object (#1262556) (awilliam)
- Change new_tmpfs to new_tmp_fs. (clumens)
- Add support for kickstart %%onerror scripts. (clumens)
- Show network spoke in the TUI reconfig mode (#1302165) (mkolman)
- network: copy static routes configured in installer to system (#1255801)
  (rvykydal)
- network: fix vlan over bond in kickstart (#1234849) (rvykydal)
- network: use NAME to find ifcfg on s390 with net.ifnames=0 (#1249750)
  (rvykydal)
- Get rid of the reimport of MultipathDevice. (clumens)
- Fix iSCSI kickstart options aren't generated (#1252879) (jkonecny)
- Fix adding offload iSCSI devices (vtrefny)
- Make the list-harddrives script mode robust (mkolman)

* Fri Apr 08 2016 Brian C. Lane <bcl@redhat.com> - 25.7-1
- Blivet API change getDeviceBy* is now get_device_by_* (bcl)
- network: don't set 803-3-ethernet.name setting (#1323589) (rvykydal)
- Log non-critical user/group errors (#1308679) (bcl)
- Fix btrfs metadata raid level kwarg. (dlehman)
- docs: Add release building document (bcl)
- Minor improvements - README and test dependencies (atodorov)
- Add more matches for network connectivity (atodorov)

* Mon Apr 04 2016 Brian C. Lane <bcl@redhat.com> - 25.6-1
- Remove an unused import from anaconda-cleanup. (clumens)
- Don't use booleans in Requires (#1323314) (dshea)
- Set CSS names on all of the anaconda classes. (#1322036) (dshea)
- Don't crash if no groups are specified (#1316816) (dshea)
- Fix only one address is shown in anaconda (#1264400) (jkonecny)
- Fix call to update optical media format. (#1322943) (dlehman)
- Reset invalid disk selection before proceeding. (dlehman)
- Multiple Dogtail tests improvements (atodorov)
- Do not allow liveinst with --image or --dirinstall (#1276349) (dshea)
- New Anaconda documentation - 25.5 (bcl)

* Wed Mar 30 2016 Brian C. Lane <bcl@redhat.com> - 25.5-1
- Don't provide subclasses of the multipath or dmraid commands. (clumens)
- Add support for chunksize raid kickstart parameter. (vtrefny)
- Convert to blivet-2.0 API. (dlehman)

* Thu Mar 24 2016 Brian C. Lane <bcl@redhat.com> - 25.4-1
- Require that the English locale data be available. (#1315494) (dshea)
- Revert "Change the default locale to C.UTF-8 (#1312607)" (#1315494) (dshea)
- Make windows in metacity closable (#1319590) (dshea)
- Fix the use of CSS psuedo-classes in the widgets. (dshea)
- Add reason when logging invalid repository (#1240379) (jkonecny)

* Sat Mar 19 2016 Brian C. Lane <bcl@redhat.com> - 25.3-1
- Apply language attributes to all labels within anaconda. (dshea)
- Add a function to apply a PangoAttrLanguage to a label. (dshea)
- Add functions to watch changes to a container widget. (dshea)
- Switch to the adwaita icon theme. (dshea)
- Fix duplicate network settings in dracut (#1293539) (jkonecny)
- Fix create device with bad name when parsing KS (#1293539) (jkonecny)
- Use a lock for repoStore access (#1315414) (bcl)
- Add missing inst prefix to the nokill option in docs (mkolman)
- Merge pull request #551 from wgwoods/master-multiple-initrd-dd-fix (wwoods)
- fix multiple inst.dd=<path> args (rhbz#1268792) (wwoods)

* Fri Mar 11 2016 Brian C. Lane <bcl@redhat.com> - 25.2-1
- Load the system-wide Xresources (#1241724) (dshea)
- Use an icon that exists in Adwaita for the dasd confirmation (dshea)
- Make it possible to skip saving of kickstarts and logs (#1285519) (mkolman)
- Add a function for empty file creation (#1285519) (mkolman)
- Run actions for argparse arguments (#1285519) (mkolman)

* Wed Mar 09 2016 Brian C. Lane <bcl@redhat.com> - 25.1-1
- don't install kernel-PAE on x86_64 (#1313957) (awilliam)
- except block in py3.5 undefines the variable (bcl)
- Remove some history from the liveinst setup. (dshea)
- Do not run the liveinst setup if not in a live environment. (dshea)
- Set GDK_BACKEND=x11 before running anaconda from liveinst. (dshea)
- Run zz-liveinst as an autostart application (dshea)
- Translate the help button. (dshea)
- Translate the required space labes in resize.py (dshea)

* Fri Mar 04 2016 Brian C. Lane <bcl@redhat.com> - 25.0-1
- Add device id to dasdfmt screen. (#1269174) (sbueno+anaconda)
- Unify displayed columns in custom spoke dialogs. (#1289577) (sbueno+anaconda)
- Show some confirmation to users if adding a DASD was successful. (#1259016)
  (sbueno+anaconda)
- Hotfix for missing storage in payload class (#1271657) (jkonecny)
- Check to see if DD repo is already in addOn list (#1268357) (bcl)
- Use the default levelbar offset values. (dshea)
- Do not change the GUI language to a missing locale. (#1312607) (dshea)
- Don't crash when setting an unavailable locale (#1312607) (dshea)
- Change the default locale to C.UTF-8 (#1312607) (dshea)
- Update the libtool version-info. (dshea)
- Use CSS to style the internal widgets. (dshea)
- Move the widgets pixmaps into resources. (dshea)
- Add a resource bundle to libAnacondaWidgets (dshea)
- Rename show_arrow and chosen_changed to show-arrow and chosen-changed (dshea)
- Remove an invalid transfer notation. (dshea)
- Stop using SGML in the docs. (dshea)
- Change the install test URL. (dshea)
- Fix nfs source crash when options change (#1264071) (bcl)
- makebumpver: Add a --dry-run option (bcl)
- NTP should have better behavior (#1309396) (jkonecny)
- Manually set clock shifts on UI idle (#1251044) (rmarshall)
- Don't remove selected shared part when Delete all (#1183880) (jkonecny)
- Don't delete shared/boot parts in deleteAll (#1183880) (jkonecny)

* Fri Feb 19 2016 Brian C. Lane <bcl@redhat.com> - 24.13-1
- tests/gui enhancements (atodorov)
- Fix gui tests for anaconda move to anaconda.py (atodorov)
- Use a different ipmi command to log events. (clumens)
- Clarify that a string in list-screens is actually a regex. (clumens)
- Merge pull request #513 from wgwoods/update-dd-docs (wwoods)
- updated driver updates docs (wwoods)
- Add specification for the user interaction config file (mkolman)
- Update zanata webui URL in translation doc. (dlehman)
- Tweak partition removal in Custom spoke (jkonecny)
- Do not skip evaluation after removing partitions (jkonecny)
- Import iutil earlier so we can use ipmi_report from check_for_ssh. (clumens)
- Make disconnect_client_callbacks more resilient (#1307063). (clumens)
- Move the langpacks install into to a separate function. (dshea)
- Fix _find_by_title method in Accordion (jkonecny)

* Fri Feb 12 2016 Brian C. Lane <bcl@redhat.com> - 24.12-1
- Use host storage for directory or image install dnf download (bcl)
- Log payloadError so we know why installation failed. (bcl)
- Add the addons directory to the rpm. (dshea)
- Use the packaged version of ordered-set (dshea)
- Remove an unused import (dshea)
- Add an uninstall hook for the renamed anaconda (dshea)
- Make langpack work in DNF (#1297823) (jsilhan)
- New Anaconda documentation - 24.11 (bcl)

* Fri Feb 05 2016 Brian C. Lane <bcl@redhat.com> - 24.11-1
- Fix makeupdates for anaconda move to anaconda.py (bcl)
- Rename ./anaconda to ./anaconda.py to work around coverage.py #425 (atodorov)
- Remove special handling for interruptible system calls. (dshea)
- Handle PEP 3101 strings in the gettext context check (dshea)
- Improve RHS summary strings in multiselection (#1265620) (jkonecny)
- Increase GI version required of AnacondaWidgets (jkonecny)
- Increment version of g-introspection for widgets (jkonecny)
- Increment the AnacondaWidgets version (jkonecny)
- Switch to the new Initial Setup unit name (#1299210) (mkolman)
- Uncomment self.check_lang_locale_views in tests/gui/ (atodorov)
- Add dogtail to test requirements (atodorov)
- Add config for easier combining of kickstart and Jenkins coverage data
  (atodorov)
- Apply the fallback style to anaconda selectors. (dshea)
- Redo the stylesheet for Gtk 3.19+ (dshea)
- Directly overwrite /usr/share/anaconda/anaconda-gtk.css (dshea)
- Merge pull request #463 from dashea/translation-tests (dshea)
- Display the name of the addon while executing it (bcl)
- Add page selection summary to the right side (#1265620) (jkonecny)
- Ask when removing new items in multiselection (#1265620) (jkonecny)
- Add multiselection with SHIFT key (#1265620) (jkonecny)
- Use show_arrow feature implemented in Selector (#1265620) (jkonecny)
- Add new property to show/hide arrow in Selector (#1265620) (jkonecny)
- Change selection logic when opening Page (#1265620) (jkonecny)
- Add new BasePage class (#1265620) (jkonecny)
- Add signal and methods to MountpointSelector (#1265620) (jkonecny)
- Fix errors with multiselection (#1265620) (jkonecny)
- Accordion class now process events for selectors (#1265620) (jkonecny)
- Change cammel case for accordion.py to new pep8 (jkonecny)
- Move selection logic from custom spoke to accordion (#1265620) (jkonecny)
- Modify ConfirmDeleteDialog now the checkbox is optional (#1265620) (jkonecny)
- Multiselection works in GUI with remove (#1265620) (jkonecny)
- Add multiselection to Accordion with control key (#1265620) (jkonecny)
- Remove bad translations from the source tarball. (dshea)
- Treat warnings from xgettext as errors. (dshea)
- Run translation-canary tests from make check. (dshea)
- Do not run pylint on translation-canary (dshea)
- Squashed 'translation-canary/' content from commit 5a45c19 (dshea)

* Fri Jan 29 2016 Brian C. Lane <bcl@redhat.com> - 24.10-1
- Add a finished method to spokes (#1300499) (bcl)
- Handle DeviceConfiguration with con = None (#1300499) (bcl)
- Log detailed information about installed packages (bcl)
- s/KickstartValueError/KickstartParseError. (clumens)
- Move requiredDeviceSize to the main Payload class (#1297905) (dshea)

* Fri Jan 08 2016 Brian C. Lane <bcl@redhat.com> - 24.9-1
- Handle unexpected DNF exit (bcl)
- Fix bad space needed messages (jkonecny)
- nosetests-3.5 is now the right version. (clumens)
- Ignore a pylint error about how we're using Popen (dshea)
- Mark an unused variable as unused (dshea)
- Ignore type-related errors for types pylint can't figure out (dshea)
- Import errors are just regular errors now (dshea)
- Replace the remaining log.warn calls with log.warning. (dshea)
- Fix an erroneously bare raise statement (dshea)
- Replace the deprecated assertEquals with assertEqual (dshea)
- Don't add a None to the list of things to unmount on ostree installs.
  (clumens)

* Wed Dec 02 2015 Brian C. Lane <bcl@redhat.com> - 24.8-1
- Fix pylint problems in the gui testing code. (clumens)
- Merge 9c5e02392d0401a3bd0adecedea03535595773ef into
  67b569253c724639c2490f5fab70f7111f699b3f (atodorov)
- Fix the replacement suggestion for "hostname" (dshea)
- Automatically generate sr (dshea)
- Fix PropertyNotFoundError PermHwAddress (#1269298) (jkonecny)
- Make sure python3.5 code can run in early initrd (bcl)
- Replace <list>.delete() with <list>.remove() in user.py (sujithpandel)
- Rename everything that still refers to LiveCD (atodorov)
- Updates to progress and storage tests (atodorov)
- Multiple changes to DogtailTestCase (atodorov)
- Move all Python files into the main gui/ directory (atodorov)
- Simplify tests by removing OutsideMixin and update Creator (atodorov)
- Modify existing tests to match latest anaconda behavior and environment
  (atodorov)
- Temporary disable test code which doesn't work (atodorov)
- Make tests/gui/ execute ./anaconda from git (atodorov)
- Add window title (#1280077) (mkolman)
- Replace execReadlines with check_output in parse-kickstart_test.py (bcl)
- Fix a spelling error in the hardware error message (#1284165). (clumens)

* Wed Nov 18 2015 Brian C. Lane <bcl@redhat.com> - 24.7-1
- Collect test-suite.log from all 'make check' invocations. Closes #452
  (atodorov)
- Fix parse-kickstart_test.py. (clumens)
- Remove mkdud.py. (clumens)
- Remove the kickstart_tests directory. (clumens)
- Always quote values in ifcfg- files (#1279131) (bcl)
- Include original kickstart in /root/original-ks.cfg (#1227939) (bcl)
- strip spaces from extlinux label and default (#1185624) (bcl)
- Report kernel failures during kickstart tests. (clumens)
- Make sure unicode in kickstart works. (dshea)
- Set the window icon (dshea)
- Only run space check in TUI if spokes are complete. (#1279413)
  (sbueno+anaconda)
- Allow a user's primary group to be created in --groups (#1279041) (dshea)
- Remove uses of broad-except. (dshea)
- Add a test for all that container minimization stuff. (clumens)
- Use the partition command in one of the kickstart_tests. (clumens)
- Don't clear the _currentIsoFile if another iso was selected (bcl)
- makeupdates: Include utils/handle-sshpw (bcl)
- Add --sshkey to kickstart sshpw command (#1274104) (bcl)
- Split exception description from exception traceback (jkonecny)
- Show DNF exception instead of silent exit (jkonecny)
- Combine results from all gettext_tests into one log file (atodorov)
- Try to run make ci with real translations. (dshea)
- Untranslate undisplayed TreeView column headers. (dshea)
- Add a test for hidden translatable strings (dshea)
- Add the translated string to markup error messages. (dshea)
- Test glade translations by default (dshea)
- Change the way glade tests are run. (dshea)
- Remove the accelerator test. (dshea)
- Add the test lib directory to $PYTHONPATH in the commit hook (dshea)
- network: create ifcfg files in tui if needed (#1268155) (rvykydal)
- Do not limit ONBOOT default setting to url and nfs installation methods
  (#1269264) (rvykydal)
- ibft: fix setting dracut boot args for static ibft nic configuration
  (#1267526) (rvykydal)
- network: Don't set --device link default for hostname only network cmd
  (#1272274) (rvykydal)
- network: assume --device=link as default also for ks on hd (#1085310)
  (rvykydal)
- network: use ibftx interface for iSCSI from iBFT in dracut (#1077291)
  (rvykydal)
- network: add s390 options to default ifcfg files (#1074570) (rvykydal)

* Fri Nov 06 2015 Brian C. Lane <bcl@redhat.com> - 24.6-1
- Fix a pylint error in the previous commits. (clumens)
- Honor ANACONDA_WIDGETS_OVERRIDES (atodorov)
- Load anaconda-gtk.css from ANACONDA_DATA if specified (atodorov)
- Use the correct path for ui categories (atodorov)
- Typo fix, it's ANACONDA_WIDGETS_DATA not ANACONDA_WIDGETS_DATADIR (atodorov)
- Allow wired network properties more grid space. (dshea)
- Improve language selection at low resolutions. (dshea)
- Make reclaim work with small screens and big labels (dshea)
- allow repo with only a name if it's a pre-defined one (#1277638) (awilliam)
- Only raise thread exceptions once (#1276579) (bcl)
- Use py3.4 crypt and salt (bcl)
- Be more careful with incomplete device types (#1256582) (dshea)
- Fix an import error in rpmostreepayload.py. (clumens)
- Fix Testing docs inclusion in Sphinx (bcl)
- Ignore interfaces with invalid VLAN IDs. (dshea)
- Cleaner logging of .treeinfo return conditions in dependant function.
  (riehecky)
- Update link to upstream kickstart docs (opensource)
- rpmostreepayload: Also unmount internal mounts during shutdown (walters)
- rpmostreepayload: Fix two issues with mounting (walters)
- Add a README for kickstart tests. (clumens)
- Make the documentation match the environment variable. (clumens)
- Check that cache PVs (if any) are in the VG the LV belongs to (#1263258)
  (vpodzime)
- Fix the alignment of the "Label" label in custom (dshea)
- Use unsafe caching during kickstart tests. (clumens)

* Wed Oct 28 2015 Brian C. Lane <bcl@redhat.com> - 24.5-1
- Improve install space required estimation (#1224048) (jkonecny)
- Update the on-disk snapshot of storage when adv. disks are added (#1267944)
  (vpodzime)
- Check that ipv6 kickstart outputs the right ip= (dshea)
- Change a variable name for pylint. (dshea)
- Do not run time_initialize for image and directory installations (#1274103)
  (bcl)
- Remove unused properties (dshea)
- Do not modify the kickstart user data until apply() (dshea)
- Make AdvancedUserDialog.run() more readable (dshea)
- Improve the behavior of the home directory input. (dshea)
- Stop setting inappropriate properties in ksdata. (dshea)
- Update the password strength bar during the password strength check. (dshea)
- Remove unnecessary grab_focus and set_sensitive calls (dshea)
- Use signal handlers in the user spoke more sensibly. (dshea)
- Fix potential issues with the username guesser. (dshea)
- Make kickstart tests growing LVs stricter (vpodzime)
- Point coverage.py to the full path of pyanaconda/ (atodorov)
- Don't set BOOTPROTO= when it isn't set (jbacik)
- Pass strings to blockdev.dasd_format, not a DASDDevice object. (#1273553)
  (sbueno+anaconda)
- Revert "Use yum to install the mock buildroot for now." (dshea)
- decode package name for /etc/sysconfig/kernel (RHBZ #1261569) (awilliam)
- Add tests for the more complicated command line options (dshea)
- Store fewer kinds of things in the dirinstall option. (dshea)
- Fix the parsing of selinux=0 (#1258569) (dshea)
- Include a local $ANACONDA_DATADIR in the test environment. (dshea)
- Move the command line arguments to anaconda_argparse. (dshea)
- Don't crash while logging binary output. (dshea)
- Decode program output even if there is no output (#1273145) (dshea)
- Add a test for _run_program with binary output (dshea)
- Test execWithCapture when the command outputs nothing. (dshea)
- Fix a long line in kickstart_tests/functions.sh. (clumens)
- Merge pull request #414 from vpodzime/master-lvm_log (vpodzime)
- Save the lvm.log Blivet may produce (vpodzime)

* Fri Oct 16 2015 Brian C. Lane <bcl@redhat.com> - 24.4-1
- Hide the places sidebar in the ISO chooser widget. (dshea)
- Use GtkResponseType values in the iso chooser dialog (dshea)
- Do not use deprecated getDevicesByInstance method (vtrefny)
- By default, skip those kickstart tests we know to be failing. (clumens)
- Fix pylint unused import (jkonecny)
- network: handle bridge device appearing before its connection (#1265593)
  (rvykydal)
- Use $KSTEST_URL in tests that still had dl.fp.o hardcoded. (dshea)
- Support CONNECT in the test proxy server. (dshea)
- Extract the file used by liveimg as a prereq (dshea)
- Convert the proxy script to a prereq. (dshea)
- Add a prereqs function to kickstart tests. (dshea)
- Fix traceback when trying to create list of unformatted DASDs. (#1268764)
  (sbueno+anaconda)
- network: handle missing connections of a device configured in GUI better
  (rvykydal)
- network: don't set NM_CONTROLLED=no for root on SAN. (rvykydal)
- Add support for other systemd units to kickstart service command (bcl)
- Merge pull request #388 from wgwoods/dd-in-initrd-fix (wwoods)
- Set the password checkbox for empty kickstart passwords. (dshea)
- Do not set the password input text with unencrypted passwords. (dshea)
- Install input checks before modifying the user GUI (#1256065) (dshea)
- Fix a lying error message in style_guide.py (dshea)
- Use "Enter" instead of "Return" for the keyboard key. (dshea)
- New Anaconda documentation - 24.3 (bcl)
- Include missing test files and scripts in Makefile.am/tarball (atodorov)
- dracut: accept inst.dd=[file:]/dd.iso (#1268792) (wwoods)
- Do not override StorageChecker.errors in StorageSpoke (#1252596) (vtrefny)
- Lookup IPv6 address without brackets (#1267872) (bcl)
- Mangle the boot device differently for systemd (#1241704) (dshea)
- Fail the media check if the systemd service failed to start. (dshea)

* Fri Oct 02 2015 Brian C. Lane <bcl@redhat.com> - 24.3-1
- Properly translate c-to-continue on the root selection screen (mkolman)
- Check minimal memory requirements properly (#1267673) (jstodola)
- Allow users to be created with an existing GID. (dshea)
- Add a test for creating a user with an existing GID. (dshea)
- Add tests for gids embmedded in the user groups list. (dshea)
- Allow the kickstart --groups list to specify GIDs. (dshea)
- Add a --groups argument to the user ks test. (dshea)
- Fix the locale pattern packages-instlangs-3 looks for. (dshea)
- Raise an error if osimg cannot be found (#1248673) (bcl)
- Use the bootloader raid levels for bootloader installation (#1266898) (bcl)
- Use otps.display_mode during early startup (#1267140) (mkolman)
- Mount stage2 cdrom after running driver-updates (#1266478) (bcl)
- Get rid of an unused import in the user spoke. (clumens)
- Log crashes from the signal handler. (dshea)
- Save a core file when anaconda crashes. (dshea)
- Keep environment selection when reentering the software spoke (#1261393)
  (mkolman)
- Only show the user spoke if no users are specified in kickstart (#1253672)
  (mkolman)
- Fix 'cat: /tmp/dd_disk: No such file or directory' (#1251394) (jkonecny)
- Do not display curl 404 errors that can be safely ignored (vtrefny)
- Catch blkid failure in driver-updates (#1262963) (bcl)
- Add kickstart tests for %%packages --instLangs (dshea)
- Do not display markup in showDetailedError. (dshea)
- Skip OEMDRV if interactive DD is requested (#1254270) (bcl)
- Drivers are simply under /run/install/DD-x/ (#1254270) (bcl)
- Fix branding when iso is downloaded from nfs or hd (#1252756) (jkonecny)
- Use yum to install the mock buildroot for now. (dshea)
- Rename the gettext tests (dshea)
- Bring back the KSTEST_HTTP_ADDON_REPO substitution in nfs-repo-and-addon.sh
  (clumens)
- Run substitution checks on the right kickstart file. (clumens)
- Tell gettext that anaconda is not a GNU package. (dshea)
- Ignore environment modification warnings in docs/conf.py (dshea)
- Check for unsubstituted strings before running a test. (dshea)
- Autopart use 90%% of disk capacity for required space compare (#1224048)
  (jkonecny)
- Fix include packages install size when downloading on root (#1224048)
  (jkonecny)
- Enable and improve the check for swap LV size in LVM cache kickstart tests
  (vpodzime)
- make-sphinx-docs: Add modules needed to document tests (bcl)
- Add test documentation (atodorov)
- Fix how the reqpart test checks for /boot, again. (clumens)
- Add a way to get default settings when running the kickstart_tests. (clumens)
- Change how we ignore non-tests in kickstart_tests. (clumens)
- Various fixes to substitution strings in kickstart_tests. (clumens)
- Move kickstart_test .ks files to .ks.in. (clumens)

* Fri Sep 11 2015 Brian C. Lane <bcl@redhat.com> - 24.2-1
- Handle driver rpms retrieved via network (#1257916) (bcl)
- Fix the types passed to chown_dir_tree (#1260318) (dshea)
- Add a test for home directory reuse (dshea)
- Use MDRaidArrayDevice.members instead of .devices (dshea)
- Make sure anaconda reads in ks file from OEMDRV device. (#1057271)
  (sbueno+anaconda)
- Try to deal with expected errors from devicetree.populate (#1257648)
  (vpodzime)
- Revert "Temporarily disable generating a coverage report." (clumens)
- Fix a DBus InvalidProperty handling (jkonecny)
- Fix another bash syntax problem in kickstart-genrules.sh (#1057271)
  (sbueno+anaconda)
- Add a test for the rootpw kickstart command (dshea)
- Add tests for setRootPassword (dshea)
- Add a /boot partition to the reqpart test. (clumens)
- Fix up a statement that's not assigned to anything. (clumens)
- Temporarily disable generating a coverage report. (clumens)
- Don't try to concatenate a list with a string (#1252444) (mkolman)
- Activate coverage for tests executed with sudo (atodorov)
- set sysroot correctly when setting root password (#1260875) (awilliam)
- Add a test for kickstarts that %%include a URL (dshea)
- Add missing python dependencies for requests. (#1259506) (dshea)
- Serve the http addon repos from the test tmpdir (dshea)
- Make make-addon-pkgs easier to use from within a test (dshea)
- Add a simple http server for use in kickstart tests. (dshea)
- Add a script to print an IP address for the host. (dshea)
- Add a cleanup hook that can be defined by kickstart tests (dshea)
- Move kickstart test support files into a separate directory. (dshea)
- Fix a python3 related error in the pre-commit hook (dshea)
- network: gui spoke TODO cleanup (rvykydal)
- libnm in spoke: add missing connection for eth device with Configure
  (rvykydal)
- libnm in spoke: allow adding missing connection for eth device externally
  (rvykydal)
- libnm in spoke: wait for valid state of added device before adding to list
  (rvykydal)
- libnm in spoke: use libmn objects instead of names an uuids (device on/off)
  (rvykydal)
- libnm in spoke: to check if device is activated just use its object
  (rvykydal)
- libnm in spoke: use connnection objects instead of uuids (edit connection)
  (rvykydal)
- libnm in spoke: refresh early when device is added (rvykydal)
- libnm in spoke: use connection object instead of uuid (DeviceConfiguration)
  (rvykydal)
- libnm in spoke: share nm client in standalone and normal spoke (rvykydal)
- libnm in spoke: add enterprise wpa connection using libnm client (rvykydal)
- libnm in spoke: use AccessPoint object in place of ssid bytearray (rvykydal)
- libnm in spoke: delete connection using libnm client (rvykydal)
- libnm in spoke: replace python-dbus workaround calls for ap security flags
  (rvykydal)
- libnm in spoke: call get_data() on ap.get_ssid() result to get ssid bytes
  (rvykydal)
- libnm in spoke: showing ip configuration of a device (rvykydal)
- libnm in spoke: NMClient -> NM.Client (rvykydal)
- libnm in spoke: gi.NetworkManager -> gi.NM (rvykydal)
- libnm in spoke: Revert "Fix crash when new device appear in Welcome screen
  (#1245960)" (rvykydal)
- libnm in spoke: Revert "Fix crash when connections are changing (#1245960)"
  (rvykydal)
- Add an ignoredisk --drives= test. (clumens)
- Add a test for the reqpart command. (clumens)
- Grab anaconda.coverage on tests that reimplement validate(). (clumens)
- Install driver-updates (dshea)
- Fix a typo in service enablement in kickstart.py. (clumens)
- Get rid of the extraneous cats and greps in user.ks. (clumens)
- Add sshkey testing to the user kickstart_test. (clumens)
- Add a kickstart test in Arabic. (clumens)
- Verify Initial Setup services are present before turning them ON/OFF
  (#1252444) (mkolman)
- Don't crash if the Japanese PC-98 keyboard is selected (#1190589) (mkolman)
- Report on all local files and exclude what we don't need instead of
  explicitly including paths we may not be aware of. (atodorov)
- Change "failed to download" messages from critical to warning. (clumens)
- getcode -> status_code in a live payload error message. (clumens)
- Fix a bash error in kickstart-genrules.sh (#1057271) (sbueno+anaconda)
- specify if=virtio,cache=none for VM drives (atodorov)
- update the test b/c latest anaconda doesn't allow weak passwords (atodorov)
- Specify format=raw to avoid warning from qemu (atodorov)
- update for Python3 nose (atodorov)
- Add a services.sh file to match the existing services.ks. (clumens)
- Add types to all existing kickstart tests. (clumens)
- Add the ability to mark kickstart tests with a type. (clumens)
- Run nm-connection-editor with the --keep-above flag (#1231856) (mkolman)

* Mon Aug 31 2015 Brian C. Lane <bcl@redhat.com> - 24.1-1
- Add a test for the user and group creation functions. (dshea)
- Get rid of libuser. (#1255066) (dshea)
- s/$releasever/rawhide/ (clumens)
- LVM on RAID kickstart test (vpodzime)
- unbuffered read in python3 only works for binary (bcl)
- don't crash if no environment set in interactive (#1257036) (awilliam)
- network: compare with ssid bytes, not str (rvykydal)
- Add dependencies for running the tests/gui tests (atodorov)
- Fix first run environment setup in software spoke (#1257036) (jkonecny)
- Stop pretending liveinst+rescue is supported (#1256061). (clumens)
- Defer to Fedora distro-wide settings for password strength (#1250746) (dshea)
- New Anaconda documentation - 24.0 (bcl)
- Do a better job reporting failures from kickstart_tests. (clumens)
- Preserve coverage results from running the kickstart_tests. (clumens)

* Mon Aug 24 2015 Brian C. Lane <bcl@redhat.com> - 24.0-1
- Remove from the docs repo=hd installation with installable tree (jkonecny)
- Fix a race between a window continuing and the next starting (#1004477)
  (dshea)
- Start hubs with the buttons insensitive. (dshea)
- Do not replace the standard streams if not necessary. (dshea)
- Fix inst.repo=hd: is not working (#1252902) (jkonecny)
- Kickstart: Added SELinux test. (kvalek)
- Kickstart tests related to SELinux. (kvalek)
- Package install and debug message logging. (kvalek)
- Don't crash if incorrect environment is set in kickstart (#1234890) (mkolman)
- Fix I/O issues when anaconda is started without a locale. (dshea)
- Move locale environment logic into localization.py (dshea)
- network: fix configuring team in kickstart pre (#1254929) (rvykydal)
- Merge pull request #311 from atodorov/add_local_coverage (clumens)
- Merge pull request #308 from atodorov/rawhide_missing_deps (clumens)
- Enable test coverage in CI (atodorov)
- Fix the single-spoke TUI message for Python 3. (dshea)
- Merge pull request #291 from atodorov/update_coverage_switch (clumens)
- Add missing requirements (atodorov)
- Add basic kickstart tests for LVM Thin Provisioning (vpodzime)
- Use the default mirrorlist instead of fixed repo URL in kickstart tests
  (vpodzime)
- Destroy the keyboard layout dialog when finished (#1254150) (dshea)
- Do not encode the geoloc timezone to bytes (#1240812) (dshea)
- use inst.debug as alternative option to start coverage (atodorov)

* Mon Aug 17 2015 Brian C. Lane <bcl@redhat.com> - 23.20-1
- Skip source url checks when network is off (#1251130) (bcl)
- Don't set net.device to link if there is no ksdevice (#1085310) (bcl)
- Reading carrier while link is down raises IOError (#1085310) (bcl)
- Don't write nfs repos to the target system (#1246212) (bcl)
- Make sure username entered in TUI if create a user chosen. (#1249660)
  (sbueno+anaconda)
- Write the empty dnf langpacks.conf to the right directory (#1253469) (dshea)
- Add pyanaconda test for network.check_ip_address (jkonecny)
- Replace IPy package by ipaddress (jkonecny)
- Correctly check return code when running rpm from makeupdates (mkolman)
- Fix crash when new device appear in Welcome screen (#1245960) (jkonecny)
- Fix crash when connections are changing (#1245960) (jkonecny)
- Make LVM cache kickstart tests more robust (vpodzime)
- product.img buildstamp should override distribution buildstamp (#1240238)
  (bcl)
- On incomplete ks, don't automatically proceed with install. (#1034282)
  (sbueno+anaconda)
- Update the translation doc with zanata branching incantations.
  (sbueno+anaconda)
- Merge pull request #287 from kparal/patch-1 (clumens)
- boot-options.rst: add a note about nfsiso (kamil.paral)
- Few fixes and amendments for the boot_options.rst file (vpodzime)
- Prevent issues with encrypted LVs on renamed VGs (#1224045) (vpodzime)
- Create and use snapshot of on-disk storage with no modifications (#1166598)
  (vpodzime)
- Implement the class for storage snapshots (vpodzime)
- Prevent any changes in the StorageSpoke if just going back (vpodzime)
- Make StorageSpoke's on_back_clicked less complicated (vpodzime)
- Add kickstart tests for the LVM cache kickstart support (vpodzime)
- Disable packages-multilib, for now. (clumens)
- Make sure the liveimg test shuts down when it finishes. (clumens)
- Change how success is checked for the basic-ostree test. (clumens)

* Fri Aug 07 2015 Brian C. Lane <bcl@redhat.com> - 23.19-1
- Add basic support for LVM cache creation in kickstart (vpodzime)
- Use labels for the rest of the non-autopart test results. (dshea)
- Use a disk label to find the filesystem for escrow results (dshea)
- Use someone else's code for PID file management. (dshea)
- Prevent incomplete translations from making the TUI unusable (#1235617)
  (mkolman)
- Apply the environment substitutions more liberally in nfs-repo-and-addon
  (dshea)
- Use stage2=hd: instead of stage2=live: (dshea)
- Add test for liveimg kickstart command (bcl)
- Fix pre-install script execution (bcl)
- test pre-install kickstart section (bcl)
- Use sys.exit() instead of the exit() created by site.py. (dshea)
- Call ipmi_report before sys.exit (dshea)
- Add a test for proxy authentication (dshea)
- Add optional authentication to the proxy server (dshea)
- Add more tests to proxy-kickstart (dshea)
- Show an alternative prompt if a hub contains only a single spoke (#1199234)
  (mkolman)
- Add few docs and improvement in check_ip_address (jkonecny)
- Check whether files actually contain translatable strings. (dshea)
- Add specific error string to TUI user dialog (#1248421) (bcl)
- Make EditTUIDialog error generic (#1248421) (bcl)
- Fix and expand nfs-repo-and-addon.ks (dshea)
- Added a script to make the packages used by nfs-repo-and-addon (dshea)
- Implement the rest of the repo options in dnfpayload. (dshea)
- Fix kickstart test for bond interface creation (jkonecny)

* Fri Jul 31 2015 Brian C. Lane <bcl@redhat.com> - 23.18-1
- Move the proxy server script into a common file. (dshea)
- Use python3 for the proxy server and remove python2 compatibility (dshea)
- makePickle now needs to return bytes (bcl)
- gi.require_version raises ValueError (bcl)
- Remove duplicate signal setup block (bcl)
- Fix three bugs discovered by driverdisk-disk.ks (clumens)
- Fix error with OEMDRV ks auto-load check. (#1057271) (sbueno+anaconda)
- Make sure TUI is readable for non-latin languages (#1182562) (mkolman)
- Equalize capacity & mount point entries (#1212615) (dshea)
- Disable GRUB os_prober on POWER (#1193281) (rmarshall)
- Cancel Container Edit Sensitizes Update (#1168656) (rmarshall)
- Fix SoftwareSpoke._kickstarted. (dshea)
- Disable a Pylint false-positive (#1234896) (mkolman)
- Add support for autostep and --autoscreenshot (#1234896) (mkolman)
- Escape \'s in doc strings (dshea)
- Ellipsize the file system type combo box (#1212615) (dshea)
- Add graphviz to make-sphinx-doc script (jkonecny)
- Remove many of a documentation compilation errors (jkonecny)
- Add class diagrams to existing spokes and hubs (jkonecny)
- Add class diagram settings to documentation (jkonecny)
- Fix the UnusuableConfigurationError dialog (#1246915) (dshea)
- Chase pygobject's stupid moving target (dshea)
- Add missing translation contexts (dshea)
- Actually translate the container type labels (dshea)
- Check whether a translated string requires a context or comment. (dshea)
- Clean up the temporary pools virt-install makes. (clumens)
- Return the same object for repeated calls to __get__ (#1245423) (dshea)
- Use sys.exit instead of os._exit. (clumens)
- Add parentheses around the IPV6 regex fragment. (dshea)
- Add tests for IPv6 literals in URLs (dshea)
- Modify Installation Source Proxy Label (#11688554) (rmarshall)

* Fri Jul 24 2015 Brian C. Lane <bcl@redhat.com> - 23.17-1
- Fix Initial PPC PReP Boot Selector Name (#1172755) (rmarshall)
- Require a newer version of pykickstart (vpodzime)
- Use dictionaries is thread-safe manner. (dshea)
- Merge pull request #234 from wgwoods/master (wwoods)
- Auto-load ks.cfg if OEMDRV volume available. (#1057271) (sbueno+anaconda)
- Check the encrypt checkbox when encrypted specified in KS (vtrefny)
- Do not raise KickstartValueError for missing passphrase (vtrefny)
- Ask for encryption passphrase when not specified in ks (#1213096) (vtrefny)
- dracut: minor cleanup (wwoods)
- dracut: fix missing messages for inst.ks=cdrom (wwoods)
- Wait forever for kickstarts on CDROM (#1168902) (wwoods)
- Use abs_builddir instead of builddir so paths will look more reasonable.
  (clumens)
- Add a new makefile target that does everything needed for jenkins. (clumens)
- Merge pull request #228 from AdamWill/logind (dshea)
- Fix crash when mirrorlist checkbox is checked (jkonecny)
- Fix crash when user start typing proxy credentials (jkonecny)
- Check repository URL before leaving Source Spoke (jkonecny)
- Add IDs to identify addon repositories (jkonecny)
- Repositories can be checked without a selection (jkonecny)
- Consolidate the language environment variables. (dshea)
- Change the generated API indices slightly (dshea)
- Ignore "mountpoint" used a format specifier (dshea)
- filesystems -> file systems, per the style guide (dshea)
- Properly parameterize a translated string (dshea)
- Fix pylint errors in rescue.py. (dshea)
- Remove unused imports (dshea)
- Remove text.py from spec file (#965985) (sbueno+anaconda)
- Merge pull request #220 from AdamWill/1243962 (dshea)
- Fix adding 'boot=' option in FIPS mode (vtrefny)
- anaconda.target: Wants systemd-logind.service (#1222413) (awilliam)
- Remove the last usage of newt and get rid of it as a dependency (#965985)
  (sbueno+anaconda)
- Enable anaconda to use the new rescue mode. (#965985) (sbueno+anaconda)
- Get rid of unnecessary constants in constants_text. (#965985)
  (sbueno+anaconda)
- Get rid of some unnecessary files. (#965985) (sbueno+anaconda)
- Display verbose packaging errors to the user (bcl)
- Show source errors from refresh method (bcl)
- Fix the validate functions in the btrfs kickstart_tests. (clumens)
- Connect kickstart lang data to dnf-langpacks (#1051816) (dshea)
- Add simple_replace config file function (bcl)
- Remove some vestiges of the old packaging module (dshea)
- Remove window boot block detection functions. (dshea)
- Remove iutil.xprogressive_delay. (dshea)
- Simplify iutil.mkdirChain. (dshea)
- Decode wifi SSIDs into strings. (#1240398) (dshea)
- Actually use the temp directory so test files get cleaned up (dshea)
- Disable the output from rpmbuild (dshea)
- Remove stray references to python2. (dshea)
- Fix possible to start installation without network (#1221109) (jkonecny)
- Fix 'q' (to quit) do not work in TUI hub (jkonecny)
- act on the right objects when stripping URL protocols (#1243962) (awilliam)
- Fix 'App' object has no attribute 'queue' (#1243316) (jkonecny)

* Thu Jul 16 2015 Brian C. Lane <bcl@redhat.com> - 23.16-1
- fix storage writing for live and ostree installs (#1236937) (awilliam)
- Add O_CREAT to the open flags when extracting rpm files. (dshea)
- Move ostree gobject version check next to the import (#1243543) (bcl)
- Remove rpmfluff from the buildrequires. (dshea)
- Only import readline if readline is necessary. (dshea)
- use the right baseurl in run_install_test.sh. (clumens)
- Don't copy the environment when starting metacity. (dshea)
- Fix the use of a temporary file in SimpleConfig.write (dshea)
- Add a test for SimpleConfig.write(use_tmp=True). (dshea)
- Remove an unnecessary chmod when creating chrony.conf (dshea)
- Fix some bad uses of chmod. (dshea)
- Add a function to open a file with specific permission bits (dshea)
- Don't ask to start vnc if user specifies text mode. (#1202277)
  (sbueno+anaconda)
- New Anaconda documentation - 23.15 (bcl)
- Add a helper for building Sphinx docs using mock. (bcl)
- Update Sphinx configuration for python3 (bcl)
- Running without a GUI can also raise ValueError in errors.py (bcl)
- parse-kickstart_test.py: fix driverdisk_test() (wwoods)
- Fix the spelling of "version" (dshea)

* Mon Jul 13 2015 Brian C. Lane <bcl@redhat.com> - 23.15-1
- Some dracut modules anaconda needs have been split into their own package.
  (clumens)
- User operation kickstart tests. (kvalek)
- Kickstart tests for UTC and LOCAL hwclock. (kvalek)
- Kickstart firewall tests. (kvalek)
- Fix Repository New_Repository has no mirror or baseurl (#1215963) (jkonecny)

* Fri Jul 10 2015 Brian C. Lane <bcl@redhat.com> - 23.14-1
- Catch blivet formatDevice ValueError in custom (#1240226) (bcl)
- There's now a python3-rpmfluff, so revert this. (clumens)
- Fix a couple other pylint problems in the driver disk tests. (clumens)
- Merge pull request #194 from wgwoods/master (wwoods)
- dracut: fix boot failure waiting for finished/dd.sh (wwoods)
- Use builddir instead of srcdir to find the dd utils (dshea)
- Fix the dd_test for python3. (dshea)
- Fix %%files to deal with compiled python3 modules (dshea)
- Add a bunch of gi.require_version calls (dshea)
- Temporarily disable the error about not importing rpmfluff. (clumens)
- Don't try to iterate over threads directly in wait_all. (clumens)
- Update the btrfs kickstart tests to use functions.sh. (clumens)
- Merge pull request #182 from wgwoods/dd-refactor (wwoods)
- driver_updates: fixes from patch review (wwoods)
- Don't be too picky about what name is --device=link (dshea)
- Ignore stderr output from parse-kickstart. (dshea)
- Add an option to execReadlines to filter out stderr. (dshea)
- Ignore interruptible system calls in the dd test (dshea)
- Fix an undefined variable in writeStorageLate (dshea)
- Connect zfcp entries to the discovery buttons (dshea)
- Connect iscsi activations to buttons (dshea)
- Connect the dasd number entry to the discovery buttons. (dshea)
- Add keyboard layouts on the row-activated signal. (dshea)
- Connect dialog inputs to default actions. (dshea)
- Remove unnecessary GtkNotebooks. (dshea)
- Re-save some dialog glade files. (dshea)
- Merge pull request #181 from wgwoods/master (wwoods)
- dd-refactor: dracut + build bits (wwoods)
- Add kickstart test for RAID1 (bcl)
- pass PYTHONPATH to the kickstart test framework (bcl)
- Write servers to chronyd.conf even if it's off (#1197575) (wwoods)
- Refresh advanced disks after disk summary dialog (#1226354) (bcl)
- parse-kickstart: just emit 'inst.dd=XXX' for driverdisk (wwoods)
- parse-kickstart: pylint fixes (wwoods)
- dd-refactor: new driver_updates.py + tests (wwoods)
- payload: fix driverdisk repos (wwoods)
- dracut: fix boot with inst.ks and no inst.{repo,stage2} (#1238987) (wwoods)
- Use the most recent versions of the btrfs, logvol, part, and raid commands.
  (clumens)
- Allow /boot partition on iscsi with ibft (#1164195) (jkonecny)
- Add kickstart tests to test btrfs installation (vtrefny)
- Fix broken test by infiniband patch (#1177032) (jkonecny)

* Thu Jul 02 2015 Brian C. Lane <bcl@redhat.com> - 23.13-1
- Add a switch for the Airplane Mode label (dshea)
- Connect labels with keyboard accelerators to a widget (dshea)
- Add a test for dangling keyboard accelerators. (dshea)
- Use pocketlint for translation and markup checking (dshea)
- Flatten the glade test directory. (dshea)
- Add support for specifying arbitrary mkfs options. (clumens)
- Fix kickstart install with infiniband (#1177032) (jkonecny)
- anaconda-dracut: Fix sysroot mount for netroot (#1232411) (bcl)
- Add RAID swaps to /etc/fstab (#1234469) (bcl)
- network: catch another race when calling dbus methods on invalid devices
  (rvykydal)
- network: GUI, add connection even when virtual device activation failed
  (#1179276) (rvykydal)
- Fix IP / hostname mismatches when showing VNC server address (#1186726)
  (rvykydal)
- Check also ipv6 default routes when looking for onboot=yes device (#1185280)
  (rvykydal)
- Merge pull request #157 from wgwoods/master_dd_fixes (wwoods)
- Do not check dependencies on invalid payloads (dshea)
- network: don't set onboot=False for default autoconnections (#1212009)
  (rvykydal)
- Fix the types used to write anaconda-tb-all.log (dshea)
- dd: drop unnecessary archive_read_data_skip (wwoods)
- dd_extract: -l should not extract modules+firmware (wwoods)
- dd: fix permissions on extracted files (#1222056) (wwoods)
- tests: add dd_tests (wwoods)

* Fri Jun 26 2015 Brian C. Lane <bcl@redhat.com> - 23.12-1
- Revert "Add an optional conditional to progress_report." (bcl)
- Fix inconsistencies in the payload messages. (dshea)
- Fix install-requires and install-buildrequires (dshea)
- anaconda-dracut: Mount /dev/mapper/live-rw (#1232411) (bcl)
- Eliminate some false test results when running glade tests. (atodorov)
- Move the knowledge about network packages into ksdata.network. (clumens)
- Add an optional conditional to progress_report. (clumens)
- Move the big block of late storage writing out of install.py. (clumens)
- The attribute is named ostreesetup.nogpg. (clumens)
- Use the index in grubenv (#1209678) (bcl)
- Do not raise an exception on EINTR from os.close or os.dup2 (dshea)
- Merge pull request #154 from mulkieran/master-959701 (mulkieran)
- Improve focus behavior in the advanced user dialog (dshea)
- Re-save advanced_user.glade (dshea)
- Depsolve kickstarted packages on the summary hub (#961280) (dshea)
- Add a kickstart test for %%packages --ignoremissing (dshea)
- Remove descriptions for RAID levels (#959701) (amulhern)
- No kexec-tools on aarch64 (bcl)

* Fri Jun 19 2015 Brian C. Lane <bcl@redhat.com> - 23.11-1
- Do not import iutil from flags (dshea)
- Ignore EINTR errors in files unlikely to encounter them (dshea)
- Reimplement the open override for the dracut scripts (dshea)
- Wrap the only non-open call found by the new pocketlint checks (dshea)
- Redefine open to retry on EINTR (dshea)
- Remove __future__ imports (dshea)
- Use python 3's OSError subclasses instead of checking errno (dshea)
- Allow kwargs in eintr_retry_call (dshea)
- Remove explicit uses of /dev/null (dshea)
- Do not retry calls to close or dup2 (dshea)
- Remove another function from isys (dshea)
- Make dialogs behave better with timed input validation (dshea)
- Fix the password/confirm checks to work with delayed validation (dshea)
- Move the URL protocol removal out of the input check (dshea)
- Remove the vestigal capslock label from the password spoke (dshea)
- Re-saved a few glade files (dshea)
- Run set_status unconditionally from update_check_status (dshea)
- Do not run input checks for every keystroke of input (#1206307) (dshea)
- Add a method to execute timed actions early (dshea)
- Use comps.environments instead of comps.environments_iter (#1221736) (dshea)
- Merge pull request #83 from mulkieran/master-requires (mulkieran)
- Only show supported autopart choices in choices combo. (amulhern)
- Strip out device types that blivet is not able to support. (amulhern)
- Update blivet required version. (amulhern)
- Fix nfs4 stage2 and repo handling (#1230329) (bcl)
- Update upd-kernel so that it actually works (#1166535) (bcl)
- Fix passing ,nfsvers=3 to dracut (#1161820) (bcl)
- Require the python3 version of iscsi-initiator-utils (dshea)
- Fix the pylint pre-commit hook for python3 and pocketlint (dshea)
- Fix a type check to work with python 3. (dshea)
- Do not log Xorg output to tty5 (dshea)

* Wed Jun 10 2015 Brian C. Lane <bcl@redhat.com> - 23.10-1
- Deal with encrypted partitions not being readable by virt-cat. (clumens)
- Make use of the restore_signals Popen argument (dshea)
- Don't allow /boot on iSCSI. (#1164195) (sbueno+anaconda)
- Merge pull request #127 from mulkieran/master-kickstart (mulkieran)
- Actually distribute the clickable message test, too (dshea)
- Fix disk argument passing to virt-cat in the ostree test. (clumens)
- Relabel all password and group files in %%post (#1228489) (dshea)
- Deal with the order of ifcfg files not being guaranteed. (clumens)
- Add a __init__.py to fix up an error when running iutil_test.py. (clumens)
- Actually run the clickable message test (dshea)
- Add a false positive to pylint checking for S390Error. (clumens)
- Let the excludedocs test pass if there are only directories left. (clumens)
- Allow successful kstest results to provide more details. (clumens)
- The escrow_cert test cannot use autopart. (clumens)
- Don't warn on PyInit__isys being unused. (clumens)
- Test that root LV is encrypted. (amulhern)
- Deal with subprocess returning bytes in tests/lib/filelist.py, too. (clumens)
- Make anaconda+python3+pocketlint work. (clumens)
- Start using our new shared pylint framework in anaconda. (clumens)
- Remove our extra pylint checkers. (clumens)
- Remove a duplicate libselinux-python3 requires. (clumens)
- Run makeupdates with Python 2 for now (mkolman)
- Don't use the _safechars private property (#1014220) (mkolman)
- Make sure directory size is returned as int (#1014220) (mkolman)
- Only warn about missing yum-utils (#1014220) (mkolman)
- Make sure set_system_time() gets an integer (#1014220) (mkolman)
- Make sure the column number in TUI is an integer (#1141242) (mkolman)
- Python 3 compatible sorting fixes (#1014220) (mkolman)
- Make version comparison Python 3 compatible (#1014220) (mkolman)
- Don't apply numeric comparison on None (#1141242) (mkolman)
- Avoid comparing None to an integer (#1141242) (mkolman)
- Handle urllib split (#1014220) (mkolman)
- Don't try to decode strings (#1014220) (mkolman)
- Rename function attributes (#1014220) (mkolman)
- Replace raw_input() with input() (#1014220) (mkolman)
- Make iterators and their usage Python 3 compatible (#1014220) (mkolman)
- Convert Python 2 metaclass magic to Python 3 metaclass magic (#1014220)
  (mkolman)
- Make the raise syntax Python 3 compatible (#1014220) (mkolman)
- Python 3 no longer does tuple parameter unpacking (#1014220) (mkolman)
- Make isys Python 3 compatible (#1014220) (mkolman)
- Set a correct mode for the tempfile (#1014220) (mkolman)
- Python 3 temp files no longer reflect external changes (#1014220) (mkolman)
- Make print usage Python 3 compatible (#1014220) (mkolman)
- Rename the warnings spoke to warnings_spoke (#1014220) (mkolman)
- Replace list comprehension with for at class level (mkolman)
- Make gettext usage Python 3 compatible (#1014220) (mkolman)
- Do not open tty5 for writing in the "a" mode (#1014220) (vpodzime)
- Do not use pykickstart's RepoData as a key in a dict (#1014220) (vpodzime)
- Do not run repo attrs' checks if they are not set up yet (#1014220)
  (vpodzime)
- Don't depend on side effects of map() (#1141242) (mkolman)
- Don't use exceptions' message attribute (#1014220) (vpodzime)
- Addapt to string type changes (#1014220) (mkolman)
- Handle modules returning bytes in Python 3 (#1014220) (mkolman)
- Add and use function that makes sure we work with strings (#1014220)
  (vpodzime)
- Handle modules requiring different string types in Python 3 (#1014220)
  (mkolman)
- Remove sitecustomize (#1014220) (mkolman)
- Make ASCII conversions Python compatible (#1014220) (mkolman)
- Remove "is Unicode" tests (#1014220) (mkolman)
- Fix ASCII conversion tests (#1014220) (mkolman)
- Return a string when calling a program (#1014220) (mkolman)
- Handle subprocess returning bytes (#1014220) (mkolman)
- Handle latin-1 strings in locale -a output (#1014220) (mkolman)
- Open the VNC password file for binary writing (#1014220) (mkolman)
- Update parse-kickstart for python3 (#1014220) (bcl)
- Update driver-updates for python3 (#1014220) (bcl)
- Update python-deps for python3 (#1014220) (bcl)
- Add a test for parse-kickstart (#1014220) (bcl)
- Make the import Python 3 compatible (#1014220) (mkolman)
- Change configparser and queue imports (#1014220) (mkolman)
- Remove imports from the __future__ (#1014220) (mkolman)
- Use the imp module directly (#1014220) (mkolman)
- Use Python 3 versions of Python dependencies  (#1014220) (mkolman)
- Use /usr/bin/python3 in scripts (#1014220) (mkolman)
- Use Python 3 versions of nose and Pylint (#1014220) (mkolman)
- Build the Anaconda widgets for Python 3 (#1014220) (mkolman)
- Update makebumpver for python3 (#1014220) (bcl)
- Fix Kickstart installation without default gateway errors out (jkonecny)
- Fix results checking in a couple ks tests. (clumens)

* Wed Jun 03 2015 Brian C. Lane <bcl@redhat.com> - 23.9-1
- Fix a usage typo in run_once_ks script. (sbueno+anaconda)
- Add kickstart tests for keyboard settings. (sbueno+anaconda)
- Add a kickstart test for lang settings. (sbueno+anaconda)
- Fix a %% call inside _(). (clumens)
- Convert ntp-pools.* to using the new kstest functions and autopart. (clumens)
- Fix up the expected output in parse-kickstart_test.py. (clumens)
- Fix a couple more pylint problems in the s390 code. (clumens)
- Use the adapted Timezone class for kickstart data (vpodzime)
- Add a kickstart test for processing NTP servers/pools configuration
  (vpodzime)
- Show error on invalid username attempts in TUI. (#1171778) (sbueno+anaconda)
- Fix dracut reads ksdevice from missing os enviromnent (jkonecny)
- Run kickstart tests through an LMC-like program, not LMC itself. (clumens)
- Move common kickstart_test code out into its own functions.sh file. (clumens)
- Switch to using autopart in the kickstart tests. (clumens)
- Fix a couple pylint errors. (sbueno+anaconda)
- Make anaconda changes necessary for libblockdev s390 plugin.
  (sbueno+anaconda)
- Add a kickstart test for lvm with percentage-based sizes. (dlehman)
- Add kickstart test for basic fixed-size lvm layout. (dlehman)
- Add a kickstart test to validate the default fstype. (dlehman)
- Add kickstart test to test bond interface creation (jkonecny)
- Add kickstart test to test vlan creation (jkonecny)
- Fix --device=link and --device not specified (#1085310) (rvykydal)
- Add kickstart test to test hostname (jkonecny)
- Add a /boot to tmpfs-fixed_size.ks. (clumens)
- Fix bad warning message when user set illegal IP (jkonecny)
- Fix bad check of illegal ip address (jkonecny)
- Add a simple tmpfs kickstart test (mkolman)
- Add a kickstart test for escrow packets and backup passphrases (dshea)
- Fix a typo that caused us to discard corrected target sizes. (#1211746)
  (dlehman)
- Don't pass anything to ./configure. (dshea)
- Fix a pylint problem in parse-kickstart_test.py. (clumens)
- Fix 0 choice in Language and Storage in TUI mode (jkonecny)
- Update html documentation for new boot-options section (bcl)
- Convert boot-options to ReST and include it in the Sphinx documents. (bcl)

* Fri May 15 2015 Brian C. Lane <bcl@redhat.com> - 23.8-1
- Clean up after processKickstart in parse-kickstart_test.py. (clumens)
- Add support to dnfpayload.py for addon NFS repos. (clumens)
- Fix IndexError: list index out of range (#1219004) (jkonecny)
- Fix a typo in proxy-kickstart.sh that was causing a test time out. (clumens)
- iSCSI Name Validation using regexes (sujith_pandel)
- Add kickstart tests for proxy usage. (dshea)
- In dracut, do not display a warning for network lines with just a hostname.
  (clumens)
- Add transport adapters to support ftp and file fetching (dshea)
- Fix for "Kickstart installation fails..." (#1197960) (jkonecny)
- Allow passing kickstart tests to be run on the command line. (clumens)
- Automatically collect environment variables to be passed to ks tests.
  (clumens)
- Use isinstance instead of type for doing type checks. (clumens)
- Remove yumpayload.py, its support files, and most references to yum.
  (clumens)
- Fix the packages-and-group wildcard exclusion test (dshea)
- Set the GUI-selected environment in the ksdata (#1192100) (dshea)
- Don't crash if the disk model is None (#1215251) (dshea)
- Correct an error message in packages-and-groups-1.ks. (clumens)
- Switch from testing for emacs* to kacst*. (clumens)
- Tests that end in a traceback are failures, not successes. (clumens)
- Don't run run_report.sh from within run_kickstart_tests.sh. (clumens)
- If a kickstart test failed due to a traceback, display that. (clumens)
- Wrap device labels earlier (#1212586) (dshea)
- Remove the angle property from the device label (dshea)
- Get rid of the find button in the filter spoke. (dshea)
- Rearrange filter.glade (dshea)
- Fix errors in the vendor column renderers. (dshea)
- Fix some minor inconsistencies in filter.glade (dshea)
- Fix issues with advanced storage searching. (dshea)
- Remove duplicate entries from search combo boxes (dshea)
- Use named IDs for the filter type combo boxes. (dshea)
- Rearrange filter.glade the way glade wants it now (dshea)
- Add a reporting support script to kickstart tests. (clumens)
- Return a specific error code when a test times out. (clumens)
- Fix indentation in run_one_ks.sh. (clumens)
- Also remove all the fonts in the packages-and-groups-1 test. (clumens)
- Enable the basic-ftp and basic-ftp-yum kickstart tests. (clumens)
- Fix a typo in groups-and-envs-2.ks (clumens)
- Get NTP pools and servers from ksdata for the runtime config (vpodzime)
- Adapt to the new argument list for save_servers_to_config. (clumens)
- Remove the restriction that /boot be below 2TB for grub (#1082331) (dshea)
- Distinguish between NTP pools and servers in GUI (vpodzime)
- Add support for chrony pool directive (mlichvar)
- Add a readme pointing to the documentation (bcl)
- Sphinx docs - use source order (bcl)
- Add html documentation for Anaconda v23.7 (bcl)
- Place html docs under ./docs/html/ (bcl)
- Configure proxy settings for dnf payload (#1211122) (bcl)
- Change online action to change (bcl)
- Check for images/install.img first for netboot (bcl)
- Ignore addon and anaconda sections in handle-sshpw (bcl)
- Ignore %%anaconda section in parse-kickstart (bcl)
- Change of label in iscsi storage spoke (jkonecny)

* Wed Apr 22 2015 Brian C. Lane <bcl@redhat.com> - 23.7-1
- Fix doReqPartition import from autopart (bcl)
- Add support for reboot --kexec kickstart command (bcl)
- Add inst.kexec and --kexec support to reboot with kexec (bcl)
- Add setup_kexec method to prepare the system for a reboot with kexec (bcl)
- Add kickstart %%pre-install section support (bcl)
- Remove the custom help button from the toolbar (bcl)
- Use multiple streams for zRAM instead of multiple devices (vpodzime)
- iscsi: pass rd.* options of devices to be mouted in dracut (#1192398)
  (rvykydal)
- Remove the unused productName import from custom_storage_helpers.py.
  (clumens)
- Remove the old custom partitioning help dialog (mkolman)
- Implement the new reqpart command. (clumens)
- Sort disks by name when checking disk selection (vpodzime)
- Set both .format's and .originalFormat's passphrase on unlock (vpodzime)
- Make the Encrypt checkbox insensitive for encrypted non-BTRFS devices
  (#1210254) (vpodzime)
- Check for Gtk before importing escape_markup (bcl)
- If the network is disabled, also disable the network part of the source
  spoke. (#1192104) (clumens)
- Add handling for unusable storage configurations. (dlehman)
- Allow markup in the label/message of DetailedErrorDialog. (dlehman)
- Allow passing an optional button list to showDetailedError. (dlehman)
- Allow kwargs with gtk_action_wait, gtk_action_nowait decorators. (dlehman)
- Fix makeupdates handling of Release: (bcl)
- Make sure we unmount the path we mounted (bcl)
- Fix up one more back_clicked reference that got missed. (clumens)
- Don't unconditionally set ksdata.lang.seen to True (#1209927) (mkolman)
- Reset the back_clicked flag if we stay on the Storage spoke (#1210003)
  (vpodzime)
- Mark the back_clicked attribute of the Storage spoke as private (vpodzime)
- TUI pwpolicy setup was supposed to be in __init__ not refresh (#1208607)
  (bcl)
- Preserve the order of boot args added by kickstart. (clumens)
- Revert "allow /boot on btrfs subvol or filesystem" (bcl)
- Connect scroll adjustments in the right class (#1206472) (dshea)

* Thu Apr 02 2015 Brian C. Lane <bcl@redhat.com> - 23.6-1
- Enforce sane disk selections. (dlehman)
- Add a test for parse-kickstart (bcl)
- Add --tmpdir to parse-kickstart for testing (bcl)
- Use the correct format for IPMI messages. (clumens)
- Do not use min_luks_entropy with pre-existing devices (#1206101) (dshea)
- Remove the dnf cache directory when resetting the repo (dshea)
- Do not add separators to the addon list when not needed (dshea)
- Only use the instclass environment if it actually exists. (dshea)

* Fri Mar 27 2015 Brian C. Lane <bcl@redhat.com> - 23.5-1
- Mock external module dependencies for readthedocs (bcl)
- Generate the pyanaconda module documentation (bcl)
- Reformat kickstart.rst using better ReST markup (bcl)
- Add some deprecation-related false positives. (clumens)
- Add Sphinx documentation support (bcl)
- Add documentation on %%anaconda kickstart command (bcl)
- Prevent Storage spoke Done button method from multiple launch (jkonecny)
- Prevent spokes from being exited more times. (jkonecny)
- Only depend on pygobject3-base in anaconda-core (#1204469) (mkolman)
- Use proxy when configured for the base repo (#1196953) (sjenning)
- Assume UTC if setting the system time without a timezone (#1200444) (dshea)
- Add boolean as return to ThreadManager.wait (jkonecny)
- Make sure LANG is always set to something (#1201896) (dshea)
- Fix pylint/translation issues from the pwpolicy patches. (clumens)

* Fri Mar 20 2015 Brian C. Lane <bcl@redhat.com> - 23.4-1
- Clean out the mock chroot before attempting to run the rest of the test.
  (clumens)
- Implement %%anaconda kickstart section for pwpolicy (bcl)
- Add pwpolicy support to TUI interface (bcl)
- Add pwpolicy for the LUKS passphrase dialog. (bcl)
- Add pwpolicy for the user spoke. (bcl)
- Use pwpolicy for the root password spoke. (bcl)
- Add the text for weak passwords to constants (bcl)
- Add tests with an FTP instrepo (dshea)
- Add kickstart tests for an NFS instrepo and addon repos. (dshea)
- Handle /boot on btrfs for live (#1200539) (bcl)
- rpmostreepayload: write storage config after shared var is mounted (#1203234)
  (rvykydal)
- Tweak tmux configuration file (jkonecny)
- Remove --device= from the new kickstart tests. (clumens)
- Add more kickstart-based packaging tests. (clumens)
- Fix enlightbox call in ZFCPDialog. (#1151144) (sbueno+anaconda)
- fix crash with bare 'inst.virtiolog' in boot args (wwoods)
- Do not attempt to set None as a warning (dshea)
- fix inst.ks.sendmac for static ip=XXX (#826657) (wwoods)

* Fri Mar 13 2015 Brian C. Lane <bcl@redhat.com> - 23.3-1
- Only insert strings into the environment (#1201411) (dshea)
- Fix the rescue kernel version list in writeBootLoader (#1201429) (dshea)
- Missing local variable check (omerusta)
- Fix the handling of nfs:// URLs. (dshea)
- Add glob support for the -a/--add option in makeupdates (mkolman)
- White Space fixes (omerusta)
- Put all mock results into the top-level source dir. (clumens)
- Merge pull request #31 from dcantrell/master (david.l.cantrell)
- Require newt-python in anaconda-core (dshea)
- Make merge-pr executable (dshea)
- Display an error for exceptions during GUI setup (dshea)
- Remove unused invisible char properties (dshea)
- Add a check for invisible_char validity (dshea)
- Connect viewport adjustments to child focus adjustments (#1192155) (dshea)
- Support '%%packages --multilib' in dnfpayload.py (#1192628) (dcantrell)

* Fri Mar 06 2015 Brian C. Lane <bcl@redhat.com> - 23.2-1
- Add rc-release target (bcl)
- Change --skip-tx to --skip-zanata in scratch-bumpver (bcl)
- Add --newrelease to makebumpver (bcl)
- Improve the addon repo name collision code (#1125322) (bcl)
- Fix the import of mountExistingSystem (vpodzime)
- Fix import error in anaconda-cleanup. (sbueno+anaconda)
- Use the new static method to get possible PE sizes (vpodzime)
- Try using the global LUKS passphrase if none is given for LV/part (#1196112)
  (vpodzime)
- Fix the help button mnemonic display on spokes (dshea)
- Only set the hub message if the message has changed (dshea)
- Wrap the info bar in a GtkRevealer (dshea)
- Add links to clickable warning and error messages. (dshea)
- Add a test to look for clickable messages that aren't clickable enough.
  (dshea)
- Increment the widgets version number (dshea)
- Allow markup and links in the info bar. (dshea)
- Add more links to gtk-doc comments (dshea)
- Handle New_Repository name collision source spoke (#1125322) (bcl)
- Fix a bad usage of execWithRedirect (#1197290) (dshea)
- Have to be root to delete /var/tmp/kstest-* on the remote machines. (clumens)
- Use the LUKS device for swap in fstab (#1196200) (vpodzime)
- Clear TUI source spoke errors that may have been leftover from a prior
  attempt. (#1192259) (sbueno+anaconda)

* Fri Feb 27 2015 Brian C. Lane <bcl@redhat.com> - 23.1-1
- Make sure python2 dnf is required (bcl)
- Fix pykickstart requirement. (clumens)
- Extract xattrs from tar payload (#1195462) (bcl)
- Add a script to rebase and merge pull requests (dshea)
- Update translation documentation for Zanata (bcl)
- Switch translation support to fedora.zanata.org (bcl)
- install.py: fix the 'is team device' check (awilliam)
- Explain why Anaconda requires rpm-devel and libarchive-devel during build
  (mkolman)
- Revert "Switch to temporary transifex branch" (bcl)
- Revert "makebumpver needs to know about anaconda-1 transifex name" (bcl)
- Commit 23.0 anaconda.pot file (bcl)
- Rename queue.py to queuefactory.py. (clumens)
- Remove references to old_tests, which no longer exists. (clumens)
- Fix package and group removing with the dnf payload. (clumens)
- Don't try to run new-kernel-pkg if it doesn't exist. (clumens)

* Fri Feb 20 2015 Brian C. Lane <bcl@redhat.com> - 23.0-1
- Remove unused imports (dshea)
- Check for unused imports in __init__ files (dshea)
- Remove timestamp-based version support. (dshea)
- Add test lib methods to check regexes (dshea)
- Cleanup BuildRequires (mkolman)
- Remove obsolete imports. (amulhern)
- Make print statement print output w/out surrounding parentheses. (amulhern)
- Remove an unused import (dshea)
- rpmostreepayload: Honor noverifyssl (walters)
- typo: packaging: Don't vary name of "verified" (walters)
- Disable the metacity mouse-button-modifier setting (dshea)
- Fix completion setting in TUI language spoke. (#1192230) (sbueno+anaconda)
- Remove the pylint false positives for the GLib module (dshea)
- Use ExtendAction for --ignore flag (amulhern)
- Use a simple ExtendAction for add_rpms option. (amulhern)
- Fix log message formating (mkolman)
- Don't clear nonexistent DNF package download location (#1193121) (mkolman)
