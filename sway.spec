Name:           sway
Version:        0.12.1
Release:        1%{?dist}
Summary:        i3-compatible window manager for Wayland
Group:          User Interface/X
License:        MIT
URL:            https://github.com/SirCmpwn/sway
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(wlc)
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  asciidoc
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pam-devel
# Dmenu is the default launcher in sway
Requires:       dmenu
# By default the Fedora background is used
Recommends:     f%{fedora}-backgrounds-base
# dmenu (as well as rxvt any many others) requires XWayland on Sway
Requires:       xorg-x11-server-Xwayland
# Sway binds the terminal shortcut to one specific terminal. In our case urxvtc-ml
Recommends:     rxvt-unicode-256color-ml
# ImageMagick is needed to take screenshots with swaygrab
Recommends:     ImageMagick

%description
Sway is a tiling window manager supporting Wayland compositor protocol and 
i3-compatible configuration.

%prep
%autosetup
mkdir %{_target_platform}

%build
export CFLAGS="%{optflags} -Wno-error"
export LDFLAGS="%{__global_ldflags}"
pushd %{_target_platform}
%cmake \
       -DBUILD_SHARED_LIBS:BOOL=OFF \
       -Dzsh-completions=YES \
       -Ddefault-wallpaper=NO \
       -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
       ..
popd
%make_build -C %{_target_platform}

%install
%make_install -C %{_target_platform}
# Set default terminal to urxvt256c-ml
sed -i 's/^set $term urxvt$/set \$term urxvt256c-ml/' %{buildroot}%{_sysconfdir}/sway/config
# Set Fedora background as default background
sed -i "s|^output \* bg .*|output * bg /usr/share/backgrounds/f%{fedora}/default/normalish/f%{fedora}.png fill|" %{buildroot}%{_sysconfdir}/sway/config

%files
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/sway
%config(noreplace) %{_sysconfdir}/sway/config
%dir %{_sysconfdir}/sway/security.d
%config(noreplace) %{_sysconfdir}/sway/security.d/00-defaults
%config %{_sysconfdir}/pam.d/swaylock
%{_mandir}/man1/sway*.1*
%{_mandir}/man5/sway*.5*
%{_mandir}/man7/sway*.7*
%caps(cap_sys_ptrace,cap_sys_tty_config=eip) %{_bindir}/sway
%{_bindir}/swaybar
%{_bindir}/swaybg
%{_bindir}/swaygrab
%{_bindir}/swaylock
%{_bindir}/swaymsg
%{_datadir}/wayland-sessions/sway.desktop
%{_datadir}/zsh/site-functions/_sway*

%changelog
* Wed Mar 15 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.12.1-1
- Update to 0.12.1

* Wed Mar 08 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.12-1
- Update to 0.12

* Tue Feb 28 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.12-0.rc2
- Update to 0.12-rc2

* Sat Feb 25 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.12-0.rc1
- Update to 0.12-rc1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-7.gitb3c0aa3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.11-6.gitb3c0aa3
- Update to HEAD

* Thu Jan 12 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.11-5
- Fix bug #1008 with backported patch

* Thu Dec 29 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.11-4
- Set ptrace capability for sway

* Wed Dec 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.11-3
- Fix LD_LIBRARY_PATH

* Wed Dec 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.11-2
- Fix bug #971 with backported patch

* Tue Dec 27 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.11-1
- Update to 0.11

* Sun Dec 18 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.11-0.rc3
- Update to 0.11-rc3

* Sat Dec 17 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.11-0.rc2
- Update to 0.11-rc2

* Sat Nov 26 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.10-2
- Require Xwayland instead of just suggesting it, since at the moment is needed by dmenu (and other)

* Wed Oct 26 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.10-1
- Update to 0.10

* Thu Oct 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.10-0.1.rc3
- Update to 0.10-rc3

* Tue Oct 04 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.10-0.1.rc2
- Update to 0.10-rc2

* Wed Sep 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.10-0.1.rc1
- Update to 0.10-rc1

* Tue Sep 06 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.9-4
- Do not Require the urxvt shell
- Rebuild due to a wlc rebuild
- Add Recommends ImageMagick

* Wed Aug 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.9-3
- Remove some compilation flags that were not needed

* Sun Aug 07 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.9-2
- Add dmenu dependency
- Add rxvt-unicode-256color-ml dependency
- Use urxvt256c-ml instead of urxvt by default
- Improve default wallpaper
- Add suggests xorg-x11-server-Xwayland

* Wed Aug 03 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.9-1
- Upgrade to 0.9

* Thu Jul 07 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.8-2
- Move ffmpeg and ImageMagick from Required to Suggested

* Thu Jul 07 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.8-1
- Update to version 0.8
- Re-enable ZSH bindings
- Remove sway wallpapers

* Sun May 29 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.7-1
- Update to version 0.7
- Drop ZSH bindings that are no longer shipped with Sway

* Thu May 05 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.6-1
- Update to current upstream version

* Wed Apr 06 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.3-1
- Update to current upstream version

* Sun Feb 14 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0-1.20160214git016a774
- Initial packaging
