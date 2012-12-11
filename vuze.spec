%define         _newname Vuze

Name:		vuze
Version:	4.3.0.4
Release:	3
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
# (Anssi) Remove win32 and osx code to fix build:
Patch106:	vuze-disable-win32-osx.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  ant, jpackage-utils, xml-commons-apis
BuildRequires:  jakarta-commons-cli
BuildRequires:  bouncycastle >= 1.43
Requires:       bouncycastle >= 1.43
BuildRequires:  eclipse-swt
BuildRequires:  junit
BuildRequires:  java-rpmbuild
Requires:	xulrunner
Requires:       eclipse-swt
Requires:	  java >= 1.6
Provides:	azureus = %{version}-%{release}
Obsoletes:	azureus < %{version}-%{release}
BuildRequires:    desktop-file-utils
BuildRequires:  locales-en
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
BuildRequires:	liblog4j-java
Requires:	liblog4j-java

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

# Mandriva: remove bouncycastle, use system one
# but only on 2010.0+, as the previous releases had bloated bouncycastle packages
rm -r org/bouncycastle
%patch104 -p1

# Mandriva: remove osx, win32 stuff
# build fails when they are present
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
export LC_ALL=ISO-8859-1
mkdir -p build/libs
build-jar-repository -p build/libs jakarta-commons-cli log4j junit swt \
	bcprov

%ant jar

%install
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins
install -pm 644 dist/Azureus2.jar $RPM_BUILD_ROOT%{_datadir}/azureus/Azureus2.jar

install -d -m755 %{buildroot}%{_bindir}

install -m755 %{SOURCE1} %{buildroot}%{_bindir}/azureus
# link as per upstream
ln -s azureus %{buildroot}%{_bindir}/vuze

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
%{_bindir}/vuze
%{_datadir}/azureus

%files console



%changelog
* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 4.3.0.4-2mdv2011.0
+ Revision: 615414
- the mass rebuild of 2010.1 packages

* Wed Dec 09 2009 Anssi Hannula <anssi@mandriva.org> 4.3.0.4-1mdv2010.1
+ Revision: 475274
- new version 4.3.0.4
- create a vuze symlink for azureus binary as per upstream
- rediff patches disable-updates.patch, disable-win32-osx.patch

* Sun Oct 04 2009 Anssi Hannula <anssi@mandriva.org> 4.2.0.8-2mdv2010.0
+ Revision: 453371
- fix gre selection in startup script

* Sun Sep 20 2009 Anssi Hannula <anssi@mandriva.org> 4.2.0.8-1mdv2010.0
+ Revision: 445553
- new version 4.2.0.8
- provide build.plugins.xml for building plugins
- replace fedora win32/osx removal patches with cleaner versions
- suggest plugin packages that are bundled in the official upstream
  installation package
- fix vuze-console description

* Wed Aug 19 2009 Anssi Hannula <anssi@mandriva.org> 4.2.0.4-1mdv2010.0
+ Revision: 417918
- new version
- provide a new rewritten startup script
  o adds support for passing commands to already active instance
  o adds support for --ui option when necessary packages are installed
    (see below)
  o selects correct GRE for browser embedding depending on arch and the
    GRE version numbers (fixes bug #44008)
  o fixes loading of SWT, fixing vuze startup (fixes bug #42756)
  o use -Xmx128m option with java for now (as per upstream)
  o dropped symlink hacks, now using vuze's own support for separated
    system-wide plugins and user plugins
- drop custom applications-registry entry, unneeded
- clean .spec
- remove patches that were not applied
- remove fedora update manager removal patches
- add java5.patch from fedora (build for target 1.5)
- update other fedora patches
- disable updates for core, internal plugins, and system-wide plugins
  (disable-updates.patch, fixes bug #46219); user-installed plugins will
  be updated, however, and plugins can be installed directly from the
  Tools menu, as with official build
- do not try to install azupdater as a system-wide plugin (shared.patch)
- fix build with recent bouncycastle (recent-bouncycastle.patch)
- drop requires on java gtk stuff, they were unneeded
- split console support into vuze-console subpackage; that package will
  be empty but it requires the extra packages that are needed for
  console/telnet support
- really use system bouncycastle
- on 2009.1 and older, keep using internal bouncycastle as bouncycastle
  packages on those releases were bloated
- drop unneeded %%post and %%postun on 2009.0+
- use liblog4j-java packages instead of log4j on cooker in order to
  reduce unneeded dependencies

* Sun Mar 15 2009 Olivier Blin <oblin@mandriva.com> 4.0.0.4-2mdv2009.1
+ Revision: 355338
- add glib-java and libgtk-java as Requires (and remove them from BuildRequires, their devel counterpart is already BuildRequired)
- fix typo in BuildRequires

  + Jérôme Soyer <saispo@mandriva.org>
    - Fix launch script

* Thu Mar 05 2009 Jérôme Soyer <saispo@mandriva.org> 4.0.0.4-1mdv2009.1
+ Revision: 348975
- Add BR
- Remove gcj support
- New upstream release

* Wed Aug 13 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:3.1.1.0-0.0.1mdv2009.0
+ Revision: 271410
- direct symlink to swt.jar
- replace swt-gtk with swt everywhere
- fix startup script
- fix build

  + David Walluck <walluck@mandriva.org>
    - fix build with eclipse-swt
    - import vuze


