# TODO
# - ldflags not functioning
Summary:	Search engine for music related metadata
Name:		glyr
Version:	1.0.5
Release:	1
License:	GPL v3+
Group:		Applications/Multimedia
URL:		https://github.com/sahib/glyr
Source0:	http://github.com/sahib/glyr/archive/%{version}.tar.gz?/%{name}-%{version}.tar.gz
# Source0-md5:	d22052a4eb2f3bbc4a89e879cb9c1740
Patch0:		optflags.patch
BuildRequires:	cmake >= 2.8.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.10
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	rpmbuild(macros) >= 1.600
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Glyr CLI tool.

The sort of metadata glyr is searching (and downloading) is usually
the data you see in your musicplayer. And indeed, originally it was
written to serve as internally library for a musicplayer, but has been
extended to work as a standalone program which is able to download:

- cover art
- lyrics
- bandphotos
- artist biography
- album reviews
- tracklists of an album
- a list of albums from a specific artist
- tags, either related to artist, album or title relations, for
  example links to wikipedia
- similar artists
- similar songs.

%package libs
Summary:	Searcheninge for Musicrelated Metadata
Group:		Libraries

%description libs
Glyr shared library.

%package devel
Summary:	Searcheninge for Musicrelated Metadata
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Glyr development files.

%prep
%setup -q
%patch0 -p0

%build
install -d build
cd build
# NOTE: CMAKE_BUILD_TYPE is not functioning in this project, so we redefine them for _RELEASE
%cmake \
	-DCMAKE_C_FLAGS_RELEASE="%{rpmcflags}" \
	-DCMAKE_EXE_LINKER_FLAGS_RELASE="%{rpmldflags}" \
	-DCMAKE_SHARED_LINKER_FLAGS_RELASE="%{rpmldflags}" \
	-DCMAKE_MODULE_LINKER_FLAGS_RELASE="%{rpmldflags}" \
	../
%{__make} VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install/fast \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a src/examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG README.textile
%attr(755,root,root) %{_bindir}/glyrc

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglyr.so.*.*.*
%ghost %{_libdir}/libglyr.so.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/glyr
%{_libdir}/libglyr.so
%{_pkgconfigdir}/libglyr.pc
%{_examplesdir}/%{name}-%{version}
