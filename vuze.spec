%define	pkgname		Vuze
%define	pkgversion	5400

Name:		vuze
Version:	5.4.0.0
Release:	2
Summary:	A BitTorrent Client
Group:		Networking/File transfer
License:	GPLv2
URL:		http://www.vuze.com/
Source0:	http://sourceforge.net/projects/azureus/files/vuze/%{pkgname}_%{pkgversion}/%{pkgname}_%{pkgversion}_source.zip
Source1:	azureus.script
Source2:	Azureus.desktop
Source3:	azureus.applications
#ant build script from Azureus-4.3.0.6
Source4:	build.xml
Patch0:		azureus-5.3.0.0-mga-cache-size.patch
Patch1:		azureus-5.3.0.0-mga-remove-manifest-classpath.patch
Patch2:		azureus-5.3.0.0-mga-no-shared-plugins.patch
Patch3:		azureus-5.3.0.0-mga-SecureMessageServiceClientHelper-bcprov.patch
Patch4:		azureus-5.3.0.0-mga-boo-osx.patch
Patch5:		azureus-5.3.0.0-mga-boo-updating-w32.patch
Patch6:		azureus-5.3.0.0-mga-stupid-invalid-characters.patch
Patch7:		azureus-5.3.0.0-mga-java5.patch
Patch8:		azureus-5.3.0.0-mga-no-bundled-apache-commons.patch
Patch9:		azureus-5.4.0.0-mga-no-bundled-json.patch
Patch10:	azureus-5.4.0.0-mga-no-bundled-bouncycastle.patch
BuildArch:	noarch

BuildRequires:	ant
BuildRequires:	apache-commons-cli
BuildRequires:	apache-commons-lang
BuildRequires:	bouncycastle >= 1.33-3
BuildRequires:	eclipse-swt >= 3.5
BuildRequires:	java-devel >= 1.7.0
BuildRequires:	jpackage-utils >= 1.5
BuildRequires:	junit
BuildRequires:	log4j
BuildRequires:	xml-commons-apis
BuildRequires:	desktop-file-utils

Requires:	apache-commons-cli
Requires:	bouncycastle >= 1.33-3
Requires:	eclipse-swt >= 3.5
Requires:	log4j
Requires:	java >= 1.8.0

Provides:	vuze = %{version}-%{release}

%description
Azureus (now %{pkgname}) implements the BitTorrent protocol using java
and comes bundled with many invaluable features for both beginners and
advanced users.

%prep
%setup -q -c

cp %{SOURCE4} .

%apply_patches

rm org/gudy/azureus2/ui/swt/osx/CarbonUIEnhancer.java
rm org/gudy/azureus2/ui/swt/osx/Start.java
rm org/gudy/azureus2/ui/swt/win32/Win32UIEnhancer.java

#hacks to org.eclipse.swt.widgets.Tree2 don't compile.
rm -fR org/eclipse

# Convert line endings...
sed -i 's/\r//' ChangeLog.txt
chmod 644 *.txt

#remove bundled libs
#rm -fR org/apache

%build
mkdir -p build/libs
build-jar-repository -p build/libs bcprov apache-commons-cli log4j \
	junit apache-commons-lang

#ppc seems to have eclipse-swt.ppc64 installed so libdir can't be used
if [ -e /usr/lib/eclipse/swt.jar ];then
	ln -s /usr/lib/eclipse/swt.jar build/libs
else
	ln -s /usr/lib64/eclipse/swt.jar build/libs
fi

%ant jar

%install
# .jar-repertory
mkdir -p %{buildroot}%{_javadir}/azureus
install -m 0644 dist/Azureus2.jar %{buildroot}%{_javadir}/azureus/Azureus2.jar

# TODO: fix launcher to be multilib-safe
mkdir -p %{buildroot}%{_bindir}
install -pm 0755 %{SOURCE1} %{buildroot}%{_bindir}/azureus

# icons
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_iconsdir}/hicolor/16x16/apps
mkdir -p %{buildroot}%{_iconsdir}/hicolor/32x32/apps
mkdir -p %{buildroot}%{_iconsdir}/hicolor/64x64/apps
install -m 0644 org/gudy/azureus2/ui/icons/a32.png %{buildroot}%{_datadir}/pixmaps/azureus.png
install -m 0644 org/gudy/azureus2/ui/icons/a16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/azureus.png
install -m 0644 org/gudy/azureus2/ui/icons/a32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/azureus.png
install -m 0644 org/gudy/azureus2/ui/icons/a64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/azureus.png

# desktop file menu-entry
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
	--remove-key=Encoding \
	--dir %{buildroot}%{_datadir}/applications %{SOURCE2}

# application-registry
mkdir -p %{buildroot}%{_datadir}/application-registry
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/application-registry

# data-plugins
install -dm 0755 %{buildroot}%{_datadir}/azureus/plugins

%files
%doc ChangeLog.txt GPL.txt
%{_bindir}/azureus
%{_datadir}/azureus/
%{_javadir}/azureus/
%{_datadir}/applications/*.desktop
%{_datadir}/application-registry/*.applications
%{_datadir}/pixmaps/azureus.png
%{_iconsdir}/hicolor/16x16/apps/azureus.png
%{_iconsdir}/hicolor/32x32/apps/azureus.png
%{_iconsdir}/hicolor/64x64/apps/azureus.png
