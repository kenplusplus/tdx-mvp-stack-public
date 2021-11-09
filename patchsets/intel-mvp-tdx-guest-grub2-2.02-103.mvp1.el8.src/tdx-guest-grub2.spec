%undefine _hardened_build

# This spec file began as CentOS's ovmf spec file, then cut down and modified.

%global tarversion 2.02
%undefine _missing_build_ids_terminate_build
%global _configure_gnuconfig_hack 0

%define source_url_prefix https://git.centos.org/rpms/grub2/raw/c8/f/SOURCES

Name:		intel-mvp-tdx-guest-grub2
Epoch:		1
Version:	2.02
Release:	103.mvp1%{?dist}
Summary:	Bootloader with support for Linux, Multiboot and more
Group:		System Environment/Base
License:	GPLv3+
URL:		http://www.gnu.org/software/grub/
Obsoletes:	grub < 1:0.98
Source0:	https://ftp.gnu.org/gnu/grub/grub-2.02.tar.gz
Source1:	grub.macros
Source4:	https://src.fedoraproject.org/repo/pkgs/grub2/unifont-5.1.20080820.pcf.gz/8c28087c5fcb3188f1244b390efffdbe/unifont-5.1.20080820.pcf.gz
Source6:	%{source_url_prefix}/gitignore
Source8:	%{source_url_prefix}/strtoull_test.c
Source9:	%{source_url_prefix}/20-grub.install
Source12:	%{source_url_prefix}/99-grub-mkconfig.install
Source13:	%{source_url_prefix}/centos-ca-secureboot.der
Source14:	%{source_url_prefix}/centossecureboot001.der
Source15:	%{source_url_prefix}/centossecurebootca2.der
Source16:	%{source_url_prefix}/centossecureboot202.der
Source17:	%{source_url_prefix}/sbat.csv.in

Source20: patches-tdx-grub-2.02-2021.09.09.tar.gz
%include %{SOURCE1}

BuildRequires:	gcc efi-srpm-macros
BuildRequires:	flex bison binutils python3-devel
BuildRequires:	ncurses-devel xz-devel bzip2-devel
BuildRequires:	freetype-devel libusb-devel
BuildRequires:	rpm-devel
BuildRequires:	rpm-devel rpm-libs
BuildRequires:	autoconf automake autogen device-mapper-devel
BuildRequires:	freetype-devel gettext-devel git
BuildRequires:	texinfo
BuildRequires:	dejavu-sans-fonts
BuildRequires:	help2man
# For %%_userunitdir macro
BuildRequires:	systemd
%ifarch %{efi_arch}
BuildRequires:	pesign >= 0.99-8
%endif
%if %{?_with_ccache: 1}%{?!_with_ccache: 0}
BuildRequires:	ccache
%endif

ExcludeArch:	s390 s390x %{arm}
Obsoletes:	%{name} <= %{evr}

%if 0%{with_legacy_arch}
Requires:	%{name}-%{legacy_package_arch} = %{evr}
%else
Requires:	%{name}-%{package_arch} = %{evr}
%endif

Provides:	grub2
Obsoletes:	grub2

%global desc \
The GRand Unified Bootloader (GRUB) is a highly configurable and \
customizable bootloader with modular architecture.  It supports a rich \
variety of kernel formats, file systems, computer architectures and \
hardware devices.\
%{nil}

%description
%{desc}

%package common
Summary:	grub2 common layout
Group:		System Environment/Base
BuildArch:	noarch
Obsoletes:	grubby < 8.40-13
Provides:	grub2-common
Obsoletes:	grub2-common

%description common
This package provides some directories which are required by various grub2
subpackages.

%package tools
Summary:	Support tools for GRUB.
Group:		System Environment/Base
Obsoletes:	%{name}-tools < %{evr}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Requires:	gettext os-prober which file
Requires(pre):	dracut
Requires(post):	dracut
Provides:	grub2-tools
Obsoletes:	grub2-tools

%description tools
%{desc}
This subpackage provides tools for support of all platforms.

