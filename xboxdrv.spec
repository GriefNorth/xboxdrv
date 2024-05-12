%global commit 944de6aeee2fc93081cb6be70e954b390cbae065
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name: xboxdrv
Version: 0.8.8
Release: 14.git%{shortcommit}%{?dist}
Summary: Userspace Xbox/Xbox360 Gamepad Driver for Linux

License: GPLv3+
URL: http://pingus.seul.org/~grumbel/xboxdrv/
Source0: %{name}.tar.xz
Source1: %{name}.service
Source2: %{name}-config.txt
Source3: %{name}-daemon

Patch0: xboxdrv-60-sec-delay.patch
Patch1: xboxdrv-build.patch

BuildRequires: gcc
BuildRequires: gcc-c++

BuildRequires: pkgconfig(sdl)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(x11)

BuildRequires: cmake
BuildRequires: bluez-libs-devel
BuildRequires: gtk2-devel
BuildRequires: libusbx-devel
BuildRequires: boost-devel
BuildRequires: libX11-devel
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(dbus-glib-1)
BuildRequires: pkgconfig

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd

%description
This is a Xbox/Xbox360 gamepad driver for Linux that works in userspace.
It is an alternative to the xpad kernel driver and has support for 
Xbox1 gamepads, Xbox360 USB gamepads and Xbox360 wireless gamepads, 
both first and third party.

%global debug_package %{nil}

%prep
%setup -q -n %{name}

%patch0 -p0
%patch1 -p1

%build
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr
make

%install
cd build
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_bindir}/xboxdrvctl

# Version 0.9
# chmod 644 %{buildroot}%{_mandir}/man1/xboxdrv*
# chmod 644 %{buildroot}%{_mandir}/man1/virtualkeyboard*
chmod 644 %{buildroot}%{_mandir}/man1/xboxdrv*
#install -pm 644 doc/xboxdrv-daemon.1 %{buildroot}%{_mandir}/man1

# Install dbus rule
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
install -pm 644 ../data/org.seul.Xboxdrv.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}.conf
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%preun
%systemd_preun %{name}.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service

%files
%{!?_licensedir:%global license %doc}
%doc PROTOCOL NEWS AUTHORS README.md examples
%license COPYING
%{_bindir}/xboxdrv
%{_mandir}/man1/xboxdrv*
# Version 0.9
# %{_bindir}/virtualkeyboard
# %{_mandir}/man1/virtualkeyboard*
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/dbus-1/system.d/org.seul.Xboxdrv.conf
