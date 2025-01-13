%global libsolv_version 0.7.20-3
%global libmodulemd_version 2.11.2-2
%global librepo_version 1.13.1
%global dnf_conflict 4.3.0
%global swig_version 3.0.12
%global libdnf_major_version 0
%global libdnf_minor_version 63
%global libdnf_micro_version 0

%define __cmake_in_source_build 1

# set sphinx package name according to distro
%global requires_python2_sphinx python2-sphinx
%global requires_python3_sphinx python3-sphinx
%if 0%{?rhel} == 7
    %global requires_python2_sphinx python-sphinx
%endif
%if 0%{?suse_version}
    %global requires_python2_sphinx python2-Sphinx
    %global requires_python3_sphinx python3-Sphinx
%endif

%bcond_with valgrind

# Do not build bindings for python3 for RHEL <= 7
%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

%if 0%{?rhel} > 7 || 0%{?fedora} > 29
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

%if 0%{?rhel} && ! 0%{?centos}
%bcond_without rhsm
%else
%bcond_with rhsm
%endif

%bcond_without selinux

%if 0%{?rhel}
%bcond_with zchunk
%else
%bcond_without zchunk
%endif

%bcond_with sanitizers

%global _cmake_opts \\\
    -DENABLE_RHSM_SUPPORT=%{?with_rhsm:ON}%{!?with_rhsm:OFF} \\\
    %{nil}

Name:           libdnf
Version:        %{libdnf_major_version}.%{libdnf_minor_version}.%{libdnf_micro_version}
Release:        20%{?dist}
Summary:        Library providing simplified C and Python API to libsolv
License:        LGPLv2+
URL:            https://github.com/rpm-software-management/libdnf
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Patch1:         0001-Revert-Improve-performance-for-module-query.patch
Patch2:         0002-Revert-Enhance-description-of-modular-solvables.patch
Patch3:         0003-Revert-Fix-typo-lates-latest.patch
Patch4:         0004-Revert-Remove-unused-code-bump-version.patch
Patch5:         0005-Revert-Report-a-new-type-of-the-module-resolve-error.patch
Patch6:         0006-Revert-Add-additional-fallback-for-module-resolve.patch
Patch7:         0007-Revert-Decide-how-to-handle-context-according-to-sta.patch
Patch8:         0008-Revert-Fix-load-update-FailSafe.patch
Patch9:         0009-Revert-Change-mechanism-of-module-conflicts.patch
Patch10:        0010-Revert-Call-addVersion2Modules-as-late-as-possible.patch
Patch11:        0011-Revert-Fix-modular-queries-with-the-new-solver.patch
Patch12:        0012-Revert-Add-compatible-layer-for-MdDocuments-v2.patch
Patch13:        0013-Revert-Add-an-alternative-constructor-for-ModulePack.patch
Patch14:        0014-Revert-Adjust-modular-solver-to-new-context-type.patch
Patch15:        0015-Revert-Change-usage-of-context-and-version-in-modula.patch
Patch16:        0016-Fix-failing-unittest-caused-by-the-revert-of-new-mod.patch
Patch17:        0017-Modify-unit-test-after-change-of-handling-advisories.patch
Patch18:        0018-Adjust-module-error-formatting-function-for-original.patch
Patch19:        0019-Remove-redundant-test.patch
Patch20:        0020-Fix-dnf_context_module_install-memory-leaks.patch
Patch21:        0021-covscan-remove-unused-vars-mark-private-func-static-return-values.patch
Patch22:        0022-hawkey-surrogateescape-error-handler-to-decode-UTF-8-strings-RhBug1893176.patch
Patch23:        0023-Turn-off-strict-validation-of-modulemd-documents-RhBug200485320071662007167.patch
Patch24:        0024-Add-unittest-for-setting-up-repo-with-empty-keyfile-RhBug1994614.patch
Patch25:        0025-Add-getLatestModules.patch
Patch26:        0026-context-Substitute-all-repository-config-options-RhB.patch
Patch27:        0027-Use-environment-variable-in-unittest-instead-of-ugly.patch
Patch28:        0028-Add-private-API-for-filling-reading-and-verifying-ne.patch
Patch29:        0029-Use-dnf-solv-userdata-to-check-versions-and-checksum.patch
Patch30:        0030-Update-unittest-to-test-the-new-private-dnf-solvfile.patch
Patch31:        0031-Increase-required-libsolv-version-for-cache-versioni.patch
Patch32:        0032-Add-more-specific-error-handling-for-loading-repomd-.patch
Patch33:        0033-libdnf-transaction-RPMItem-Fix-handling-transaction-.patch
Patch34:        0034-libdnf-transaction-TransactionItem-Set-short-action-.patch
Patch35:        0035-Do-not-print-errors-on-failovermethod-repo-option-Rh.patch
Patch36:        0036-sack-query.hpp-Add-a-missing-include.patch
Patch37:        0037-context-dnf_context_remove-accepts-package-spec-as-d.patch
Patch38:        0038-context-Fix-doc-dnf_context_install-remove-update-di.patch
Patch39:        0039-advisory-upgrade-filter-out-advPkgs-with-different-a.patch
Patch40:        0040-Add-obsoletes-to-filtering-for-advisory-candidates.patch
Patch41:        0041-Fix-listing-a-repository-without-cpeid-RhBug-2066334.patch
Patch42:        0042-Allow-change-of-arch-during-security-updates-with-no.patch
Patch43:        0043-Update-translations.patch
Patch44:        0044-Add_repoid_to_solver_error_messagase.patch
Patch45:        0045-conf-Support-proxy-_none_-in-main-config-RhBug-21557.patch
Patch46:        0046-Update-translations-RHEL-8.9.patch
Patch47:        0047-filterAdvisory-installed_solvables-sort-RhBug2212838.patch
Patch48:        0048-Avoid-reinstal-installonly-packages-marked-for-ERASE.patch
Patch49:        0049-PGP-Set-a-default-creation-SELinux-labels-on-GnuPG-d.patch
Patch50:        0050-repo-Don-t-try-to-perform-labeling-if-SELinux-is-dis.patch


BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libsolv-devel >= %{libsolv_version}
BuildRequires:  pkgconfig(librepo) >= %{librepo_version}
BuildRequires:  pkgconfig(check)
%if %{with valgrind}
BuildRequires:  valgrind
%endif
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.46.0
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  rpm-devel >= 4.11.0
%if %{with rhsm}
BuildRequires:  pkgconfig(librhsm) >= 0.0.3
%endif
%if %{with zchunk}
BuildRequires:  pkgconfig(zck) >= 0.9.11
%endif
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(cppunit)
BuildRequires:  pkgconfig(libcrypto)
%if %{with selinux}
BuildRequires:  pkgconfig(libselinux)
%endif
BuildRequires:  pkgconfig(modulemd-2.0) >= %{libmodulemd_version}
BuildRequires:  pkgconfig(smartcols)
BuildRequires:  gettext
BuildRequires:  gpgme-devel

%if %{with sanitizers}
BuildRequires:  libasan
BuildRequires:  liblsan
BuildRequires:  libubsan
%endif

Requires:       libmodulemd%{?_isa} >= %{libmodulemd_version}
Requires:       libsolv%{?_isa} >= %{libsolv_version}
Requires:       librepo%{?_isa} >= %{librepo_version}

%if %{without python2}
# Obsoleted from here so we can track the fast growing version easily.
# We intentionally only obsolete and not provide, this is a broken upgrade
# prevention, not providing the removed functionality.
Obsoletes:      python2-%{name} < %{version}-%{release}
Obsoletes:      python2-hawkey < %{version}-%{release}
Obsoletes:      python2-hawkey-debuginfo < %{version}-%{release}
Obsoletes:      python2-libdnf-debuginfo < %{version}-%{release}
%endif

%description
A Library providing simplified C and Python API to libsolv.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libsolv-devel%{?_isa} >= %{libsolv_version}

%description devel
Development files for %{name}.

%if %{with python2}
%package -n python2-%{name}
%{?python_provide:%python_provide python2-%{name}}
Summary:        Python 2 bindings for the libdnf library.
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  python2-devel
%if !0%{?mageia}
BuildRequires:  %{requires_python2_sphinx}
%endif
%if 0%{?rhel} == 7
BuildRequires:  swig3 >= %{swig_version}
%else
BuildRequires:  swig >= %{swig_version}
%endif

%description -n python2-%{name}
Python 2 bindings for the libdnf library.
%endif
# endif with python2

%if %{with python3}
%package -n python3-%{name}
%{?python_provide:%python_provide python3-%{name}}
Summary:        Python 3 bindings for the libdnf library.
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  python3-devel
BuildRequires:  %{requires_python3_sphinx}
BuildRequires:  swig >= %{swig_version}

%description -n python3-%{name}
Python 3 bindings for the libdnf library.
%endif

%if %{with python2}
%package -n python2-hawkey
Summary:        Python 2 bindings for the hawkey library
%{?python_provide:%python_provide python2-hawkey}
BuildRequires:  python2-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python2-%{name} = %{version}-%{release}
# Fix problem with hawkey - dnf version incompatibility
# Can be deleted for distros where only python2-dnf >= 2.0.0
Conflicts:      python2-dnf < %{dnf_conflict}
Conflicts:      python-dnf < %{dnf_conflict}

%description -n python2-hawkey
Python 2 bindings for the hawkey library.
%endif
# endif with python2

%if %{with python3}
%package -n python3-hawkey
Summary:        Python 3 bindings for the hawkey library
%{?python_provide:%python_provide python3-hawkey}
BuildRequires:  python3-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3-%{name} = %{version}-%{release}
# Fix problem with hawkey - dnf version incompatibility
# Can be deleted for distros where only python3-dnf >= 2.0.0
Conflicts:      python3-dnf < %{dnf_conflict}
# Obsoletes F27 packages
Obsoletes:      platform-python-hawkey < %{version}-%{release}

%description -n python3-hawkey
Python 3 bindings for the hawkey library.
%endif