%ifarch x86_64
%package tools-efi
Summary:	Support tools for GRUB.
Group:		System Environment/Base
Requires:	gettext os-prober which file
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-tools < %{evr}
Provides:	grub2-tools-efi
Obsoletes:	grub2-tools-efi

%description tools-efi
%{desc}
This subpackage provides tools for support of EFI platforms.
%endif

%package tools-minimal
Summary:	Support tools for GRUB.
Group:		System Environment/Base
Requires:	gettext
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-tools < %{evr}
Provides:	grub2-tools-minimal
Obsoletes:	grub2-tools-minimal

%description tools-minimal
%{desc}
This subpackage provides tools for support of all platforms.

%package tools-extra
Summary:	Support tools for GRUB.
Group:		System Environment/Base
Requires:	gettext os-prober which file
Requires:	%{name}-tools-minimal = %{epoch}:%{version}-%{release}
Requires:	%{name}-common = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-tools < %{evr}
Provides:	grub2-tools-extra
Obsoletes:	grub2-tools-extra

%description tools-extra
%{desc}
This subpackage provides tools for support of all platforms.

%if 0%{with_efi_arch}
%{expand:%define_efi_variant %%{package_arch} -o}
%endif
%if 0%{with_alt_efi_arch}
%{expand:%define_efi_variant %%{alt_package_arch}}
%endif
%if 0%{with_legacy_arch}
%{expand:%define_legacy_variant %%{legacy_package_arch}}
%endif

%prep
%do_common_setup

#PATCHSETBEGIN
ExtractPatches()
{
    local patchtarball=$1

    if [ ! -f $patchtarball ]; then
        echo "ExtractPatches"
        exit 1
    fi
    tar vxf $patchtarball
}
ExtractPatches %{SOURCE20}
for p in *.patch; do
     echo "Applying TDX patch: "$p
     patch -p1 -F1 -s < $p
done
#PATCHSETEND

%if 0%{with_efi_arch}
mkdir grub-%{grubefiarch}-%{tarversion}
#grep -A100000 '# stuff "make" creates' .gitignore > grub-%{grubefiarch}-%{tarversion}/.gitignore
cp .gitignore grub-%{grubefiarch}-%{tarversion}/.gitignore
cp %{SOURCE4} grub-%{grubefiarch}-%{tarversion}/unifont.pcf.gz
sed -e "s,@@VERSION@@,%{evr},g" %{SOURCE17} \
	> grub-%{grubefiarch}-%{tarversion}/sbat.csv
git add grub-%{grubefiarch}-%{tarversion}
%endif
%if 0%{with_alt_efi_arch}
mkdir grub-%{grubaltefiarch}-%{tarversion}
#grep -A100000 '# stuff "make" creates' .gitignore > grub-%{grubaltefiarch}-%{tarversion}/.gitignore
cp .gitignore  grub-%{grubaltefiarch}-%{tarversion}/.gitignore
cp %{SOURCE4} grub-%{grubaltefiarch}-%{tarversion}/unifont.pcf.gz
git add grub-%{grubaltefiarch}-%{tarversion}
%endif
%if 0%{with_legacy_arch}
mkdir grub-%{grublegacyarch}-%{tarversion}
#grep -A100000 '# stuff "make" creates' .gitignore > grub-%{grublegacyarch}-%{tarversion}/.gitignore
cp .gitignore grub-%{grublegacyarch}-%{tarversion}/.gitignore
cp %{SOURCE4} grub-%{grublegacyarch}-%{tarversion}/unifont.pcf.gz
git add grub-%{grublegacyarch}-%{tarversion}
%endif
git commit -m "After making subdirs"

%build
%if 0%{with_efi_arch}
%{expand:%do_primary_efi_build %%{grubefiarch} %%{grubefiname} %%{grubeficdname} %%{_target_platform} %%{efi_target_cflags} %%{efi_host_cflags} %{SOURCE13} %{SOURCE14} centossecureboot001 %{SOURCE15} %{SOURCE16} centossecureboot202}
%endif
%if 0%{with_alt_efi_arch}
%{expand:%do_alt_efi_build %%{grubaltefiarch} %%{grubaltefiname} %%{grubalteficdname} %%{_alt_target_platform} %%{alt_efi_target_cflags} %%{alt_efi_host_cflags} %{SOURCE13} %{SOURCE14} centossecureboot001 %{SOURCE15} %{SOURCE16} centossecureboot202}
%endif
%if 0%{with_legacy_arch}
%{expand:%do_legacy_build %%{grublegacyarch}}
%endif
makeinfo --info --no-split -I docs -o docs/grub-dev.info \
	docs/grub-dev.texi
