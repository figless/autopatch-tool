%global with_bundled 1
%global with_debug 1
%global with_check 1

%global provider        github
%global provider_tld    com
%global project         mongodb
%global repo            mongo-tools
# https://github.com/mongodb/mongo-tools
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          bd441aa9f15a804220bb2f69835d627df90e7e30
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

# Git hash in https://github.com/mongodb/mongo which corresponds to Version
%global mongohash a14d55980c2cdc565d4704a7e3ad37e4e535c1b2

# Define commands for building - from go-compilers-golang-compiler rpm
# BUILD_ID can be generated for golang build no matter of debuginfo
%define gobuild(o:) \
%ifnarch ppc64 \
scl enable go-toolset-1.10 -- go build -buildmode pie -compiler gc -tags=rpm_crashtraceback -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags'" -a -v -x %{?**};\
%else \
scl enable go-toolset-1.10 -- go build -compiler gc -tags=rpm_crashtraceback -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags'" -a -v -x %{?**};\
%endif

# Define commands for testing - from go-compilers-golang-compiler rpm
%define gotest() scl enable go-toolset-1.10 'go test -compiler gc -ldflags "${LDFLAGS:-}" %{?**}';


Name:		%{repo}
Version:        3.6.6
Release:        1%{?dist}
Summary:        MongoDB Tools
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
# Mongo-tools does not contain man files yet
# - see https://groups.google.com/forum/#!topic/mongodb-dev/t6Sd2Bki12I
Source1:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/bsondump.1
Source2:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongodump.1
Source3:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongoexport.1
Source4:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongofiles.1
Source5:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongoimport.1
Source6:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongooplog.1
Source7:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongorestore.1
Source8:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongostat.1
Source9:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongotop.1
Source10:       https://github.com/mongodb/mongo/raw/%{mongohash}/APACHE-2.0.txt

Patch0:         change-import-path.patch

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  x86_64 aarch64 ppc64le s390x
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
#BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires:  go-toolset-1.10-golang
BuildRequires:  openssl-devel

%if ! 0%{?with_bundled}
BuildRequires:  golang(github.com/howeyc/gopass)
BuildRequires:  golang(github.com/jessevdk/go-flags)
BuildRequires:  golang(github.com/smartystreets/goconvey/convey)
BuildRequires:  golang(github.com/10gen/openssl)
BuildRequires:  golang(golang.org/x/crypto/ssh/terminal)
BuildRequires:  golang(gopkg.in/mgo.v2)
BuildRequires:  golang(gopkg.in/mgo.v2/bson)
BuildRequires:  golang(gopkg.in/tomb.v2)
BuildRequires:  golang(github.com/nsf/termbox-go)
%endif

Conflicts:      mongodb < 3.0.0

%description
The MongoDB tools provides import, export, and diagnostic capabilities.

%package devel
Summary:       %{summary}
BuildArch:     noarch

%if ! 0%{?with_bundled}
Requires:      golang(github.com/howeyc/gopass)
Requires:      golang(github.com/jessevdk/go-flags)
Requires:      golang(github.com/smartystreets/goconvey/convey)
Requires:      golang(github.com/10gen/openssl)
Requires:      golang(golang.org/x/crypto/ssh/terminal)
Requires:      golang(gopkg.in/mgo.v2)
Requires:      golang(gopkg.in/mgo.v2/bson)
Requires:      golang(gopkg.in/tomb.v2)
Requires:      golang(github.com/nsf/termbox-go)
%endif

Provides:      golang(%{import_path}/bsondump) = %{version}-%{release}
Provides:      golang(%{import_path}/common) = %{version}-%{release}
Provides:      golang(%{import_path}/common/archive) = %{version}-%{release}
Provides:      golang(%{import_path}/common/auth) = %{version}-%{release}
Provides:      golang(%{import_path}/common/bsonutil) = %{version}-%{release}
Provides:      golang(%{import_path}/common/db) = %{version}-%{release}
Provides:      golang(%{import_path}/common/db/kerberos) = %{version}-%{release}
Provides:      golang(%{import_path}/common/db/openssl) = %{version}-%{release}
Provides:      golang(%{import_path}/common/failpoint) = %{version}-%{release}
Provides:      golang(%{import_path}/common/intents) = %{version}-%{release}
Provides:      golang(%{import_path}/common/json) = %{version}-%{release}
Provides:      golang(%{import_path}/common/log) = %{version}-%{release}
Provides:      golang(%{import_path}/common/options) = %{version}-%{release}
Provides:      golang(%{import_path}/common/password) = %{version}-%{release}
Provides:      golang(%{import_path}/common/progress) = %{version}-%{release}
Provides:      golang(%{import_path}/common/signals) = %{version}-%{release}
Provides:      golang(%{import_path}/common/testutil) = %{version}-%{release}
Provides:      golang(%{import_path}/common/text) = %{version}-%{release}
Provides:      golang(%{import_path}/common/util) = %{version}-%{release}
Provides:      golang(%{import_path}/mongodump) = %{version}-%{release}
Provides:      golang(%{import_path}/mongoexport) = %{version}-%{release}
Provides:      golang(%{import_path}/mongofiles) = %{version}-%{release}
Provides:      golang(%{import_path}/mongoimport) = %{version}-%{release}
Provides:      golang(%{import_path}/mongoimport/csv) = %{version}-%{release}
Provides:      golang(%{import_path}/mongorestore) = %{version}-%{release}
Provides:      golang(%{import_path}/mongostat) = %{version}-%{release}
Provides:      golang(%{import_path}/mongotop) = %{version}-%{release}