%prep
%autosetup -S git -p1
%if %{with python2}
mkdir build-py2
%endif
%if %{with python3}
mkdir build-py3
%endif

%build
%if %{with python2}
pushd build-py2
  %if 0%{?mageia} || 0%{?suse_version}
    cd ..
    %define _cmake_builddir build-py2
    %define __builddir build-py2
  %endif
  %cmake -DPYTHON_DESIRED:FILEPATH=%{__python2} -DWITH_MAN=OFF ../ %{!?with_zchunk:-DWITH_ZCHUNK=OFF} %{!?with_valgrind:-DDISABLE_VALGRIND=1} %{_cmake_opts} -DLIBDNF_MAJOR_VERSION=%{libdnf_major_version} -DLIBDNF_MINOR_VERSION=%{libdnf_minor_version} -DLIBDNF_MICRO_VERSION=%{libdnf_micro_version} \
    -DWITH_SANITIZERS=%{?with_sanitizers:ON}%{!?with_sanitizers:OFF} \
    -DENABLE_SELINUX=%{?with_selinux:ON}%{!?with_selinux:OFF}
  %make_build
popd
%endif
# endif with python2

%if %{with python3}
pushd build-py3
  %if 0%{?mageia} || 0%{?suse_version}
    cd ..
    %define _cmake_builddir build-py3
    %define __builddir build-py3
  %endif
  %cmake -DPYTHON_DESIRED:FILEPATH=%{__python3} -DWITH_GIR=0 -DWITH_MAN=0 -Dgtkdoc=0 ../ %{!?with_zchunk:-DWITH_ZCHUNK=OFF} %{!?with_valgrind:-DDISABLE_VALGRIND=1} %{_cmake_opts} -DLIBDNF_MAJOR_VERSION=%{libdnf_major_version} -DLIBDNF_MINOR_VERSION=%{libdnf_minor_version} -DLIBDNF_MICRO_VERSION=%{libdnf_micro_version} \
    -DWITH_SANITIZERS=%{?with_sanitizers:ON}%{!?with_sanitizers:OFF} \
    -DENABLE_SELINUX=%{?with_selinux:ON}%{!?with_selinux:OFF}
  %make_build
popd
%endif

%check
%if %{with python2}
pushd build-py2
  make ARGS="-V" test
popd
%endif
%if %{with python3}
# If we didn't run the general tests yet, do it now.
%if %{without python2}
pushd build-py3
  make ARGS="-V" test
popd
%else
# Otherwise, run just the Python tests, not all of
# them, since we have coverage of the core from the
# first build
pushd build-py3/python/hawkey/tests
  make ARGS="-V" test
popd
%endif
%endif

%install
%if %{with python2}
pushd build-py2
  %make_install
popd
%endif
%if %{with python3}
pushd build-py3
  %make_install
popd
%endif

%find_lang %{name}

%if (0%{?rhel} && 0%{?rhel} <= 7) || 0%{?suse_version}
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%else
%ldconfig_scriptlets
%endif

%files -f %{name}.lang
%license COPYING
%doc README.md AUTHORS
%{_libdir}/%{name}.so.*
%dir %{_libdir}/libdnf/
%dir %{_libdir}/libdnf/plugins/
%{_libdir}/libdnf/plugins/README
%if %{with sanitizers}
%{_sysconfdir}/profile.d/dnf-sanitizers.sh
%endif

%files devel
%doc %{_datadir}/gtk-doc/html/%{name}/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%if %{with python2}
%files -n python2-%{name}
%{python2_sitearch}/%{name}/
%endif

%if %{with python3}
%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%endif

%if %{with python2}
%files -n python2-hawkey
%{python2_sitearch}/hawkey/
%endif

%if %{with python3}
%files -n python3-hawkey
%{python3_sitearch}/hawkey/
%endif

%changelog
* Mon Jun 24 2024 Petr Pisar <ppisar@redhat.com> - 0.63.0-20
- Do not set a default SELinux creation context if SELinux appears to be
  disabled (RHEL-43231)

* Wed Oct 18 2023 Petr Pisar <ppisar@redhat.com> - 0.63.0-19
- Set default SELinux labels on GnuPG directories (RHEL-6421)

* Fri Oct 13 2023 Jaroslav Rohel <jrohel@redhat.com> - 0.63.0-18
- filterAdvisory: match installed_solvables sort with lower_bound (RhBug:2212838, RHEL-1244)
- Avoid reinstalling installonly packages marked for ERASE (RhBug:2163474, RHEL-1253)

* Fri Sep 08 2023 Marek Blaha <mblaha@redhat.com> - 0.63.0-17
- Update translations

* Wed May 31 2023 Nicola Sella <nsella@redhat.com> - 0.63-0-16
- Support "proxy=_none_" in main config (RhBug:2155713)

* Wed May 17 2023 Jaroslav Rohel <jrohel@redhat.com> - 0.63.0-15
- Add repoid to solver error messages (RhBug:2179409,2179413)

* Wed Mar 08 2023 Marek Blaha <mblaha@redhat.com> - 0.63.0-14
- Update translations