makeinfo --info --no-split -I docs -o docs/grub.info \
	docs/grub.texi
makeinfo --html --no-split -I docs -o docs/grub-dev.html \
	docs/grub-dev.texi
makeinfo --html --no-split -I docs -o docs/grub.html \
	docs/grub.texi

%install
set -e
rm -fr $RPM_BUILD_ROOT

%do_common_install
%if 0%{with_efi_arch}
%{expand:%do_efi_install %%{grubefiarch} %%{grubefiname} %%{grubeficdname}}
%endif
%if 0%{with_alt_efi_arch}
%{expand:%do_alt_efi_install %%{grubaltefiarch} %%{grubaltefiname} %%{grubalteficdname}}
%endif
%if 0%{with_legacy_arch}
%{expand:%do_legacy_install %%{grublegacyarch} %%{alt_grub_target_name} 0%{with_efi_arch}}
%endif

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
ln -s grub2-set-password ${RPM_BUILD_ROOT}/%{_sbindir}/grub2-setpassword
echo '.so man8/grub2-set-password.8' > ${RPM_BUILD_ROOT}/%{_datadir}/man/man8/grub2-setpassword.8
%ifnarch x86_64
rm -vf ${RPM_BUILD_ROOT}/%{_bindir}/grub2-render-label
rm -vf ${RPM_BUILD_ROOT}/%{_sbindir}/grub2-bios-setup
rm -vf ${RPM_BUILD_ROOT}/%{_sbindir}/grub2-macbless
%endif

# TODO: find_lang introduce build broken so remove it temporary
#%find_lang grub

# Make selinux happy with exec stack binaries.
mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}/prelink.conf.d/
cat << EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/prelink.conf.d/grub2.conf
# these have execstack, and break under selinux
-b /usr/bin/grub2-script-check
-b /usr/bin/grub2-mkrelpath
-b /usr/bin/grub2-fstest
-b /usr/sbin/grub2-bios-setup
-b /usr/sbin/grub2-probe
-b /usr/sbin/grub2-sparc64-setup
EOF

# Install kernel-install scripts
install -d -m 0755 %{buildroot}%{_prefix}/lib/kernel/install.d/
install -D -m 0755 -t %{buildroot}%{_prefix}/lib/kernel/install.d/ %{SOURCE9}
install -D -m 0755 -t %{buildroot}%{_prefix}/lib/kernel/install.d/ %{SOURCE12}
install -d -m 0755 %{buildroot}%{_sysconfdir}/kernel/install.d/
install -m 0644 /dev/null %{buildroot}%{_sysconfdir}/kernel/install.d/20-grubby.install
install -m 0644 /dev/null %{buildroot}%{_sysconfdir}/kernel/install.d/90-loaderentry.install
# Install systemd user service to set the boot_success flag
install -D -m 0755 -t %{buildroot}%{_userunitdir} \
	docs/grub-boot-success.{timer,service}
install -d -m 0755 %{buildroot}%{_userunitdir}/timers.target.wants
ln -s ../grub-boot-success.timer \
	%{buildroot}%{_userunitdir}/timers.target.wants
# Install systemd system-update unit to set boot_indeterminate for offline-upd
install -D -m 0755 -t %{buildroot}%{_unitdir} docs/grub-boot-indeterminate.service
install -d -m 0755 %{buildroot}%{_unitdir}/system-update.target.wants
ln -s ../grub-boot-indeterminate.service \
	%{buildroot}%{_unitdir}/system-update.target.wants

# Don't run debuginfo on all the grub modules and whatnot; it just
# rejects them, complains, and slows down extraction.
%global finddebugroot "%{_builddir}/%{?buildsubdir}/debug"

