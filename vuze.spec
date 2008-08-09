%define gcj_support 0

Name:           vuze
Version:        3.1.1.0
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        BitTorrent Client
Group:          Networking/File transfer
License:        GPL
URL:            http://azureus.sourceforge.net/
Source0:        http://download.sourceforge.net/sourceforge/azureus/Vuze_3.1.1.0_source.zip
#Source0:        http://superb-west.dl.sourceforge.net/sourceforge/azureus/Azureus_%{version}_source.zip

Source1:        azureus.script
Source2:        Azureus.desktop
Source3:        azureus.applications

# FIXME: (walluck): These are the plugins shipped with vuze. Need to build.
%if 0
Source4:        http://azureus.sourceforge.net/plugins/azupnpav_0.2.2.zip
Source5:        http://azureus.sourceforge.net/plugins/azplugins_2.1.6.jar
Source6:        http://azureus.sourceforge.net/plugins/azrating_1.3.1.jar
Source7:        http://azureus.sourceforge.net/plugins/azupdater_1.8.8.zip
%endif

Source100:      ChangeLog.txt
Source101:      GPL.txt
Source102:      vuze-build.xml
Source103:      build.xml

Patch200:         vuze-no-win32-or-macosx.patch
Patch201:         vuze-swt.patch
Patch202:         vuze-no-com-sun.patch
Patch203:         vuze-no-old-bcprov.patch
Patch204:         vuze-remove-manifest-classpath.patch

Patch0:         azureus-remove-win32-osx-platforms.patch
Patch1:         azureus-remove-win32-PlatformManagerUpdateChecker.patch
Patch2:         azureus-cache-size.patch
Patch3:         azureus-remove-manifest-classpath.patch
# (anssi) causes azureus to get stuck during loading:
###Patch7:         azureus-themed.patch
Patch8:         azureus-rh-bugzilla-180418.patch
Patch9:         azureus-no-shared-plugins.patch
Patch12:        azureus-no-updates-PluginInitializer.patch
# (anssi) still causes splash screen to remain on indefinitely
###Patch13:        azureus-no-updates-PluginInterfaceImpl.patch
Patch14:        azureus-no-update-manager-AzureusCoreImpl.patch
Patch15:        azureus-no-update-manager-CorePatchChecker.patch
Patch16:        azureus-no-update-manager-CoreUpdateChecker.patch
Patch18:        azureus-no-update-manager-PluginInstallerImpl.patch
Patch19:        azureus-no-update-manager-PluginUpdatePlugin.patch
Patch20:        azureus-no-update-manager-SWTUpdateChecker.patch
#Patch22:        azureus-no-update-manager-UpdateMonitor.patch
Patch23:        azureus-no-update-manager-PluginInstallerImpl-2.patch
#Patch25:        azureus-no-update-manager-MainStatusBar.patch
#Patch26:       azureus-nativetabs.patch
Patch27:        azureus-SecureMessageServiceClientHelper-bcprov.patch
#Patch28:        azureus-UDPConnectionSet-bcprov.patch
#Patch29:        azureus-CryptoHandlerECC-bcprov.patch
#Patch30:        azureus-CryptoSTSEngineImpl-bcprov.patch
Patch31:        azureus-fix-menu-MainMenu.patch
Patch32:        azureus-no-update-manager-MainMenu.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Obsoletes:      azureus < %{epoch}:%{version}-%{release}
Provides:       azureus = %{epoch}:%{version}-%{release}

BuildRequires:  ant, java-rpmbuild >= 0:1.5
# (anssi 01/2008) AFAICS not needed:
# BuildRequires: xml-commons-apis
BuildRequires:  jakarta-commons-cli, log4j
BuildRequires:  junit
# (anssi) needed only by patch7, not applied:
# BuildRequires:  libgconf-java
BuildRequires:  bouncycastle >= 0:1.33
BuildRequires:  eclipse-swt
Requires:       eclipse-swt
# (anssi) needed only by patch7, not applied:
# Requires:       libgconf-java
Requires:       bouncycastle >= 0:1.33
Requires:       java
Requires:       jpackage-utils
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRequires:  desktop-file-utils
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description 
Azureus implements the BitTorrent protocol using java language and
comes bundled with many invaluable features for both beginners and
advanced users.

%prep
%setup -q -c -n %{name}3
%{__cp} -a %{SOURCE100} %{SOURCE101} %{SOURCE102} %{SOURCE103} .
rm -r org/bouncycastle
# XXX: rm -r org/json
%{__perl} -pi -e 's/\r\n$/\n/g' com/aelitis/azureus/core/update/impl/AzureusRestarterImpl.java \
                                com/aelitis/azureus/ui/swt/views/skin/TorrentListViewsUtils.java \
                                org/gudy/azureus2/platform/PlatformManagerFactory.java \
                                org/gudy/azureus2/platform/PlatformManagerPluginDelegate.java \
                                org/gudy/azureus2/ui/swt/ImageRepository.java \
                                com/aelitis/azureus/core/clientmessageservice/secure/impl/SecureMessageServiceClientHelper.java \
                                com/aelitis/azureus/ui/swt/shells/LightBoxBrowserWindow.java \
                                org/gudy/azureus2/ui/swt/components/shell/LightBoxShell.java \
                                org/gudy/azureus2/ui/swt/components/shell/StyledShell.java