* Wed Oct 26 2022 Nicola Sella <nsella@redhat.com> - 0.63.0-13
- Allow change of arch during security updates with noarch (RhBug:2124483)

* Tue Sep 13 2022 Lukas Hrazky <lhrazky@redhat.com> - 0.63.0-12
- Fix listing a repository without cpeid (RhBug:2066334)

* Thu Jul 21 2022 Lukas Hrazky <lhrazky@redhat.com> - 0.63.0-11
- Add obsoletes to filtering for advisory candidates

* Tue Jun 14 2022 Lukas Hrazky <lhrazky@redhat.com> - 0.63.0-10
- Do not print errors on failovermethod repo option
- the dnf_context_remove() function accepts `<package-spec>`, doc updates
- advisory upgrade: filter out advPkgs with different arch

* Wed May 04 2022 Lukas Hrazky <lhrazky@redhat.com> - 0.63.0-8
- Substitute all repository config options (fixes substitution of baseurl)
- Use solvfile userdata to store and check checksums and solv versions
- Fix handling transaction id in resolveTransactionItemReason
- Set short action for Reason Change

* Fri Jan 14 2022 Pavla Kratochvilova <pkratoch@redhat.com> - 0.63.0-7
- Rebuild with new release number

* Tue Jan 11 2022 Pavla Kratochvilova <pkratoch@redhat.com> - 0.63.0-6
- Add getLatestModules()

* Mon Nov 29 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 0.63.0-5
- Add unittest for setting up repo with empty keyfile (RhBug:1994614)

* Tue Nov 09 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 0.63.0-4
- Bump release number because of conflicting version of 8.5 build

* Tue Nov 09 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 0.63.0-3
-  Turn off strict validation of modulemd documents (RhBug:2004853,2007166,2007167)

* Tue Jul 27 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 0.63.0-2
- Fix: dnf_context_module_install: memory leaks
- covscan: remove unused vars, mark private func static, return values
- DNF does not fail on non UTF-8 file names in a package

* Wed May 19 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 0.63.0-1
- Update to 0.62.0
- Hardening: add signature check with rpmcliVerifySignatures (RhBug:1932079)
- Support allow_vendor_change setting in dnf context API
- Add a new option module_obsoletes
- Add new API applyObsoletes() function to apply modular obsoletes
- Do not allow 1 as installonly_limit value (RhBug:1926261)
- Add a config option to check TLS certificate revocation status (using OCSP stapling), defaults to false (RhBug:1814383)
- Swdb: Add a method to get the current transaction
- [context,API] Functions for accessing main/global configuration options
- [context,API] Function for adding setopt
- Add getter for modular obsoletes from ModuleMetadata
- Add ModulePackage.getStaticContext() and getRequires()
- Fix modular queries with the new solver
- Fix: Fully set ssl in newHandle function
- [conf] Add options for working with certificates used with proxy
- Modify module NSVCA parsing - context definition (RhBug:1926771)
- [context] Fix: dnf_package_is_installonly (RhBug:1928056)
- Add getApplicablePackages to advisory and isApplicable to advisorymodule
- Keep isAdvisoryApplicable to preserve API
- [context] Support config file option "proxy_auth_method", defaults "any"
- Support main config file options "installonlypkgs" and "protected_packages". Changes behaviour of microdnf and PackageKit.
- Properly handle multiple collections in updateinfo.xml (RhBug:1804234)
- Fix a crash when [media] section in .treeinfo is missing for bootable media (RhBug:1946024)
- Add new dnf_context_module_install() C API

* Fri Feb 12 2021 Nicola Sella <nsella@redhat.com> - 0.55.0-6
- Fix removal step during modular enable in context part

* Thu Feb 11 2021 Nicola Sella <nsella@redhat.com> - 0.55.0-5
- Add new option module_stream_switch

* Mon Feb 08 2021 Nicola Sella <nsella@redhat.com> - 0.55.0-4
- [context] improve retrieving repository configuration
- Allow loading incomplete cache and loading ext solv files without its repodata

* Fri Jan 29 2021 Nicola Sella <nsella@redhat.com> - 0.55.0-3
- Avoid multilib file conflict in config.h (RhBug:1918818)
- [modules] Add special handling for src artifacts (RhBug:1809314)

* Fri Jan 15 2021 Nicola Sella <nsella@redhat.com> - 0.55.0-2
- Better msgs if "basecachedir" or "proxy_password" isn't set (RhBug:1888946)

* Mon Nov 09 2020 Nicola Sella <nsella@redhat.com> - 0.55.0-1
- Add vendor to dnf API (RhBug:1876561)
- Add formatting function for solver error
- Add error types in ModulePackageContainer
- Implement module enable for context part
- Improve string formatting for translation
- Remove redundant printf and change logging info to notice (RhBug:1827424)
- Add allow_vendor_change option (RhBug:1788371) (RhBug:1788371)

* Thu Aug 20 2020 Nicola Sella <nsella@redhat.com> - 0.48.0-5
- [covscan] Handle exception in a python binding by the proper function (RhBug:1870492)