%global dip RPM_BUILD_ROOT=%{finddebugroot} %{__debug_install_post}
%define __debug_install_post (						\
	mkdir -p %{finddebugroot}/usr					\
	mv ${RPM_BUILD_ROOT}/usr/bin %{finddebugroot}/usr/bin		\
	mv ${RPM_BUILD_ROOT}/usr/sbin %{finddebugroot}/usr/sbin		\
	%{dip}								\
	install -m 0755 -d %{buildroot}/usr/lib/ %{buildroot}/usr/src/	\
	cp -al %{finddebugroot}/usr/lib/debug/				\\\
		%{buildroot}/usr/lib/debug/				\
	cp -al %{finddebugroot}/usr/src/debug/				\\\
		%{buildroot}/usr/src/debug/ )				\
	mv %{finddebugroot}/usr/bin %{buildroot}/usr/bin		\
	mv %{finddebugroot}/usr/sbin %{buildroot}/usr/sbin		\
	%{nil}

%undefine buildsubdir

%pre tools
if [ -f /boot/grub2/user.cfg ]; then
    if grep -q '^GRUB_PASSWORD=' /boot/grub2/user.cfg ; then
	sed -i 's/^GRUB_PASSWORD=/GRUB2_PASSWORD=/' /boot/grub2/user.cfg
    fi
elif [ -f %{efi_esp_dir}/user.cfg ]; then
    if grep -q '^GRUB_PASSWORD=' %{efi_esp_dir}/user.cfg ; then
	sed -i 's/^GRUB_PASSWORD=/GRUB2_PASSWORD=/' \
	    %{efi_esp_dir}/user.cfg
    fi
elif [ -f /etc/grub.d/01_users ] && \
	grep -q '^password_pbkdf2 root' /etc/grub.d/01_users ; then
    if [ -f %{efi_esp_dir}/grub.cfg ]; then
	# on EFI we don't get permissions on the file, but
	# the directory is protected.
	grep '^password_pbkdf2 root' /etc/grub.d/01_users | \
		sed 's/^password_pbkdf2 root \(.*\)$/GRUB2_PASSWORD=\1/' \
	    > %{efi_esp_dir}/user.cfg
    fi
    if [ -f /boot/grub2/grub.cfg ]; then
	install -m 0600 /dev/null /boot/grub2/user.cfg
	chmod 0600 /boot/grub2/user.cfg
	grep '^password_pbkdf2 root' /etc/grub.d/01_users | \
		sed 's/^password_pbkdf2 root \(.*\)$/GRUB2_PASSWORD=\1/' \
	    > /boot/grub2/user.cfg
    fi
fi

%post tools
if [ "$1" = 1 ]; then
	/sbin/install-info --info-dir=%{_infodir} %{_infodir}/grub2.info.gz || :
	/sbin/install-info --info-dir=%{_infodir} %{_infodir}/grub2-dev.info.gz || :
fi

if [ "$1" = 2 ]; then
	/sbin/grub2-switch-to-blscfg --backup-suffix=.rpmsave &>/dev/null || :
fi

%triggerun -- grub2 < 1:1.99-4
# grub2 < 1.99-4 removed a number of essential files in postun. To fix upgrades
# from the affected grub2 packages, we first back up the files in triggerun and
# later restore them in triggerpostun.
# https://bugzilla.redhat.com/show_bug.cgi?id=735259