##%%patch100 -p1
#%%patch101 -p1
%patch200 -p0 -b .no-win32-or-macosx
%patch201 -p0 -b .swt
%patch202 -p0
%patch203 -p0 -b .no-old-bcprov
%patch204 -p0 -b .remove-manifest-classpath
%if 0
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
# (anssi) see above
###%patch7 -p0
%patch8 -p0
%patch9 -p0
#%patch11 -p0
%patch12 -p0
# (anssi) see above
###%patch13 -p0
%endif
#%%patch14 -p0
#%%patch15 -p0
#%%patch16 -p0
#%%patch18 -p0
#%%patch19 -p0
#%%patch20 -p0
# FIXME
#%%patch22 -p0
#%%patch23 -p0
#%%patch25 -p0
%if 0
#%%patch26 -p0
%patch27 -p0
#%patch28 -p0
#%patch29 -p0
#%patch30 -p0
%patch31 -p0
%endif
#%%patch32 -p0

mkdir -p build/libs
build-jar-repository -p build/libs jakarta-commons-cli swt log4j junit bcprov
# (anssi) Used by unapplied patch7 only, if re-enabled remember to modify azureus.script as well
#%if %mdkversion == 200700
#gtk2.8 glib0.2
#%else
#gtk2.10 glib0.4
#%endif

find ./ -name osx | xargs rm -r
find ./ -name macosx | xargs rm -r
find ./ -name win32\* | xargs rm -r
find ./ -name Win32\* | xargs rm -r
# Remove test code
rm org/gudy/azureus2/ui/swt/test/PrintTransferTypes.java

# Convert line endings...
%{__sed} -i 's/\r$//g' *.txt
chmod 644 *.txt

%build
%{ant} jar

%if 0
mkdir -p plugins/azplugins
cd plugins/azplugins
unzip -q %{SOURCE5}
rm -f *.jar `find ./ -name \*class`
find ./ -name \*java | xargs %{javac} -cp `build-classpath swt-gtk`:../..:.
find ./ -name \*java | xargs rm
%{jar} cvf azplugins_2.1.1.jar *
cd ../..

unzip -q %{SOURCE6}
cd plugins/bdcc
unzip *.jar
rm -f *.jar `find ./ -name \*class`
find ./ -name \*java | xargs %{javac} -cp `build-classpath swt-gtk`:../..:.
find ./ -name \*java | xargs rm
%{jar} cvf bdcc_2.2.2.jar *
cd ../..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__mkdir_p} %{buildroot}%{_javadir}

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins
install -pm 644 dist/Azureus2.jar $RPM_BUILD_ROOT%{_javadir}/Azureus2.jar
install -p -D -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/azureus
sed --in-place -e "s:/usr/lib:%{_libdir}:g;" $RPM_BUILD_ROOT%{_bindir}/azureus

%if 0
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/azplugins
install -pm 644 plugins/azplugins/azplugins_2.1.1.jar $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/azplugins/azplugins_2.1.1.jar
install -pm 644 plugins/azplugins/plugin.properties $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/azplugins/plugin.properties

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/bdcc
install -pm 644 plugins/bdcc/bdcc_2.2.2.jar $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/bdcc/bdcc_2.2.2.jar
install -pm 644 plugins/bdcc/plugin.properties $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/bdcc/plugin.properties
%endif

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps
install -m 644 org/gudy/azureus2/ui/icons/a32.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/azureus.png
install -m 644 org/gudy/azureus2/ui/icons/a16.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/azureus.png
install -m 644 org/gudy/azureus2/ui/icons/a32.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/azureus.png
install -m 644 org/gudy/azureus2/ui/icons/a64.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps/azureus.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
%{_bindir}/desktop-file-install --vendor mandriva            \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications      \
        --add-category X-MandrivaLinux-Internet-FileTransfer \
        --remove-category Application                        \
        %{SOURCE2}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/application-registry
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/application-registry

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{gcj_support}
%{update_gcjdb}
%endif
%{update_desktop_database}
%{update_mime_database}
%update_icon_cache hicolor

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif
%{clean_desktop_database}
%{clean_mime_database}
%clean_icon_cache hicolor

%files
%defattr(0644,root,root,0755)
%doc *.txt
%{_datadir}/applications/*
%{_datadir}/application-registry/*
%{_datadir}/pixmaps/azureus.png
%{_datadir}/icons/hicolor/16x16/apps/azureus.png
%{_datadir}/icons/hicolor/32x32/apps/azureus.png
%{_datadir}/icons/hicolor/64x64/apps/azureus.png
%attr(0755,root,root) %{_bindir}/azureus
%{_datadir}/azureus
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