* Tue Jul 28 2020 Marek Blaha <mblaha@redhat.com> - 0.48.0-4
- Update translations (RhBug:1820548)

* Fri Jul 17 2020 Nicola Sella <nsella@redhat.com> - 0.48.0-3
- Add log file level main config option (RhBug:1802074)
- Accept '==' as an operator in reldeps (RhBug:1847946)

* Wed Jun 10 2020 Ales Matej <amatej@redhat.com> - 0.48.0-2
- [history] Fix dnf history rollback when a package was removed (RhBug:1683134)

* Wed Jun 03 2020 Nicola Sella <nsella@redhat.com> - 0.48.0-1
- Update to 0.48.0
- swdb: Catch only SQLite3 exceptions and simplify the messages
- MergedTransaction list multiple comments (RhBug:1773679)
- Modify CMake to pull *.po files from weblate
- Optimize DependencyContainer creation from an existing queue
- fix a memory leak in dnf_package_get_requires()
- Fix memory leaks on g_build_filename()
- Fix memory leak in dnf_context_setup()
- Add `hy_goal_favor` and `hy_goal_disfavor`
- Define a cleanup function for `DnfPackageSet`
- dnf-repo: fix dnf_repo_get_public_keys double-free
- Do not cache RPMDB
- Use single-quotes around string literals used in SQL statements
- SQLite3: Do not close the database if it wasn't opened (RhBug:1761976)
- Don't create a new history DB connection for in-memory DB
- transaction/Swdb: Use a single logger variable in constructor
- utils: Add a safe version of pathExists()
- swdb: Handle the case when pathExists() fails on e.g. permission
- Repo: prepend "file://" if a local path is used as baseurl
- Move urlEncode() to utils
- utils: Add 'exclude' argument to urlEncode()
- Encode package URL for downloading through librepo (RhBug:1817130)
- Replace std::runtime_error with libdnf::RepoError
- Fixes and error handling improvements of the File class
- [context] Use ConfigRepo for gpgkey and baseurl (RhBug:1807864)
- [context] support "priority" option in .repo config file (RhBug:1797265)

* Fri Apr 03 2020 Ales Matej <amatej@redhat.com> - 0.47.0-1
- Update to 0.47.0
- Allow excluding packages with "excludepkgs" and globs
- Make parsing of reldeps more strict (RhBug:1788107)
- Add expanding solvable provides for dependency matching (RhBug:1534123)
- DnfRepo: fix module_hotfixes keyfile priority level
- Add custom exceptions to libdnf interface
- Port to libmodulemd-2 API (RhBug:1693683)
- Add prereq_ignoreinst & regular_requires properties for pkg (RhBug:1543449)
- Reset active modules when no module enabled or default (RhBug:1767351)
- Add comment option to transaction (RhBug:1773679)
- Baseurl is not exclusive with mirrorlist/metalink (RhBug:1775184)
- Add new function to reset all modules in C API (dnf_context_reset_all_modules)
- Handle situation when an unprivileged user cannot create history database (RhBug:1634385)
- Add query filter: latest by priority
- Add setter for running kernel protection setting
- Add DNF_NO_PROTECTED flag to allow empty list of protected packages
- Config options: only first empty value clears existing (RhBug:1788154)
- [conf] Set useful default colors when color is enabled
- [context] Use installonly_limit from global config (RhBug:1256108)
- [context] Add API to get/set "install_weak_deps"
- [context] Adds support for includepkgs in repository configuration.
- [context] Adds support for excludepkgs, exclude, includepkgs, and disable_excludes in main configuration.
- [context] Added function dnf_transaction_set_dont_solve_goal
- [context] Added functions dnf_context_get/set_config_file_path
- [context] Respect "plugins" global conf value
- [context] Add API to disable/enable plugins
- [context] Create new repo instead of reusing old one (RhBug:1795004)
- [context] Error when main config file can't be opened (RhBug:1794864)
- [context] Add function function dnf_context_is_set_config_file_path
- [context] Support repositories defined in main configuration file

* Tue Feb 18 2020 Ales Matej <amatej@redhat.com> - 0.39.1-5
- Fix filtering of packages by advisory (RhBug:1770125)

* Fri Jan 31 2020 Marek Blaha <mblaha@redhat.com> - 0.39.1-4
- [translations] Update translations from zanata (RhBug:1754965)

* Mon Jan 13 2020 Ales Matej <amatej@redhat.com> - 0.39.1-3
- Add two new query filters: obsoletes_by_priority, upgrades_by_priority (RhBug:1769466)
- [context] Add wildcard support in dnf_context_repo_set_data (RhBug:1781420)
- Remove killGpgAgent function (RhBug:1781601)

* Thu Dec 12 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.39.1-2
- [user-agent] Stop checking os-release(5) data against a hard-coded whitelist (RhBug:1777255)

* Mon Nov 25 2019 Ales Matej <amatej@redhat.com> - 0.39.1-1
- Update to 0.39.1
- Report reason how package was excluded (RhBug:1649754)
- Additional Arm detection improvements (RhBug:1691430)
- Set skip_if_unavailable for media repos to skip their update (RhBug:1716067)
- Add support of xml:base for remote and local url in context (RhBug:1734350,1717865)

