Summary:	Search engine for music related metadata
Summary(pl.UTF-8):	Silnik wyszukiwania metadanych związanych z muzyką
Name:		glyr
Version:	1.0.10
Release:	1
License:	LGPL v3+
Group:		Applications/Multimedia
#Source0Download: https://github.com/sahib/glyr/releases
Source0:	https://github.com/sahib/glyr/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	85f5f8608bb78d4dd01c7170ea4c6997
Patch0:		optflags.patch
URL:		https://github.com/sahib/glyr
BuildRequires:	cmake >= 2.8.0
BuildRequires:	curl-devel
BuildRequires:	glib2-devel >= 1:2.10
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	rpmbuild(macros) >= 1.605
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

%description -l pl.UTF-8
Narzędzie Glyr działające z linii poleceń.

Rodzaje metadanych wyszukiwanych (i pobieranych) przez glyra to zwykle
dane widziane w odtwarzaczu muzyki. I faktycznie, pierwotnie kod
został napisany jako wewnętrzna biblioteka dla odtwarzacza muzyki, ale
następnie został rozszerzony, aby działał jako samodzielny program,
potrafiący pobrać:
 - grafikę z okładki
 - teksty
 - fotografie zespołu
 - biografię wykonawcy
 - listę ścieżek albumu
 - listę albumów wykonawcy
 - znaczniki, powiązane z wykonawcą, albumem lub tytułami, na przykład
   odnośniki do wikipedii
 - podobnych wykonawców
 - podobne utwory.

%package libs
Summary:	Search engine for music related metadata - shared library
Summary(pl.UTF-8):	Silnik wyszukiwania metadanych związanych z muzyką - biblioteka współdzielona
Group:		Libraries
Requires:	glib2 >= 1:2.10

%description libs
Glyr is a search engine for music related metadata. This package
contains shared library.

%description libs -l pl.UTF-8
Glyr to silnik wyszukiwania metadanych związanych z muzyką. Ten
pakiet zawiera bibliotekę współdzieloną.

%package devel
Summary:	Header files for Glyr library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Glyr
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	curl-devel
Requires:	glib2-devel >= 1:2.10
Requires:	sqlite3-devel >= 3

%description devel
Glyr development files.

%prep
%setup -q
%patch -P0 -p0

%build
install -d build
cd build
# NOTE: CMAKE_BUILD_TYPE is not functioning in this project, so we redefine them for _RELEASE
%cmake .. \
	-DCMAKE_C_FLAGS_RELEASE="%{rpmcflags}" \
	-DCMAKE_EXE_LINKER_FLAGS_RELEASE="%{rpmldflags}" \
	-DCMAKE_SHARED_LINKER_FLAGS_RELEASE="%{rpmldflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install/fast \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a src/examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG README.textile
%attr(755,root,root) %{_bindir}/glyrc

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglyr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglyr.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglyr.so
%{_includedir}/glyr
%{_pkgconfigdir}/libglyr.pc
%{_examplesdir}/%{name}-%{version}