# Back up the files before uninstalling old grub2
mkdir -p /boot/grub2.tmp &&
mv -f /boot/grub2/*.mod \
      /boot/grub2/*.img \
      /boot/grub2/*.lst \
      /boot/grub2/device.map \
      /boot/grub2.tmp/ || :

%triggerpostun -- grub2 < 1:1.99-4
# ... and restore the files.
test ! -f /boot/grub2/device.map &&
test -d /boot/grub2.tmp &&
mv -f /boot/grub2.tmp/*.mod \
      /boot/grub2.tmp/*.img \
      /boot/grub2.tmp/*.lst \
      /boot/grub2.tmp/device.map \
      /boot/grub2/ &&
rm -r /boot/grub2.tmp/ || :

%preun tools
if [ "$1" = 0 ]; then
	/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/grub2.info.gz || :
	/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/grub2-dev.info.gz || :
fi

# TODO: find_lang introduce build broken so remove it temporary
#%files common -f grub.lang
%files common
%dir %{_libdir}/grub/
%dir %{_datarootdir}/grub/
%dir %{_datarootdir}/grub/themes/
%exclude %{_datarootdir}/grub/themes/*
%attr(0700,root,root) %dir %{_sysconfdir}/grub.d
%{_prefix}/lib/kernel/install.d/20-grub.install
%{_sysconfdir}/kernel/install.d/20-grubby.install
%{_sysconfdir}/kernel/install.d/90-loaderentry.install
%{_prefix}/lib/kernel/install.d/99-grub-mkconfig.install
%dir %{_datarootdir}/grub
%exclude %{_datarootdir}/grub/*
%dir /boot/grub2
%dir /boot/grub2/themes/
%dir /boot/grub2/themes/system
%exclude /boot/grub2/themes/system/*
%attr(0700,root,root) %dir /boot/grub2
%exclude /boot/grub2/*
%dir %attr(0700,root,root) %{efi_esp_dir}
%exclude %{efi_esp_dir}/*
%license COPYING
%ghost %config(noreplace) %verify(not size mode md5 mtime) /boot/grub2/grubenv
%doc INSTALL
%doc NEWS
%doc README
%doc THANKS
%doc TODO
%doc docs/grub.html
%doc docs/grub-dev.html
%doc docs/font_char_metrics.png

%files tools-minimal
%{_sysconfdir}/prelink.conf.d/grub2.conf
%{_sbindir}/grub2-get-kernel-settings
%attr(4755, root, root) %{_sbindir}/grub2-set-bootflag
%{_sbindir}/grub2-set-default
%{_sbindir}/grub2-set*password
%{_bindir}/grub2-editenv
%{_bindir}/grub2-mkpasswd-pbkdf2

%{_datadir}/man/man3/grub2-get-kernel-settings*
%{_datadir}/man/man8/grub2-set-default*
%{_datadir}/man/man8/grub2-set*password*
%{_datadir}/man/man1/grub2-editenv*
%{_datadir}/man/man1/grub2-mkpasswd-*

%ifarch x86_64
%files tools-efi
%{_sbindir}/grub2-macbless
%{_bindir}/grub2-render-label
%{_datadir}/man/man8/grub2-macbless*
%{_datadir}/man/man1/grub2-render-label*
%endif

%files tools
%attr(0644,root,root) %ghost %config(noreplace) %{_sysconfdir}/default/grub
%config %{_sysconfdir}/grub.d/??_*
%ifarch ppc64 ppc64le
%exclude %{_sysconfdir}/grub.d/10_linux
%else
%exclude %{_sysconfdir}/grub.d/10_linux_bls
%endif
%{_sysconfdir}/grub.d/README
%{_userunitdir}/grub-boot-success.timer
%{_userunitdir}/grub-boot-success.service
%{_userunitdir}/timers.target.wants
%{_unitdir}/grub-boot-indeterminate.service
%{_unitdir}/system-update.target.wants
%{_infodir}/grub2*
%{_datarootdir}/grub/*
%{_sbindir}/grub2-install
%exclude %{_datarootdir}/grub/themes
%exclude %{_datarootdir}/grub/*.h
%{_datarootdir}/bash-completion/completions/grub
%{_sbindir}/grub2-mkconfig
%{_sbindir}/grub2-switch-to-blscfg
%{_sbindir}/grub2-probe
%{_sbindir}/grub2-rpm-sort
%{_sbindir}/grub2-reboot
%{_bindir}/grub2-file
%{_bindir}/grub2-menulst2cfg
%{_bindir}/grub2-mkimage
%{_bindir}/grub2-mkrelpath
%{_bindir}/grub2-script-check
%{_datadir}/man/man?/*

# exclude man pages from tools-extra
%exclude %{_datadir}/man/man8/grub2-sparc64-setup*
%exclude %{_datadir}/man/man8/grub2-install*
%exclude %{_datadir}/man/man1/grub2-fstest*
%exclude %{_datadir}/man/man1/grub2-glue-efi*
%exclude %{_datadir}/man/man1/grub2-kbdcomp*
%exclude %{_datadir}/man/man1/grub2-mkfont*
%exclude %{_datadir}/man/man1/grub2-mklayout*
%exclude %{_datadir}/man/man1/grub2-mknetdir*
%exclude %{_datadir}/man/man1/grub2-mkrescue*
%exclude %{_datadir}/man/man1/grub2-mkstandalone*
%exclude %{_datadir}/man/man1/grub2-syslinux2cfg*

# exclude man pages from tools-minimal
%exclude %{_datadir}/man/man3/grub2-get-kernel-settings*
%exclude %{_datadir}/man/man8/grub2-set-default*
%exclude %{_datadir}/man/man8/grub2-set*password*
%exclude %{_datadir}/man/man1/grub2-editenv*
%exclude %{_datadir}/man/man1/grub2-mkpasswd-*
%exclude %{_datadir}/man/man8/grub2-macbless*
%exclude %{_datadir}/man/man1/grub2-render-label*

%if %{with_legacy_arch}
%{_sbindir}/grub2-install
%ifarch x86_64
%{_sbindir}/grub2-bios-setup
%else
%exclude %{_sbindir}/grub2-bios-setup
%exclude %{_datadir}/man/man8/grub2-bios-setup*
%endif
%ifarch %{sparc}
%{_sbindir}/grub2-sparc64-setup
%else
%exclude %{_sbindir}/grub2-sparc64-setup
%exclude %{_datadir}/man/man8/grub2-sparc64-setup*
%endif
%ifarch %{sparc} ppc ppc64 ppc64le
%{_sbindir}/grub2-ofpathname
%else
%exclude %{_sbindir}/grub2-ofpathname
%exclude %{_datadir}/man/man8/grub2-ofpathname*
%endif
%endif

%files tools-extra
%{_sbindir}/grub2-sparc64-setup
%{_sbindir}/grub2-ofpathname
%{_bindir}/grub2-fstest
%{_bindir}/grub2-glue-efi
%{_bindir}/grub2-kbdcomp
%{_bindir}/grub2-mkfont
%{_bindir}/grub2-mklayout
%{_bindir}/grub2-mknetdir
%ifnarch %{sparc}
%{_bindir}/grub2-mkrescue
%endif
%{_bindir}/grub2-mkstandalone
%{_bindir}/grub2-syslinux2cfg
%{_sysconfdir}/sysconfig/grub
%{_datadir}/man/man8/grub2-sparc64-setup*
%{_datadir}/man/man8/grub2-install*
%{_datadir}/man/man1/grub2-fstest*
%{_datadir}/man/man1/grub2-glue-efi*
%{_datadir}/man/man1/grub2-kbdcomp*
%{_datadir}/man/man1/grub2-mkfont*
%{_datadir}/man/man1/grub2-mklayout*
%{_datadir}/man/man1/grub2-mknetdir*
%{_datadir}/man/man1/grub2-mkrescue*
%{_datadir}/man/man1/grub2-mkstandalone*
%{_datadir}/man/man8/grub2-ofpathname*
%{_datadir}/man/man1/grub2-syslinux2cfg*
%exclude %{_datarootdir}/grub/themes/starfield

%if 0%{with_efi_arch}
%{expand:%define_efi_variant_files %%{package_arch} %%{grubefiname} %%{grubeficdname} %%{grubefiarch} %%{target_cpu_name} %%{grub_target_name}}
%endif
%if 0%{with_alt_efi_arch}
%{expand:%define_efi_variant_files %%{alt_package_arch} %%{grubaltefiname} %%{grubalteficdname} %%{grubaltefiarch} %%{alt_target_cpu_name} %%{alt_grub_target_name}}
%endif
%if 0%{with_legacy_arch}
%{expand:%define_legacy_variant_files %%{legacy_package_arch} %%{grublegacyarch}}
%endif