* Wed Nov 13 2019 Ales Matej <amatej@redhat.com> - 0.38.1-1
- Update to 0.38.1
- Change the best option default to false
- Use more descriptive message when failed to retrieve GPG key (RhBug:1605117)
- Add removeMetadataTypeFromDownload function to the API
- Context part of libdnf can now read vars (urlvars) from dirs and environment
- Throw exception immediately if file cannot be opened
- Add test when there is no primary metadata in compatible format (RhBug:1744960)
- Various improvements to countme features
- Don't abort on rpmdb checksum calculation failure
- Enable module dependency trees when using set_modules_enabled_by_pkgset() (RhBug:1762314)
- Resolve problem with --best and search in provides (RhBug:1737469)
- New method "Query::filterSubject()", replaces Solution::getBestSolution()
- The Solution class was removed
- Add query argument into get_best_query and get_best_solution
- Add module reset function into dnf_context
- Add method to get all repository metadata locations
- Catch NoModuleException in case of not existent value was used in persistor (RhBug:1761773)

* Tue Oct 22 2019 Ales Matej <amatej@redhat.com> - 0.35.5-1
- Update to 0.35.5
- Make libdnf own its plugin directory (RhBug:1714265)
- Set priority of dnf.conf.d drop-ins
- Fix toString() to not insert [] (RhBug:1584442)
- Fix handling large number of filenames on input (RhBug:1690915)
- Detect armv7 with crypto extension only on arm version >= 8
- A new standardized User-Agent field consisting of the libdnf and OS version
  (including the variant) (RhBug:1156007)
- Add basic countme support (RhBug:1647454)
- Fix crash in PackageKit (RhBug:1636803)
- Do not create @System.solv files (RhBug:1707995)
- Set LRO_CACHEDIR so zchunk works again (RhBug:1739867)
- Improve detection of extras packages by comparing (name, arch) pair instead
  of full NEVRA (RhBuh:1684517)
- Improve handling multilib packages in the history command (RhBug:1728637)
- Repo download: use full error description into the exception text (RhBug:1741442)
- Properly close hawkey.log (RhBug:1594016)
- Fix dnf updateinfo --update to not list advisories for packages updatable
  only from non-enabled modules
- Apply modular filtering by package name (RhBug:1702729)

* Wed Oct 16 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.35.1-9
- Prevent reinstalling modified packages with same NEVRA (RhBug:1728252,1644241,1760825)

* Fri Sep 06 2019 Marek Blaha <mblaha@redhat.com> - 0.35.1-8
- Enhanced fix of moving directories in minimal container (RhBug:1700341)

* Thu Sep 05 2019 Jaroslav Mracek <jmracek@redhat.com> - 0.35.1-7
- Remove patch to not fail when installing modular RPMs without modular metadata

* Thu Sep 05 2019 Marek Blaha <mblaha@redhat.com> - 0.35.1-6
- Fix moving directories in minimal container (RhBug:1700341)

* Tue Aug 06 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.35.1-5
- Add suport for query sequence conversions

* Thu Aug 01 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.35.1-4
- Fix typo in error message (RhBug:1726661)
- Update localizations from zanata (RhBug:1689991)
- Don't disable nonexistent but required repositories (RhBug:1689331)
- Ignore trailing blank lines of multiline value (RhBug:1722493)
- Re-size includes map before re-computation (RhBug:1725213)

* Tue Jul 16 2019 Marek Blaha <mblaha@redhat.com> - 0.35.1-3
- Fix attaching and detaching of libsolvRepo and repo_internalize_trigger()
  (RhBug:1730224)

* Thu Jul 04 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.35.1-2
- Add patch to not fail when installing modular RPMs without modular metadata

* Tue Jun 11 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.35.1-1
- Update to 0.35.1
- Skip invalid key files in "/etc/pki/rpm-gpg" with warning (RhBug:1644040)
- Enable timestamp preserving for downloaded data (RhBug:1688537)
- Fix 'database is locked' error (RhBug:1631533)
- Replace the 'Failed to synchronize cache' message (RhBug:1712055)
- Fix 'no such table: main.trans_cmdline' error (RhBug:1596540)
- Fix: skip_if_unavailable=true for local repositories (RhBug:1716313)
- Add support of modular FailSafe (RhBug:1623128)
- Add support of DNF main config file in context; used by PackageKit and
  microdnf (RhBug:1689331)
- Exit gpg-agent after repokey import (RhBug:1650266)

