%define         _newname Vuze

Name:		vuze
Version:	4.0.0.4
Release:	%mkrel 2
Summary:	A BitTorrent Client
Group:		Networking/File transfer
License:	GPLv2+
URL:		http://azureus.sourceforge.net

Source0:	http://downloads.sourceforge.net/azureus/%{_newname}_%{version}_source.zip

Source1:	azureus.script
Source2:	Azureus.desktop
Source3:	azureus.applications
#Source4:	azureus-License.txt

#Source5:	azplugins_2.1.6.jar
#Source6:	bdcc_2.2.2.zip

Patch0:		azureus-remove-win32-osx-platforms.patch
Patch2:		azureus-cache-size.patch
Patch3:		azureus-remove-manifest-classpath.patch
Patch9:		azureus-no-shared-plugins.patch
Patch12:	azureus-no-updates-PluginInitializer.patch
#Patch13:	azureus-no-updates-PluginInterfaceImpl.patch
Patch14:	azureus-no-update-manager-AzureusCoreImpl.patch
Patch15:	azureus-no-update-manager-CorePatchChecker.patch
Patch16:	azureus-no-update-manager-CoreUpdateChecker.patch
Patch18:	azureus-no-update-manager-PluginInstallerImpl.patch
Patch19:	azureus-no-update-manager-PluginUpdatePlugin.patch
Patch20:	azureus-no-update-manager-SWTUpdateChecker.patch
Patch22:	azureus-no-update-manager-UpdateMonitor.patch
Patch23:	azureus-no-update-manager-PluginInstallerImpl-2.patch
Patch27:	azureus-SecureMessageServiceClientHelper-bcprov.patch
Patch28:	azureus-configuration.patch
Patch31:	azureus-fix-menu-MainMenu.patch

Patch50:        azureus-4.0.0.4-boo-windows.diff
Patch51:        azureus-4.0.0.4-boo-osx.diff
Patch52:        azureus-4.0.0.4-screw-w32-tests.diff
Patch53:        azureus-4.0.0.4-boo-updating-w32.diff
Patch54:        azureus-4.0.0.4-screw-win32utils.diff
Patch55:        azureus-4.0.0.4-oops-return.diff
Patch56:        azureus-4.0.0.4-silly-java-tricks-are-for-kids.diff
Patch57:        azureus-4.0.0.4-stupid-invalid-characters.diff

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  ant, jpackage-utils, xml-commons-apis
BuildRequires:  jakarta-commons-cli, log4j
BuildRequires:  libgconf-java
BuildRequires:  bouncycastle
BuildRequires:  eclipse-swt
BuildRequires:  junit
BuildRequires:  glib-java-devel, libgtk-java-devel
BuildRequires:  java-rpmbuild
Requires:       jakarta-commons-cli, log4j
Requires:	xulrunner
Requires:       eclipse-swt
Requires:       libgconf-java
Requires:       bouncycastle
Requires:	  java
BuildRequires:    java-devel
BuildRequires:    desktop-file-utils
BuildRequires:    libgkt-java, glib-java
Requires(post):   desktop-file-utils
Requires(postun): desktop-file-utils
BuildArch:      noarch


%description
Azureus (now %{_newname}) implements the BitTorrent protocol using java
and comes bundled with many invaluable features for both beginners and
advanced users.

%prep
%setup -q -c
#%patch0 -p0
%patch2 -p0
%patch3 -p0
%patch9 -p0
#%patch12 -p0
#%patch13 -p0
%patch14 -p0
%patch15 -p0
#%patch16 -p0
#%patch18 -p0
#%patch19 -p0
#%patch20 -p0
#%patch22 -p0
#%patch23 -p0
%patch27 -p0
%patch28 -p0
#%patch31 -p0
#rm com/aelitis/azureus/core/update -rf
#find ./ -name osx | xargs rm -r
#find ./ -name macosx | xargs rm -r
#find ./ -name win32 | xargs rm -r
#find ./ -name Win32\* | xargs rm -r
# Remove test code
%patch50 -b .orig
%patch51 -b .orig
%patch52 -b .orig
%patch53 -b .orig
%patch54 -b .orig
%patch55 -b .orig
%patch56 -b .orig
%patch57 -b .orig -p1
rm org/gudy/azureus2/ui/swt/test/PrintTransferTypes.java
#sed -i -e \
#  "s|sun.security.action.GetPropertyAction|gnu.java.security.action.GetPropertyAction|" \
#  org/gudy/azureus2/core3/internat/MessageText.java

# Convert line endings...
sed -i 's/\r//' ChangeLog.txt
chmod 644 *.txt


%build
mkdir -p build/libs
build-jar-repository -p build/libs bcprov jakarta-commons-cli log4j \
  gtk2.10 glib0.4 junit
ln -s %{_libdir}/eclipse/swt.jar build/libs

%ant jar

#mkdir -p plugins/azplugins
#pushd plugins
#pushd azplugins
#unzip -q %{SOURCE5}
#rm -f *.jar `find ./ -name \*class`
#find ./ -name \*java | xargs javac -cp %{_libdir}/eclipse/swt.jar:../..:.
#find ./ -name \*java | xargs rm
#jar cvf azplugins_2.1.6.jar .
#popd
#popd

#unzip -q %{SOURCE6}
#pushd plugins
#pushd bdcc
#unzip *.jar
#rm -f *.jar `find ./ -name \*class`
#find ./ -name \*java | xargs javac -cp %{_libdir}/eclipse/swt.jar:../..:.
#find ./ -name \*java | xargs rm
#jar cvf bdcc_2.2.2.jar .
#popd
#popd

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins
install -pm 644 dist/Azureus2.jar $RPM_BUILD_ROOT%{_datadir}/azureus/Azureus2.jar
# TODO: fix launcher to be multilib-safe
install -p -D -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/azureus
sed --in-place "s:/usr/lib:%{_libdir}:g" $RPM_BUILD_ROOT%{_bindir}/azureus

#install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/azplugins
#install -pm 644 plugins/azplugins/azplugins_2.1.6.jar $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/azplugins/azplugins_2.1.6.jar
#install -pm 644 plugins/azplugins/plugin.properties $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/azplugins/plugin.properties

#install -dm 755 $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/bdcc
#install -pm 644 plugins/bdcc/bdcc_2.2.2.jar $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/bdcc/bdcc_2.2.2.jar
#install -pm 644 plugins/bdcc/plugin.properties $RPM_BUILD_ROOT%{_datadir}/azureus/plugins/bdcc/plugin.properties

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

mkdir -p $RPM_BUILD_ROOT%{_datadir}/application-registry
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/application-registry


%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_desktop_database}
%{update_mime_database}
%update_icon_cache hicolor

%postun
%{clean_desktop_database}
%{clean_mime_database}
%clean_icon_cache hicolor

%files
%defattr(-,root,root)
%doc ChangeLog.txt GPL.txt
%{_datadir}/applications/*
%{_datadir}/application-registry/*
%{_datadir}/pixmaps/azureus.png
%{_datadir}/icons/hicolor/16x16/apps/azureus.png
%{_datadir}/icons/hicolor/32x32/apps/azureus.png
%{_datadir}/icons/hicolor/64x64/apps/azureus.png
%{_bindir}/azureus
%{_datadir}/azureus