%description devel
This package contains library source intended for
building other packages which use %{project}/%{repo}.

%prep
%setup -q -n %{repo}-%{commit}
%if ! 0%{?with_bundled}
%patch0 -p1
%endif

sed -i.bak -e "s/built-without-version-string/%{version}/" \
           -e "s/built-without-git-spec/%{shortcommit}/" \
           common/options/options.go


%build
# Make link for etcd itself
mkdir -p src/github.com/mongodb
ln -s ../../../  src/github.com/mongodb/mongo-tools

%if 0%{?with_bundled}
export GOPATH=$(pwd):$(pwd)/vendor:%{gopath}
%else
export GOPATH=$(pwd):%{gopath}
%endif

mkdir bin
binaries=(bsondump mongostat mongofiles mongoexport mongoimport mongorestore mongodump mongotop)
for bin in "${binaries[@]}"; do
  %gobuild -o bin/${bin} \-tags ssl ${bin}/main/${bin}.go
done

# Copy Apache license
cp %{SOURCE10} $(basename %{SOURCE10})

%install
# main package binary
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 bin/* %{buildroot}%{_bindir}

install -d -m 755            %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE4} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE5} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE6} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE7} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE8} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE9} %{buildroot}%{_mandir}/man1/

install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done

# testing files for this project
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
cp -r mongorestore/testdata %{buildroot}/%{gopath}/src/%{import_path}/mongorestore/testdata
echo "%%{gopath}/src/%%{import_path}/mongorestore/testdata" >> devel.file-list
cp -r mongostat/test_data %{buildroot}/%{gopath}/src/%{import_path}/mongostat/test_data
echo "%%{gopath}/src/%%{import_path}/mongostat/test_data" >> devel.file-list

sort -u -o devel.file-list devel.file-list

%check
%if 0%{?with_check}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%endif

%gotest %{import_path}/common/bsonutil
# import cycle not allowed in test
#%gotest %{import_path}/common/db
# upstream bug, removed field from Intents struct
#%%gotest %{import_path}/common/intents
# redeclaration of C
#gotest {import_path}/common/json
# import cycle not allowed in test
#gotest {import_path}/common/log
%gotest %{import_path}/common/progress
%gotest %{import_path}/common/text
#%gotest %{import_path}/common/util
%gotest %{import_path}/mongodump
%gotest %{import_path}/mongoexport
%gotest %{import_path}/mongofiles
#gotest {import_path}/mongoimport
%gotest %{import_path}/mongorestore
%gotest %{import_path}/mongostat
#%gotest %{import_path}/mongoreplay

%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE.md APACHE-2.0.txt
%doc Godeps README.md CONTRIBUTING.md THIRD-PARTY-NOTICES
%{_bindir}/*
%{_mandir}/man1/*

%files devel -f devel.file-list
%license LICENSE.md
%doc Godeps README.md CONTRIBUTING.md THIRD-PARTY-NOTICES
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}

%changelog
* Mon Aug 06 2018 mskalick@redhat.com - 3.6.6-1
- Rebase to upstream release 3.6.6

* Tue Apr 17 2018 mskalick@redhat.com - 3.6.4-0.1.gite657a1d
- Change version to 3.6.4 - still used latest sources from v3.6 branch
  (to support openssl 1.1.0 and new go compiler)

* Thu Apr 12 2018 mskalick@redhat.com - 3.6.3-0.2.gite657a1d
- Update to latest commit from v3.6 upstream branch (will became r3.6.4-rc1 release)
- Rebase to Fedora commit e48cd06

* Mon Feb 26 2018 Marek Skalický <mskalick@redhat.com> - 3.6.3-0.1.git2b10d84
- Rebase to latest upstream release

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-0.9.git17a5573
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-0.8.git17a5573
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-0.7.git17a5573
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Marek Skalický <mskalick@redhat.com> - 3.2.1-0.6.git17a5573
- Exclude ppc64 architecture (missing cgo)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-0.5.git17a5573
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-0.4.git17a5573
- https://fedoraproject.org/wiki/Changes/golang1.7

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-0.3.git17a5573
- https://fedoraproject.org/wiki/Changes/golang1.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-0.2.git17a5573
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 jchaloup <jchaloup@redhat.com> - 3.1.1-0.1.git17a5573
- Update to 3.2.1
  resolves: #1282650

* Mon Nov 09 2015 jchaloup <jchaloup@redhat.com> - 3.0.4-0.2.gitefe71bf
- Update to spec-2.1
  resolves: #1279140

* Mon Jun 22 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.4-1
- Repacked by using gofed tool (thanks to jchaloup@redhat.com)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.3-1
- Upgrade to version 3.0.3
- Add Apache license

* Mon May 4 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.2-1
- Initial packaging