* Mon May 13 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.33.0-1
- Update to 0.33.0
- Enhance sorting for module list (RhBug:1590358)
- [DnfRepo] Add methods for alternative repository metadata type and download (RhBug:1656314)
- Remove installed profile on module enable or disable (RhBug:1653623)
- Enhance modular solver to handle enabled and default module streams differently (RhBug:1648839)
- Add support of wild cards for modules (RhBug:1644588)
- Exclude module pkgs that have conflict
- Enhance config parser to preserve order of data, and keep comments and format
- Improve ARM detection
- Add support for SHA-384
- Return empty query if incorrect reldep (RhBug:1687135)
- ConfigParser: Improve compatibility with Python ConfigParser and dnf-plugin-spacewalk (RhBug:1692044)
- ConfigParser: Unify default set of string represenation of boolean values
- Fix segfault when interrupting dnf process (RhBug:1610456)
- Installroot now requires absolute path
- Support "_none_" value for repo option "proxy" (RhBug:1680272)
- Add support for Module advisories
- Add support for xml:base attribute from primary.xml (RhBug:1691315)
- Improve detection of Platform ID (RhBug:1688462)

* Fri Apr 26 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.22.5-6
- Rebuild for libsolv soname bump (in libsolve update to 0.7.4)

* Wed Apr 03 2019 Jaroslav Mracek <jmracek@redhat.com> - 0.22.5-5
- Backport patches to set default to skip_if_unavailable to false (RhBug:1692452)

* Tue Feb 12 2019 Jaroslav Mracek <jmracek@redhat.com> - 0.22.5-4
- Backport patch to exclude module pkgs that have conflict (RhBug:1670496)

* Fri Feb 08 2019 Jaroslav Mracek <jmracek@redhat.com> - 0.22.5-3
- Backport patches to add support for modular updateinfoxml applicability

* Wed Feb 06 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.22.5-2
- Add patch: Add best as default behavior (RhBug1670776)

* Mon Dec 17 2018 Daniel Mach <dmach@redhat.com> - 0.22.4-1
- Enhance LIBDNF plugins support
- [repo] Check whether metadata cache is expired (RhBug:1539620,1648274)
- [sack] Implement dnf_sack_get_rpmdb_version()

* Fri Nov 23 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.22.3-1
- Permanently disable Python2 build for Fedora 30+
- Update to 0.22.3
- Modify solver_describe_decision to report cleaned (RhBug:1486749)
- [swdb] create persistent WAL files (RhBug:1640235)
- Relocate ModuleContainer save hook (RhBug:1632518)
- [transaction] Fix transaction item lookup for obsoleted packages (RhBug: 1642796)
- Fix memory leaks and memory allocations
- [repo] Possibility to extend downloaded repository metadata

* Wed Oct 24 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.22.0-2
- Add patch Modify-solver_describe_decision-to-report-cleaned-RhBug1486749
- Add patch swdb-create-persistent-WAL-files-RhBug1640235
- Add patch Relocate-ModuleContainer-save-hook-RhBug1632518
- Add patch Test-if-sack-is-present-and-run-save-module-persistor-RhBug1632518

* Mon Oct 15 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.22.0-1
- Fix segfault in repo_internalize_trigger (RhBug:1375895)
- Change sorting of installonly packages (RhBug:1627685)
- [swdb] Fixed pattern searching in history db (RhBug:1635542)
- Check correctly gpg for repomd when refresh is used (RhBug:1636743)
- [conf] Provide additional VectorString methods for compatibility with Python list.
- [plugins] add plugin loading and hooks into libdnf

* Tue Sep 25 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.20.0-1
- [module] Report module solver errors
- [module] Enhance module commands and errors
- [transaction] Fixed several problems with SWDB
- Remove unneeded regex URL tests (RhBug:1598336)
- Allow quoted values in ini files (RhBug:1624056)
- Filter out not unique set of solver problems (RhBug:1564369)
- Resolves: rhbz#1614531 - dnf 3.2 does not depsolve correctly
- Resolves: rhbz#1614346 - dnf rollback doesn't work after install/downgrade/upgrade
- bug 1605274 - DNF crashes on * in installation repository URL
- Resolves: rhbz#1623383 - dnf.exceptions.ConfigError: Error parsing ...

* Mon Sep 10 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.19.1-1
- Fix compilation errors on gcc-4.8.5
- [module] Allow module queries on disabled modules (RhBug:1627081)

* Fri Sep 07 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.19.0-1
- [query] Reldeps can contain a space char (RhBug:1612462)
- [transaction] Avoid adding duplicates via Transaction::addItem()
- Fix compilation errors on gcc-4.8.5
- [module] Make available ModuleProfile using SWIG
- [module] Redesign module disable and reset

* Fri Aug 31 2018 Daniel Mach <dmach@redhat.com> - 0.18.0-1
- [repo] Implement GPG key import
- [repo] Introduce Repo class replacing dnf.repo.Repo
- [context] Fix memory corruption in dnf_context
- [rhsm] Fix: RHSM don't write .repo file with same content (RhBug:1600452)
- [module] Create /etc/dnf/modules.d if it doesn't exist.
- [module] Forward C++ exceptions to bindings.

* Thu Aug 16 2018 Daniel Mach <dmach@redhat.com> - 0.17.2-2
- [module] Create /etc/dnf/modules.d if it doesn't exist.
- [module] Forward C++ exceptions to bindings.

