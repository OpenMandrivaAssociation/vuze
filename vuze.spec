%define         _newname Vuze

Name:		vuze
Version:	4.2.0.8
Release:	%mkrel 1
Summary:	A BitTorrent Client
Group:		Networking/File transfer
License:	GPLv2+
URL:		http://azureus.sourceforge.net

Source0:	http://downloads.sourceforge.net/azureus/%{_newname}_%{version}_source.zip

# Mandriva version of startup script:
Source1:	azureus.startup.script
Source2:	Azureus.desktop

# replace RELEASE-4_2_0_4 below:
# cvs -z3 -d:pserver:anonymous@azureus.cvs.sourceforge.net:/cvsroot/azureus co -p -r RELEASE-4_2_0_4 azureus2/build.xml > build.xml
Source4:        build.xml
# cvs -z3 -d:pserver:anonymous@azureus.cvs.sourceforge.net:/cvsroot/azureus co -p plugins/build.xml > build.plugins.xml
Source5:	build.plugins.xml

# Fedora patches
Patch2:         azureus-cache-size.patch
Patch3:         azureus-remove-manifest-classpath.patch
# Do not offer to install plugins as shared
Patch9:         azureus-no-shared-plugins.patch
Patch27:        azureus-SecureMessageServiceClientHelper-bcprov.patch
Patch28:        azureus-configuration.patch
Patch57:        azureus-4.0.0.4-stupid-invalid-characters.diff
Patch58:        azureus-4.2.0.4-java5.patch

# Mandriva patches
# (Anssi) Disable updates for core files, internal plugins, and plugins installed in /usr/share.
# Also remove warning dialog about not being able to update plugins in /usr/share.
# Note that plugins "azupdater" and "azupnpav" are automatically downloaded to user dir
# if not already installed in /usr/share.
Patch102:	vuze-disable-updates.patch
# (Anssi) Do not try to install azupdater into /usr/share, put it in user directory instead.
Patch103:	vuze-shared.patch
# (Anssi) adapt for recent bouncycastle
Patch104:	vuze-recent-bouncycastle.patch
# (Anssi) Same java5.patch above, but for plugins' build.xml
Patch105:	vuze-plugins-build-remove-target.patch
# (Anssi) Remove win32 and osx code:
Patch106:	vuze-disable-win32-osx.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  ant, jpackage-utils, xml-commons-apis
BuildRequires:  jakarta-commons-cli
%if %{mdkversion} >= 201000
BuildRequires:  bouncycastle >= 1.43
Requires:       bouncycastle >= 1.43
%endif
BuildRequires:  eclipse-swt
BuildRequires:  junit
BuildRequires:  java-rpmbuild
Requires:	xulrunner
Requires:       eclipse-swt
Requires:	  java >= 1.6
Provides:	azureus = %{version}-%{release}
Obsoletes:	azureus < %{version}-%{release}
BuildRequires:    desktop-file-utils
BuildArch:      noarch
# Bundled in official package
Suggests:	vuze-plugin-azplugins
# Bundled in official package
Suggests:	vuze-plugin-azrating
# Bundled in official package + automatically installed by vuze on startup
Suggests:	vuze-plugin-azupdater
# Bundled in official package + automatically installed by vuze on startup
Suggests:	vuze-plugin-azupnpav

%description
Vuze (previously Azureus) implements the BitTorrent protocol using java
and comes bundled with many invaluable features for both beginners and
advanced users.

If you need console or telnet support, you need to install package
vuze-console.

%package console
Summary:	Console interface support for Vuze
Group:		Networking/File transfer
Requires:	%{name}
Requires:	jakarta-commons-cli
%if %{mdkversion} >= 201000
BuildRequires:	liblog4j-java
Requires:	liblog4j-java
%else
# package with more bloat
BuildRequires:	log4j
Requires:	log4j
%endif

%description console
Console interface support for Vuze (previously Azureus) bittorrent
client.

