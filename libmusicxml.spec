%define		major	3
%define		libname	%mklibname musicxml %{major}
%define		devname	%mklibname musicxml -d
%define		oname	libmusicxml2

Summary:		A toolbox to support the MusicXML format
Name:		libmusicxml
Version:		3.22
Release:		1
License:		LGPLv2.1+ and MusicXML Public License v3.0
Group:		Publishing
Url:		https://www.musicxml.com/
Source0:	https://github.com/grame-cncm/libmusicxml/archive/%{name}-%{version}.tar.gz
Source100:	libmusicxml.rpmlintrc
Patch0:		libmusicxml-3.0.0-fix-Doxyfile.patch
Patch1:		libmusicxml-3.22-fix-library-names.patch
Patch2:		libmusicxml-3.22-fix-CMAKEOPT.patch
Patch3:		libmusicxml-3.22-rename-uplink-things.patch
Patch4:		libmusicxml-3.22-fix-ties-in-chords.patch
BuildRequires:		cmake
BuildRequires:		doxygen

%description
MusicXML is a standard open format for exchanging digital sheet music. It was
designed from the ground up for sharing sheet music files between applications
and for archiving sheet music files for use in the future.
This package provides a complete toolbox to allow MusicXML support.

#------------------------------------------------------------------------------

%package -n %{libname}
Summary:	Library and XML files for MusicXML support
Group:		System/Libraries
Provides:	%{name} = %{EVRD}

%description -n %{libname}
MusicXML is a standard open format for exchanging digital sheet music.
This package contains the binary library and XML files needed to provide
MusicXML support.

%files -n %{libname}
%license license.txt 
%doc readme.md doc/introductionToMusicxml/IntroductionToMusicXML.pdf
%{_libdir}/%{name}.so.%{major}*

#------------------------------------------------------------------------------

%package -n %{devname}
Summary:		Development files for %{libname}
Group:			Development/C++
Requires:		%{libname} = %{EVRD}
Provides:		%{name}-devel = %{EVRD}

%description -n %{devname}
MusicXML is a standard open format for exchanging digital sheet music.
This package contains the development files needed to provide MusicXML
support.

%files -n %{devname}
%license license.txt
%doc doc/html/*
%{_includedir}/%{name}/*.h
%{_libdir}/%{name}.so
%{_datadir}/%{name}/schema/3.1/*

#------------------------------------------------------------------------------

%package tools
Summary:	Development files for %{libname}
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Requires:	%{name}-dtd = %{EVRD}
%rename		%{name}-examples

%description tools
MusicXML is a standard open format for exchanging digital sheet music.
This package contains sample programs and tools built with %{libname}.

%files tools
%license license.txt
#doc doc/userSGuideToXml2ly/userSGuideToXml2ly.pdf
%{_bindir}/*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/misc
%dir %{_datadir}/%{name}/samples
%dir %{_datadir}/%{name}/xml2guido
%{_datadir}/%{name}/misc/*
%{_datadir}/%{name}/samples/*
%{_datadir}/%{name}/xml2guido/*.xml

#------------------------------------------------------------------------------

%package dtd
Summary:		Development files for %{libname}
Group:			Publishing
Requires:		%{libname} = %{EVRD}
Provides:		%{name}-dtd = %{EVRD}

%description dtd
MusicXML is a standard open format for exchanging digital sheet music.
This package contains the XML files needed to provide MusicXML support.

%files dtd
%doc dtds/3.1/README.md
%{_datadir}/%{name}/dtds/2.0
%{_datadir}/%{name}/dtds/3.0
%{_datadir}/%{name}/dtds/3.1

#------------------------------------------------------------------------------


%prep
%autosetup -p1 -n %{name}-%{version}

# Fix perms
find src/ -name "*.h" -o -name "*.cpp" | xargs chmod 0644


%build
cd build
%cmake	\
		-DCMAKE_CONFIGURATION_TYPES="Release" \
		-DLIBRARY_OUTPUT_PATH="%{_libdir}"

# HACK: Fix hardcoded library installation place in cmake_install.cmake
# because changing "LIBRARY_OUTPUT_PATH" in CMakeLists.txt file does not have any effect
sed -i 's|"${CMAKE_INSTALL_PREFIX}/lib"|"${CMAKE_INSTALL_PREFIX}/%{_lib}"|g' cmake_install.cmake

%make_build

# Make docs
pushd ../../doc
	doxygen -u
	doxygen Doxyfile
popd


%install
%make_install -C build/build

# Manually install various useful stuff:
# 1. Other example tools (xml2midi, xmlclone...)
mkdir -p %{buildroot}%{_bindir}
mv build/bin/xml2midi %{buildroot}%{_bindir}/
cp build/bin/{xmlclone,xmlfactory,xmliter} %{buildroot}%{_bindir}/
cp build/bin/{countnotes,partsummary,RandomMusic} %{buildroot}%{_bindir}/

# 2. Dtd files for MusicXML
mkdir -p %{buildroot}%{_datadir}/%{name}/dtds/{2.0,3.0,3.1}
cp dtds/2.0/* %{buildroot}%{_datadir}/%{name}/dtds/2.0
cp dtds/3.0/* %{buildroot}%{_datadir}/%{name}/dtds/3.0
cp -a dtds/3.1/* %{buildroot}%{_datadir}/%{name}/dtds/3.1

# 3. Sample & test files
mkdir -p %{buildroot}%{_datadir}/%{name}/samples/{musicxml,scores}
mkdir -p %{buildroot}%{_datadir}/%{name}/misc
mkdir -p %{buildroot}%{_datadir}/%{name}/xml2guido
cp files/misc/* %{buildroot}%{_datadir}/%{name}/misc/
cp -a files/samples/musicxml/* %{buildroot}%{_datadir}/%{name}/samples/musicxml/
#cp files/samples/scores/*.{gif,pdf} %%{buildroot}%%{_datadir}/%%{name}/samples/scores/
cp files/xml2guido/* %{buildroot}%{_datadir}/%{name}/xml2guido

# Drop unwanted stuff
rm -f %{buildroot}%{_prefix}/CHANGELOG.txt
rm -f %{buildroot}%{_prefix}/README.html
rm -f %{buildroot}%{_datadir}/%{name}/doc/*
rmdir %{buildroot}%{_datadir}/%{name}/doc/
rm -f %{buildroot}%{_libdir}/*.a

# Fix perms
chmod -x %{buildroot}%{_datadir}/%{name}/dtds/3.1/schema/*