* Mon Aug 13 2018 Daniel Mach <dmach@redhat.com> - 0.17.2-1
- [sqlite3] Change db locking mode to DEFAULT.
- [doc] Add libsmartcols-devel to devel deps.

* Mon Aug 13 2018 Daniel Mach <dmach@redhat.com> - 0.17.1-1
- [module] Solve a problem in python constructor of NSVCAP if no version.
- [translations] Update translations from zanata.
- [transaction] Fix crash after using dnf.comps.CompsQuery and forking the process in Anaconda.
- [module] Support for resetting module state.
- [output] Introduce wrapper for smartcols.

* Tue Aug 07 2018 Daniel Mach <dmach@redhat.com> - 0.17.0-1
- [conf] Add module_platform_id option.
- [module] Add ModulePackageContainer class.
- [module] Add ModulePersistor class.
- [sack] Module filtering made available in python API
- [sack] Module auto-enabling according to installed packages

* Fri Jul 27 2018 Daniel Mach <dmach@redhat.com> - 0.16.1-1
- [module] Implement 'module_hotfixes' conf option to skip filtering RPMs from hotfix repos.
- [goal] Fix distupgrade filter, allow downgrades.
- [context] Allow to set module platform in context.
- [module] Introduce proper modular dependency solving.
- [module] Platform pseudo-module based on /etc/os-release.
- [goal] Add Goal::listSuggested().
- [l10n] Support for translations, add gettext build dependency.

* Sun Jul 22 2018 Daniel Mach <dmach@redhat.com> - 0.16.0-1
- Fix RHSM plugin
- Add support for logging
- Bump minimal libmodulemd version to 1.6.1

* Mon Jul 09 2018 Igor Gnatenko <ignatenko@redhat.com> - 0.15.2-2
- Fix librhsm support logic

* Fri Jun 29 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.15.2-1
- Update to 0.15.1
- Resolves: rhbz#1595487

* Fri Jun 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.15.1-2
- Restore proper ldconfig_scriptlets

* Tue Jun 26 2018 Jaroslav Mracek <jmracek@redhat.com> - 0.15.1-1
- Update to 0.15.1

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 0.11.1-6
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Igor Gnatenko <ignatenko@redhat.com> - 0.11.1-4
- Switch to %%ldconfig_scriptlets

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.11.1-3
- Use better Obsoletes for platform-python

* Fri Nov 03 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.11.1-2
- Remove platform-python subpackage

* Mon Oct 16 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.11.1-1
- Rerelease of 0.11.1-1
- Improvement query performance
- Run file query in hy_subject_get_best_solution only for files (arguments that start with ``/`` or
  ``*/``)
- Resolves: rhbz#1498207 - DNF crash during upgrade installation F26 -> F27

* Tue Oct 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.11.0-1
- Update to 0.11.0

* Mon Oct 02 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.10.1-2
- Rerelease of 0.10.1-1

* Wed Sep 27 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.10.1-1
- Update to 0.10.1
- It improves query performance with name and arch filters. Also nevra filter will now
  handle string with or without epoch.
- Additionally for python bindings it renames NEVRA._has_just_name() to NEVRA.has_just_name() due
  to movement of code into c part of library.
- Resolves: rhbz#1260242 - --exclude does not affect dnf remove's removal of requirements
- Resolves: rhbz#1485881 - DNF claims it cannot install package, which have been already installed
- Resolves: rhbz#1361187 - [abrt] python-ipython-console: filter_updown(): python3.5 killed by SIGABRT

* Fri Sep 15 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.3-8
- Disable platform python on old releases

* Tue Aug 15 2017 Lumír Balhar <lbalhar@redhat.com> - 0.9.3-7
- Add platform-python subpackage

* Fri Aug 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.3-6
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.3-5
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.3-4
- Rebuilt for RPM soname bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.9.3-1
- Update to 0.9.3

* Sat Jul 01 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.2-1
- Update to 0.9.2

* Mon Jun 12 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.9.1-1
- Update to 0.9.1

* Mon May 22 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Tue May 02 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.8.2-1
- Update to 0.8.2

* Fri Mar 24 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Tue Mar 21 2017 Jaroslav Mracek <jmracek@redhat.com> - 0.8.0-1
- Update to 0.8.0

* Mon Feb 20 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.7.4-1
- Update to 0.7.4

* Fri Feb 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Wed Feb 08 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.7.2-1
- 0.7.2

* Fri Jan 06 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.7.1-1
- 0.7.1

* Wed Dec 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.0-0.7gitf9b798c
- Rebuild for Python 3.6

* Mon Dec 19 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.7.0-0.6gitf9b798c
- Use new upstream URL

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.7.0-0.5gitf9b798c
- Rebuild for Python 3.6

* Tue Dec 06 2016 Martin Hatina <mhatina@redhat.com> - 0.7.0-0.4gitf9b798c
- Increase conflict version of dnf

* Thu Dec 01 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.7.0-0.3gitf9b798c
- Update to latest snapshot

* Fri Nov 04 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.7.0-0.2git8bd77f8
- Update to latest snapshot

* Thu Sep 29 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.7.0-0.1git179c0a6
- Initial package