You can run Vuze in console mode with command "azureus --ui=console" and
in telnet mode with "azureus --ui=telnet".

%prep
%setup -q -c

cp %{SOURCE4} %{SOURCE5} .
%patch2 -p0
%patch3 -p1 -b .remove-manifest-classpath
%patch9 -p0
%patch27 -p1 -b .nobcprov
%patch28 -p0

%patch57 -b .orig -p1

%patch58 -p1 -b .java5
%patch105 -p0

rm org/gudy/azureus2/ui/swt/test/PrintTransferTypes.java
#sed -i -e \
#  "s|sun.security.action.GetPropertyAction|gnu.java.security.action.GetPropertyAction|" \
#  org/gudy/azureus2/core3/internat/MessageText.java

# Convert line endings...
sed -i 's/\r//' ChangeLog.txt
chmod 644 *.txt

%if %{mdkversion} >= 201000
# Mandriva: remove bouncycastle, use system one
# but only on 2010.0+, as the previous releases had bloated bouncycastle packages
rm -r org/bouncycastle
%patch104 -p1
%endif

# Mandriva: remove osx, win32 stuff
rm -r com/aelitis/azureus/util/win32
rm -r org/gudy/azureus2/ui/swt/osx
rm -r org/gudy/azureus2/ui/swt/win32
rm -r org/gudy/azureus2/platform/macosx
rm -r org/gudy/azureus2/platform/win32
rm org/gudy/azureus2/ui/swt/test/Win32TransferTypes.java
%patch106 -p1

# Mandriva: remove core updaters
rm org/gudy/azureus2/update/CorePatchChecker.java
rm org/gudy/azureus2/update/CoreUpdateChecker.java
rm org/gudy/azureus2/ui/swt/updater2/SWTUpdateChecker.java
rm org/gudy/azureus2/ui/swt/updater2/PreUpdateChecker.java
rm org/gudy/azureus2/platform/unix/PlatformManagerUnixPlugin.java
rm org/gudy/azureus2/platform/PlatformManagerPluginDelegate.java
%patch102 -p1
%patch103 -p1

%build
mkdir -p build/libs
build-jar-repository -p build/libs jakarta-commons-cli log4j junit swt \
%if %{mdkversion} >= 201000
	bcprov
%endif

%ant jar

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins
install -pm 644 dist/Azureus2.jar $RPM_BUILD_ROOT%{_datadir}/azureus/Azureus2.jar

install -d -m755 %{buildroot}%{_bindir}

sed 's,@LIB@,%{_lib},' %{SOURCE1} > %{buildroot}%{_bindir}/azureus
chmod 0755 %{buildroot}%{_bindir}/azureus

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps
install -m 644 org/gudy/azureus2/ui/icons/a32.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/azureus.png
install -m 644 org/gudy/azureus2/ui/icons/a16.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/azureus.png
install -m 644 org/gudy/azureus2/ui/icons/a32.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/azureus.png
install -m 644 org/gudy/azureus2/ui/icons/a64.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps/azureus.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install \
	--dir ${RPM_BUILD_ROOT}%{_datadir}/applications	\
	%{SOURCE2}

# build.xml for building plugins
install -m644 build.plugins.xml %{buildroot}%{_datadir}/azureus

%clean
rm -rf $RPM_BUILD_ROOT

%if %{mdkversion} < 200900
%post
%{update_desktop_database}
%update_icon_cache hicolor
%update_menus

%postun
%{clean_desktop_database}
%clean_icon_cache hicolor
%clean_menus
%endif

%files
%defattr(-,root,root)
%doc ChangeLog.txt
%{_datadir}/applications/*
%{_datadir}/pixmaps/azureus.png
%{_datadir}/icons/hicolor/16x16/apps/azureus.png
%{_datadir}/icons/hicolor/32x32/apps/azureus.png
%{_datadir}/icons/hicolor/64x64/apps/azureus.png
%{_bindir}/azureus
%{_datadir}/azureus

%files console

